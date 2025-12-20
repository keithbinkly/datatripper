"""
YAML generation for resources.yaml and authors.yaml

Generates properly formatted YAML entries matching the existing schema.
"""

from datetime import date
from typing import Optional
from .classifiers import ClassifiedResource


def generate_resource_yaml(resource: ClassifiedResource) -> str:
    """
    Generate a YAML entry for resources.yaml.

    Args:
        resource: ClassifiedResource from the pipeline

    Returns:
        Formatted YAML string ready to append to resources.yaml
    """
    # Format alternate labels
    alt_labels_yaml = "\n".join(f"      - {label}" for label in resource.alternate_labels)

    # Format published date
    pub_date = resource.published_date if resource.published_date else "~"

    # Escape title if it contains special chars
    title = resource.title
    if ":" in title or '"' in title:
        title = f'"{title}"'

    yaml = f"""
  - id: {resource.id}
    url: {resource.url}
    preferredLabel: {title}
    alternateLabels:
{alt_labels_yaml}
    definition: >
      {resource.definition}

    # Provenance
    author: {resource.author_id}
    source: {resource.source}
    contentType: {resource.content_type}
    publishedDate: {pub_date}
    dateAdded: {date.today().isoformat()}

    # Classification
    domain: {resource.domain}
    category: {resource.category}
    granularity: {resource.granularity}

    # Relationships
    relationships: []

    # Quality
    validationStatus: unvalidated

    # Display
    readingTime: {resource.reading_time}
    color: "{resource.color}"
"""
    return yaml.strip()


def generate_author_yaml(
    author_id: str,
    author_name: str,
    affiliation: Optional[str] = None,
    is_organization: bool = False,
    source_url: Optional[str] = None,
) -> str:
    """
    Generate a YAML entry for authors.yaml.

    Args:
        author_id: The author ID (e.g., 'c-doctorow')
        author_name: Full author name
        affiliation: Company/org if known
        is_organization: Whether this is an org, not individual
        source_url: URL where author info was found

    Returns:
        Formatted YAML string ready to append to authors.yaml
    """
    perspective = "organization" if is_organization else "practitioner"
    affiliation_line = affiliation if affiliation else "~"

    yaml = f"""
  - id: {author_id}
    name: {author_name}
    # Demographics
    birthYear: ~
    generation: ~
    gender: ~
    location:
      city: ~
      country: ~
      continent: ~
    # Professional
    jobTitle: ~
    industry: ~
    affiliation: {affiliation_line}
    perspectiveType: {perspective}
    yearsInField: ~
    # Background
    education: ~
    nativeLanguage: ~
    # Meta
    socialFollowing: ~
    bio: >
      [To be researched]
    bioSource: {source_url if source_url else '~'}
"""
    return yaml.strip()


def generate_review_entry(resource: ClassifiedResource) -> str:
    """
    Generate a review queue entry for human validation.

    Args:
        resource: ClassifiedResource that needs review

    Returns:
        Formatted YAML for queue/pending.yaml
    """
    yaml = f"""
  - id: {resource.id}
    url: {resource.url}
    title: {resource.title}

    # Classification (confidence: {resource.confidence:.0%})
    domain: {resource.domain}
    category: {resource.category}
    reasoning: >
      {resource.reasoning}

    # Suggested definition
    definition: >
      {resource.definition}

    # Review actions
    status: pending
    flagged_issues:
      - low_confidence_classification
{f"      - new_author: {resource.author_id}" if resource.is_new_author else ""}
    added: {date.today().isoformat()}
"""
    return yaml.strip()


def format_for_display(resource: ClassifiedResource) -> str:
    """
    Format a classified resource for terminal display.

    Args:
        resource: ClassifiedResource to display

    Returns:
        Formatted string for CLI output
    """
    confidence_bar = "█" * int(resource.confidence * 10) + "░" * (10 - int(resource.confidence * 10))
    def_score_bar = "█" * int(resource.definition_score * 10) + "░" * (10 - int(resource.definition_score * 10))
    review_flag = " ⚠️  NEEDS REVIEW" if resource.needs_review else " ✓"

    # Format definition feedback if available
    feedback_line = ""
    if resource.definition_feedback:
        feedback_line = f"\n│ Feedback:    {resource.definition_feedback[:60]}..."

    return f"""
┌─────────────────────────────────────────────────────────────────────────────
│ {resource.title[:70]}
├─────────────────────────────────────────────────────────────────────────────
│ ID:          {resource.id}
│ URL:         {resource.url[:60]}...
│
│ Domain:      {resource.domain} → {resource.category}
│ Type:        {resource.content_type} ({resource.granularity})
│ Confidence:  [{confidence_bar}] {resource.confidence:.0%}{review_flag}
│
│ Definition:
│   {resource.definition[:200]}...
│
│ Def Score:   [{def_score_bar}] {resource.definition_score:.0%}{feedback_line}
│
│ Alt Labels:  {', '.join(resource.alternate_labels)}
│
│ Author:      {resource.author_name} ({resource.author_id})
│              {"[NEW AUTHOR]" if resource.is_new_author else "[EXISTING]"}
│ Source:      {resource.source}
│ Reading:     {resource.reading_time} ({resource.word_count} words)
└─────────────────────────────────────────────────────────────────────────────
"""
