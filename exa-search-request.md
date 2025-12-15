# Exa Search Request: Substack Author Metadata

**Purpose:** Fill in missing author metadata for knowledge base articles
**Agent:** Cursor (with Exa MCP access)
**Source:** `substack-bookmarks-categorized.md`

---

## Instructions

Use Exa search to find:
1. **Author full name** - from LinkedIn, Twitter, or about page
2. **Author affiliation** - company, role, or organization
3. **Publication description** - tagline or focus area
4. **Author location** - city/country if discoverable

### Rules
- Only update if confident (>90% match)
- Prefer LinkedIn > Twitter > Substack About page
- Note source URL for each finding
- Skip if ambiguous or multiple possible matches

### Output Format
Update the corresponding entry in `authors.yaml` or create new entries:

```yaml
- id: author-handle
  name: Full Name
  handle: "@twitter_or_substack"
  affiliation: Company Name
  role: Job Title
  location:
    city: City
    country: Country
  bioSource: https://linkedin.com/in/...
```

---

## High Priority - Prolific Authors

### Modern Data 101 (s-paul?)
- **Substack:** https://moderndata101.substack.com/
- **Search queries:**
  - `"Modern Data 101" substack author linkedin`
  - `site:linkedin.com "Modern Data 101" data`
- **Missing:** Full name, location, affiliation
- **Articles in KB:** 12

### Seattle Data Guy (Ben Rogojan)
- **Substack:** https://seattledataguy.substack.com/
- **Likely known:** Confirm as Ben Rogojan
- **Search queries:**
  - `"Seattle Data Guy" Ben Rogojan linkedin`
- **Articles in KB:** 7

### The Algorithmic Bridge
- **Substack:** https://thealgorithmicbridge.com/
- **Search queries:**
  - `"The Algorithmic Bridge" author substack linkedin`
- **Missing:** Author name, affiliation
- **Articles in KB:** 4

### The Dankoe (Dan Koe)
- **Substack:** https://thedankoe.com/
- **Likely known:** Dan Koe
- **Search queries:**
  - `"Dan Koe" linkedin location`
- **Missing:** Location, current role
- **Articles in KB:** 3

### Future Proof Data Science
- **Substack:** https://futureproofdatascience.substack.com/
- **Search queries:**
  - `"Future Proof Data Science" author linkedin`
- **Missing:** Author name, affiliation
- **Articles in KB:** 1

---

## Medium Priority - Niche Authors

### Jeff (Exen.io)
- **Substack:** https://jeff4exenio.substack.com/
- **Search queries:**
  - `Exen.io founder linkedin`
  - `"jeff" exen.io data linkedin`
- **Missing:** Full name, location
- **Articles in KB:** 2

### Rasmus Engelbrecht
- **Substack:** https://rasmusengelbrecht.substack.com/
- **Search queries:**
  - `"Rasmus Engelbrecht" linkedin semantic layer`
- **Missing:** Location, affiliation
- **Articles in KB:** 1

### Jimmy Pang
- **Substack:** https://jimmypang.substack.com/
- **Search queries:**
  - `"Jimmy Pang" dbt data engineering linkedin`
- **Missing:** Location, affiliation
- **Articles in KB:** 1

### Jessica Talisman
- **Substack:** https://jessicatalisman.substack.com/
- **Search queries:**
  - `"Jessica Talisman" Adobe knowledge management linkedin`
- **Known:** Adobe, Senior Information Architect
- **Missing:** City (likely SF Bay Area, Seattle, or San Jose)
- **Articles in KB:** 1

### Jay Sobel
- **Substack:** jaysobel.substack.com
- **Search queries:**
  - `"Jay Sobel" dbt labs linkedin`
- **Missing:** Full name confirmation, role at dbt Labs
- **Articles in KB:** 1

### Juan Sequeda
- **Substack:** https://juansequeda.substack.com/
- **Search queries:**
  - `"Juan Sequeda" knowledge graph data.world linkedin`
- **Likely:** data.world, Principal Scientist
- **Missing:** Confirm current role, location
- **Articles in KB:** 1

### Ramona Ctruta
- **Substack:** ramonactruta.substack.com
- **Search queries:**
  - `"Ramona Ctruta" knowledge architect linkedin`
- **Missing:** Full profile
- **Articles in KB:** 1

### Jenna Jordan
- **Website:** jennajordan.me
- **Search queries:**
  - `"Jenna Jordan" librarian data teams linkedin`
