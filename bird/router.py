"""
Bookmark router - routes triaged tweets to appropriate queues.

Routes tweets based on intent:
- learn → intake-queue.md (for full ingestion pipeline)
- try → queues/try-queue.md (tools/repos to experiment with)
- review → queues/review-queue.md (needs human review)
- quote → queues/quotes.yaml (extracted wisdom)
- skip → logged but not queued
"""

import yaml
from datetime import datetime
from pathlib import Path
from typing import Optional

from .triage import TriageResult


class BookmarkRouter:
    """
    Routes triaged bookmarks to appropriate queues.

    Usage:
        router = BookmarkRouter()
        for result in triage_results:
            router.route(result)
        router.flush()  # Write all queues to disk
    """

    def __init__(
        self,
        base_dir: Optional[Path] = None,
        intake_queue: Optional[Path] = None,
    ):
        """
        Initialize router with queue paths.

        Args:
            base_dir: Base directory for queue files (default: project root)
            intake_queue: Path to main intake queue (default: intake-queue.md)
        """
        self.base_dir = base_dir or Path(__file__).parent.parent
        self.queues_dir = self.base_dir / "queues"
        self.queues_dir.mkdir(exist_ok=True)

        # Queue file paths
        self.intake_queue = intake_queue or self.base_dir / "intake-queue.md"
        self.try_queue = self.queues_dir / "try-queue.md"
        self.review_queue = self.queues_dir / "review-queue.md"
        self.quotes_file = self.queues_dir / "quotes.yaml"
        self.log_file = self.queues_dir / "bird-log.jsonl"

        # Buffers for batch writing
        self._learn_buffer: list[TriageResult] = []
        self._try_buffer: list[TriageResult] = []
        self._review_buffer: list[TriageResult] = []
        self._quote_buffer: list[TriageResult] = []

        # Stats
        self.stats = {
            "learn": 0,
            "try": 0,
            "review": 0,
            "quote": 0,
            "skip": 0,
        }

    def route(self, result: TriageResult):
        """
        Route a triaged tweet to the appropriate queue.

        Args:
            result: TriageResult from triage classifier
        """
        self.stats[result.intent] += 1

        if result.intent == "learn":
            self._learn_buffer.append(result)
        elif result.intent == "try":
            self._try_buffer.append(result)
        elif result.intent == "review":
            self._review_buffer.append(result)
        elif result.intent == "quote":
            self._quote_buffer.append(result)
        # skip: just log, don't queue

        # Always log
        self._log(result)

    def _log(self, result: TriageResult):
        """Append result to log file."""
        import json

        entry = {
            "timestamp": datetime.now().isoformat(),
            "tweet_id": result.tweet_id,
            "author": result.author_handle,
            "intent": result.intent,
            "content_type": result.content_type,
            "primary_url": result.primary_url,
            "confidence": result.confidence,
            "reasoning": result.reasoning,
        }

        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")

    def flush(self):
        """Write all buffered items to their queue files."""
        if self._learn_buffer:
            self._write_learn_queue()
        if self._try_buffer:
            self._write_try_queue()
        if self._review_buffer:
            self._write_review_queue()
        if self._quote_buffer:
            self._write_quotes()

    def _write_learn_queue(self):
        """Append learn items to intake-queue.md."""
        lines = [
            "",
            f"## Bird Bookmarks - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "",
        ]

        for result in self._learn_buffer:
            # Format as markdown link
            title = self._extract_title(result)
            if result.primary_url:
                lines.append(f"- [{title}]({result.primary_url})")
                lines.append(f"  - Source tweet: {result.tweet_url}")
                lines.append(f"  - Type: {result.content_type}")
                lines.append(f"  - Confidence: {result.confidence:.0%}")
            else:
                # No URL, add the tweet itself
                lines.append(f"- Tweet by @{result.author_handle}")
                lines.append(f"  - URL: {result.tweet_url}")
                lines.append(f"  - Text: {result.tweet_text[:100]}...")

        lines.append("")

        with open(self.intake_queue, "a") as f:
            f.write("\n".join(lines))

        self._learn_buffer.clear()

    def _write_try_queue(self):
        """Write try items to try-queue.md."""
        lines = []

        # Add header if file doesn't exist
        if not self.try_queue.exists():
            lines.extend([
                "# Try Queue",
                "",
                "Tools, repos, and libraries to experiment with.",
                "",
                "---",
                "",
            ])

        lines.extend([
            f"## {datetime.now().strftime('%Y-%m-%d')}",
            "",
        ])

        for result in self._try_buffer:
            title = self._extract_title(result)
            lines.append(f"### {title}")
            lines.append("")
            if result.primary_url:
                lines.append(f"- **URL**: {result.primary_url}")
            lines.append(f"- **Source**: {result.tweet_url}")
            lines.append(f"- **Author**: @{result.author_handle}")
            lines.append(f"- **Why**: {result.reasoning}")
            lines.append("")
            lines.append(f"> {result.tweet_text[:200]}...")
            lines.append("")

        with open(self.try_queue, "a") as f:
            f.write("\n".join(lines))

        self._try_buffer.clear()

    def _write_review_queue(self):
        """Write review items to review-queue.md."""
        lines = []

        # Add header if file doesn't exist
        if not self.review_queue.exists():
            lines.extend([
                "# Review Queue",
                "",
                "Threads, opinions, and content needing human review.",
                "",
                "---",
                "",
            ])

        lines.extend([
            f"## {datetime.now().strftime('%Y-%m-%d')}",
            "",
        ])

        for result in self._review_buffer:
            lines.append(f"### @{result.author_handle}")
            lines.append("")
            lines.append(f"- **Tweet**: {result.tweet_url}")
            lines.append(f"- **Type**: {result.content_type}")
            lines.append(f"- **Reason**: {result.reasoning}")
            lines.append("")
            lines.append(f"> {result.tweet_text}")
            lines.append("")
            if result.primary_url:
                lines.append(f"**Link**: {result.primary_url}")
                lines.append("")

        with open(self.review_queue, "a") as f:
            f.write("\n".join(lines))

        self._review_buffer.clear()

    def _write_quotes(self):
        """Append quotes to quotes.yaml."""
        # Load existing quotes
        if self.quotes_file.exists():
            with open(self.quotes_file) as f:
                data = yaml.safe_load(f) or {"quotes": []}
        else:
            data = {"quotes": []}

        # Add new quotes
        for result in self._quote_buffer:
            if result.extracted_quote:
                quote_entry = {
                    "quote": result.extracted_quote,
                    "author": result.author_name,
                    "handle": result.author_handle,
                    "source": result.tweet_url,
                    "topic": result.quote_topic,
                    "added": datetime.now().strftime("%Y-%m-%d"),
                }
                data["quotes"].append(quote_entry)

        # Write back
        with open(self.quotes_file, "w") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False)

        self._quote_buffer.clear()

    def _extract_title(self, result: TriageResult) -> str:
        """Extract a title from the result."""
        # If URL is GitHub, extract repo name
        if result.primary_url and "github.com" in result.primary_url:
            parts = result.primary_url.rstrip("/").split("/")
            if len(parts) >= 5:
                return f"{parts[-2]}/{parts[-1]}"

        # Use first ~60 chars of tweet as title
        text = result.tweet_text.replace("\n", " ")
        if len(text) > 60:
            return text[:57] + "..."
        return text

    def get_stats(self) -> dict:
        """Get routing statistics."""
        return self.stats.copy()

    def print_stats(self):
        """Print routing statistics."""
        total = sum(self.stats.values())
        print(f"\n📊 Routing Stats ({total} total)")
        print("─" * 30)
        print(f"  📚 Learn:  {self.stats['learn']}")
        print(f"  🔧 Try:    {self.stats['try']}")
        print(f"  👀 Review: {self.stats['review']}")
        print(f"  💬 Quote:  {self.stats['quote']}")
        print(f"  ⏭️  Skip:   {self.stats['skip']}")
