import unittest

from extract_title import extract_title


class TestExtractTitle(unittest.TestCase):
    def test_eq(self):
        title = extract_title("#      This is the Title      ")
        self.assertEqual(title, "This is the Title")

    def test_error(self):
        with self.assertRaises(Exception):
            extract_title("## Title that does't match the regex")

if __name__ == "__main__":
    unittest.main()