- **Missing:** Affiliation, location
- **Articles in KB:** 1

---

## Lower Priority - Single Article Authors

### Torsten Walbaum
- **Search:** `"Torsten Walbaum" linkedin AI`
- **Articles:** 2

### Tyler Folkman
- **Search:** `"Tyler Folkman" AI linkedin claude`
- **Articles:** 1

### Gregor Ojstersek
- **Search:** `"Gregor Ojstersek" engineering leader linkedin`
- **Articles:** 1

### Giacomo Falcone
- **Search:** `"Giacomo Falcone" learning linkedin`
- **Articles:** 1

### Howard Yu
- **Search:** `"Howard Yu" IMD business school linkedin`
- **Likely:** IMD Professor
- **Articles:** 1

### Leonie Monigatti
- **Known:** Weaviate Developer Advocate
- **Search:** `"Leonie Monigatti" Weaviate location`
- **Missing:** City (likely Amsterdam or Germany)
- **Articles:** 1

### Sankalp Agarwal
- **Website:** sankalp.bearblog.dev
- **Search:** `"Sankalp Agarwal" engineer prompt caching linkedin`
- **Articles:** 1

### Casey Handmer
- **Website:** caseyhandmer.wordpress.com
- **Search:** `"Casey Handmer" energy linkedin`
- **Articles:** 1

### David Bau
- **Website:** davidbau.com
- **Search:** `"David Bau" AI researcher linkedin`
- **Articles:** 1

---

## Publication Research

These Substack publications need description/focus area:

| Publication | URL | Suggested Search |
|-------------|-----|------------------|
| Modern Data 101 | moderndata101.substack.com | `"Modern Data 101" substack about` |
| Pipeline to Insights | pipeline2insights.substack.com | `"Pipeline to Insights" data substack` |
| Metadata Weekly | metadataweekly.substack.com | `"Metadata Weekly" author about` |
| Learn Analytics Engineering | learnanalyticsengineering.substack.com | `"Learn Analytics Engineering" about` |
| dbtips | dbtips.substack.com | `dbtips substack author` |
| Gradient Flow | gradientflow.substack.com | `"Gradient Flow" AI substack ben lorica` |
| Elite AI-Assisted Coding | elite-ai-assisted-coding.dev | `"Elite AI-Assisted Coding" author` |
| Hands On Data | handsondata.substack.com | `"Hands On Data" substack author` |
| nastengraph | nastengraph.substack.com | `nastengraph substack data warehouse` |

---

## Exa Search API Reference

```python
# Example Exa search for author discovery
from exa_py import Exa

exa = Exa(api_key="YOUR_KEY")

# Author search
result = exa.search(
    query="\"Seattle Data Guy\" Ben Rogojan linkedin",
    num_results=5,
    type="keyword"
)

# Publication about page
result = exa.search(
    query="Modern Data 101 substack about author",
    num_results=3,
    use_autoprompt=True
)
```

---

## Output Checklist

After completing searches, update:

- [ ] `authors.yaml` - Add/update author entries
- [ ] `substack-bookmarks-categorized.md` - Update Author/Source column where confirmed
- [ ] This file - Mark completed searches with checkmarks

### Completed Searches
<!-- Mark completed items here -->
- [ ] Modern Data 101
- [ ] Seattle Data Guy
- [ ] The Algorithmic Bridge
- [ ] The Dankoe
- [ ] Future Proof Data Science
- [ ] Jeff (Exen.io)
- [ ] Rasmus Engelbrecht
- [ ] Jimmy Pang
- [ ] Jessica Talisman
- [ ] Jay Sobel
- [ ] Juan Sequeda
- [ ] Ramona Ctruta
- [ ] Jenna Jordan

---

## Schema for authors.yaml

```yaml
# Author entry schema
- id: string  # kebab-case-name
  name: string  # Full display name
  handle: string | null  # @twitter or substack handle
  gender: enum [male, female, non-binary, unknown]
  affiliation: string | null  # Company/org
  role: string | null  # Job title
  location:
    city: string | null
    country: string | null
    continent: string | null  # Derived
  bioSource: string  # URL where bio info found
  substacks:
    - name: Publication Name
      url: https://example.substack.com/
      focus: string  # 1-line description
  expertise:
    - string  # e.g., "dbt", "semantic layers", "data engineering"
  socialLinks:
    linkedin: string | null
    twitter: string | null
    website: string | null
```
