import unittest
from pathlib import Path
from unittest.mock import Mock, patch

TESTS_DIR = Path(__file__).parent.parent
HELLO_PATCH = (TESTS_DIR / "hello.patch").read_text()


class TestReviewer(unittest.TestCase):
    @patch("pythonbridge.core.reviewer.load_environment")
    @patch("pythonbridge.core.reviewer.get_diff")
    @patch("pythonbridge.core.reviewer.GroqLLM")
    @patch("pythonbridge.core.reviewer.post_review")
    def test_review_pr_reviews_files(
        self, mock_post_review, mock_llm_class, mock_get_diff, mock_load_env
    ):
        # https://docs.github.com/en/rest/pulls/pulls#list-pull-requests-files
        mock_file = Mock()
        mock_file.filename = "pythonbridge/tests/hello.py"
        mock_file.status = "added"
        mock_file.patch = HELLO_PATCH

        mock_get_diff.return_value = [mock_file]

        mock_llm = Mock()
        mock_llm.review_code.return_value = "Looks good, no issues found."
        mock_llm_class.return_value = mock_llm

        from pythonbridge.core.reviewer import review_pr

        payload = {
            "number": 1,
            "repository": {"full_name": "owner/repo"},
            "installation": {"id": "12345"},
        }

        reviews = review_pr(payload)

        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["filename"], "pythonbridge/tests/hello.py")
        self.assertEqual(reviews[0]["status"], "added")
        self.assertEqual(reviews[0]["review"], "Looks good, no issues found.")

        mock_load_env.assert_called_once()
        mock_get_diff.assert_called_once_with(payload)
        mock_llm.review_code.assert_called_once_with(mock_file.patch)

    @patch("pythonbridge.core.reviewer.load_environment")
    @patch("pythonbridge.core.reviewer.get_diff")
    @patch("pythonbridge.core.reviewer.GroqLLM")
    @patch("pythonbridge.core.reviewer.post_review")
    def test_review_pr_skips_files_without_patch(
        self, mock_post_review, mock_llm_class, mock_get_diff, mock_load_env
    ):
        # Deleted files have no patch (no diff to review)
        mock_file = Mock()
        mock_file.filename = "deleted.py"
        mock_file.status = "removed"
        mock_file.patch = None

        mock_get_diff.return_value = [mock_file]

        mock_llm = Mock()
        mock_llm_class.return_value = mock_llm

        from pythonbridge.core.reviewer import review_pr

        payload = {
            "number": 1,
            "repository": {"full_name": "owner/repo"},
            "installation": {"id": "12345"},
        }

        reviews = review_pr(payload)

        self.assertEqual(len(reviews), 1)
        self.assertEqual(reviews[0]["filename"], "deleted.py")
        self.assertIsNone(reviews[0]["review"])
        # LLM should NOT be called
        mock_llm.review_code.assert_not_called()


if __name__ == "__main__":
    unittest.main()
