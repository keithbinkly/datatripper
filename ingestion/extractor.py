"""
Content extraction using Unstructured

Extracts clean text and metadata from URLs, PDFs, and other sources.
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse

import httpx
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import clean, clean_extra_whitespace


@dataclass
class ExtractedContent:
    """Structured content extracted from a source."""
    url: str
    title: Optional[str]
    text: str
    author_name: Optional[str]
    published_date: Optional[str]
    source_platform: str
    word_count: int
    has_code: bool
    has_video: bool
    fetch_timestamp: str


# Platform detection patterns
PLATFORM_PATTERNS = {
    "substack.com": "Substack",
    "medium.com": "Medium",
    "github.com": "GitHub",
    "github.io": "GitHub",
    "youtube.com": "YouTube",
    "youtu.be": "YouTube",
    "arxiv.org": "arXiv",
    "pluralistic.net": "Pluralistic",
    "every.to": "Every",
    "a]16z.com": "a16z",
    "anthropic.com": "Anthropic",
    "openai.com": "OpenAI",
    "getdbt.com": "dbt Blog",
    "docs.getdbt.com": "dbt Docs",
    "tableau.com": "Tableau",
    "pudding.cool": "The Pudding",
    "quillette.com": "Quillette",
}


def detect_platform(url: str) -> str:
    """Detect the source platform from URL."""
    parsed = urlparse(url)
    domain = parsed.netloc.lower().replace("www.", "")

    for pattern, platform in PLATFORM_PATTERNS.items():
        if pattern in domain:
            return platform

    # Fallback: use domain as platform name
    parts = domain.split(".")
    if len(parts) >= 2:
        return parts[-2].title()
    return "Website"


def detect_content_type(elements: list, url: str) -> tuple[bool, bool]:
    """Detect if content has code blocks or video embeds."""
    text_content = " ".join(e.text for e in elements if hasattr(e, "text"))

    has_code = any([
        "```" in text_content,
        "<code>" in text_content.lower(),
        "<pre>" in text_content.lower(),
        bool(re.search(r'def \w+\(|function \w+\(|class \w+[:\(]', text_content)),
    ])

    has_video = any([
        "youtube.com" in url.lower(),
        "youtu.be" in url.lower(),
        "vimeo.com" in url.lower(),
        "video" in url.lower(),
    ])

    return has_code, has_video


def extract_author_from_elements(elements: list) -> Optional[str]:
    """Try to extract author name from page elements."""
    for el in elements:
        text = getattr(el, "text", "")
        # Common byline patterns
        if match := re.search(r"(?:by|written by|author:?)\s+([A-Z][a-z]+ [A-Z][a-z]+)", text, re.I):
            return match.group(1)
    return None


def extract_date_from_elements(elements: list) -> Optional[str]:
    """Try to extract publication date from page elements."""
    for el in elements:
        text = getattr(el, "text", "")
        # ISO date pattern
        if match := re.search(r"(\d{4}-\d{2}-\d{2})", text):
            return match.group(1)
        # Common date formats
        if match := re.search(r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})", text, re.I):
            try:
                from dateutil import parser
                dt = parser.parse(match.group(1))
                return dt.strftime("%Y-%m-%d")
            except:
                pass
    return None


def extract_url(url: str, timeout: int = 30) -> ExtractedContent:
    """
    Extract content from a URL using Unstructured.

    Args:
        url: The URL to extract content from
        timeout: Request timeout in seconds

    Returns:
        ExtractedContent with extracted text and metadata
    """
    # Fetch the page
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) data-centered-bot/1.0"
    }

    response = httpx.get(url, headers=headers, timeout=timeout, follow_redirects=True)
    response.raise_for_status()

    # Parse with Unstructured
    elements = partition_html(text=response.text)

    # Extract title
    title = None
    for el in elements:
        if getattr(el, "category", None) == "Title":
            title = clean_extra_whitespace(el.text)
            break

    # Extract body text
    body_categories = {"NarrativeText", "ListItem", "UncategorizedText"}
    body_elements = [e for e in elements if getattr(e, "category", None) in body_categories]

    text_parts = []
    for el in body_elements:
        cleaned = clean(el.text, extra_whitespace=True, trailing_punctuation=False)
        if cleaned and len(cleaned) > 20:  # Skip tiny fragments
            text_parts.append(cleaned)

    full_text = "\n\n".join(text_parts)

    # Detect metadata
    has_code, has_video = detect_content_type(elements, url)
    author = extract_author_from_elements(elements)
    pub_date = extract_date_from_elements(elements)
    platform = detect_platform(url)

    return ExtractedContent(
        url=url,
        title=title,
        text=full_text,
        author_name=author,
        published_date=pub_date,
        source_platform=platform,
        word_count=len(full_text.split()),
        has_code=has_code,
        has_video=has_video,
        fetch_timestamp=datetime.utcnow().isoformat(),
    )


def estimate_reading_time(word_count: int, has_video: bool = False) -> str:
    """Estimate reading time based on word count."""
    if has_video:
        return "video"

    # Average reading speed: 200-250 wpm
    minutes = max(1, round(word_count / 225))

    if minutes < 60:
        return f"{minutes}m"
    else:
        hours = minutes // 60
        remaining = minutes % 60
        if remaining > 0:
            return f"{hours}h {remaining}m"
        return f"{hours}h"
