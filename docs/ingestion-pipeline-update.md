# Ingestion Pipeline: From Manual to Automated

*December 2024 — Status Update*

---

## The Problem We Had

Adding a resource to data-centered.com meant:

1. Find interesting article
2. Read it, decide if it fits the taxonomy
3. Open `resources.yaml`, scroll to the right section
4. Manually write 30+ lines of YAML (title, definition, domain, category, author, relationships...)
5. Look up or create author entry in `authors.yaml`
6. Think about how it relates to existing resources
7. Hope you didn't make a typo

**Time per resource:** 10-15 minutes of focused work.

**Result:** A backlog of 50+ bookmarked articles that never got added.

---

## What We Built

An automated ingestion pipeline using **Unstructured** for content extraction and **DSPy** for LLM-powered classification.

```
URL → Extract → Classify → Enrich → Generate YAML
```

**New workflow:**
```bash
python ingest.py add "https://example.com/article" --dry-run
```

The pipeline:
- Fetches and parses the URL
- Classifies into our 7 domains and categories
- Generates a definition with semantic boundaries
- Extracts author information
- Creates ready-to-append YAML

**Time per resource:** 2-3 minutes (mostly review).

---

## Current State

### What Works

```
✓ Single URL ingestion
✓ Automatic domain/category classification
✓ Definition generation
✓ Author extraction
✓ YAML generation matching our schema
✓ Human review queue for low-confidence classifications
✓ CLI with dry-run mode
```

### Known Limitations

```
✗ No duplicate detection (can add same URL twice)
✗ No batch processing (one URL at a time)
✗ Truncates long articles at 4000 chars
✗ No relationship discovery
✗ Author bios require manual research
✗ YouTube/video content not handled
```

---

## The Roadmap

After analyzing 50+ tools from our intake queue, we identified three phases of improvements:

### Phase 1: Foundation (4 hours)

| Task | Impact |
|------|--------|
| Replace extraction with summarize.sh | YouTube support, better scraping |
| Add duplicate detection | No more double-entries |
| Add batch mode | Process intake-queue.md at once |
| Add definition quality scoring | Catch weak definitions |
| Log classification reasoning | Debug wrong classifications |

**Outcome:** Reliable, bulk-capable ingestion.

### Phase 2: Intelligence (10 hours)

| Task | Impact |
|------|--------|
| Context compression for long articles | Better classification accuracy |
| Parallel relationship search | 4x faster as KB grows |
| Author enrichment via GitHub API | Automatic bio/affiliation |
| Lazy DSPy module loading | 40-60% token reduction |

**Outcome:** Smarter, faster, cheaper ingestion.

### Phase 3: Advanced (2-3 days)

| Task | Impact |
|------|--------|
| Semiosis-style KB quality testing | Systematic quality measurement |
| Experiential learning | Pipeline improves over time |
| Package as Claude Skill | Seamless invocation |
| CocoIndex integration | Knowledge graph visualization |

**Outcome:** Self-improving, visual, enterprise-grade.

---

## End State Vision

After completing all phases:

```
┌─────────────────────────────────────────────────────────────────────┐
│                                                                     │
│  $ ingest "https://example.com/article"                             │
│                                                                     │
│  📥 Fetching...                                                     │
│  ✓ Extracted: "Context Engineering for AI Agents" (2,847 words)    │
│                                                                     │
│  🔍 Checking for duplicates...                                      │
│  ✓ No duplicates found                                              │
│  ℹ Similar: context-engineering-weaviate (0.72 similarity)          │
│                                                                     │
│  🧠 Classifying...                                                  │
│  ✓ Domain: knowledge-engineering → Context Engineering              │
│  ✓ Confidence: 94% (auto-approved)                                  │
│                                                                     │
│  📝 Generating definition...                                        │
│  ✓ Quality score: 0.91                                              │
│                                                                     │
│  👤 Author: Cory Doctorow                                           │
│  ✓ Found on GitHub: cory@eff.org, EFF                               │
│                                                                     │
│  🔗 Suggested relationships:                                        │
│  • related → context-engineering-weaviate                           │
│  • broader → ai-context-gap                                         │
│                                                                     │
│  ✅ Added to knowledge base                                          │
│  ✅ Author enriched                                                  │
│  ✅ Relationships created                                            │
│                                                                     │
│  📊 Session stats: 3 resources added, 0 duplicates, $0.02 spent    │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Capabilities Summary

| Capability | Before | After Phase 1 | After Phase 3 |
|------------|--------|---------------|---------------|
| Time per resource | 10-15 min | 2-3 min | 30 sec |
| Batch processing | No | Yes | Yes |
| Duplicate detection | No | Yes | Yes |
| YouTube support | No | Yes | Yes |
| Author enrichment | Manual | Manual | Automatic |
| Relationship discovery | Manual | Manual | Automatic |
| Quality measurement | None | Basic | Systematic |
| Learning over time | No | No | Yes |
| Knowledge graph | No | No | Yes |

---

## Key Insights from Research

These findings shaped our roadmap:

> **"87.5% of agent failures are context problems, not model capability."**
> — Weaviate Context Engineering

We're adding context compression and selection for long articles.

> **"Small models benefit most from shared memory (+0.66 pts)."**
> — Spark: Shared Memory for Coding Agents

We're adding experiential learning from successful classifications.

> **"Tool Search reduces tokens by 85%."**
> — Anthropic Advanced Tool Use

We're adding lazy DSPy module loading.

> **"Quality is the production killer."**
> — LangChain State of Agent Engineering 2025

We're adding definition quality scoring and KB testing.

---

## Resources Informing This Work

- [summarize.sh](https://summarize.sh/) - Robust content extraction CLI
- [Semiosis](https://github.com/AnswerLayer/semiosis) - KB quality testing framework
- [CocoIndex](https://cocoindex.io/) - Incremental indexing to graphs
- [LangChain Context Engineering](https://blog.langchain.com/context-engineering-for-agents/) - 4 context strategies
- [Relace Fast Agentic Search](https://www.relace.ai/blog/fast-agentic-search) - Parallel search patterns
- [Anthropic Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use) - Tool Search Tool
- [Agent Skills](https://agentskills.io/) - Skills packaging format

---

## Next Steps

Phase 1 tasks are tracked in Beads:

```
bd list --status open
```

First priority: Replace extraction with summarize.sh wrapper (30 min, immediate quality boost).

---

*Built with Claude Code + DSPy + Unstructured*
