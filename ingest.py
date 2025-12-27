#!/usr/bin/env python3
"""
data-centered ingestion CLI

Usage:
    python ingest.py add <url>              Add a single URL
    python ingest.py add <url> --dry-run    Preview without writing
    python ingest.py batch <file>           Process URLs from markdown file
    python ingest.py batch <file> --dry-run Preview batch without processing
    python ingest.py review                 Review pending resources

Examples:
    python ingest.py add "https://pluralistic.net/2024/06/21/seedbed/"
    python ingest.py add "https://moderndata101.substack.com/p/ai-ready-data" --dry-run
    python ingest.py batch intake-queue.md --dry-run
"""

import argparse
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse

import yaml


def normalize_url(url: str) -> str:
    """Normalize URL for deduplication."""
    parsed = urlparse(url)
    # Remove fragment, normalize path
    normalized = urlunparse((
        parsed.scheme.lower(),
        parsed.netloc.lower().replace("www.", ""),
        parsed.path.rstrip("/") or "/",
        "",  # params
        parsed.query,
        "",  # fragment
    ))
    return normalized


def load_existing_urls() -> dict[str, str]:
    """Load existing resource URLs from resources.yaml.

    Returns:
        Dict mapping normalized URL to resource ID
    """
    resources_file = Path(__file__).parent / "resources.yaml"
    if not resources_file.exists():
        return {}

    with open(resources_file) as f:
        data = yaml.safe_load(f)

    if not data or "resources" not in data:
        return {}

    urls = {}
    for r in data["resources"]:
        if "url" in r and "id" in r:
            urls[normalize_url(r["url"])] = r["id"]
    return urls


def check_duplicate(url: str, existing_urls: dict[str, str]) -> str | None:
    """Check if URL already exists in knowledge base.

    Returns:
        Resource ID if duplicate found, None otherwise
    """
    normalized = normalize_url(url)
    return existing_urls.get(normalized)


def load_existing_authors() -> set[str]:
    """Load existing author IDs from authors.yaml."""
    authors_file = Path(__file__).parent / "authors.yaml"
    if not authors_file.exists():
        return set()

    with open(authors_file) as f:
        data = yaml.safe_load(f)

    if not data or "authors" not in data:
        return set()

    return {a["id"] for a in data["authors"] if "id" in a}


def load_config() -> dict:
    """Load ingestion configuration."""
    config_file = Path(__file__).parent / "config" / "ingestion.yaml"
    if config_file.exists():
        with open(config_file) as f:
            return yaml.safe_load(f)
    return {
        "llm": {"provider": "anthropic", "model": "claude-sonnet-4-20250514"},
        "classification": {"confidence_threshold": 0.7},
    }


