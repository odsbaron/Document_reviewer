import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doc_review_agent.document_loader import load_document


class DocumentLoaderTests(unittest.TestCase):
    def test_loads_markdown_as_text_document(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.md"
            path.write_text("# Title\n\nBody text", encoding="utf-8")

            document = load_document(path)

        self.assertEqual(document.path.name, "sample.md")
        self.assertIn("Title", document.text)
        self.assertEqual(document.kind, "markdown")

    def test_rejects_unsupported_extension(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "sample.xls"
            path.write_text("data", encoding="utf-8")

            with self.assertRaises(ValueError) as ctx:
                load_document(path)

        self.assertIn(".xls", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
