# Author Research Queue

Use Exa search to fill in missing demographic data for authors in `authors.yaml`.

---

## Instructions

### Where to put answers
Update fields directly in `/Users/kbinkly/git-repos/data-centered/authors.yaml`

### Rules
- **Only update if confident** - leave `~` if uncertain
- **Note your source** - update `bioSource` if you find a better primary source (LinkedIn > Twitter > blog)
- **City granularity** - prefer city over just country when findable
- **Don't guess** - if search returns nothing definitive, skip

### Field format
```yaml
location:
  city: San Francisco    # or ~
  country: USA           # or ~
  continent: North America  # derive from country
```

---

## High Priority (LinkedIn-findable)

### j-talisman (Jessica Talisman)
- **Missing:** `city`
- **Known:** Adobe, USA, Senior Information Architect
- **Search:** `"Jessica Talisman" Adobe location` or `site:linkedin.com "Jessica Talisman" Adobe`
- **Likely:** SF Bay Area, Seattle, or San Jose (Adobe offices)

### v-vashishta (Vin Vashishta)
- **Missing:** `city`
- **Known:** USA, V Squared AI CEO
- **Search:** `"Vin Vashishta" location` or check linkedin.com/in/vineetvashishta
- **Likely:** Texas or California

### a-karpathy (Andrej Karpathy)
- **Missing:** `city`
- **Known:** USA, former Tesla/OpenAI
- **Search:** `"Andrej Karpathy" location`
- **Likely:** SF Bay Area

### t-macey (Tobias Macey)
- **Missing:** `city`
- **Known:** USA, Data Engineering Podcast host
- **Search:** `"Tobias Macey" location` or `"Data Engineering Podcast" host location`

### k-flerlage (Kevin Flerlage)
- **Missing:** `city`, `affiliation`
- **Known:** USA, Tableau Zen Master, Analytics Manager
- **Search:** `"Kevin Flerlage" Tableau location`
- **Note:** Has twin brother Ken, runs Flerlage Twins blog

### j-shaffer (Jeffrey Shaffer)
- **Missing:** `city`, `jobTitle`
- **Known:** USA, Tableau expert
- **Search:** `"Jeffrey Shaffer" Tableau location`
- **Likely:** Cincinnati area (check Data + Science blog)

### j-lindquist (John Lindquist)
- **Missing:** `city`
- **Known:** USA, Egghead.io co-founder
- **Search:** `"John Lindquist" egghead location`

---

## Medium Priority (Substack/Platform authors)

### s-paul
- **Missing:** `full name`, `gender`, `city`, `country`, `jobTitle`
- **Search:** `"Modern Data 101" author` or `site:linkedin.com "Modern Data 101"`
- **bioSource:** https://moderndata101.substack.com/

### p-sankar
- **Missing:** `full name`, `gender`, `city`, `country`, `jobTitle`
- **Known:** Atlan affiliation
- **Search:** `site:linkedin.com Atlan "Sankar"` or check Atlan team page

### v-dacanay
- **Missing:** `full name`, `gender`, `city`, `country`, `jobTitle`
- **Search:** `"Metadata Weekly" author linkedin`
- **bioSource:** https://metadataweekly.substack.com/

### j-jordan
- **Missing:** `full name`, `gender`, `city`, `country`, `jobTitle`
- **Search:** `"Data Intelligence Platform" substack author`

### j-sobel
- **Missing:** `full name`, `gender`, `city`, `country`, `jobTitle`
- **Known:** dbt Labs
- **Search:** `site:linkedin.com "Sobel" "dbt Labs"` or check dbt Labs team page

### a-negro (Alessandro Negro)
- **Missing:** `city`, `country`, `jobTitle`, `affiliation`
- **Search:** `"Alessandro Negro" knowledge graph linkedin`
- **Note:** Italian name, may be in Europe or US

### s-agarwal (Sankalp Agarwal)
- **Missing:** `city`, `country`, `jobTitle`, `affiliation`
- **Search:** `"Sankalp Agarwal" engineer linkedin`
- **bioSource:** https://sankalp.bearblog.dev/

### l-monigatti (Leonie Monigatti)
- **Missing:** `city`, `country`
- **Known:** Weaviate Developer Advocate
- **Search:** `"Leonie Monigatti" Weaviate location`
- **Likely:** Amsterdam (Weaviate HQ) or Germany

### j-ouyang (Jenny Ouyang)
- **Missing:** `city`, `country`, `jobTitle`, `affiliation`
- **Search:** `"Jenny Ouyang" linkedin`

### j-pang (Jimmy Pang)
- **Missing:** `city`, `country`, `jobTitle`, `affiliation`
- **Search:** `"Jimmy Pang" data engineering linkedin`

---

## Lower Priority (Limited web presence)

### j-johansson (John Johansson)
- **Missing:** `city`, `country`, `jobTitle`, `affiliation`
- **Search:** `"John Johansson" Tableau`
- **Note:** Common name, may be hard to disambiguate

### f-sebben (Felipe Sebben)
- **Missing:** `city`, `country`, `jobTitle`
- **Search:** `"Felipe Sebben" Tableau linkedin`
- **Likely:** Brazil (Portuguese name)

### k-klaassen (Kieran Klaassen)
- **Missing:** `city`, `country`, `jobTitle`, `affiliation`
- **Search:** `"Kieran Klaassen" linkedin`

### m-mengto (Meng To)
- **Missing:** `city`, `country`
- **Known:** Design+Code founder
- **Search:** `"Meng To" Design+Code location`

### thedotmack (Mack Talcott)
- **Missing:** `city`, `country`, `jobTitle`
- **Search:** `"Mack Talcott" linkedin` or `thedotmack github`

### gouline (Mike Gouline)
- **Missing:** `city`, `country`, `jobTitle`
- **Search:** `"Mike Gouline" linkedin`

### ponderedw
- **Missing:** Everything (GitHub handle only)
- **Search:** `ponderedw github` - likely pseudonym, may not find

---

## Organizations (if time permits)

### momo-research
- **Missing:** `foundedYear`, `city`, `country`
- **Search:** `"Momo" AI assistant company`

### answerlayer-team
- **Missing:** `foundedYear`, `city`, `country`
- **Search:** `AnswerLayer company location`

### the-pudding
- **Missing:** `city`
- **Known:** USA
- **Search:** `"The Pudding" office location`
- **Likely:** NYC or distributed

### the-data-hustle
- **Missing:** `foundedYear`, `city`, `country`
- **Search:** `"The Data Hustle" author`

### spark-research
- **Missing:** `city`, `country`
- **Search:** Check arXiv paper authors for affiliations

---

## Example Update

Before:
```yaml
- id: j-talisman
  location:
    city: ~
    country: USA
```

After (if found):
```yaml
- id: j-talisman
  location:
    city: San Jose
    country: USA
```
