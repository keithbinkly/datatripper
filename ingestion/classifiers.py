"""
DSPy classification and enrichment modules

Uses DSPy for structured LLM outputs with type safety.
"""

import dspy
from dataclasses import dataclass
from typing import Optional


# =============================================================================
# TAXONOMY (from resources.yaml)
# =============================================================================

DOMAINS = {
    "knowledge-engineering": {
        "name": "Knowledge Engineering",
        "description": "AI projects fail because corporate data lacks business context. Traditional pipelines decouple data from meaning—creating an AI Context Gap.",
        "color": "#06b6d4",
        "categories": [
            "Core Architecture",
            "Semantic Layer",
            "Knowledge Graphs",
            "Semantic Foundations",
            "Agentic Analytics",
            "Process Knowledge",
            "Context Engineering",
            "Knowledge Quality",
        ],
    },
    "ai-llms": {
        "name": "AI & LLMs",
        "description": "Foundational knowledge about how AI systems work—memory architectures, LLM behavior, evaluation methods, and prompt engineering principles.",
        "color": "#a855f7",
        "categories": [
            "LLM Foundations",
            "Agent Memory",
            "AI Evaluation",
            "Prompt Engineering",
        ],
    },
    "ai-tools": {
        "name": "AI Tools & Infrastructure",
        "description": "Practical tools, frameworks, and infrastructure for building AI applications and agent systems.",
        "color": "#10b981",
        "categories": [
            "Agent Infrastructure",
            "Development Tools",
        ],
    },
    "analytics-engineering": {
        "name": "Analytics Engineering",
        "description": "Best practices for data transformation, semantic modeling, and dbt development.",
        "color": "#f97316",
        "categories": [
            "dbt Practices",
            "Data Modeling",
            "Transformation Tools",
        ],
    },
    "data-visualization": {
        "name": "Data Visualization",
        "description": "Design patterns, exemplars, and best practices for effective data visualization and dashboard design.",
        "color": "#8b5cf6",
        "categories": [
            "Chart Design",
            "Dashboard Exemplars",
            "UI/UX Principles",
        ],
    },
    "data-storytelling": {
        "name": "Data Storytelling",
        "description": "Techniques for narrative data journalism, scrollytelling, and compelling data-driven stories.",
        "color": "#ec4899",
        "categories": [
            "Process Guides",
            "Scrollytelling",
            "Data Journalism",
        ],
    },
    "career-development": {
        "name": "Career Development",
        "description": "Resources for data career growth, portfolio building, and professional development.",
        "color": "#6366f1",
        "categories": [
            "Portfolio Building",
            "Career Strategy",
        ],
    },
}

CONTENT_TYPES = ["essay", "blog", "video", "podcast", "documentation", "paper"]
GRANULARITIES = ["foundational", "conceptual", "implementation", "advanced"]
RELATIONSHIP_TYPES = ["broader", "narrower", "related", "requires-prerequisite", "governed-by", "is-example-of"]


# =============================================================================
# DSPy SIGNATURES
# =============================================================================

class ClassifyResource(dspy.Signature):
    """Classify a resource into the data-centered.com knowledge base taxonomy.

    The knowledge base covers: knowledge engineering, AI/LLMs, AI tools,
    analytics engineering, data visualization, data storytelling, and career development.
    """

    title: str = dspy.InputField(desc="Resource title")
    content: str = dspy.InputField(desc="First ~4000 chars of resource content")
    url: str = dspy.InputField(desc="Source URL")
    taxonomy: str = dspy.InputField(desc="JSON of available domains and their categories")

    domain: str = dspy.OutputField(desc="Domain ID (e.g., 'knowledge-engineering', 'ai-llms')")
    category: str = dspy.OutputField(desc="Category within the domain (e.g., 'Core Architecture')")
    content_type: str = dspy.OutputField(desc="One of: essay, blog, video, podcast, documentation, paper")
    granularity: str = dspy.OutputField(desc="One of: foundational, conceptual, implementation, advanced")
    confidence: float = dspy.OutputField(desc="Classification confidence from 0.0 to 1.0")
    reasoning: str = dspy.OutputField(desc="Brief explanation of classification choice")


