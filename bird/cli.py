#!/usr/bin/env python3
"""
Bird bookmark pipeline CLI.

Usage:
    python -m bird.cli poll              Poll bookmarks and route to queues
    python -m bird.cli poll --dry-run    Preview without writing
    python -m bird.cli poll --simple     Use heuristic classifier (no LLM)
    python -m bird.cli status            Show queue status and stats
    python -m bird.cli process           Process learn queue through ingestion

Examples:
    # One-time poll (add to cron for continuous)
    python -m bird.cli poll

    # Preview what would be routed
    python -m bird.cli poll --dry-run --limit 5

    # Process articles from learn queue
    python -m bird.cli process --dry-run
"""

import argparse
import sys
from pathlib import Path


def cmd_poll(args):
    """Poll bookmarks and route to queues."""
    from .poller import BookmarkPoller
    from .router import BookmarkRouter
    from .triage import TweetTriageClassifier, SimpleTriageClassifier

    print("🐦 Polling bookmarks...")

    # Initialize poller
    poller = BookmarkPoller(limit=args.limit)

    try:
        new_tweets = list(poller.get_new_bookmarks())
    except RuntimeError as e:
        print(f"✗ {e}")
        sys.exit(1)

    if not new_tweets:
        print("No new bookmarks found.")
        return

    print(f"Found {len(new_tweets)} new bookmark(s)")

    # Initialize classifier
    if args.simple:
        print("Using simple heuristic classifier...")
        classifier = SimpleTriageClassifier()
    else:
        print("Using LLM classifier...")
        from ingestion.classifiers import configure_dspy

        try:
            configure_dspy()
        except Exception as e:
            print(f"✗ Failed to configure DSPy: {e}")
            print("  Falling back to simple classifier...")
            classifier = SimpleTriageClassifier()
            args.simple = True

        if not args.simple:
            classifier = TweetTriageClassifier()

    # Initialize router
    router = BookmarkRouter()

    # Process each tweet
    print("\n📋 Classifying and routing...")
    print("─" * 50)

    for i, tweet in enumerate(new_tweets, 1):
        print(f"\n[{i}/{len(new_tweets)}] @{tweet.author_handle}")
        print(f"    {tweet.text[:60]}...")

        # Classify
        if args.simple:
            result = classifier.classify(
                tweet_id=tweet.id,
                tweet_text=tweet.text,
                author_name=tweet.author_name,
                author_handle=tweet.author_handle,
                has_media=tweet.has_media,
                is_thread=tweet.is_thread,
            )
        else:
            result = classifier(
                tweet_id=tweet.id,
                tweet_text=tweet.text,
                author_name=tweet.author_name,
                author_handle=tweet.author_handle,
                author_bio=tweet.author_bio,
                has_media=tweet.has_media,
                is_thread=tweet.is_thread,
            )

        # Show classification
        intent_emoji = {
            "learn": "📚",
            "try": "🔧",
            "review": "👀",
            "quote": "💬",
            "skip": "⏭️",
        }
        emoji = intent_emoji.get(result.intent, "❓")
        print(f"    {emoji} {result.intent} ({result.content_type}) - {result.confidence:.0%}")
        print(f"    → {result.reasoning[:60]}...")

        if result.primary_url:
            print(f"    🔗 {result.primary_url[:60]}...")

        if not args.dry_run:
            router.route(result)

    # Flush queues
    if not args.dry_run:
        router.flush()
        poller.save_seen()
        print("\n✅ Routed to queues")
    else:
        print("\n[dry-run] Would route to queues")

    router.print_stats()


def cmd_status(args):
    """Show queue status."""
    base_dir = Path(__file__).parent.parent
    queues_dir = base_dir / "queues"

    print("📊 Queue Status")
    print("─" * 40)

    # Check intake queue
    intake_queue = base_dir / "intake-queue.md"
    if intake_queue.exists():
        content = intake_queue.read_text()
        # Count markdown links
        import re
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content)
        print(f"📥 Intake queue: {len(links)} links")
    else:
        print("📥 Intake queue: not found")

    # Check other queues
    for queue_file, emoji, name in [
        (queues_dir / "try-queue.md", "🔧", "Try queue"),
        (queues_dir / "review-queue.md", "👀", "Review queue"),
        (queues_dir / "quotes.yaml", "💬", "Quotes"),
    ]:
        if queue_file.exists():
            if queue_file.suffix == ".yaml":
                import yaml
                with open(queue_file) as f:
                    data = yaml.safe_load(f) or {}
                count = len(data.get("quotes", []))
            else:
                # Count headers as items
                content = queue_file.read_text()
                count = content.count("### ")
            print(f"{emoji} {name}: {count} items")
        else:
            print(f"{emoji} {name}: empty")

    # Check seen bookmarks
    seen_file = Path.home() / ".bird-seen-bookmarks"
    if seen_file.exists():
        count = len([l for l in seen_file.read_text().split("\n") if l])
        print(f"\n📌 Seen bookmarks: {count}")

    # Check log
    log_file = queues_dir / "bird-log.jsonl"
    if log_file.exists():
        lines = log_file.read_text().strip().split("\n")
        print(f"📝 Log entries: {len(lines)}")


def cmd_process(args):
    """Process learn queue through ingestion pipeline."""
    import subprocess

    base_dir = Path(__file__).parent.parent
    intake_queue = base_dir / "intake-queue.md"

    if not intake_queue.exists():
        print("No intake queue found.")
        return

    cmd = ["python", "ingest.py", "batch", str(intake_queue)]

    if args.dry_run:
        cmd.append("--dry-run")

    if args.auto_approve:
        cmd.append("--auto-approve")

    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, cwd=base_dir)


def main():
    parser = argparse.ArgumentParser(
        description="Bird bookmark pipeline for data-centered",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # poll command
    poll_parser = subparsers.add_parser("poll", help="Poll bookmarks and route to queues")
    poll_parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    poll_parser.add_argument("--simple", action="store_true", help="Use heuristic classifier (no LLM)")
    poll_parser.add_argument("--limit", type=int, default=50, help="Max bookmarks to fetch")

    # status command
    subparsers.add_parser("status", help="Show queue status")

    # process command
    process_parser = subparsers.add_parser("process", help="Process learn queue through ingestion")
    process_parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    process_parser.add_argument("--auto-approve", action="store_true", help="Skip review queue")

    args = parser.parse_args()

    if args.command == "poll":
        cmd_poll(args)
    elif args.command == "status":
        cmd_status(args)
    elif args.command == "process":
        cmd_process(args)


if __name__ == "__main__":
    main()
