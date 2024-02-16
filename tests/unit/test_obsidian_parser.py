"""
    MdtoHtml Unit
    Api Util: Api Utils
    Source: MdtoHtml/src/modules/obsidian_parser.py

"""
import sys
 
# sys.path.insert(0, "/Users/alix/Programming/repos/md-to-html/src")
sys.path.append("/Users/alix/Programming/repos/md-to-html/src")
from modules import obsidian_parser

EXAMPLE_MD_1 = """
Relative Link: [Layout Validator](Layout%20Validator.md)
Obsidian link: [To Do](To%20Do.md)

"""

EXAMPLE_MD_2 = """
This is `special` text that needs `html` tags.
"""

class TestObsidianParser:

    def test__parse_achnors(self):
        """Test that we can parse out anchor tags, for both reltive links and external links.
        """
        result = obsidian_parser.parse_anchors(EXAMPLE_MD_1)
        expected = """\nRelative Link: <a href="./Layout%20Validator.html">Layout Validator</a>"""
        expected += """\nObsidian link: <a href="./To%20Do.html">To Do</a>\n\n"""
        assert result == expected
    
    def test__parse_backticks(self):
        """Checks that we replace single backticks.
        """
        result = obsidian_parser.parse_backticks(EXAMPLE_MD_2)
        expected = '\nThis is <pre class="obsidian-backtick">special</pre> text that needs '
        expected += '<pre class="obsidian-backtick">html</pre> tags.\n'
        assert result == expected