class GenerateDefinition(dspy.Signature):
    """Generate a precise definition with semantic boundaries.

    Good definitions explain:
    1. What the resource IS (core thesis/content)
    2. What it is NOT (scope boundaries)
    3. Why it matters (value proposition)
    """

    title: str = dspy.InputField()
    content: str = dspy.InputField(desc="Full extracted content")
    domain: str = dspy.InputField(desc="Classified domain")
    category: str = dspy.InputField(desc="Classified category")

    definition: str = dspy.OutputField(
        desc="2-3 sentence definition covering what it IS, scope boundaries, and why it matters"
    )
    alternate_labels: list[str] = dspy.OutputField(
        desc="3-5 search terms, synonyms, or acronyms for discoverability"
    )


class ExtractAuthor(dspy.Signature):
    """Extract author information from content and metadata."""

    content: str = dspy.InputField(desc="Page content")
    url: str = dspy.InputField()
    detected_author: str = dspy.InputField(desc="Author name if detected from byline, or empty")
    platform: str = dspy.InputField(desc="Source platform name")

    author_name: str = dspy.OutputField(desc="Full author name")
    author_id: str = dspy.OutputField(desc="Suggested ID in format: f-lastname (e.g., 'c-doctorow')")
    is_organization: bool = dspy.OutputField(desc="True if author is company/org, not individual")
    affiliation: str = dspy.OutputField(desc="Company, university, or organization if mentioned")


class GenerateResourceId(dspy.Signature):
    """Generate a stable, descriptive resource ID."""

    title: str = dspy.InputField()
    author_id: str = dspy.InputField()
    domain: str = dspy.InputField()

    resource_id: str = dspy.OutputField(
        desc="Kebab-case ID like 'ai-context-gap-sankar' or 'prompt-engineering-guide'. Max 50 chars, descriptive, unique."
    )


class ScoreDefinition(dspy.Signature):
    """Score a definition for quality.

    Good definitions:
    1. Explain what the resource IS (core thesis/content)
    2. Clarify scope boundaries (what it is NOT or doesn't cover)
    3. State why it matters (value proposition)
    4. Are concise (2-3 sentences, under 100 words)
    5. Use clear, accessible language
    """

    definition: str = dspy.InputField(desc="The definition to score")
    title: str = dspy.InputField(desc="Resource title for context")
    domain: str = dspy.InputField(desc="Domain for context")

    covers_what: bool = dspy.OutputField(desc="True if definition explains what the resource IS")
    covers_scope: bool = dspy.OutputField(desc="True if definition clarifies scope/boundaries")
    covers_why: bool = dspy.OutputField(desc="True if definition states why it matters")
    is_concise: bool = dspy.OutputField(desc="True if 2-3 sentences and under 100 words")
    is_clear: bool = dspy.OutputField(desc="True if uses clear, accessible language")
    score: float = dspy.OutputField(desc="Overall quality score from 0.0 to 1.0")
    feedback: str = dspy.OutputField(desc="Brief feedback on how to improve the definition")


# =============================================================================
# DSPy MODULES
# =============================================================================

class ResourceClassifier(dspy.Module):
    """Classifies resources into the taxonomy."""

    def __init__(self):
        super().__init__()
        self.classify = dspy.ChainOfThought(ClassifyResource)

    def forward(self, title: str, content: str, url: str) -> dict:
        import json

        # Build taxonomy string for context
        taxonomy = {
            domain_id: {
                "name": info["name"],
                "description": info["description"],
                "categories": info["categories"],
            }
            for domain_id, info in DOMAINS.items()
        }

        result = self.classify(
            title=title,
            content=content[:4000],
            url=url,
            taxonomy=json.dumps(taxonomy, indent=2),
        )

        # Validate outputs
        domain = result.domain if result.domain in DOMAINS else "knowledge-engineering"
        category = result.category
        if category not in DOMAINS[domain]["categories"]:
            category = DOMAINS[domain]["categories"][0]

        content_type = result.content_type if result.content_type in CONTENT_TYPES else "essay"
        granularity = result.granularity if result.granularity in GRANULARITIES else "conceptual"

        try:
            confidence = float(result.confidence)
            confidence = max(0.0, min(1.0, confidence))
        except:
            confidence = 0.5

        return {
            "domain": domain,
            "category": category,
            "content_type": content_type,
            "granularity": granularity,
            "confidence": confidence,
            "reasoning": result.reasoning,
            "color": DOMAINS[domain]["color"],
        }


class DefinitionGenerator(dspy.Module):
    """Generates definitions and alternate labels."""

    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(GenerateDefinition)

    def forward(self, title: str, content: str, domain: str, category: str) -> dict:
        result = self.generate(
            title=title,
            content=content[:6000],
            domain=domain,
            category=category,
        )

        # Ensure alternate_labels is a list
        alt_labels = result.alternate_labels
        if isinstance(alt_labels, str):
            alt_labels = [l.strip() for l in alt_labels.split(",")]

        return {
            "definition": result.definition,
            "alternate_labels": alt_labels[:5],
        }


