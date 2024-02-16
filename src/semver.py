"""Semver

"""

def update_version():
    version_txt = open("version.txt", "r")
    version_txt_str = version_txt.read()
    print(version_txt_str)
    last = version_txt_str.rfind(".")
    number = int(version_txt_str[last+1:].replace("\n", ""))
    new_number = number + 1
    new_version = version_txt_str[:last + 1] + str(new_number)
    print(new_version)
    version_txt = open("version.txt", "w")
    version_txt.write(new_version)
    version_txt.close()

if  __name__ == "__main__":
    update_version()
