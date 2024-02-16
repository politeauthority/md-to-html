"""Misc

"""
import re

import arrow


def filter_md_ext(phile_name: str, replace_with: str=None) -> str:
    """
    """
    if phile_name[-3:] == ".md":
        if replace_with:
            phile_name = phile_name[:-3] + replace_with
        else:
            phile_name = phile_name[:-3]
    return phile_name


def handle_md_html_pre_tags(raw_text: str) -> str:
    """Attempts to find all back ticked items and wrap them in html <pre> tags.
    # @todo: This regex doesnt appear to be working properly.
    """
    # string = "This is a string with `backticks` around words and `multiple backticks` too."
    pattern = r"`([^`]+)`"
    # Find all occurrences using findall()
    matches = re.findall(pattern, raw_text)
    # Print the matched substrings
    # print("Matched substrings:", matches)
    for match in matches:
        start = raw_text.find("`%s`" % match)
        if start:
            left_over = raw_text[start + 1:]
            closing_tick = left_over.find("`") + start + 2
            # print(raw_text[start:closing_tick])
            replace = "`%s`" % match
            with_str = "<pre>%s</pre>" % match
            raw_text = raw_text.replace(replace, with_str)
        continue
    if len(matches) > 1:
        raw_text = handle_md_html_pre_tags(raw_text)
    return raw_text

def handle_obsidian_anchors(raw_text: str) -> str:
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
            filter_md_ext(parenthesis_content, ".html"),
            bracket_content)
        # print("Replace: %s" % replace_str)
        # print("with: %s" % with_str)
        cleaned_text = cleaned_text.replace(replace_str, with_str)
    return cleaned_text

    
def handle_backticks(raw_text: str) -> str:
    """Get all `backticked` items and replace with <pre> tags.
    """
    regex = r"`([^`]+)`"
    test_str = ("`catch this`\n"
	"```yamlsomething cool: not this```\n")
    matches = re.search(regex, raw_text)
    cleaned_text = raw_text
    if not matches:
        return cleaned_text
    # print ("Match was found at {start}-{end}: {match}".format(start = matches.start(), end = matches.end(), match = matches.group()))
    for groupNum in range(0, len(matches.groups())):
        groupNum = groupNum + 1
        match_text = matches.group(groupNum)
        cleaned_text = cleaned_text.replace(
            "`%s`" %  match_text,
            "<pre>%s</pre>" % match_text)
        
    return cleaned_text

def handle_obsidain_code_blocks(raw_text: str) -> str:
    """Get all `backticked` items and replace with <pre> tags.
    """
    regex = r"```([^`]+)```"
    test_str = ("`catch this`\n"
	"```yamlsomething cool: not this```\n")
    matches = re.search(regex, raw_text)
    cleaned_text = raw_text
    if not matches:
        return cleaned_text
    # print ("Match was found at {start}-{end}: {match}".format(start = matches.start(), end = matches.end(), match = matches.group()))
    for groupNum in range(0, len(matches.groups())):
        groupNum = groupNum + 1

        match_text = matches.group(groupNum)
        cleaned_text = cleaned_text.replace(
            "```%s```" %  match_text,
            '<code class="json hljs">%s</code>' % match_text)
        
    return cleaned_text

def handle_obsidian_check_boxes(raw_text: str) -> str:
    print("\nChecking for Check boxes\n")
    pattern = r"<li>\[x\]"
    # (<li>\[x\])( \D+$</li>)
    # matches = re.search(pattern, raw_text)
    cleaned_text = raw_text
    # if not matches:
    #     return cleaned_text
    check_html = '<label class="container">Create dev environment<input type="checkbox" checked="checked"><span class="checkmark"></span></label>'

    regex = r"<li>\[x\]"

    test_str = ("<li>[x] Here</li>\n"
        "<li>[ ] Empty</li>\n")

    matches = re.finditer(regex, test_str, re.MULTILINE)

    for matchNum, match in enumerate(matches, start=1):       
        print ("Match {matchNum} was found at {start}-{end}: {match}".format(matchNum = matchNum, start = match.start(), end = match.end(), match = match.group()))
        for groupNum in range(0, len(match.groups())):
            groupNum = groupNum + 1
            print ("Group {groupNum} found at {start}-{end}: {group}".format(groupNum = groupNum, start = match.start(groupNum), end = match.end(groupNum), group = match.group(groupNum)))
            import ipdb; ipdb.set_trace()
    return cleaned_text




def handle_obsidian_line_breaks(raw_text: str) -> str:
    """Convert new lines to break tags.
    \n -> <br/>
    """
    cleaned_text = raw_text.replace("\n", "<br/>")
    return cleaned_text

def get_date_updated() -> str:
    """
    @todo: Get the actual file modification time stamp if possible.
    """
    now =  arrow.utcnow()
    month_str = str(now.month)
    if now.month < 10:
        month_str = "0" + month_str
    day_str = str(now.day)
    if now.day < 10:
        day_str = "0" + day_str
    now_str = "%s-%s-%s" % (now.year, month_str, day_str)
    return now_str

def get_date_generated() -> str:
    """Create the date generated in a pretty format.
    """
    now =  arrow.utcnow()
    month_str = str(now.month)
    if now.month < 10:
        month_str = "0" + month_str
    day_str = str(now.day)
    if now.day < 10:
        day_str = "0" + day_str
    now_str = "%s-%s-%s" % (now.year, month_str, day_str)
    return now_str

def asset_path(relative_path: str) -> str:
    """Find the relative location of the assets directory for a given file.
    """
    num_slashes = relative_path.count("/")
    rel_path = ""
    count = 0
    while num_slashes > count:
        rel_path = rel_path + "../"
        count +=  1
    return rel_path + "assets"

def index_path(relative_path: str) -> str:
    """Find the relative location of the assets directory for a given file.
    """
    num_slashes = relative_path.count("/")
    rel_path = ""
    count = 0
    while num_slashes > count:
        rel_path = rel_path + "../"
        count +=  1
    return rel_path + ""


# End File: md-to-html/src/modules/export_markdown.py
