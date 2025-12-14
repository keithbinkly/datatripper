# Agent Guide: Processing Resources

Instructions for AI agents adding resources to this knowledge base.

## Philosophy

This isn't just a bookmark list. We track **knowledge provenance**—understanding *whose* knowledge you're building on. Every resource needs an author, and every author gets demographic metadata to surface representation gaps.

## Processing a Resource Dump

When given a batch of URLs/resources:

### 1. For each resource, extract or research:

```yaml
- id: kebab-case-identifier          # Required: stable, unique
  url: https://...                    # Required: canonical URL
  preferredLabel: "Title Here"        # Required: authoritative title
  alternateLabels:                    # Optional: synonyms, search terms
    - alternate name
    - acronym
  definition: >                       # Required: 1-2 sentence description
    What this resource teaches and why it matters.

  # Provenance
  author: author-id                   # Required: references authors.yaml
  source: Platform Name               # Required: Substack, YouTube, etc.
  contentType: essay                  # Required: essay | podcast | video | documentation | blog | paper
  publishedDate: 2024-01-15           # Optional: YYYY-MM-DD if known
  dateAdded: 2024-12-14               # Required: today's date

  # Classification
  domain: knowledge-engineering       # Required: must match domains list
  category: Core Architecture         # Required: must match domain's categories
  granularity: conceptual             # Required: foundational | conceptual | implementation | advanced

  # Relationships (optional but valuable)
  relationships:
    - type: related                   # broader | narrower | related | requires-prerequisite | governed-by | is-example-of
      target: other-resource-id

  # Quality
  validationStatus: unvalidated       # unvalidated | reviewed | tested

  # Display
  readingTime: 10m                    # Required: estimated consumption time
  color: "#06b6d4"                    # Optional: inherit from domain
```

### 2. For each author, create or update entry in authors.yaml:

```yaml
- id: firstname-initial-lastname      # e.g., j-talisman, k-cagle
  name: Full Name

  # Demographics (use ~ for unknown, research if possible)
  birthYear: ~
  generation: ~                       # Gen X, Millennial, etc.
  gender: ~                           # female, male, non-binary, ~
  location:
    city: ~
    country: USA
    continent: North America

  # Professional
  jobTitle: ~
  industry: ~
  affiliation: Company/Publication
  perspectiveType: practitioner       # practitioner | academic | vendor | journalist | researcher
  yearsInField: ~

  # Background
  education: ~
  nativeLanguage: ~

  # Meta
  socialFollowing: ~                  # small (<10k), medium (10k-100k), large (>100k)
  bio: >
    Brief description of who they are and their expertise.
  bioSource: https://...              # Where you got the bio info
```

### 3. Research author demographics

For each new author:
1. Check LinkedIn, Twitter/X, personal website
2. Look for: location, job title, affiliation, education
3. Note `bioSource` for where you found information
4. Use `~` for genuinely unknown fields—don't guess

**Why this matters:** The insights dashboard shows geographic distribution, gender balance, perspective types. Gaps in data = gaps in understanding representation.

## Granularity Levels

| Level | Description | Example |
|-------|-------------|---------|
| `foundational` | Core concepts, prerequisites | "What is an ontology?" |
| `conceptual` | Mental models, frameworks | "Knowledge graph architecture patterns" |
| `implementation` | How-to, practical guides | "Building a taxonomy in Neo4j" |
| `advanced` | Deep dives, cutting edge | "Neurosymbolic AI approaches" |

## Perspective Types

| Type | Description |
|------|-------------|
| `practitioner` | Works hands-on building systems |
| `academic` | University researcher, professor |
| `vendor` | Works for tool/platform company |
| `journalist` | Tech writer, reporter |
| `researcher` | Independent or industry researcher |

## Content Types

`essay` | `podcast` | `video` | `documentation` | `blog` | `paper`

## Relationship Types

| Type | Meaning |
|------|---------|
| `broader` | Target is a more general concept |
| `narrower` | Target is a more specific concept |
| `related` | Conceptually connected |
| `requires-prerequisite` | Should read target first |
| `governed-by` | Target provides standards/rules |
| `is-example-of` | Target is the general pattern |

## Ontology Mappings (Optional)

For linked data interoperability, resources can map to external ontologies/vocabularies:

```yaml
  # Ontology Mappings
  ontologyMappings:
    exactMatch: http://dbpedia.org/resource/Knowledge_graph
    closeMatch: http://www.wikidata.org/entity/Q33002955
    wikidataId: Q33002955
    dbpediaUri: http://dbpedia.org/resource/Knowledge_graph
    lcsh: http://id.loc.gov/authorities/subjects/sh2019001234
    schemaType: TechArticle
```

| Field | Purpose | Example |
|-------|---------|---------|
| `exactMatch` | Equivalent concept (skos:exactMatch) | DBpedia or other ontology URI |
| `closeMatch` | Similar but not identical (skos:closeMatch) | Related Wikidata entity |
| `wikidataId` | Wikidata entity ID | `Q33002955` (Knowledge graph) |
| `dbpediaUri` | DBpedia resource URI | `http://dbpedia.org/resource/Ontology` |
| `lcsh` | Library of Congress Subject Heading | `http://id.loc.gov/authorities/subjects/...` |
| `schemaType` | Schema.org type | `Article`, `TechArticle`, `LearningResource` |

**How to find mappings:**
1. Search Wikidata for the concept: https://www.wikidata.org
2. Check DBpedia for equivalent: https://dbpedia.org
3. Search LCSH: https://id.loc.gov/authorities/subjects.html
4. Reference Schema.org types: https://schema.org/docs/full.html

**When to add mappings:**
- Resources about well-defined concepts (knowledge graphs, ontologies, taxonomies)
- Topics with clear Wikidata/Wikipedia entries
- Skip for highly specific or proprietary content

## Example: Processing a Dump

User provides:
```
Here are some resources to add:
- https://example.com/knowledge-graphs-101
- https://youtube.com/watch?v=xyz (Joe Reis on data modeling)
```

Agent should:
1. Fetch/read each URL to understand content
2. Create resource entries with full metadata
3. Check if authors exist in authors.yaml
4. Create new author entries if needed, researching demographics
5. Add resources to appropriate category section in resources.yaml
6. Update `metadata.totalResources` count
7. Commit with message like "Add 2 resources: knowledge graphs, data modeling"

## File Locations

```
/resources.yaml    # All resources, organized by category
/authors.yaml      # All author demographic data
/kb-*.html         # Topic pages (reference only, don't edit for resource adds)
```

## Don'ts

- Don't guess demographics—use `~` for unknown
- Don't skip author entries—every resource needs one
- Don't duplicate IDs—check existing resources first
- Don't add resources without `definition`—we need semantic context
- Don't forget `dateAdded`—always today's date
