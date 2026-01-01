"""
Tweet triage classifier for routing bookmarked tweets.

Classifies tweets into intents:
- learn: Articles, essays, videos worth adding to KB
- try: Tools, repos, libraries to experiment with
- review: Threads, opinions needing human review
- quote: Wisdom, insights to extract and save
- skip: Not relevant to knowledge base
"""

import dspy
import re
from dataclasses import dataclass
from typing import Optional


# =============================================================================
# DSPy SIGNATURES
# =============================================================================

class TriageTweet(dspy.Signature):
    """Classify a bookmarked tweet to determine how to process it.

    Consider:
    - Does it contain links to articles/resources worth learning from?
    - Does it reference tools/repos/libraries to try?
    - Is it a thread or opinion needing deeper review?
    - Does it contain a standalone insight/quote worth saving?
    - Is it relevant to: knowledge engineering, AI/LLMs, data, analytics, visualization?
    """

    tweet_text: str = dspy.InputField(desc="Full text of the tweet")
    author_name: str = dspy.InputField(desc="Tweet author's display name")
    author_bio: str = dspy.InputField(desc="Tweet author's bio, if available")
    urls_in_tweet: str = dspy.InputField(desc="Comma-separated URLs found in tweet")
    has_media: bool = dspy.InputField(desc="Whether tweet contains images/video")
    is_thread: bool = dspy.InputField(desc="Whether this is part of a thread")

    intent: str = dspy.OutputField(
        desc="One of: learn, try, review, quote, skip"
    )
    content_type: str = dspy.OutputField(
        desc="One of: article, video, podcast, repo, thread, tool, insight, other"
    )
    primary_url: str = dspy.OutputField(
        desc="Most relevant URL to process, or 'none' if no URL needed"
    )
    confidence: float = dspy.OutputField(
        desc="Confidence in classification from 0.0 to 1.0"
    )
    reasoning: str = dspy.OutputField(
        desc="Brief explanation of why this classification"
    )


class ExtractQuote(dspy.Signature):
    """Extract a memorable quote or insight from a tweet.

    Good quotes are:
    - Self-contained (make sense without context)
    - Insightful (teach something non-obvious)
    - Quotable (worth remembering/sharing)
    """

    tweet_text: str = dspy.InputField()
    author_name: str = dspy.InputField()

    quote: str = dspy.OutputField(desc="The extracted quote, cleaned up if needed")
    topic: str = dspy.OutputField(desc="What topic/theme this quote relates to")
    is_quotable: bool = dspy.OutputField(desc="True if this is actually worth saving")


# =============================================================================
# DATA CLASSES
# =============================================================================

@dataclass
class TriageResult:
    """Result of triaging a bookmarked tweet."""

    # Original tweet data
    tweet_id: str
    tweet_text: str
    author_name: str
    author_handle: str
    tweet_url: str

    # Classification
    intent: str  # learn, try, review, quote, skip
    content_type: str  # article, video, podcast, repo, thread, tool, insight, other
    primary_url: Optional[str]
    confidence: float
    reasoning: str

    # Extracted data (for quotes)
    extracted_quote: Optional[str] = None
    quote_topic: Optional[str] = None

    def should_process(self) -> bool:
        """Whether this tweet should be processed further."""
        return self.intent != "skip" and self.confidence >= 0.5


# =============================================================================
# URL EXTRACTION
# =============================================================================

def extract_urls(text: str) -> list[str]:
    """Extract URLs from tweet text."""
    # Match http(s) URLs
    url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
    urls = re.findall(url_pattern, text)

    # Clean up trailing punctuation
    cleaned = []
    for url in urls:
        # Remove trailing punctuation that's likely not part of URL
        url = url.rstrip('.,;:!?)')
        if url:
            cleaned.append(url)

    return cleaned


def is_github_url(url: str) -> bool:
    """Check if URL is a GitHub repository."""
    return "github.com" in url and "/blob/" not in url and "/issues/" not in url


def is_video_url(url: str) -> bool:
    """Check if URL is a video platform."""
    video_domains = ["youtube.com", "youtu.be", "vimeo.com", "loom.com"]
    return any(domain in url for domain in video_domains)


def is_podcast_url(url: str) -> bool:
    """Check if URL is a podcast platform."""
    podcast_domains = ["podcasts.apple.com", "spotify.com", "overcast.fm", "pocketcasts.com"]
    return any(domain in url for domain in podcast_domains)


# =============================================================================
# TRIAGE CLASSIFIER
# =============================================================================

