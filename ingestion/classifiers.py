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

    # Display
    reading_time: str
    word_count: int


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
    """Full ingestion pipeline combining all modules."""

    def __init__(self, existing_authors: Optional[set[str]] = None):
        self.classifier = ResourceClassifier()
        self.definition_gen = DefinitionGenerator()
        self.author_extractor = AuthorExtractor()
        self.id_generator = IdGenerator()
        self.existing_authors = existing_authors or set()

    def process(self, extracted) -> ClassifiedResource:
        """
        Process extracted content through the full pipeline.

        Args:
            extracted: ExtractedContent from extractor.py

        Returns:
            ClassifiedResource ready for YAML generation
        """
        from .extractor import estimate_reading_time

        # Step 1: Classify
        classification = self.classifier(
            title=extracted.title or "Untitled",
            content=extracted.text,
            url=extracted.url,
        )

        # Step 2: Generate definition
        definition = self.definition_gen(
            title=extracted.title or "Untitled",
            content=extracted.text,
            domain=classification["domain"],
            category=classification["category"],
        )

        # Step 3: Extract author
        author = self.author_extractor(
            content=extracted.text,
            url=extracted.url,
            detected_author=extracted.author_name,
            platform=extracted.source_platform,
        )

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

        return ClassifiedResource(
            id=resource_id,
            url=extracted.url,
            title=extracted.title or "Untitled",
            definition=definition["definition"],
            alternate_labels=definition["alternate_labels"],
            author_id=author["author_id"],
            author_name=author["author_name"],
            is_new_author=author["author_id"] not in self.existing_authors,
            source=extracted.source_platform,
            content_type=content_type,
            published_date=extracted.published_date,
            domain=classification["domain"],
            category=classification["category"],
            granularity=classification["granularity"],
            color=classification["color"],
            confidence=classification["confidence"],
            reasoning=classification["reasoning"],
            needs_review=classification["confidence"] < 0.7,
            reading_time=estimate_reading_time(extracted.word_count, extracted.has_video),
            word_count=extracted.word_count,
        )
