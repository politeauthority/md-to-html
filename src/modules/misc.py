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

# def handle_obsidian_anchors(raw_text: str) -> str:
#     pattern = r"\[([^\]]+)\(([^)]+)\)\]"
#     text = "[thing](/heres-a-link/to-a site)"
#     match = re.search(pattern, raw_text)
#     if match:
#         bracket_content = match.group(1)
#         parenthesis_content = match.group(2)
#         print(f"Text within brackets: {bracket_content}")
#         print(f"Content within parenthesis: {parenthesis_content}")
#     else:
#         print("No match found.")
#     import ipdb; ipdb.set_trace()

def get_date_updated():
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



# End File: md-to-html/src/modules/export_markdown.py
