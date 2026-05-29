import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doc_review_agent.models import Finding, ReviewResult
from doc_review_agent.report import render_markdown_report


class ReportTests(unittest.TestCase):
    def test_renders_findings_with_required_fields(self):
        result = ReviewResult(
            document_path="sample.md",
            summary="Found 1 issue.",
            findings=[
                Finding(
                    agent="logic",
                    location="Section 1",
                    excerpt="A therefore B.",
                    issue_type="unsupported conclusion",
                    severity="high",
                    reason="The premise does not establish the conclusion.",
                    recommendation="Add evidence for B or weaken the conclusion.",
                    needs_human_review=True,
                )
            ],
            raw_agent_outputs=[],
        )

        report = render_markdown_report(result)

        self.assertIn("# Document Review Report", report)
        self.assertIn("sample.md", report)
        self.assertIn("unsupported conclusion", report)
        self.assertIn("Needs human review: yes", report)


if __name__ == "__main__":
    unittest.main()
