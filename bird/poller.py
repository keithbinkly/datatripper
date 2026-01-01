"""
Bookmark poller for bird CLI integration.

Polls Twitter/X bookmarks via bird CLI and tracks which ones
have been seen to avoid duplicate processing.
"""

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterator, Optional


@dataclass
class Tweet:
    """Parsed tweet from bird CLI output."""

    id: str
    text: str
    author_name: str
    author_handle: str
    author_bio: str
    created_at: str
    has_media: bool
    is_thread: bool
    raw_json: dict

    @classmethod
    def from_bird_json(cls, data: dict) -> "Tweet":
        """Parse tweet from bird --json output."""
        # bird returns tweets in this structure
        tweet_id = data.get("id") or data.get("rest_id", "")

        # Author info
        user = data.get("user", {}) or data.get("core", {}).get("user_results", {}).get("result", {})
        legacy_user = user.get("legacy", {})

        author_name = legacy_user.get("name") or user.get("name", "Unknown")
        author_handle = legacy_user.get("screen_name") or user.get("screen_name", "unknown")
        author_bio = legacy_user.get("description") or user.get("description", "")

        # Tweet content
        legacy = data.get("legacy", {})
        text = legacy.get("full_text") or data.get("text", "")
        created_at = legacy.get("created_at") or data.get("created_at", "")

        # Media detection
        media = legacy.get("entities", {}).get("media", [])
        extended_media = legacy.get("extended_entities", {}).get("media", [])
        has_media = bool(media or extended_media)

        # Thread detection (reply to self)
        in_reply_to = legacy.get("in_reply_to_screen_name")
        is_thread = in_reply_to == author_handle

        return cls(
            id=str(tweet_id),
            text=text,
            author_name=author_name,
            author_handle=author_handle,
            author_bio=author_bio,
            created_at=created_at,
            has_media=has_media,
            is_thread=is_thread,
            raw_json=data,
        )


class BookmarkPoller:
    """
    Polls bookmarks from bird CLI and tracks seen tweets.

    Usage:
        poller = BookmarkPoller()
        for tweet in poller.get_new_bookmarks():
            process(tweet)
        poller.save_seen()
    """

    def __init__(
        self,
        seen_file: Optional[Path] = None,
        bird_path: str = "bird",
        limit: int = 50,
    ):
        """
        Initialize bookmark poller.

        Args:
            seen_file: Path to file tracking seen bookmark IDs
            bird_path: Path to bird CLI executable
            limit: Maximum bookmarks to fetch per poll
        """
        self.seen_file = seen_file or Path.home() / ".bird-seen-bookmarks"
        self.bird_path = bird_path
        self.limit = limit
        self._seen_ids: set[str] = set()
        self._new_seen: set[str] = set()  # Track new IDs this session
        self._load_seen()

    def _load_seen(self):
        """Load previously seen bookmark IDs."""
        if self.seen_file.exists():
            self._seen_ids = set(self.seen_file.read_text().strip().split("\n"))
            # Filter empty strings
            self._seen_ids = {id for id in self._seen_ids if id}

    def save_seen(self):
        """Persist seen bookmark IDs to file."""
        all_seen = self._seen_ids | self._new_seen
        self.seen_file.write_text("\n".join(sorted(all_seen)))

    def mark_seen(self, tweet_id: str):
        """Mark a tweet ID as seen."""
        self._new_seen.add(tweet_id)

    def is_seen(self, tweet_id: str) -> bool:
        """Check if tweet has been seen."""
        return tweet_id in self._seen_ids or tweet_id in self._new_seen

    def fetch_bookmarks(self) -> list[Tweet]:
        """
        Fetch bookmarks from bird CLI.

        Returns:
            List of Tweet objects from bookmarks
        """
        try:
            result = subprocess.run(
                [self.bird_path, "bookmarks", "--json", "--limit", str(self.limit)],
                capture_output=True,
                text=True,
                timeout=60,
            )

            if result.returncode != 0:
                raise RuntimeError(f"bird CLI error: {result.stderr}")

            # Parse JSON output
            data = json.loads(result.stdout)

            # bird returns array of tweets
            if isinstance(data, list):
                return [Tweet.from_bird_json(t) for t in data]
            elif isinstance(data, dict) and "data" in data:
                return [Tweet.from_bird_json(t) for t in data["data"]]
            else:
                return []

        except FileNotFoundError:
            raise RuntimeError(
                "bird CLI not found. Install with: npm install -g @steipete/bird"
            )
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse bird output: {e}")
        except subprocess.TimeoutExpired:
            raise RuntimeError("bird CLI timed out")

    def get_new_bookmarks(self) -> Iterator[Tweet]:
        """
        Fetch and yield only new (unseen) bookmarks.

        Yields:
            Tweet objects for bookmarks not yet seen
        """
        tweets = self.fetch_bookmarks()

        for tweet in tweets:
            if not self.is_seen(tweet.id):
                self.mark_seen(tweet.id)
                yield tweet

    def get_all_bookmarks(self) -> Iterator[Tweet]:
        """
        Fetch and yield all bookmarks (including seen).

        Yields:
            All Tweet objects from bookmarks
        """
        yield from self.fetch_bookmarks()


class MockBookmarkPoller(BookmarkPoller):
    """
    Mock poller for testing without bird CLI.

    Reads tweets from a JSON file instead of calling bird.
    """

    def __init__(
        self,
        mock_file: Path,
        seen_file: Optional[Path] = None,
    ):
        super().__init__(seen_file=seen_file)
        self.mock_file = mock_file

    def fetch_bookmarks(self) -> list[Tweet]:
        """Load tweets from mock file."""
        if not self.mock_file.exists():
            return []

        with open(self.mock_file) as f:
            data = json.load(f)

        if isinstance(data, list):
            return [Tweet.from_bird_json(t) for t in data]
        return []


def poll_once(
    seen_file: Optional[Path] = None,
    bird_path: str = "bird",
    limit: int = 50,
) -> list[Tweet]:
    """
    Convenience function to poll bookmarks once.

    Returns:
        List of new (unseen) Tweet objects
    """
    poller = BookmarkPoller(seen_file=seen_file, bird_path=bird_path, limit=limit)
    new_tweets = list(poller.get_new_bookmarks())
    poller.save_seen()
    return new_tweets


if __name__ == "__main__":
    # Quick test
    import sys

    print("Polling bookmarks...")
    try:
        tweets = poll_once(limit=10)
        print(f"Found {len(tweets)} new bookmarks")
        for t in tweets[:3]:
            print(f"  - @{t.author_handle}: {t.text[:60]}...")
    except RuntimeError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