def cmd_add(url: str, dry_run: bool = False, auto_approve: bool = False):
    """Add a single URL to the knowledge base."""
    import os

    from ingestion.extractor import extract_url
    from ingestion.classifiers import configure_dspy, IngestionPipeline
    from ingestion.yaml_writer import (
        generate_resource_yaml,
        generate_author_yaml,
        generate_review_entry,
        format_for_display,
    )

    config = load_config()
    existing_authors = load_existing_authors()
    existing_urls = load_existing_urls()

    # Check for duplicates first
    print(f"\n🔍 Checking for duplicates...")
    if duplicate_id := check_duplicate(url, existing_urls):
        print(f"✗ Duplicate found: {duplicate_id}")
        print(f"  URL already exists in knowledge base")
        print(f"  Use --force to add anyway (not implemented)")
        sys.exit(1)
    print(f"✓ No duplicate found")

    # Check for API key
    provider = config["llm"]["provider"]
    env_var = "ANTHROPIC_API_KEY" if provider == "anthropic" else "OPENAI_API_KEY"
    if not os.environ.get(env_var):
        print(f"\n✗ Missing {env_var}")
        print(f"  Set it with: export {env_var}='your-key-here'")
        print(f"  Or add to your shell profile (~/.zshrc or ~/.bashrc)")
        sys.exit(1)

    print(f"\n📥 Fetching: {url}")
    print("─" * 60)

    # Step 1: Extract content
    try:
        extracted = extract_url(url)
        print(f"✓ Extracted: {extracted.title}")
        print(f"  {extracted.word_count} words, platform: {extracted.source_platform}")
    except Exception as e:
        print(f"✗ Extraction failed: {e}")
        sys.exit(1)

    # Step 2: Configure DSPy and run pipeline
    print("\n🧠 Classifying with LLM...")
    configure_dspy(
        provider=config["llm"]["provider"],
        model=config["llm"]["model"],
    )

    pipeline = IngestionPipeline(existing_authors=existing_authors)
    result = pipeline.process(extracted)

    # Step 3: Display results
    print(format_for_display(result))

    if dry_run:
        print("\n📋 Generated YAML (dry run - not written):")
        print("─" * 60)
        print(generate_resource_yaml(result))
        if result.is_new_author:
            print("\n📋 New Author YAML:")
            print("─" * 60)
            print(generate_author_yaml(
                result.author_id,
                result.author_name,
                source_url=url,
            ))
        return

    # Step 4: Handle based on confidence
    threshold = config["classification"]["confidence_threshold"]

    if result.needs_review and not auto_approve:
        print(f"\n⚠️  Confidence ({result.confidence:.0%}) below threshold ({threshold:.0%})")
        print("    Adding to review queue...")

        queue_file = Path(__file__).parent / "queue" / "pending.yaml"
        queue_file.parent.mkdir(exist_ok=True)

        # Load or create queue
        if queue_file.exists():
            with open(queue_file) as f:
                queue = yaml.safe_load(f) or {"pending": []}
        else:
            queue = {"pending": []}

        # Add to queue (as dict, not raw YAML string)
        queue["pending"].append({
            "id": result.id,
            "url": result.url,
            "title": result.title,
            "domain": result.domain,
            "category": result.category,
            "confidence": result.confidence,
            "reasoning": result.reasoning,
            "definition": result.definition,
            "author_id": result.author_id,
            "is_new_author": result.is_new_author,
        })

        with open(queue_file, "w") as f:
            yaml.dump(queue, f, default_flow_style=False, allow_unicode=True)

        print(f"    Written to: {queue_file}")
        print("\n    Run `python ingest.py review` to approve/edit")
        return

    # Step 5: Write to files
    resources_file = Path(__file__).parent / "resources.yaml"
    authors_file = Path(__file__).parent / "authors.yaml"

    # Append resource
    with open(resources_file, "a") as f:
        f.write("\n")
        f.write(generate_resource_yaml(result))
        f.write("\n")
    print(f"\n✓ Resource written to: {resources_file}")

    # Append author if new
    if result.is_new_author:
        with open(authors_file, "a") as f:
            f.write("\n")
            f.write(generate_author_yaml(
                result.author_id,
                result.author_name,
                source_url=url,
                github_enrichment=result.github_enrichment,
            ))
            f.write("\n")
        print(f"✓ New author written to: {authors_file}")
        if result.github_enrichment:
            print(f"  ✓ Enriched from GitHub: {result.github_enrichment.get('github', '')}")

    print("\n✅ Done! Resource added to knowledge base.")


def cmd_review():
    """Interactive review of pending resources."""
    queue_file = Path(__file__).parent / "queue" / "pending.yaml"

    if not queue_file.exists():
        print("No pending resources to review.")
        return

    with open(queue_file) as f:
        queue = yaml.safe_load(f)

    if not queue or not queue.get("pending"):
        print("No pending resources to review.")
        return

    pending = queue["pending"]
    print(f"\n📋 {len(pending)} resource(s) pending review\n")

    for i, item in enumerate(pending):
        print(f"[{i+1}/{len(pending)}] {item['title']}")
        print(f"    URL: {item['url']}")
        print(f"    Classification: {item['domain']} → {item['category']}")
        print(f"    Confidence: {item['confidence']:.0%}")
        print(f"    Reasoning: {item['reasoning'][:100]}...")
        print()

        action = input("    [a]pprove / [s]kip / [e]dit / [d]elete? ").strip().lower()

        if action == "a":
            # Re-run with auto-approve
            cmd_add(item["url"], auto_approve=True)
            pending.remove(item)
        elif action == "d":
            pending.remove(item)
            print("    Deleted.")
        elif action == "e":
            print("    (Edit not yet implemented - use 'a' to approve then edit YAML)")
        else:
            print("    Skipped.")

    # Save updated queue
    queue["pending"] = pending
    with open(queue_file, "w") as f:
        yaml.dump(queue, f, default_flow_style=False, allow_unicode=True)

    print(f"\n✓ Queue updated. {len(pending)} item(s) remaining.")


