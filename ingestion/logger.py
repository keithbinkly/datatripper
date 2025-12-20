"""
Ingestion pipeline logging.

Persists DSPy reasoning and pipeline decisions for debugging and analysis.
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Optional


class IngestionLogger:
    """Logs ingestion pipeline decisions and reasoning."""

    def __init__(self, log_dir: Optional[Path] = None):
        self.log_dir = log_dir or Path(__file__).parent.parent / "logs" / "ingestion"
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.current_run: dict[str, Any] = {}
        self.run_id: Optional[str] = None

    def start_run(self, url: str) -> str:
        """Start a new ingestion run."""
        self.run_id = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        self.current_run = {
            "run_id": self.run_id,
            "url": url,
            "started_at": datetime.utcnow().isoformat(),
            "steps": [],
        }
        return self.run_id

    def log_step(
        self,
        step_name: str,
        inputs: dict[str, Any],
        outputs: dict[str, Any],
        reasoning: Optional[str] = None,
    ):
        """Log a pipeline step."""
        step = {
            "step": step_name,
            "timestamp": datetime.utcnow().isoformat(),
            "inputs": self._serialize(inputs),
            "outputs": self._serialize(outputs),
        }
        if reasoning:
            step["reasoning"] = reasoning
        self.current_run["steps"].append(step)

    def log_extraction(self, extracted: Any):
        """Log extraction results."""
        self.log_step(
            "extraction",
            inputs={"url": extracted.url},
            outputs={
                "title": extracted.title,
                "word_count": extracted.word_count,
                "platform": extracted.source_platform,
                "has_code": extracted.has_code,
                "has_video": extracted.has_video,
            },
        )

    def log_classification(self, classification: dict):
        """Log classification results with reasoning."""
        self.log_step(
            "classification",
            inputs={},
            outputs={
                "domain": classification["domain"],
                "category": classification["category"],
                "content_type": classification["content_type"],
                "granularity": classification["granularity"],
                "confidence": classification["confidence"],
            },
            reasoning=classification.get("reasoning"),
        )

    def log_definition(self, definition: dict, score_result: Optional[dict] = None):
        """Log definition generation and scoring."""
        outputs = {
            "definition": definition["definition"],
            "alternate_labels": definition["alternate_labels"],
        }
        if score_result:
            outputs["score"] = score_result["score"]
            outputs["criteria"] = score_result.get("criteria", {})
            outputs["feedback"] = score_result.get("feedback")
        self.log_step("definition", inputs={}, outputs=outputs)

    def log_author(self, author: dict):
        """Log author extraction."""
        self.log_step(
            "author",
            inputs={},
            outputs={
                "author_id": author["author_id"],
                "author_name": author["author_name"],
                "is_organization": author.get("is_organization", False),
            },
        )

    def finish_run(self, success: bool, resource_id: Optional[str] = None, error: Optional[str] = None):
        """Finish the run and write to log file."""
        self.current_run["finished_at"] = datetime.utcnow().isoformat()
        self.current_run["success"] = success
        if resource_id:
            self.current_run["resource_id"] = resource_id
        if error:
            self.current_run["error"] = error

        # Write to log file
        log_file = self.log_dir / f"{self.run_id}.json"
        with open(log_file, "w") as f:
            json.dump(self.current_run, f, indent=2)

        return log_file

    def _serialize(self, obj: Any) -> Any:
        """Serialize objects for JSON."""
        if isinstance(obj, dict):
            return {k: self._serialize(v) for k, v in obj.items()}
        if isinstance(obj, list):
            return [self._serialize(v) for v in obj]
        if hasattr(obj, "__dict__"):
            return {k: self._serialize(v) for k, v in obj.__dict__.items() if not k.startswith("_")}
        try:
            json.dumps(obj)
            return obj
        except (TypeError, ValueError):
            return str(obj)


# Global logger instance
_logger: Optional[IngestionLogger] = None


def get_logger() -> IngestionLogger:
    """Get or create the global logger instance."""
    global _logger
    if _logger is None:
        _logger = IngestionLogger()
    return _logger
