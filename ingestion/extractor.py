"""
Content extraction using summarize.sh CLI

Extracts clean text and metadata from URLs, YouTube videos, and other sources.
Uses summarize.sh (https://summarize.sh/) for robust extraction with fallbacks.
"""

import json
import re
import subprocess
from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from urllib.parse import urlparse


@dataclass
class ExtractedContent:
    """Structured content extracted from a source."""
    url: str
    title: Optional[str]
    description: Optional[str]
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
    "a16z.com": "a16z",
    "anthropic.com": "Anthropic",
    "openai.com": "OpenAI",
    "getdbt.com": "dbt Blog",
    "docs.getdbt.com": "dbt Docs",
    "tableau.com": "Tableau",
    "pudding.cool": "The Pudding",
    "quillette.com": "Quillette",
    "langchain.com": "LangChain",
    "weaviate.io": "Weaviate",
    "cocoindex.io": "CocoIndex",
    "relace.ai": "Relace",
}


def detect_platform(url: str, site_name: Optional[str] = None) -> str:
    """Detect the source platform from URL or site name."""
    # Try site name first if provided
    if site_name:
        # Clean up common patterns
        name = site_name.replace(".com", "").replace(".io", "").replace(".ai", "")
        if name and len(name) < 30:
            return name.title()

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


def detect_content_signals(text: str, url: str) -> tuple[bool, bool]:
    """Detect if content has code blocks or is video content."""
    has_code = any([
        "```" in text,
        re.search(r'def \w+\(|function \w+\(|class \w+[:\(]', text),
        re.search(r'import \w+|from \w+ import', text),
        "<code>" in text.lower(),
    ])

    has_video = any([
        "youtube.com" in url.lower(),
        "youtu.be" in url.lower(),
        "vimeo.com" in url.lower(),
    ])

    return has_code, has_video


def extract_author_from_text(text: str) -> Optional[str]:
    """Try to extract author name from content text."""
    # Look for common byline patterns in first 1000 chars
    search_text = text[:1000]

    patterns = [
        r"(?:^|\n)\*\*([A-Z][a-z]+ [A-Z][a-z]+)\*\*\n",  # **Author Name** on own line
        r"(?:by|written by|author:?)\s+([A-Z][a-z]+ [A-Z][a-z]+)",
        r"(?:^|\n)([A-Z][a-z]+ [A-Z][a-z]+)\n(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)",
    ]

    for pattern in patterns:
        if match := re.search(pattern, search_text, re.I | re.M):
            return match.group(1)

    return None


def extract_date_from_text(text: str) -> Optional[str]:
    """Try to extract publication date from content text."""
    search_text = text[:2000]

    # ISO date pattern
    if match := re.search(r"(\d{4}-\d{2}-\d{2})", search_text):
        return match.group(1)

    # Common date formats: "Sep 11, 2025" or "September 11, 2025"
    if match := re.search(
        r"((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \d{1,2},? \d{4})",
        search_text,
        re.I
    ):
        try:
            from dateutil import parser
            dt = parser.parse(match.group(1))
            return dt.strftime("%Y-%m-%d")
        except Exception:
            pass

    return None


def extract_url(url: str, timeout: int = 120) -> ExtractedContent:
    """
    Extract content from a URL using summarize.sh CLI.

    Args:
        url: The URL to extract content from
        timeout: Request timeout in seconds

    Returns:
        ExtractedContent with extracted text and metadata
    """
    # Call summarize.sh with --extract-only --json
    try:
        result = subprocess.run(
            ["summarize", url, "--extract-only", "--json", f"--timeout={timeout}s"],
            capture_output=True,
            text=True,
            timeout=timeout + 10,
        )

        if result.returncode != 0:
            raise RuntimeError(f"summarize failed: {result.stderr}")

        data = json.loads(result.stdout)
        extracted = data.get("extracted", {})

    except FileNotFoundError:
        raise RuntimeError(
            "summarize.sh not found. Install with: brew install steipete/tap/summarize"
        )
    except json.JSONDecodeError as e:
        raise RuntimeError(f"Failed to parse summarize output: {e}")

    # Extract fields from JSON response
    title = extracted.get("title")
    description = extracted.get("description")
    content = extracted.get("content", "")
    word_count = extracted.get("wordCount", len(content.split()))
    site_name = extracted.get("siteName")

    # Detect metadata from content
    has_code, has_video = detect_content_signals(content, url)
    author = extract_author_from_text(content)
    pub_date = extract_date_from_text(content)
    platform = detect_platform(url, site_name)

    # Check if this was a YouTube video (has transcript info)
    if extracted.get("transcriptSource"):
        has_video = True

    return ExtractedContent(
        url=url,
        title=title,
        description=description,
        text=content,
        author_name=author,
        published_date=pub_date,
        source_platform=platform,
        word_count=word_count,
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
