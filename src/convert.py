"""Convert

"""

import os

import yaml

from modules import misc
from modules.export_markdown import ExportMarkdown

CONFIG_FILE = os.environ.get("MKDOWN_TO_HTML_CONFIG")


class Convert:

    def __init__(self):
        self.load_config()
        self.md_files = {}
        self.export_structure = {}

    def load_config(self):
        """Read the local configiuration yaml file."""
        if not os.path.exists(CONFIG_FILE):
            print("ERROR: Cannot open config file: %s" % CONFIG_FILE) 
            exit(1)
        with open(CONFIG_FILE, "r") as file:
            self.config = yaml.safe_load(file)
            self.config = self.config["mdToHtml"]

    def run(self):
        self.get_files()
        self.filter_files()
        self.convert_files()

    def get_files(self) -> bool:
        """Collect all thr markdown files in the vault.
        """
        total_files = 0
        for root, dirs, files in os.walk(self.config["obdisianPath"], topdown=False):
            for name in files:
                if name[-3:] == ".md":
                    full_path = os.path.join(root, name)
                    total_files += 1
                    relative_path =  self._get_valut_relative_path(full_path)
                    if self.config["files"]["vaultRoot"]:
                        export_relative = relative_path.replace(
                            self.config["files"]["vaultRoot"] + "/",
                            "")
                        export_path = os.path.join(
                            self.config["export"]["path"],
                            export_relative
                        )
                    else:
                        export_relative = relative_path
                        export_path = os.path.join(
                            self.config["export"],
                                relative_path,
                        )
                    export_path = misc.filter_md_ext(export_path, ".html")
                    export_relative = misc.filter_md_ext(export_relative, ".html")
                    self.md_files[relative_path] = {
                        "name": name,
                        "relative_path": relative_path,
                        "export_path": export_path,
                        "export_relative": export_relative,
                        "full_path": full_path
                    }
                    # self.export_structure[export_path] = self.md_files[relative_path]
        print("Total Markdown: %s" % total_files)
        return True

    def filter_files(self):
        """Filter the files, only keeping the files that should be exported.
        """
        if self.config["files"]["vaultRoot"]:
            self._filter_vault_root()
        elif self.config["files"]["include"]:
            self._filter_include()
        else:
            print("Error can only handle includes right now")
            exit(1)

    def convert_files(self):
        exported = ExportMarkdown(self.config, self.md_files).run()

    def _filter_vault_root(self):
        vault_root = self.config["files"]["vaultRoot"]
        print("Using Vault Root: %s" % vault_root)
        new_files = {}
        export_files = {}
        incl_rel_path_len = len(vault_root)
        for relative_path, phile_info in self.md_files.items():
            os.path.join(self.config["obdisianPath"], vault_root)
            inc_path = os.path.join(self.config["obdisianPath"], vault_root)
            incl_path_len = len(inc_path)
            if phile_info["full_path"][:incl_path_len] == inc_path:
                new_files[relative_path] = phile_info
                phile_dirs = os.path.dirname(phile_info["export_relative"])
                if "/" in phile_dirs:
                    phile_dirs = phile_dirs.split("/")
                else:
                    if phile_dirs == "":
                        continue
                    phile_dirs = [phile_dirs]
                for phile_dir in phile_dirs:
                    if phile_dir not in export_files:
                        export_files[phile_dir] = {}
                    export_files[phile_dir] = phile_info

                # export_files[os.path.dirname(phile_info["export_relative"])
                # export_files[phile_info[relative_path]] = self.md_files[relative_path]
        self.md_files = new_files
        print("Total Files to Export: %s" % len(new_files))
        return True

    def _filter_include(self):
        """Filter files based on their relative path.
        @todo: Add an error if config values arent right.
        """
        new_files = {}
        for incl_rel_path in self.config["files"]["paths"]:
            incl_rel_path_len = len(incl_rel_path)
            for full_path, phile in self.mkdown_files.items():
                if phile["relative_path"][:incl_rel_path_len] == incl_rel_path:
                    new_files[full_path] = phile
        self.md_files = new_files
        print("Total Files to Export: %s" % len(new_files))
        return True

    def _get_valut_relative_path(self, full_path: str) -> str:
         replace_str = self.config["obdisianPath"]
         if replace_str[-1:] != "/":
             replace_str = replace_str + "/"
         relative_path = full_path.replace(replace_str, "")
         return relative_path


def test():
    translated = "x"
    translated = misc.handle_obsidian_check_boxes(translated)

if __name__ == "__main__":
    # test()
    Convert().run()