class AuthorExtractor(dspy.Module):
    """Extracts and normalizes author information."""

    def __init__(self):
        super().__init__()
        self.extract = dspy.ChainOfThought(ExtractAuthor)

    def forward(self, content: str, url: str, detected_author: str, platform: str) -> dict:
        result = self.extract(
            content=content[:3000],
            url=url,
            detected_author=detected_author or "",
            platform=platform,
        )

        return {
            "author_name": result.author_name,
            "author_id": result.author_id.lower().replace(" ", "-"),
            "is_organization": result.is_organization,
            "affiliation": result.affiliation,
        }


class IdGenerator(dspy.Module):
    """Generates stable resource IDs."""

    def __init__(self):
        super().__init__()
        self.generate = dspy.ChainOfThought(GenerateResourceId)

    def forward(self, title: str, author_id: str, domain: str) -> str:
        result = self.generate(
            title=title,
            author_id=author_id,
            domain=domain,
        )

        # Sanitize ID
        resource_id = result.resource_id.lower()
        resource_id = "".join(c if c.isalnum() or c == "-" else "-" for c in resource_id)
        resource_id = "-".join(part for part in resource_id.split("-") if part)

        return resource_id[:50]


class DefinitionScorer(dspy.Module):
    """Scores definition quality."""

    def __init__(self):
        super().__init__()
        self.score = dspy.Predict(ScoreDefinition)

    def forward(self, definition: str, title: str, domain: str) -> dict:
        result = self.score(
            definition=definition,
            title=title,
            domain=domain,
        )

        # Calculate score from criteria
        criteria = [
            result.covers_what,
            result.covers_scope,
            result.covers_why,
            result.is_concise,
            result.is_clear,
        ]
        criteria_score = sum(1 for c in criteria if c) / len(criteria)

        try:
            llm_score = float(result.score)
            llm_score = max(0.0, min(1.0, llm_score))
        except:
            llm_score = criteria_score

        # Average of criteria and LLM score
        final_score = (criteria_score + llm_score) / 2

        return {
            "score": round(final_score, 2),
            "criteria": {
                "covers_what": result.covers_what,
                "covers_scope": result.covers_scope,
                "covers_why": result.covers_why,
                "is_concise": result.is_concise,
                "is_clear": result.is_clear,
            },
            "feedback": result.feedback,
        }


# =============================================================================
# PIPELINE
# =============================================================================

@dataclass
class ClassifiedResource:
    """Fully classified and enriched resource."""
    # Core
    id: str
    url: str
    title: str
    definition: str
    alternate_labels: list[str]

    # Provenance
    author_id: str
    author_name: str
    is_new_author: bool
    source: str
    content_type: str
    published_date: Optional[str]

    # Classification
    domain: str
    category: str
    granularity: str
    color: str

    # Quality
    confidence: float
    reasoning: str
    needs_review: bool
    definition_score: float
    definition_feedback: Optional[str]

    # Display
    reading_time: str
    word_count: int

    # GitHub enrichment (optional, for new authors)
    github_enrichment: Optional[dict] = None


def configure_dspy(provider: str = "anthropic", model: str = "claude-sonnet-4-20250514"):
    """Configure DSPy with the specified LLM provider."""
    if provider == "anthropic":
        lm = dspy.LM(f"anthropic/{model}", temperature=0.3)
    elif provider == "openai":
        lm = dspy.LM(f"openai/{model}", temperature=0.3)
    else:
        raise ValueError(f"Unknown provider: {provider}")

    dspy.configure(lm=lm)


