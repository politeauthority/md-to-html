"""Convert

"""
import os
import shutil
import re

import jinja2
import markdown


CONFIG = {
    "OBSIDIAN_PATH": "/Users/alix/Library/Mobile Documents/iCloud~md~obsidian/Documents/Alix-Vault/test",
    "FILES": {
        "INCLUDE": True,
        "EXCLUDE": False,
        "PATH": ["MD To HTML"]
    },
    "EXPORT": {
        "PATH": "/Users/alix/Programming/repos/md-to-html/export",
    },
    "TEMPLATE": {
        "DIR": "/Users/alix/Programming/repos/md-to-html/templates/",
        "NAME": "obsidian_1",
        "LAYOUT": "layout_2.html"
    }
}


class Convert:
    def __init__(self):
        self.mkdown_files = {}
        self.environment = jinja2.Environment(
            loader=jinja2.FileSystemLoader("../templates/")
        )

    def run(self):
        self.get_files()
        self.filter_files()
        self.convert_files()
        self.copy_assests()

    def get_files(self):
        total_files = 0
        for root, dirs, files in os.walk(CONFIG["OBSIDIAN_PATH"], topdown=False):
            for name in files:
                if name[-3:] == ".md":
                    full_path = os.path.join(root, name)
                    total_files += 1
                    self.mkdown_files[full_path] = {
                        "name": name,
                        "relative_path": self._get_valut_relative_path(full_path),
                        "full_path": full_path
                    }
        print("\n Total Markdown: %s" % total_files)

    def filter_files(self):
        if CONFIG["FILES"]["INCLUDE"]:
            self._filter_include()
        else:
            print("Error can only handle includes right now")
            exit(1)

    def convert_files(self):
        self._clean_export_path()
        for full_path, phile in self.mkdown_files.items():
            self.convert_file(phile)

    def convert_file(self, phile): 
        layout_file = os.path.join(
            CONFIG["TEMPLATE"]["NAME"],
            CONFIG["TEMPLATE"]["LAYOUT"]
        )
        the_file = open(phile["full_path"], 'r').read()
        the_content = self._translate_md_to_html(the_file)

        title = self._filter_md_ext(phile["name"])
        template = self.environment.get_template(layout_file)
        phile_content = template.render(title=title,content=the_content)
        self.write_file(phile, phile_content)

    def write_file(self, phile_info, phile_content:str) -> bool:
        write_path = CONFIG["EXPORT"]["PATH"]
        print(write_path)
        print(phile_info)

        dir_path = os.path.join(
            write_path,
            os.path.dirname(phile_info["relative_path"])
        )
        new_rel_path = "%s.html" % phile_info["relative_path"][-3:]
        if not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)
            print("Made dir: %s" % dir_path)
        full_relative_path = os.path.join(
            write_path,
            self._filter_md_ext(phile_info["relative_path"]) + ".html")
        the_file = open(full_relative_path, "w")
        the_file.write(phile_content)
        the_file.close()
        print("Wrote: %s" % full_relative_path)

    def copy_assests(self) -> bool:
        assest_dir = os.path.join(CONFIG["TEMPLATE"]["DIR"], CONFIG["TEMPLATE"]["NAME"], "assets")
        to_path = os.path.join(CONFIG["EXPORT"]["PATH"], "assets")
        print("Copying Assets: %s" % assest_dir)
        if not os.path.exists(assest_dir):
            print("No assests to copy")
            return True
        shutil.copytree(assest_dir, to_path)
        return True


    def _translate_md_to_html(self, raw_markdown: str) -> str:
        translated_mkdir = self._handle_pre_tags(raw_markdown)
        return markdown.markdown(raw_markdown)

    def _handle_pre_tags(self, raw_text: str):
        # string = "This is a string with `backticks` around words and `multiple backticks` too."
        pattern = r"`([^`]+)`"
        # Find all occurrences using findall()
        matches = re.findall(pattern, raw_text)
        # Print the matched substrings
        print("Matched substrings:", matches)
        for match in matches:
            start = raw_text.find("`%s`" % match)
            if start:
                left_over = raw_text[start + 1:]
                closing_tick = left_over.find("`") + start + 2
                print(raw_text[start:closing_tick])
                replace = "`%s`" % match
                with_str = "<pre>%s</pre>" % match
                raw_text = raw_text.replace(replace, with_str)
            continue
        if len(matches) > 1:
            raw_text = self._handle_pre_tags(raw_text)
        return raw_text



    def _clean_export_path(self):
        the_path = CONFIG["EXPORT"]["PATH"]
        if not os.path.exists(the_path):
            return True
        print("Clearing existing export")
        shutil.rmtree(the_path)
        return True


    def _filter_include(self):
        """Filter files based on their relative path.
        @todo: Add an error if config values arent right.
        """
        new_files = {}
        for incl_rel_path in CONFIG["FILES"]["PATH"]:
            incl_rel_path_len = len(incl_rel_path)
            for full_path, phile in self.mkdown_files.items():
                print(phile["relative_path"])
                print(phile["relative_path"][:incl_rel_path_len])
                print("\n")
                if phile["relative_path"][:incl_rel_path_len] == incl_rel_path:
                    new_files[full_path] = phile
        self.mkdown_files = new_files
        print("\n Total Included: %s" % len(new_files))
        return True

    def _filter_md_ext(self, phile_name: str) -> str:
        if phile_name[-3:] == ".md":
            return phile_name[:-3]
        return phile_name

    def _get_valut_relative_path(self, full_path: str) -> str:
         replace_str = CONFIG["OBSIDIAN_PATH"]
         if replace_str[-1:] != "/":
             replace_str = replace_str + "/"
         relative_path = full_path.replace(replace_str, "")
         return relative_path

if __name__ == "__main__":
    Convert().run()