"""
Bird integration for automated bookmark-to-knowledge-base pipeline.

This module provides:
- Tweet triage classifier (routes bookmarks by intent)
- Bookmark polling and deduplication
- Queue routing to existing ingestion pipeline
"""

from .triage import TweetTriageClassifier, TriageResult
from .poller import BookmarkPoller
from .router import BookmarkRouter

__all__ = [
    "TweetTriageClassifier",
    "TriageResult",
    "BookmarkPoller",
    "BookmarkRouter",
]
