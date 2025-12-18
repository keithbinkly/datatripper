# Automated Ingestion Pipeline Design

## Overview

An automated pipeline to ingest new resources into `data-centered.com` using **Unstructured** for content extraction and **DSPy** for semantic classification and metadata generation.

---

## Architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Input Sources  │────▶│  Unstructured    │────▶│  DSPy Modules   │
│  - URLs         │     │  (Content Parse) │     │  (Classify &    │
│  - PDFs         │     │  - HTML → Text   │     │   Enrich)       │
│  - RSS Feeds    │     │  - PDF → Text    │     │                 │
│  - Bookmarks    │     │  - Clean/Chunk   │     │                 │
└─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                          │
                                                          ▼
┌─────────────────────────────────────────────────────────────────────┐
│                        DSPy Pipeline                                │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐  ┌──────────────┐  │
│  │ Classifier │  │ Definition │  │ Author     │  │ Relationship │  │
│  │ - domain   │  │ Generator  │  │ Extractor  │  │ Mapper       │  │
│  │ - category │  │ - scope    │  │ - name     │  │ - broader    │  │
│  │ - content  │  │ - bounds   │  │ - platform │  │ - related    │  │
│  │   Type     │  │ - value    │  │ - bio      │  │ - requires   │  │
│  └────────────┘  └────────────┘  └────────────┘  └──────────────┘  │
└─────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
                    ┌───────────────────────┐
                    │  YAML Generation      │
                    │  - resources.yaml     │
                    │  - authors.yaml       │
                    │  - Review Queue       │
                    └───────────────────────┘
```

---

## Components

### 1. Content Ingestion (Unstructured)

**Purpose:** Extract clean, structured text from diverse content formats.

```python
from unstructured.partition.auto import partition
from unstructured.partition.html import partition_html
from unstructured.cleaners.core import clean

def ingest_url(url: str) -> dict:
    """Extract and clean content from a URL."""
    elements = partition_html(url=url)

    # Extract key sections
    title = next((e.text for e in elements if e.category == "Title"), None)
    body_elements = [e for e in elements if e.category in ("NarrativeText", "ListItem")]

    return {
        "url": url,
        "title": title,
        "text": "\n".join(clean(e.text) for e in body_elements),
        "metadata": {
            "detected_language": detect_language(body_elements),
            "word_count": sum(len(e.text.split()) for e in body_elements),
            "has_code": any("```" in e.text or "<code>" in e.text for e in elements)
        }
    }
```

**Supported Input Types:**
- URLs (HTML articles, blog posts)
- PDFs (papers, ebooks)
- RSS/Atom feeds (batch ingestion)
- Browser bookmarks export (JSON/HTML)
- Markdown files

### 2. DSPy Classification Module

**Purpose:** Classify content into the existing taxonomy.

```python
import dspy

class ResourceClassifier(dspy.Signature):
    """Classify a resource into the data-centered.com taxonomy."""

    title: str = dspy.InputField(desc="Resource title")
    content: str = dspy.InputField(desc="First 2000 chars of content")
    existing_domains: list = dspy.InputField(desc="Available domains from resources.yaml")
    existing_categories: list = dspy.InputField(desc="Available categories per domain")

    domain: str = dspy.OutputField(desc="Best matching domain ID")
    category: str = dspy.OutputField(desc="Best matching category within domain")
    content_type: str = dspy.OutputField(
        desc="One of: essay, blog, video, podcast, documentation, paper"
    )
    granularity: str = dspy.OutputField(
        desc="One of: foundational, conceptual, implementation, advanced"
    )
    confidence: float = dspy.OutputField(desc="Classification confidence 0-1")
```

### 3. DSPy Definition Generator

**Purpose:** Generate precise, bounded definitions.

```python
class DefinitionGenerator(dspy.Signature):
    """Generate a definition that establishes semantic boundaries."""

    title: str = dspy.InputField()
    content: str = dspy.InputField(desc="Full extracted content")
    domain: str = dspy.InputField(desc="Classified domain")

    definition: str = dspy.OutputField(
        desc="2-3 sentence definition: what it IS, what it IS NOT, why it matters"
    )
    alternate_labels: list = dspy.OutputField(
        desc="3-5 search terms, synonyms, or acronyms for discoverability"
    )
    reading_time: str = dspy.OutputField(
        desc="Estimated reading time (e.g., '10m', '45m', '2h')"
    )
