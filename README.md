# data-centered

**[View Site](https://keithbinkly.github.io/data-centered/)**

A digital garden built on a files-over-CMS philosophy. Topics span technology, culture, ideas—whatever's worth tending.

## Why Files Over CMS?

This project uses plain YAML files as the single source of truth for all content, rather than a traditional CMS. This approach is gaining momentum in the industry—Lee Robinson recently [migrated cursor.com from a CMS back to raw code and Markdown](https://leerob.com/agents), citing faster builds, lower costs, and reduced complexity.

Our reasoning:
- **Version controlled** — content changes tracked in git like code
- **Human readable** — YAML is easy to read and edit without tooling
- **No lock-in** — data isn't trapped in a proprietary CMS database
- **AI-friendly** — agents can read, understand, and work with structured files directly
- **Simple architecture** — static HTML, no build step, no framework overhead

## Data Architecture

```
data-centered/
├── resources.yaml      # All resources across topics (source of truth)
├── authors.yaml        # Contributor metadata & demographics
├── kb-*.html           # Topic pages (any subject worth exploring)
└── styles.css          # TUI-inspired design system
```

### resources.yaml

Structured metadata for every resource in the knowledge base:

```yaml
resources:
  - id: ai-ready-data-technical-assessment
    url: https://example.com/article
    preferredLabel: "AI-Ready Data: Technical Assessment"
    alternateLabels: [AI data readiness, data architecture]
    definition: >
      Practical framework for assessing data readiness for AI.
    author: s-paul
    source: Substack
    contentType: essay
    domain: knowledge-engineering
    category: Core Architecture
    granularity: conceptual
    readingTime: 10m
```

### authors.yaml

Tracks *whose knowledge* you're building on—demographics, perspectives, and professional background:

```yaml
authors:
  - id: j-talisman
    name: Jessica Talisman
    gender: female
    location:
      country: USA
      continent: North America
    jobTitle: Senior Information Architect
    perspectiveType: practitioner
    yearsInField: 25
```

This enables the **Insights Dashboard**—a TUI-style visualization showing geographic distribution, gender balance, perspective types (practitioner vs academic vs vendor), and gaps in representation.

## Knowledge Provenance

The core idea: understanding *where* knowledge comes from matters as much as the knowledge itself.

By tracking author demographics and perspective types, the system surfaces:
- Whose voices are represented (and whose are missing)
- Geographic and cultural distribution
- Balance between practitioners, academics, vendors, journalists
- Potential blind spots in the knowledge base

## Design

Mobile-first, terminal-inspired UI:
- Sticky section headers
- Collapsible sections
- Compact link rows with tap-to-expand
- Monospace aesthetic

## License

MIT
