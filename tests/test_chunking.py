import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from doc_review_agent.chunking import chunk_text


class ChunkingTests(unittest.TestCase):
    def test_short_text_returns_single_chunk(self):
        self.assertEqual(chunk_text("hello", max_chars=100), ["hello"])

    def test_chunks_long_text_without_exceeding_limit(self):
        text = "\n\n".join([f"paragraph {i} " + ("x" * 20) for i in range(20)])

        chunks = chunk_text(text, max_chars=120, overlap_chars=20)

        self.assertGreater(len(chunks), 1)
        self.assertTrue(all(len(chunk) <= 120 for chunk in chunks))
        self.assertIn("paragraph 0", chunks[0])
        self.assertIn("paragraph 19", chunks[-1])


if __name__ == "__main__":
    unittest.main()
