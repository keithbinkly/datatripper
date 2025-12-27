"""
GitHub author enrichment module.

Enriches author metadata using the GitHub API.
Works without authentication (60 req/hour) or with GITHUB_TOKEN (5000 req/hour).
"""

import os
import re
from dataclasses import dataclass
from typing import Optional
from urllib.parse import urlparse
import json


@dataclass
class GitHubProfile:
    """Enriched author data from GitHub."""
    username: str
    name: Optional[str]
    bio: Optional[str]
    location: Optional[str]
    company: Optional[str]
    blog: Optional[str]
    twitter: Optional[str]
    public_repos: int
    followers: int


def extract_github_username(url: str) -> Optional[str]:
    """Extract GitHub username from a URL if it's a GitHub profile."""
    parsed = urlparse(url)
    if parsed.netloc not in ("github.com", "www.github.com"):
        return None

    path = parsed.path.strip("/")
    if "/" in path:
        # It's a repo or deeper path, not a profile
        return None

    if path and not path.startswith(("features", "enterprise", "pricing", "about")):
        return path

    return None


def search_github_user(name: str, token: Optional[str] = None) -> Optional[str]:
    """Search GitHub for a user by name, return best-match username."""
    import urllib.request
    import urllib.error

    # Clean name for search
    query = name.replace("-", " ").strip()
    search_url = f"https://api.github.com/search/users?q={query.replace(' ', '+')}&per_page=5"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "data-centered-ingestion",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = urllib.request.Request(search_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        if not data.get("items"):
            return None

        # Try to find exact name match
        for item in data["items"]:
            if item.get("login", "").lower() == name.lower().replace(" ", ""):
                return item["login"]

        # Return top result as fallback
        return data["items"][0]["login"]

    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        return None


def fetch_github_profile(username: str, token: Optional[str] = None) -> Optional[GitHubProfile]:
    """Fetch GitHub profile data for a username."""
    import urllib.request
    import urllib.error

    url = f"https://api.github.com/users/{username}"

    headers = {
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "data-centered-ingestion",
    }
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())

        return GitHubProfile(
            username=data.get("login", username),
            name=data.get("name"),
            bio=data.get("bio"),
            location=data.get("location"),
            company=data.get("company"),
            blog=data.get("blog"),
            twitter=data.get("twitter_username"),
            public_repos=data.get("public_repos", 0),
            followers=data.get("followers", 0),
        )

    except (urllib.error.URLError, json.JSONDecodeError, KeyError):
        return None


def enrich_author(
    author_name: str,
    author_id: str,
    source_url: str,
    existing_github: Optional[str] = None,
) -> dict:
    """
    Enrich author data with GitHub information.

    Args:
        author_name: Full author name
        author_id: Existing author ID (e.g., 'c-doctorow')
        source_url: Original article URL (might contain GitHub link)
        existing_github: Known GitHub username if any

    Returns:
        Dict with enrichment data (empty if no GitHub found)
    """
    token = os.environ.get("GITHUB_TOKEN")

    # Priority 1: Use existing GitHub username
    username = existing_github

    # Priority 2: Check if source URL is from GitHub
    if not username:
        username = extract_github_username(source_url)

    # Priority 3: Search by author name
    if not username:
        username = search_github_user(author_name, token)

    if not username:
        return {}

    profile = fetch_github_profile(username, token)
    if not profile:
        return {}

    enrichment = {
        "github": f"https://github.com/{profile.username}",
        "github_username": profile.username,
    }

    # Only add fields with values
    if profile.location:
        enrichment["location"] = profile.location
    if profile.company:
        # Clean company (often has @ prefix)
        company = profile.company.lstrip("@").strip()
        enrichment["affiliation"] = company
    if profile.twitter:
        enrichment["twitter"] = f"https://twitter.com/{profile.twitter}"
    if profile.bio:
        enrichment["bio"] = profile.bio[:200]  # Truncate long bios
    if profile.followers >= 100:
        enrichment["github_followers"] = profile.followers

    return enrichment


def enrich_authors_batch(authors: list[dict], dry_run: bool = False) -> list[dict]:
    """
    Enrich a batch of authors with GitHub data.

    Args:
        authors: List of author dicts with at least 'id' and 'preferredLabel'
        dry_run: If True, print what would be enriched without modifying

    Returns:
        List of enriched author dicts
    """
    enriched = []

    for author in authors:
        author_id = author.get("id", "")
        author_name = author.get("preferredLabel", "")

        # Skip if already has GitHub
        if author.get("github"):
            enriched.append(author)
            continue

        data = enrich_author(
            author_name=author_name,
            author_id=author_id,
            source_url=author.get("source_url", ""),
        )

        if data:
            if dry_run:
                print(f"  Would enrich {author_id}: {data.get('github')}")
            else:
                author.update(data)

        enriched.append(author)

    return enriched
