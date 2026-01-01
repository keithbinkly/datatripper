# Bird Integration: Bookmark-to-Knowledge-Base Pipeline

Automated pipeline that converts Twitter/X bookmarks into knowledge base entries.

Based on [@alexhillman's workflow](https://x.com/alexhillman) using [@steipete's bird CLI](https://github.com/steipete/bird).

## Overview

```
┌─────────────────────────────────────────────────────────────┐
│  1. BOOKMARK (you)                                          │
│     See interesting tweet → bookmark it                     │
└─────────────────────────┬───────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────┐
│  2. POLL (cron every 60s)                                   │
│     bird bookmarks → detect new → classify                  │
└─────────────────────────┬───────────────────────────────────┘
                          │
          ┌───────────────┼───────────────┬─────────────────┐
          ▼               ▼               ▼                 ▼
    ┌──────────┐   ┌──────────┐   ┌──────────┐      ┌──────────┐
    │  LEARN   │   │   TRY    │   │  REVIEW  │      │  QUOTES  │
    │ articles │   │  repos   │   │ threads  │      │ insights │
    └────┬─────┘   └──────────┘   └──────────┘      └──────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────┐
│  3. INGEST (existing pipeline)                              │
│     python ingest.py batch intake-queue.md                  │
└─────────────────────────────────────────────────────────────┘
```

## Setup

### 1. Install bird CLI

```bash
# npm
npm install -g @steipete/bird

# or Homebrew (macOS)
brew install steipete/tap/bird

# or run without installing
bunx @steipete/bird whoami
```

### 2. Authenticate bird

Bird uses browser cookies for authentication:

```bash
# Check if authenticated
bird whoami

# If not, bird will guide you through cookie extraction
# Supports Safari, Chrome, Firefox
```

### 3. Test the integration

```bash
# Check current bookmark count
bird bookmarks --json | jq length

# Dry-run poll (no changes)
python -m bird.cli poll --dry-run --limit 5

# Poll with simple heuristics (no LLM cost)
python -m bird.cli poll --simple --dry-run
```

## Usage

### Manual Poll

```bash
# Poll and route bookmarks
python -m bird.cli poll

# Use simple classifier (no LLM, free)
python -m bird.cli poll --simple

# Preview without writing
python -m bird.cli poll --dry-run
```

### Check Status

```bash
python -m bird.cli status
```

Output:
```
📊 Queue Status
────────────────────────────────────
📥 Intake queue: 57 links
🔧 Try queue: 3 items
👀 Review queue: 5 items
💬 Quotes: 12 items

📌 Seen bookmarks: 89
📝 Log entries: 89
```

### Process Learn Queue

```bash
# Process articles through full ingestion pipeline
python -m bird.cli process

# Preview
python -m bird.cli process --dry-run
```

### Continuous Polling (cron)

```bash
# Edit crontab
crontab -e

# Add line (poll every minute)
* * * * * /path/to/data-centered/bird/poll-bookmarks.sh

# Or every 5 minutes with simple classifier
*/5 * * * * /path/to/data-centered/bird/poll-bookmarks.sh --simple
```

## Classification

### Intents

| Intent | Destination | Content Types |
|--------|-------------|---------------|
| `learn` | `intake-queue.md` | Articles, essays, videos, podcasts |
| `try` | `queues/try-queue.md` | GitHub repos, tools, libraries |
| `review` | `queues/review-queue.md` | Threads, opinions, discussions |
| `quote` | `queues/quotes.yaml` | Standalone insights, wisdom |
| `skip` | Logged only | Off-topic, duplicates |

### Classifiers

**LLM Classifier** (default)
- Uses DSPy with Claude for intelligent classification
- Understands context, author expertise, content type
- Higher accuracy but costs tokens

**Simple Classifier** (`--simple`)
- Rule-based heuristics
- Free, fast, offline-capable
- Good for high-volume, obvious signals (GitHub URLs, videos)

Heuristics:
- GitHub URL → `try` (repo)
- YouTube/Vimeo URL → `learn` (video)
- Podcast URL → `learn` (podcast)
- Thread → `review` (thread)
- Short tweet, no URLs → `quote` (insight)

## Queue Files

### intake-queue.md

Markdown links for the ingestion pipeline:

```markdown
## Bird Bookmarks - 2024-12-15 10:30

- [Context Engineering for AI Systems](https://example.com/article)
  - Source tweet: https://x.com/user/status/123
  - Type: article
  - Confidence: 92%
```

### queues/try-queue.md

Tools and repos to experiment with:

```markdown
### steipete/bird

- **URL**: https://github.com/steipete/bird
- **Source**: https://x.com/steipete/status/456
- **Author**: @steipete
- **Why**: Twitter CLI tool for automation

> Just released bird - a CLI for Twitter...
```

### queues/review-queue.md

Content needing human review:

```markdown
### @thoughtleader

- **Tweet**: https://x.com/thoughtleader/status/789
- **Type**: thread
- **Reason**: Multi-part thread with opinions on AI

> Here's my controversial take on why...
```

### queues/quotes.yaml

Extracted wisdom:

```yaml
quotes:
  - quote: "The best code is no code at all."
    author: Jeff Atwood
    handle: codinghorror
    source: https://x.com/codinghorror/status/101112
    topic: software engineering
    added: 2024-12-15
```

## Workflow Tips

### 1. Bookmark Strategically

The pipeline works best when you:
- Bookmark tweets with **links** to articles/resources
- Bookmark **GitHub repos** you want to try
- Bookmark **insights** worth remembering

### 2. Review Periodically

```bash
# Check what's accumulated
python -m bird.cli status

# Process learn queue when ready
python -m bird.cli process --dry-run
python -m bird.cli process
```

### 3. Tune Classification

If too many items go to `review`:
- Use `--simple` for obvious content (repos, videos)
- Run LLM classifier less frequently for nuanced tweets

### 4. Compound Effect

As the pipeline runs:
1. Bookmarks automatically captured
2. Links extracted and classified
3. Articles processed through ingestion pipeline
4. Authors discovered and enriched
5. Knowledge base grows organically

## Files

| File | Purpose |
|------|---------|
| `bird/triage.py` | Tweet classification (DSPy + heuristics) |
| `bird/poller.py` | Bookmark fetching and deduplication |
| `bird/router.py` | Queue routing logic |
| `bird/cli.py` | Command-line interface |
| `bird/poll-bookmarks.sh` | Cron-ready shell script |
| `queues/` | Output queues (try, review, quotes) |
| `~/.bird-seen-bookmarks` | Seen tweet IDs (deduplication) |

## Troubleshooting

### "bird CLI not found"

```bash
npm install -g @steipete/bird
# or
export PATH="$PATH:./node_modules/.bin"
```

### "bird not authenticated"

```bash
bird whoami
# Follow prompts to extract browser cookies
```

### "DSPy configuration failed"

```bash
export ANTHROPIC_API_KEY='your-key'
# or use simple classifier
python -m bird.cli poll --simple
```

### "No new bookmarks"

- Check if bird can see bookmarks: `bird bookmarks --limit 5`
- Reset seen file: `rm ~/.bird-seen-bookmarks`
