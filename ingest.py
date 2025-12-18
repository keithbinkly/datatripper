#!/usr/bin/env python3
"""
data-centered ingestion CLI

Usage:
    python ingest.py add <url>           Add a single URL
    python ingest.py add <url> --dry-run Preview without writing
    python ingest.py review              Review pending resources

Examples:
    python ingest.py add "https://pluralistic.net/2024/06/21/seedbed/"
    python ingest.py add "https://moderndata101.substack.com/p/ai-ready-data" --dry-run
"""

import argparse
import sys
from pathlib import Path

import yaml


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
            ))
            f.write("\n")
        print(f"✓ New author written to: {authors_file}")

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

    args = parser.parse_args()

    if args.command == "add":
        cmd_add(args.url, dry_run=args.dry_run, auto_approve=args.auto_approve)
    elif args.command == "review":
        cmd_review()


if __name__ == "__main__":
    main()
