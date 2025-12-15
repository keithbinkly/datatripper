# Resource Intake Queue

## Instructions
Paste resources below. Include URL and any available metadata. Skip items without sources.

Format per resource:
```
- URL:
- Title:
- Author:
- Source/Publication:
- Date Published:
- Notes:
```

---

## Queue

<!-- Paste new resources here for processing -->

---

## Archive: 2025-12-13 Source Batch

*Original source document preserved for reference*

# Resources

Master resource library for all data work: grapht, government data viz, enterprise semantic layer, career content.

Tags: `#viz` `#dbt` `#ai-tools` `#gov-data` `#design` `#engineering` `#career`

For philosophy and rules, see `DESIGN_PRINCIPLES.md`.

---

## Design Inspiration

### Tableau Exemplars
*Outstanding dashboards and guides worth emulating*
- [Visual Vocabulary](https://public.tableau.com/app/profile/andy.kriebel/viz/VisualVocabulary/VisualVocabulary) (Andy Kriebel) - Chart type selection guide
- [Bar Design Guide](https://public.tableau.com/app/profile/john.johansson/viz/BarDesignGuide/BarDesignGuide) (John Johansson) - Bar chart best practices
- [10 Commandments of Big Numbers](https://public.tableau.com/app/profile/felipe.sebben/viz/The10CommandmentsofBigNumbersinPractice/The10CommandmentsofBigNumbers) (Felipe Sebben) - KPI card design
- [KPI Color Encoding](https://public.tableau.com/views/MasteringTableau2_KPIcollection1-ColorencodingforKPIcards/Dashboard) - KPI card color patterns
- [Tableau Chart Catalog](https://public.tableau.com/app/profile/kevin.flerlage/viz/TheTableauChartCatalog/TableauChartExamples) (Kevin Flerlage) - Comprehensive chart examples

### UI/UX Articles
- **[10 UI Design Principles](https://x.com/kieranklaassen/status/1992350089118183433)** - Fewer colors, larger fonts, whitespace, system fonts, high contrast
- **[Avoiding AI Slop Design](https://x.com/mengto/status/1992213336205951143)** - Swiss design, Japanese minimalism, Apple's design system

### Physical Material Inspiration
Study these for "precise and weighty" texture:
- Fine leather goods - grain patterns, natural texture
- Wood furniture - visible grain, solid construction
- Precision instruments - weighted controls, smooth movement
- Luxury automotive dashboards - Ferrari, Lamborghini, Rolls Royce

### Game UI Inspiration
**Diegetic UI (integrated into world):**
- Dead Space - health bar on spine, holographic inventory
- Metro series - watch-based UI, physical map checking
- Alien: Isolation - motion tracker, chunky 70s-futurism

**Weighted interactions:**
- Destiny (Bungie) - legendary weapon feel, "30 seconds of fun"
- DOOM (2016/Eternal) - snappy but weighted weapon switching
- Ghost of Tsushima - Guiding Wind, natural minimalism

**Data visualization in games:**
- Hitman 3 - sophisticated mission briefing overlays
- Watch Dogs 2 - grounded cyberpunk hacking visuals
- The Division - military-grade holographic interfaces

---

## Data Storytelling

### The Pudding
**Process Guides:**
- [How to Make Dope Shit Part 1](https://pudding.cool/process/how-to-make-dope-shit-part-1/)
- [How to Make Dope Shit Part 2](https://pudding.cool/process/how-to-make-dope-shit-part-2/)
- [How to Make Dope Shit Part 3](https://pudding.cool/process/how-to-make-dope-shit-part-3/)
- [Scrollytelling Implementation](https://pudding.cool/process/how-to-implement-scrollytelling/)
- [Responsive Scrollytelling](https://pudding.cool/process/responsive-scrollytelling/)

**GitHub Repos:**
- [Svelte Starter](https://github.com/the-pudding/svelte-starter)
- [Love Songs](https://github.com/the-pudding/pop-love-songs)
- [Svelte Templates](https://github.com/the-pudding/svelte-templates)
- [Data Sets](https://github.com/the-pudding/data)

---

## Frontend Libraries

### Visualization
- **[D3.js](https://d3js.org/)** - Custom data visualizations
- **[LayerCake](https://layercake.graphics/)** - Svelte-D3 integration
- **[Scrollama](https://github.com/russellgoldenberg/scrollama)** - Scroll-driven storytelling
- **[SvelteKit](https://kit.svelte.dev/)** - Production framework

### Animation & Components
- **[aura.build](https://aura.build)** - High-quality animated components
  - [nebula.aura.build](https://nebula.aura.build)
  - [sakura.aura.build](https://sakura.aura.build)
  - [aura.build/components](https://aura.build/components)
- **[codepen.io](https://codepen.io)** - Component examples and animations
- **[21st.dev](https://21st.dev)** - Modern component library
- **[uiverse.io](https://uiverse.io)** - UI elements and animations

### React Utilities
- **[aitmpl.com/hooks](https://aitmpl.com/hooks)** - Ready-to-use hooks collection ([source](https://x.com/dani_avila7/status/1992271574729363928))

---

## Technical Stack

### Observability
- **[Arize Phoenix](https://github.com/Arize-ai/phoenix)** - OpenTelemetry instrumentation patterns
  - `openinference-instrumentation-anthropic` for Claude Code OTEL collection

### Data Transformation
- **dbt** - Data transformation pipelines
- **Docker** - Containerized development environment

### Image Generation
- **[Nano Banana (Gemini) Skill](https://github.com/EveryInc/every-marketplace/tree/d44804fc39d60bb7914d971cc90bdb98e3b3e710/plugins/compounding-engineering/skills/gemini-imagegen)** - Visual assets and mockups
  - Excellent for cartography - hand-drawn maps from satellite imagery ([example](https://x.com/bilawalsidhu/status/1991635734546284703))
- **[Consistent Hero Images Workflow](https://open.substack.com/pub/jennyouyang/p/how-i-create-consistent-hero-images-and-why-i-havent-switched-to-nanobanana)** (Jenny Ouyang) - Process for creating consistent image assets

---

## AI/LLM Tools

### Context Engineering & Memory `✅ Evaluated 2025-12-10`

*Foundational research for transforming agents from stateless to learning systems*

- **[Context Engineering for Agents](https://blog.langchain.com/context-engineering-for-agents/)** (LangChain) `✅ Evaluated`
  - **What:** Comprehensive framework - 4 strategies (Write, Select, Compress, Isolate) with failure modes
  - **Key insight:** Failure modes (poisoning, distraction, clash, confusion) more useful than success patterns
  - **Implemented:** `tools/kg/agent_integration.py` - `check_context_health()` function

- **[Context Engineering Deep Dive](https://weaviate.io/blog/context-engineering)** (Weaviate) `✅ Evaluated`
  - **What:** Framework covering Write/Select/Compress/Isolate strategies with implementation details
  - **Key insight:** 87.5% of agent failures are context problems, not model capability
  - **Implemented:** Health check patterns in `tools/kg/agent_integration.py`

- **[How Prompt Caching Works](https://sankalp.bearblog.dev/how-prompt-caching-works/)** `✅ Evaluated`
  - **What:** Technical deep dive on prompt caching (Anthropic, OpenAI, Gemini implementations)
  - **Key patterns:** Stable prefixes, append-only context, ~90% cost reduction on cached tokens
  - **Actionable:** Structure system prompts with static content first, dynamic last

- **[Momo Research: Context Engineering](https://github.com/momo-personal-assistant/momo-research)** `✅ Evaluated` - **🔥 HIGH IMPACT**
  - **What:** Complete framework for AI agent memory across sessions (Google + Manus insights)
  - **Key patterns:** 5-layer memory stack, compaction strategies, memory-as-a-tool
  - **Integration:** Beads `dbt-agent-z5d` (Build Memory Manager module)
  - **Why massive:** Provides unified architecture to connect our KG, KB, session logs, Beads

- **[Spark: Shared Memory for Coding Agents](https://arxiv.org/html/2511.08301v1)** `✅ Evaluated` - **🔥 HIGH IMPACT**
  - **What:** Shared memory architecture enabling agents to learn from each other
  - **Key finding:** Small models benefit most (+0.66 pts vs +0.05 for GPT-5)
  - **Integration:** Beads `dbt-agent-o47` (Implement Session Consolidation)
  - **Why massive:** Enables collective intelligence - Migration agent solves problem → QA agent knows instantly

- **[Memory in AI Agents](https://www.leoniemonigatti.com/blog/memory-in-ai-agents.html)** (Leonie Monigatti) `✅ Evaluated`
  - **What:** Clear taxonomy of memory types (CoALA framework, Letta architecture)
  - **Key insight:** We have all 4 memory types (working, semantic, episodic, procedural) but they're not connected
  - **Integration:** Vocabulary/taxonomy for memory architecture design

### Knowledge Quality & Testing

- **[Semiosis: KB Unit Testing](https://github.com/AnswerLayer/semiosis)** `✅ Evaluated` - **🔥 HIGH IMPACT**
  - **What:** "Unit testing for your knowledge base" - measures if documentation actually works
  - **Key metrics:** Completeness, redundancy, semantic density, critical boundaries (η_c thresholds)
  - **Integration:** Beads `dbt-agent-fdu` (Build KB Quality Testing)
  - **Why massive:** We have 21K chunks - but are they useful? Which are critical vs redundant?

- **[Holy Trinity for Enterprise Data](https://substack.com/inbox/post/179387219)** `✅ Evaluated`
  - **What:** Meta Grid pattern for coordinating multiple metadata repositories
  - **Key insight:** "LLMs trained on fragmented glossaries will hallucinate"
  - **Integration:** Informs Multi-Repository coordination design
  - **Pattern:** Lightweight coordination across KG, KB, Skills, Beads, session logs

### Agent Infrastructure (Future Capabilities)

- **[ADE-Bench](https://github.com/dbt-labs/ade-bench)** (dbt Labs) `✅ Evaluated` - **🔥 HIGH IMPACT**
  - **What:** Benchmark for AI data engineering agents - 8 challenge categories, 60+ tasks
  - **Categories:** Migrations, modeling, documentation, testing, debugging, optimization, MetricFlow, multi-agent
  - **Key insight:** dbt Labs' official benchmark for evaluating agent capabilities
  - **Integration:** Use as validation framework for our migration/QA agents

- **[OSGym](https://github.com/agiopen-org/osgym)** `✅ Evaluated` - Distributed infrastructure for training OS agents
  - **Status:** WATCH (if we need systematic agent training/evaluation)
  - **Key pattern:** Replay buffer, distributed workers, accessibility tree for semantic state

- **[Simular.ai](https://www.simular.ai/)** `✅ Evaluated` - Production-grade computer use agents
  - **Status:** WATCH (if we need browser/desktop automation beyond MCP APIs)
  - **Key stat:** 90.1% WebVoyager, 69.9% OSWorld, Best Paper ICLR 2025

- **[Browser.cash](https://browser.cash/developers)** `❌ Incomplete` - AI browser infrastructure
  - **Status:** DEFER - developer docs not accessible, only marketing page
  - **Re-evaluate when:** Direct API documentation available

### Prompt Execution & Session Memory `✅ Evaluated 2025-12-12`

*Tools for executing prompts and maintaining memory across sessions*

- **[mdflow](https://github.com/johnlindquist/mdflow)** `✅ Evaluated` - **⭐ ADOPT (Priority 3)**
  - **What:** Executable markdown CLI - transforms `.md` files into runnable AI prompts
  - **Key feature:** File imports with `@./path/**/*.sql` - auto-inlines files into prompts
  - **Expected impact:** -95% context loading time, eliminates manual file reads
  - **Status:** Queued for evaluation in `docs/guides/tool-evaluation.md`
  - **Install:** `npm install -g mdflow`
  - **Use case:** `mdflow review-pipeline.claude.md --pipeline merchant` → loads all models + patterns

- **[claude-mem](https://github.com/thedotmack/claude-mem)** `✅ Evaluated` - **📋 EVALUATE (Priority 4)**
  - **What:** Persistent memory plugin for Claude Code - automatic context injection between sessions
  - **Key features:** Auto context at startup, progressive disclosure, "Endless Mode" for extended sessions
  - **Overlap:** Some overlap with existing Beads/unified_retrieval, but auto-injection is unique
  - **Status:** Queued for 1-week evaluation in `docs/guides/tool-evaluation.md`
  - **Install:** `/plugin marketplace add thedotmack/claude-mem`
  - **Risk:** Low - easily removable plugin

- **[snipt](https://github.com/snipt/snipt)** `⏸️ Deferred` - System-wide text snippet expansion
  - **What:** Type `:shortcut` anywhere → expands to predefined content
  - **Why deferred:** Lower ROI than mdflow/claude-mem, VS Code snippets already exist
  - **Reconsider if:** Manual dbt command typing becomes significant pain point

### Other AI Tools

- **[LLM Council](https://github.com/karpathy/llm-council)** (Karpathy) - Query multiple LLMs, compare responses
- **[Agentic Data Scientist](https://github.com/K-Dense-AI/agentic-data-scientist)** - AI hypothesis testing ([source](https://x.com/k_dense_ai/status/1991884557021499859))
- **[CodeWiki](https://github.com/FSoft-AI4Code/CodeWiki/)** - AI-generated documentation for large codebases
- **[OpenMemory](https://github.com/CaviraOSS/OpenMemory/)** - Long-term memory for AI agents
- **[Better Agents](https://github.com/langwatch/better-agents)** (LangWatch) `#TODO` - CLI scaffolding for agent projects with best practices: AGENTS.md, scenario tests, prompt versioning, evaluation notebooks, MCP config
  - [ ] Evaluate for agentic dbt pipeline project structure
  - [ ] Test scenario testing for agent behavior validation
- **[Advanced Tool Use](https://www.anthropic.com/engineering/advanced-tool-use)** (Anthropic) `#TODO` - Three features for scaling tool use:
  - **Tool Search Tool** - On-demand tool discovery, 85% token reduction
  - **Programmatic Tool Calling** - Orchestrate tools via code, parallel execution
  - **Tool Use Examples** - 72%→90% accuracy on complex parameters
  - [ ] Implement for agentic dbt environment (multiple MCP servers)
  - [ ] Add examples to dbt/semantic layer tool definitions

### Agent Failure Modes & Solutions
*For long-running AI coding agents*

| Problem | Initializer Agent Fix | Coding Agent Fix |
|---------|----------------------|------------------|
| Declares victory too early | Set up feature list JSON with end-to-end descriptions | Read feature list at session start, pick one feature to work on |
| Leaves env with bugs/undocumented progress | Write initial git repo + progress notes file | Start by reading progress notes + git logs, run basic test, end with commit + progress update |
| Marks features done prematurely | Set up feature list file | Self-verify all features, only mark "passing" after testing |
| Spends time figuring out how to run app | Write `init.sh` script to run dev server | Start session by reading `init.sh` |

---

## Context & Workflow

- **[Filesystems for Context Engineering](https://blog.langchain.com/how-agents-can-use-filesystems-for-context-engineering/)** (LangChain)
- **[ThinkDashboard](https://github.com/MatiasDesuu/ThinkDashboard/)** - Bookmark dashboard
- **[Beads UI Viewer](https://x.com/doodlestein/status/1993911933272019175)** - UI for Beads task tracker (used for both work dbt/semantic layer and grapht project management)

### Multi-Agent Orchestration Pattern `#TODO`
*Source: @doodlestein tweet on agentic workflow*

**Architecture:**
- 9 agents across 3 platforms (Claude Code, Codex, Gemini CLI) working in parallel
- **Beads** as central task/dependency tracker
- **`bv` tool** - Graph theory analysis on tasks:
  - `bv -robot-insights` - Find bottlenecks blocking downstream work
  - `bv -robot-priority` - Rank by graph centrality (what unblocks most)
  - `bv -robot-plan` - Identify parallel tracks for concurrent work
- **Agent mail** - MCP-based messaging for inter-agent coordination
- **AGENTS.md** - Shared context doc all agents read first

**Key prompt patterns:**
```
"Re-read AGENTS.md first. Then use bv to get insights on what each agent 
should most usefully work on. Share insights via agent mail and explain 
how/why using bv. Use ultrathink."
```

**TODO:** Explore applying this pattern to:
- [ ] Agentic dbt pipeline orchestration
- [ ] Task graph analysis on dbt DAG (bottlenecks, critical path)
- [ ] Multi-agent semantic layer development
- [ ] Beads integration with `bv`-style analysis

---

## Enterprise / Day Job

*Resources for agentic dbt pipeline + semantic layer development environment*

### Data Catalog & Governance
- **[DataHub](https://datahub.com/)** - Metadata platform, data catalog, AI-ready context management

### dbt Best Practices (Articles)
- **[Modeling Success with dbt](https://www.getdbt.com/blog/modeling-success-dbt)** `✅ Evaluated` - dbt Labs guide on data modeling architecture
  - **Integrated into:** `migration-quick-reference.md` (grain rule), `canonical-models-registry.md` (conformed dimensions), `troubleshooting.md` (anti-patterns)
  - **Key insights:** Architecture before implementation, grain is critical, conformed dimensions
- **[dbt MCP Server Conversational Analytics](https://www.getdbt.com/blog/dbt-mcp-server-conversational-analytics)** `✅ Evaluated` - Norlys case study on AI + dbt
  - **Key insight:** Metrics-first approach, upfront data quality investment
  - **Bead:** `dbt-agent-9x5` (domain expertise integration)
- **[Understanding Data Marts](https://jimmypang.substack.com/p/understanding-data-marts-in-modern)** `✅ Evaluated` - Jimmy Pang on modern mart architecture
  - **Key insights:** 5 mart types, tag-based execution, denormalization for cloud
  - **Beads:** `dbt-agent-a85` (mart types), `dbt-agent-qpe` (tag-based execution)

### dbt Tools
- **[dbt-incremental-ci](https://github.com/ponderedw/dbt-incremental-ci)** `✅ Evaluated`
  - **What:** Copies prod data into CI schema for faster, more accurate testing
  - **Key insight:** CI tests against real prod data, not empty schemas
  - **Status:** WATCH - evaluate when CI pipeline optimization needed
  - **Complement to:** `upstream-prod` (different approach, same goal)

- **[upstream-prod](https://github.com/gouline/upstream-prod)** `✅ Evaluated` - dbt package for using prod data in dev, intelligently redirects refs
  - **Status:** KEEP (verified 2025-12-02)
  - **Result:** -97% dev cycle time (55 sec vs 15-30 min)
  - **Integrated into:** `docs/guides/tool-evaluation.md` (Evaluation #1)
  - **How to use:** Add to packages.yml, use `{{ ref_upstream('model') }}` macro
- **[dbt-to-cube](https://github.com/nicholasyager/dbt-to-cube)** - Automates dbt → Cube.js → Superset pipeline, keeps metrics in sync
  - Market validation for semantic layer automation tooling

### IDEs & Development Environments
- **[Nao IDE](https://www.nao.ai/)** - AI data IDE (VS Code fork) with native warehouse connection, dbt-aware
  - Schema + codebase context for AI copilot
  - Built-in data quality checks, column-level lineage
  - Y Combinator backed

---

## Government Data `#gov-data`

*For data catalog and collision hypothesis projects*

### Data Sources
- **[NOAA Storm Events Database](https://www.ncdc.noaa.gov/stormevents/)** - Storm data by county, direct download
- **[CDC WONDER](https://wonder.cdc.gov/)** - Mortality data including opioid deaths, county-level
- **[data.gov](https://data.gov/)** - 300k+ datasets (poor discoverability - opportunity for Dataset Discovery Assistant)

### Collision Hypotheses (from past analysis)
Promising correlations to explore:
- Storms × Opioid deaths (2-month lag hypothesis)
- Climate deviation × Crime patterns
- Air quality × Assault rates
- Drought duration × Suicide rates in agricultural areas

### Reference: Organizing Large Link Libraries
- **[Jeffrey Shaffer's Tableau Reference Guide](https://www.intotableaudata.com/)** - Good model for accordion-style organization with categories

---

## Engineering

- **[Every Engineering Skill Explained](https://x.com/kieranklaassen/status/1992349643607617924)** - Fundamental engineering competencies

---

## AI Learning Resources `#learning`

*Curated from [Ruben's Free AI Courses Guide](https://ruben.substack.com/p/free)*

### ChatGPT/OpenAI
- [ChatGPT Fundamentals](https://academy.openai.com/public/clubs/work-users-ynjqu/resources/chatgpt-basics) - Basics in 3 min
- [Prompting Class](https://academy.openai.com/public/clubs/work-users-ynjqu/resources/prompting) - Science of prompt engineering
- [ChatGPT Image Generation](https://chatgpt.com/features/image-generation/) - Official guide + prompt library

### Claude/Anthropic
- [Claude Basics](https://anthropic.skilljar.com/ai-fluency-framework-foundations) - Anthropic Learning Hub
- [Claude 4 Best Practices](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/claude-4-best-practices) - Advanced prompting
- [Claude Use Cases](https://claude.com/resources/use-cases) - Copy/paste examples
- [Claude Skills Analysis](https://open.substack.com/pub/cashandcache/p/i-analyzed-40-claude-skills-failures) - Detailed guide on skill failures and recommendations

### Gemini/Google
- [Gemini Prompting Guide](https://services.google.com/fh/files/misc/gemini-for-google-workspace-prompting-guide-101.pdf) - Complete guide (PDF)
- [Gemini Context Engineering](https://drive.google.com/file/d/1JW6Q_wwvBjMz9xzOtTldFfPiF7BrdEeQ/view) - Context > prompts
- [Gemini Deep Research](https://gemini.google/tg/overview/deep-research/) - Web/file research
- [Awesome Nano Banana Images](https://github.com/PicoTrex/Awesome-Nano-Banana-images/blob/main/README_en.md) - Case studies repo

### Video Generation
- [Sora Tutorials](https://academy.openai.com/public/collections/sora-tutorials-2025-03-11) - OpenAI video basics
- [Veo-3 Prompt Guide](https://cloud.google.com/vertex-ai/generative-ai/docs/video/video-gen-prompt-guide) - Google video model

### Automation
- [Zapier Learn](https://learn.zapier.com/build-your-first-zap) - Build your first zap
- [Lindy Academy](https://www.lindy.ai/academy-lessons/getting-started-101) - AI automation

### Deep Learning (Expert)
- [Machine Learning - Andrew Ng](https://www.coursera.org/specializations/machine-learning-introduction) - Coursera
- [Deep Dive into LLMs - Karpathy](https://www.youtube.com/watch?v=zjkBMFhNj_g) - By ChatGPT co-creator

---

## 📥 Inbox (Learner Agent Landing Zone)

**Drop new links here.** Run `/learner` to evaluate and integrate them.

```
Paste links below this line (one per line, with optional notes):
───────────────────────────────────────────────────────────────
Semantic Layer docs (pending evaluation):
https://docs.getdbt.com/docs/use-dbt-semantic-layer/consume-metrics
https://docs.getdbt.com/docs/use-dbt-semantic-layer/setup-sl
https://docs.getdbt.com/docs/use-dbt-semantic-layer/sl-architecture
https://docs.getdbt.com/docs/use-dbt-semantic-layer/deploy-sl
https://docs.getdbt.com/docs/use-dbt-semantic-layer/exports
───────────────────────────────────────────────────────────────
```

**Recently Evaluated (2025-12-12):**
- ✅ mdflow → **ADOPT** (Priority 3) - See "Prompt Execution & Session Memory" section
- 📋 claude-mem → **EVALUATE** (Priority 4) - See "Prompt Execution & Session Memory" section
- ⏸️ snipt → **DEFERRED** - Lower ROI than other tools

**Format options:**
- Just URL: `https://example.com/article`
- URL + note: `https://example.com/article - great patterns for incremental models`
- URL + type hint: `https://example.com/tool [TOOL] - dbt package for X`

---

## To Be Categorized

*Overflow area - resources that don't fit existing sections*

---

## Career Content Analysis `#career`

*Reddit data subreddit analysis for editorial decisions*

### Portfolio & Career Advice
- [The Data Portfolio That Actually Works](https://open.substack.com/pub/thedatahustle/p/the-data-portfolio-that-actually) (The Data Hustle) - How to build an effective portfolio

### Target Subreddits
- r/datascience
- r/dataengineering
- r/BusinessIntelligence

### Key Findings (from past analysis)
- Career advice dominates (~40% of posts)
- Largest segments: career changers, mid-career feeling stalled
- Technical help/tools: ~24%
- Potential for animated bar chart race showing topic trends over time

### Tools Used
- **PRAW** - Python Reddit API Wrapper
- **Anthropic API** - For content classification into categories

---

## Related Documents
- `DESIGN_PRINCIPLES.md` - Philosophy, rules, checklists
- `README.md` - Project overview
- `__The_Pudding__Techniques__Tools___Best_Practices` - Detailed Pudding analysis

---

## Processed

### 2025-12-13 Batch (27 resources added)

**Data Visualization (6):**
- `visual-vocabulary-tableau` - Andy Kriebel chart selection guide
- `bar-design-guide` - John Johansson bar chart best practices
- `10-commandments-big-numbers` - Felipe Sebben KPI card design
- `tableau-chart-catalog` - Kevin Flerlage chart examples
- `10-ui-design-principles` - Kieran Klaassen UI principles
- `avoiding-ai-slop-design` - Meng To Swiss/Japanese minimalism

**Data Storytelling (5):**
- `pudding-dope-shit-1` through `pudding-dope-shit-3` - Process guides
- `pudding-scrollytelling-implementation` - Technical scrollytelling
- `pudding-responsive-scrollytelling` - Responsive design

**Context Engineering (4):**
- `context-engineering-agents-langchain` - LangChain framework
- `context-engineering-weaviate` - Weaviate framework (87.5% failure stat)
- `how-prompt-caching-works` - Sankalp Agarwal technical dive
- `filesystems-context-engineering` - LangChain filesystem patterns

**Agent Memory (3):**
- `momo-context-engineering-research` - 5-layer memory stack
- `spark-shared-memory-agents` - Cross-agent learning paper
- `memory-in-ai-agents` - Leonie Monigatti taxonomy

**Knowledge Quality (2):**
- `semiosis-kb-unit-testing` - KB testing framework
- `holy-trinity-enterprise-data` - Meta Grid pattern

**AI Tools (6):**
- `ade-bench-dbt` - dbt Labs agent benchmark
- `llm-council-karpathy` - Multi-LLM comparison
- `advanced-tool-use-anthropic` - Tool search, programmatic calling
- `mdflow-executable-markdown` - Executable prompts
- `claude-mem-persistent-memory` - Session persistence
- `consistent-hero-images-workflow` - Jenny Ouyang image workflow

**Data Engineering (5):**
- `modeling-success-dbt` - dbt modeling guide
- `dbt-mcp-conversational-analytics` - Norlys case study
- `understanding-data-marts` - Jimmy Pang mart architecture
- `dbt-incremental-ci` - CI with prod data
- `upstream-prod` - Dev with prod data (-97% cycle time)

**Career Development (1):**
- `data-portfolio-that-works` - Portfolio building guide

**Reference (1):**
- `tableau-reference-guide-shaffer` - Jeffrey Shaffer Tableau guide

---

### Skipped (no source URL or deferred):
- Physical Material Inspiration (conceptual, no URLs)
- Game UI Inspiration (game references, not articles)
- Most tool documentation (D3, SvelteKit, etc. - reference docs)
- Browser.cash (marked incomplete)
- snipt (marked deferred)
- OpenAI/Gemini learning resources (official docs, not unique content)