```

### 4. DSPy Author Extractor

**Purpose:** Extract author metadata for provenance tracking.

```python
class AuthorExtractor(dspy.Signature):
    """Extract author information from content and source."""

    content: str = dspy.InputField()
    url: str = dspy.InputField()
    page_metadata: dict = dspy.InputField(desc="<meta> tags, byline, etc.")

    author_name: str = dspy.OutputField()
    source_platform: str = dspy.OutputField(
        desc="Platform name: Substack, Medium, GitHub, etc."
    )
    author_id_suggestion: str = dspy.OutputField(
        desc="Suggested author ID in format: f-lastname"
    )
    is_organization: bool = dspy.OutputField(
        desc="True if author is a company/org, not individual"
    )
```

### 5. DSPy Relationship Mapper

**Purpose:** Identify connections to existing resources.

```python
class RelationshipMapper(dspy.Signature):
    """Map relationships to existing resources in the knowledge base."""

    new_resource: dict = dspy.InputField(desc="The classified new resource")
    existing_resources: list = dspy.InputField(
        desc="List of existing resource IDs and definitions"
    )

    relationships: list = dspy.OutputField(
        desc="""List of relationship dicts with keys:
        - type: broader | narrower | related | requires-prerequisite | governed-by | is-example-of
        - target: existing resource ID
        - rationale: why this relationship exists
        """
    )
```

---

## Pipeline Flow

### Step 1: URL Submission
```bash
python ingest.py add "https://example.com/article"
```

### Step 2: Content Extraction (Unstructured)
- Fetch and parse URL
- Extract title, body, author byline, publication date
- Clean and normalize text
- Detect content type from structure (video embed? code blocks? podcast player?)

### Step 3: Classification (DSPy)
- Load existing taxonomy from `resources.yaml`
- Run classifier with content
- If confidence < 0.7, flag for human review

### Step 4: Enrichment (DSPy)
- Generate definition with semantic boundaries
- Extract alternate labels for searchability
- Identify author, lookup or create author entry
- Map relationships to existing resources

### Step 5: YAML Generation
```python
def generate_resource_yaml(classified: dict) -> str:
    """Generate YAML entry for resources.yaml."""
    return f"""
  - id: {classified['id']}
    url: {classified['url']}
    preferredLabel: {classified['title']}
    alternateLabels:
{yaml_list(classified['alternate_labels'], indent=6)}
    definition: >
      {classified['definition']}

    # Provenance
    author: {classified['author_id']}
    source: {classified['source']}
    contentType: {classified['content_type']}
    publishedDate: {classified.get('published_date', '~')}
    dateAdded: {today()}

    # Classification
    domain: {classified['domain']}
    category: {classified['category']}
    granularity: {classified['granularity']}

    # Relationships
    relationships:
{yaml_relationships(classified['relationships'])}

    # Quality
    validationStatus: unvalidated

    # Display
    readingTime: {classified['reading_time']}
    color: "{domain_colors[classified['domain']]}"
"""
```

### Step 6: Human Review Queue
- Resources with confidence < 0.7 go to review queue
- New authors require human validation
- Relationships flagged for verification

---

## CLI Interface

```bash
# Add single URL
python ingest.py add "https://example.com/article"

# Batch import from RSS feed
python ingest.py feed "https://blog.example.com/rss"

# Import browser bookmarks (folder-based categorization)
python ingest.py bookmarks ~/bookmarks.html --folder "Data Engineering"

# Review pending resources
python ingest.py review

# Regenerate definitions for existing resources
python ingest.py regenerate-definitions --domain knowledge-engineering
```

---

## Configuration

```yaml
# config/ingestion.yaml

llm:
  provider: anthropic  # or openai, local
  model: claude-3-5-sonnet-20241022
  temperature: 0.3