class TweetTriageClassifier(dspy.Module):
    """Classifies bookmarked tweets for routing."""

    def __init__(self):
        super().__init__()
        self.triage = dspy.ChainOfThought(TriageTweet)
        self.extract_quote = dspy.Predict(ExtractQuote)

    def forward(
        self,
        tweet_id: str,
        tweet_text: str,
        author_name: str,
        author_handle: str,
        author_bio: str = "",
        has_media: bool = False,
        is_thread: bool = False,
    ) -> TriageResult:
        """
        Classify a tweet and determine routing.

        Args:
            tweet_id: Twitter/X tweet ID
            tweet_text: Full tweet text
            author_name: Display name of tweet author
            author_handle: @handle of tweet author
            author_bio: Author's profile bio
            has_media: Whether tweet has images/video
            is_thread: Whether this is part of a thread

        Returns:
            TriageResult with classification and routing info
        """
        # Extract URLs from tweet
        urls = extract_urls(tweet_text)
        urls_str = ", ".join(urls) if urls else "none"

        # Run triage classification
        result = self.triage(
            tweet_text=tweet_text,
            author_name=author_name,
            author_bio=author_bio or "No bio available",
            urls_in_tweet=urls_str,
            has_media=has_media,
            is_thread=is_thread,
        )

        # Validate intent
        valid_intents = ["learn", "try", "review", "quote", "skip"]
        intent = result.intent.lower() if result.intent.lower() in valid_intents else "review"

        # Validate content type
        valid_types = ["article", "video", "podcast", "repo", "thread", "tool", "insight", "other"]
        content_type = result.content_type.lower() if result.content_type.lower() in valid_types else "other"

        # Override based on URL heuristics
        if urls:
            primary = urls[0]
            if is_github_url(primary) and intent == "learn":
                intent = "try"
                content_type = "repo"
            elif is_video_url(primary):
                content_type = "video"
            elif is_podcast_url(primary):
                content_type = "podcast"

        # Parse confidence
        try:
            confidence = float(result.confidence)
            confidence = max(0.0, min(1.0, confidence))
        except:
            confidence = 0.5

        # Get primary URL
        primary_url = None
        if result.primary_url and result.primary_url.lower() != "none":
            primary_url = result.primary_url
        elif urls:
            primary_url = urls[0]

        # Build tweet URL
        tweet_url = f"https://x.com/{author_handle}/status/{tweet_id}"

        # Extract quote if intent is quote
        extracted_quote = None
        quote_topic = None
        if intent == "quote":
            quote_result = self.extract_quote(
                tweet_text=tweet_text,
                author_name=author_name,
            )
            if quote_result.is_quotable:
                extracted_quote = quote_result.quote
                quote_topic = quote_result.topic
            else:
                # Not actually quotable, change to skip
                intent = "skip"
                confidence = 0.3

        return TriageResult(
            tweet_id=tweet_id,
            tweet_text=tweet_text,
            author_name=author_name,
            author_handle=author_handle,
            tweet_url=tweet_url,
            intent=intent,
            content_type=content_type,
            primary_url=primary_url,
            confidence=confidence,
            reasoning=result.reasoning,
            extracted_quote=extracted_quote,
            quote_topic=quote_topic,
        )


# =============================================================================
# SIMPLE HEURISTIC CLASSIFIER (no LLM)
# =============================================================================

class SimpleTriageClassifier:
    """
    Rule-based triage classifier that doesn't require an LLM.

    Use this for fast, cost-free classification when:
    - Tweet contains obvious signals (GitHub URL, video link)
    - You want to pre-filter before LLM classification
    """

    def classify(
        self,
        tweet_id: str,
        tweet_text: str,
        author_name: str,
        author_handle: str,
        has_media: bool = False,
        is_thread: bool = False,
    ) -> TriageResult:
        """Classify using simple heuristics."""

        urls = extract_urls(tweet_text)
        tweet_url = f"https://x.com/{author_handle}/status/{tweet_id}"

        # Default values
        intent = "review"
        content_type = "other"
        primary_url = urls[0] if urls else None
        confidence = 0.6
        reasoning = "Classified by heuristics"

        # Check for GitHub repos
        github_urls = [u for u in urls if is_github_url(u)]
        if github_urls:
            intent = "try"
            content_type = "repo"
            primary_url = github_urls[0]
            confidence = 0.9
            reasoning = "Contains GitHub repository link"

        # Check for videos
        elif any(is_video_url(u) for u in urls):
            intent = "learn"
            content_type = "video"
            primary_url = next(u for u in urls if is_video_url(u))
            confidence = 0.8
            reasoning = "Contains video link"

        # Check for podcasts
        elif any(is_podcast_url(u) for u in urls):
            intent = "learn"
            content_type = "podcast"
            primary_url = next(u for u in urls if is_podcast_url(u))
            confidence = 0.8
            reasoning = "Contains podcast link"

        # Check for articles (non-social URLs)
        elif urls:
            social_domains = ["twitter.com", "x.com", "facebook.com", "linkedin.com"]
            article_urls = [u for u in urls if not any(d in u for d in social_domains)]
            if article_urls:
                intent = "learn"
                content_type = "article"
                primary_url = article_urls[0]
                confidence = 0.7
                reasoning = "Contains article link"

        # Check for threads
        elif is_thread:
            intent = "review"
            content_type = "thread"
            confidence = 0.7
            reasoning = "Thread requires human review"

        # Short tweets might be quotes
        elif len(tweet_text) < 280 and not urls:
            intent = "quote"
            content_type = "insight"
            confidence = 0.5
            reasoning = "Short tweet without links - potential quote"

        return TriageResult(
            tweet_id=tweet_id,
            tweet_text=tweet_text,
            author_name=author_name,
            author_handle=author_handle,
            tweet_url=tweet_url,
            intent=intent,
            content_type=content_type,
            primary_url=primary_url,
            confidence=confidence,
            reasoning=reasoning,
        )
