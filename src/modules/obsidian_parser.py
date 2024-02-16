"""Obsidian Parser

"""
import re

from . import misc


def parse_anchors(raw_text: str) -> str:
    """Update all obsidian links
    [thing](heres-a-link/to-a site.md) -> <a href="./heres-a-link/to-a-side.html>Thing</a>"
    """
    pattern = r"\[([^\]]+)\]\(([^\)]+)\)"
    cleaned_text = raw_text
    matches = re.findall(pattern, raw_text)
    if not matches:
        return cleaned_text
    for match in matches:
        bracket_content = match[0]
        parenthesis_content = match[1]
        # print(f"Text within brackets: {bracket_content}")
        # print(f"Content within parenthesis: {parenthesis_content}")
        if parenthesis_content[:7] == "http://" or parenthesis_content[:8] == "https://":
            # @todo: Exernal links in a new window
            continue
        replace_str = "[%s](%s)" % (bracket_content, parenthesis_content)
        with_str = '<a href="./%s">%s</a>' % (
            misc.filter_md_ext(parenthesis_content, ".html"),
            bracket_content)
        # print("Replace: %s" % replace_str)
        # print("with: %s" % with_str)
        cleaned_text = cleaned_text.replace(replace_str, with_str)
    return cleaned_text

def parse_backticks(raw_text: str) -> str:
    """Get all `backticked` items and replace with <pre> tags.
    @todo: This is broken and is replacing code blocks as well.
    """
    regex = r"`([^`]+)`"
    matches = re.findall(regex, raw_text)
    cleaned_text = raw_text
    if not matches:
        return cleaned_text
    # print ("Match was found at {start}-{end}: {match}".format(start = matches.start(), end = matches.end(), match = matches.group()))

    for match in matches:
        tick_content = match
        replace_str = "`%s`" % (tick_content)
        with_str = '<pre class="obsidian-backtick">%s</pre>' % (tick_content)
        cleaned_text = cleaned_text.replace(replace_str, with_str)
        
    return cleaned_text

# End File: MdtoHtml/src/modules/obsidian_parser.py