classification:
  confidence_threshold: 0.7
  auto_approve_threshold: 0.9

author_lookup:
  # APIs to check for author metadata
  sources:
    - linkedin
    - twitter
    - github

relationships:
  # Maximum relationships to suggest per resource
  max_suggestions: 5
  # Minimum similarity score to suggest relationship
  similarity_threshold: 0.6
```

---

## Data Flow Example

**Input:** `https://pluralistic.net/2024/06/21/seedbed/`

**Unstructured Output:**
```json
{
  "url": "https://pluralistic.net/2024/06/21/seedbed/",
  "title": "LLM Maximalism",
  "text": "For more than a year now, I've been cautioning...",
  "metadata": {
    "word_count": 2847,
    "has_code": false,
    "detected_author": "Cory Doctorow"
  }
}
```

**DSPy Classification:**
```json
{
  "domain": "ai-llms",
  "category": "LLM Foundations",
  "content_type": "essay",
  "granularity": "conceptual",
  "confidence": 0.85
}
```

**DSPy Definition:**
```json
{
  "definition": "Critical analysis of LLM hype and the tendency to overfit business processes to AI capabilities. Argues against 'maximalist' integration where every process is forced through an LLM regardless of suitability.",
  "alternate_labels": ["AI hype critique", "LLM overreach", "AI maximalism"],
  "reading_time": "15m"
}
```

**Generated YAML:**
```yaml
- id: llm-maximalism-doctorow
  url: https://pluralistic.net/2024/06/21/seedbed/
  preferredLabel: "LLM Maximalism"
  alternateLabels:
    - AI hype critique
    - LLM overreach
    - AI maximalism
  definition: >
    Critical analysis of LLM hype and the tendency to overfit business
    processes to AI capabilities. Argues against 'maximalist' integration
    where every process is forced through an LLM regardless of suitability.

  # Provenance
  author: c-doctorow
  source: Pluralistic
  contentType: essay
  publishedDate: 2024-06-21
  dateAdded: 2024-12-18

  # Classification
  domain: ai-llms
  category: LLM Foundations
  granularity: conceptual

  # Relationships
  relationships:
    - type: related
      target: ai-context-gap

  # Quality
  validationStatus: unvalidated

  # Display
  readingTime: 15m
  color: "#a855f7"
```

---

## Future Enhancements

### Phase 2: Vector Search
- **FAISS or Qdrant** for similarity-based relationship discovery
- Embed all resource definitions
- Find semantically similar resources beyond keyword matching

### Phase 3: RSS Auto-Sync
- Monitor configured RSS feeds
- Auto-ingest new posts meeting quality criteria
- Daily digest of new additions

### Phase 4: Quality Scoring
- Use **cleanlab** to identify noisy/low-quality entries
- Confidence intervals on classifications
- Human feedback loop to improve models

---

## Dependencies

```toml
[project]
name = "data-centered-ingestion"
dependencies = [
    "unstructured[all-docs]>=0.15.0",
    "dspy-ai>=2.5.0",
    "pyyaml>=6.0",
    "python-slugify>=8.0",
    "httpx>=0.27.0",
    "feedparser>=6.0",
    "beautifulsoup4>=4.12",
]
```

---

## File Structure

```
data-centered/
├── ingest.py              # CLI entry point
├── ingestion/
│   ├── __init__.py
│   ├── extractors.py      # Unstructured wrappers
│   ├── classifiers.py     # DSPy modules
│   ├── yaml_writer.py     # YAML generation
│   └── review_queue.py    # Human review management
├── config/
│   └── ingestion.yaml     # Pipeline configuration
├── queue/
│   └── pending.yaml       # Resources awaiting review
├── resources.yaml         # Main knowledge base
└── authors.yaml           # Author metadata
```

---

## Implementation Priority

1. **Core Pipeline** - Single URL ingestion with classification
2. **CLI Interface** - Add, review, approve workflow
3. **Author Management** - Lookup and creation
4. **Relationship Mapping** - Connect to existing resources
5. **Batch Import** - RSS and bookmarks support
6. **Vector Search** - Semantic relationship discovery