def extract_markdown_links(content: str) -> list[tuple[str, str]]:
    """Extract markdown links from content.

    Returns:
        List of (title, url) tuples
    """
    import re
    # Match [title](url) pattern
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, content)

    # Filter to http(s) URLs only
    return [(title, url) for title, url in matches if url.startswith(('http://', 'https://'))]


def cmd_batch(file_path: str, dry_run: bool = False, auto_approve: bool = False):
    """Process URLs from a markdown file."""
    from pathlib import Path

    file = Path(file_path)
    if not file.exists():
        print(f"✗ File not found: {file_path}")
        sys.exit(1)

    content = file.read_text()
    links = extract_markdown_links(content)

    if not links:
        print("No markdown links found in file.")
        return

    print(f"\n📋 Found {len(links)} links in {file.name}")
    print("─" * 60)

    # Load existing URLs for duplicate check
    existing_urls = load_existing_urls()

    # Categorize links
    new_links = []
    duplicate_links = []

    for title, url in links:
        if dup_id := check_duplicate(url, existing_urls):
            duplicate_links.append((title, url, dup_id))
        else:
            new_links.append((title, url))

    print(f"\n✓ {len(new_links)} new URLs")
    print(f"✗ {len(duplicate_links)} duplicates (will skip)")

    if duplicate_links:
        print("\nDuplicates:")
        for title, url, dup_id in duplicate_links[:5]:
            print(f"  - {title[:40]}... → {dup_id}")
        if len(duplicate_links) > 5:
            print(f"  ... and {len(duplicate_links) - 5} more")

    if not new_links:
        print("\nNo new URLs to process.")
        return

    print(f"\nNew URLs to process:")
    for i, (title, url) in enumerate(new_links[:10], 1):
        print(f"  {i}. {title[:50]}...")
    if len(new_links) > 10:
        print(f"  ... and {len(new_links) - 10} more")

    if dry_run:
        print(f"\n[dry-run] Would process {len(new_links)} URLs")
        return

    # Process each URL
    print(f"\n📥 Processing {len(new_links)} URLs...")
    print("─" * 60)

    successes = 0
    failures = []

    for i, (title, url) in enumerate(new_links, 1):
        print(f"\n[{i}/{len(new_links)}] {title[:40]}...")
        try:
            cmd_add(url, dry_run=False, auto_approve=auto_approve)
            successes += 1
        except SystemExit:
            # cmd_add calls sys.exit on failure
            failures.append((title, url))
        except Exception as e:
            print(f"  ✗ Error: {e}")
            failures.append((title, url))

    print(f"\n{'─' * 60}")
    print(f"📊 Batch complete: {successes} succeeded, {len(failures)} failed")
    if failures:
        print("\nFailed URLs:")
        for title, url in failures:
            print(f"  - {url}")


def main():
    parser = argparse.ArgumentParser(
        description="data-centered knowledge base ingestion",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # add command
    add_parser = subparsers.add_parser("add", help="Add a URL to the knowledge base")
    add_parser.add_argument("url", help="URL to ingest")
    add_parser.add_argument("--dry-run", action="store_true", help="Preview without writing")
    add_parser.add_argument("--auto-approve", action="store_true", help="Skip review queue")

    # review command
    subparsers.add_parser("review", help="Review pending resources")

    # batch command
    batch_parser = subparsers.add_parser("batch", help="Process URLs from a markdown file")
    batch_parser.add_argument("file", help="Markdown file containing URLs")
    batch_parser.add_argument("--dry-run", action="store_true", help="Preview without processing")
    batch_parser.add_argument("--auto-approve", action="store_true", help="Skip review queue")

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args.url, dry_run=args.dry_run, auto_approve=args.auto_approve)
    elif args.command == "review":
        cmd_review()
    elif args.command == "batch":
        cmd_batch(args.file, dry_run=args.dry_run, auto_approve=args.auto_approve)


if __name__ == "__main__":
    main()
