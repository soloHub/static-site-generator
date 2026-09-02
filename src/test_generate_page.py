import unittest
from generate_page import extract_title

class TestGeneratePage(unittest.TestCase):
    def test_extract_title(self):
        md = """
# Heading 1

## Heading 2

#### Heading 3
"""
        title = extract_title(md)
        self.assertEqual(title, 'Heading 1')

    def test_extract_title_multiple(self):
        md = """
# Heading 3

# Heading 2

# Heading 1
"""
        title = extract_title(md)
        self.assertEqual(title, 'Heading 3')


if __name__ == "__main__":
    unittest.main()        