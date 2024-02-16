"""Export Markdown

"""
import os
import shutil

import jinja2
import markdown

from . import misc
from . import obsidian_parser


class ExportMarkdown:

    def __init__(self, config: dict, md_files: dict, toc: dict):
        self.config = config
        self.md_files = md_files
        self.toc = toc
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader(
                os.path.join(
                    self.config["export"]["template"]["dir"],
                    self.config["export"]["template"]["name"])))

    def run(self):
        """Export Markdown entrypoint.
        """
        print("Running export with template: %s" % self.config["export"]["template"]["name"])
        self.clean_export_path()
        for file_path, file_info in self.md_files.items():
            self.convert_file(file_info)
        self.create_index()
        self.copy_assests()

    def clean_export_path(self) -> bool:
        """Clear the export directory.

        """
        the_path = self.config["export"]["path"]
        if not os.path.exists(the_path):
            return True
        print("Clearing existing export")
        shutil.rmtree(the_path)
        return True    
    
    def convert_file(self, file_info: dict) -> bool:
        """Converts an Obsidian markdown file into an html file.

        """
        template = self.environment.get_template("markdown_1.html")
        the_file = open(file_info["full_path"], 'r').read()
        the_content = self.translate_md_to_html(the_file)
        
        if self.config["files"]["vaultRoot"]:
            asset_path = misc.asset_path(file_info["export_relative"])
            index_path = misc.index_path(file_info["export_relative"])
        else:
            asset_path = misc.asset_path(file_info["relative_path"])
            index_path = misc.index_path(file_info["relative_path"])

        data = {
            "title": misc.filter_md_ext(file_info["name"]),
            "content": the_content,
            "date_updated": misc.get_date_updated(),
            "date_generated": misc.get_date_generated(),
            "asset_path": asset_path,
            "index_path": index_path
        }
        phile_content = template.render(**data)
        self.write_file(file_info, phile_content)
        return True

    def translate_md_to_html(self, raw_markdown: str) -> str:
        """Translates a markdown file to html.
        @todo: fix relative links and pre tags
        """
        translated = raw_markdown
        # translated_md = misc.handle_md_html_pre_tags(raw_markdown)
        # if "## Check Boxes" in raw_markdown:
        #     import ipdb; ipdb.set_trace()
        translated = obsidian_parser.parse_anchors(translated)
        translated = obsidian_parser.parse_backticks(translated)
        # translated = misc.handle_obsidain_code_blocks(translated)
        # translated = misc.handle_obsidian_check_boxes(translated)
        # translated = misc.handle_obsidian_line_breaks(translated)
        return markdown.markdown(translated)

    def write_file(self, phile_info: dict, phile_content:str) -> bool:
        """Write a phile to the filesystem.
        """
        write_file = phile_info["export_path"]
        dir_path = os.path.dirname(write_file)
        write_file = misc.filter_md_ext(write_file, ".html")
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
        the_file = open(write_file, "w")
        the_file.write(phile_content)
        the_file.close()
        print("Wrote: %s" % write_file)
        return True

    def create_index(self) -> bool:
        """Create the table of contents / index file.
        """
        template = self.environment.get_template("table_of_contents.html")
        the_files = []


        for file_name, file_info in self.md_files.items():
            tpl_file_info = {
                "name": misc.filter_md_ext(file_info["name"]),
                "relative_path": file_info["export_relative"],
            }
            the_files.append(tpl_file_info)
        data = {
            "files": the_files,
            "asset_path": "./assets",
            "index_path": "./index.html",
            "date_generated": misc.get_date_generated(),
            "date_updated": misc.get_date_updated(),
            "toc": self.toc
        }
        phile_content = template.render(**data)
        phile_info = {
            "name": "Index",
            "relative_path": "index.md",
            "export_path": os.path.join(self.config["export"]["path"], "index.html"),
        }
        self.write_file(phile_info, phile_content)
        return True

    def copy_assests(self) -> bool:
        """Copies static assests such as css and javascript files to the export.
        """
        assest_dir = os.path.join(
            self.config["export"]["template"]["dir"],
            self.config["export"]["template"]["name"],
            "assets")
        to_path = os.path.join(self.config["export"]["path"], "assets")
        print("Copying Assets: %s" % assest_dir)
        if not os.path.exists(assest_dir):
            print("No assests to copy")
            return True
        shutil.copytree(assest_dir, to_path)
        return True

# End File: md-to-html/src/modules/export_markdown.py