class IngestionPipeline:
    """Full ingestion pipeline combining all modules.

    Uses lazy loading for DSPy modules to reduce startup time and memory
    usage when not all modules are needed.
    """

    def __init__(
        self,
        existing_authors: Optional[set[str]] = None,
        score_definitions: bool = True,
        enable_logging: bool = True,
        enrich_github: bool = True,
    ):
        # Lazy-loaded module cache
        self._classifier = None
        self._definition_gen = None
        self._definition_scorer = None
        self._author_extractor = None
        self._id_generator = None

        self.existing_authors = existing_authors or set()
        self.score_definitions = score_definitions
        self.enable_logging = enable_logging
        self.enrich_github = enrich_github
        self._logger = None
        self._logger_loaded = False

    @property
    def classifier(self) -> ResourceClassifier:
        if self._classifier is None:
            self._classifier = ResourceClassifier()
        return self._classifier

    @property
    def definition_gen(self) -> DefinitionGenerator:
        if self._definition_gen is None:
            self._definition_gen = DefinitionGenerator()
        return self._definition_gen

    @property
    def definition_scorer(self) -> Optional[DefinitionScorer]:
        if not self.score_definitions:
            return None
        if self._definition_scorer is None:
            self._definition_scorer = DefinitionScorer()
        return self._definition_scorer

    @property
    def author_extractor(self) -> AuthorExtractor:
        if self._author_extractor is None:
            self._author_extractor = AuthorExtractor()
        return self._author_extractor

    @property
    def id_generator(self) -> IdGenerator:
        if self._id_generator is None:
            self._id_generator = IdGenerator()
        return self._id_generator

    @property
    def logger(self):
        if not self._logger_loaded:
            self._logger_loaded = True
            if self.enable_logging:
                from .logger import get_logger
                self._logger = get_logger()
        return self._logger

    def process(self, extracted) -> ClassifiedResource:
        """
        Process extracted content through the full pipeline.

        Args:
            extracted: ExtractedContent from extractor.py

        Returns:
            ClassifiedResource ready for YAML generation
        """
        from .extractor import estimate_reading_time

        # Start logging
        if self.logger:
            self.logger.start_run(extracted.url)
            self.logger.log_extraction(extracted)

        # Step 1: Classify
        classification = self.classifier(
            title=extracted.title or "Untitled",
            content=extracted.text,
            url=extracted.url,
        )
        if self.logger:
            self.logger.log_classification(classification)

        # Step 2: Generate definition
        definition = self.definition_gen(
            title=extracted.title or "Untitled",
            content=extracted.text,
            domain=classification["domain"],
            category=classification["category"],
        )

        # Step 2b: Score definition quality (optional)
        definition_score = 1.0
        definition_feedback = None
        score_result = None
        if self.definition_scorer:
            score_result = self.definition_scorer(
                definition=definition["definition"],
                title=extracted.title or "Untitled",
                domain=classification["domain"],
            )
            definition_score = score_result["score"]
            definition_feedback = score_result["feedback"]

        if self.logger:
            self.logger.log_definition(definition, score_result)

        # Step 3: Extract author
        author = self.author_extractor(
            content=extracted.text,
            url=extracted.url,
            detected_author=extracted.author_name,
            platform=extracted.source_platform,
        )

        # Step 3b: GitHub enrichment for new authors (optional)
        github_enrichment = {}
        is_new_author = author["author_id"] not in self.existing_authors
        if self.enrich_github and is_new_author:
            try:
                from .github_enrichment import enrich_author
                github_enrichment = enrich_author(
                    author_name=author["author_name"],
                    author_id=author["author_id"],
                    source_url=extracted.url,
                )
            except Exception:
                pass  # GitHub enrichment is optional, don't fail pipeline

        if self.logger:
            self.logger.log_author(author)

        # Step 4: Generate ID
        resource_id = self.id_generator(
            title=extracted.title or "Untitled",
            author_id=author["author_id"],
            domain=classification["domain"],
        )

        # Determine content type from signals
        content_type = classification["content_type"]
        if extracted.has_video:
            content_type = "video"

        # Determine if review needed
        needs_review = classification["confidence"] < 0.7 or definition_score < 0.7

        # Finish logging
        if self.logger:
            self.logger.finish_run(success=True, resource_id=resource_id)

        return ClassifiedResource(
            id=resource_id,
            url=extracted.url,
            title=extracted.title or "Untitled",
            definition=definition["definition"],
            alternate_labels=definition["alternate_labels"],
            author_id=author["author_id"],
            author_name=author["author_name"],
            is_new_author=is_new_author,
            source=extracted.source_platform,
            content_type=content_type,
            published_date=extracted.published_date,
            domain=classification["domain"],
            category=classification["category"],
            granularity=classification["granularity"],
            color=classification["color"],
            confidence=classification["confidence"],
            reasoning=classification["reasoning"],
            needs_review=needs_review,
            definition_score=definition_score,
            definition_feedback=definition_feedback,
            reading_time=estimate_reading_time(extracted.word_count, extracted.has_video),
            word_count=extracted.word_count,
            github_enrichment=github_enrichment if github_enrichment else None,
        )
