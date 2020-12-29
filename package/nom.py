import sys, requests
import zipfile
import os
from os import get_terminal_size
import pathlib
from glob import glob
import shutil
import re
import json
import string
import random
import ctypes
import shutil

def center(text: str)-> str:
    """
    Returns a centered string
    """
    return text.center(get_terminal_size().columns)

def printl(text: str)-> None:
    print("\r", end="")
    print(text, end="")

def random_string(length: int):
    l = []

    for _ in range(length):
        l.append(random.choice(string.ascii_letters + string.digits))

    return "".join(l)

def check_for_dirs()-> list:
    if not os.path.exists(pkg_dir + "\\temp"):
        os.umask(0)
        os.mkdir(pkg_dir + "\\temp", mode=0o777)

    if not os.path.exists(pkg_dir + "\\packages"):
        os.umask(0)
        os.mkdir(pkg_dir + "\\packages", mode=0o777)

    dirs = glob(pkg_dir + "\\packages\\*/")
    ndirs = []

    for x in dirs:
        ndirs.append(x[:-1])

    return ndirs

def parse_version(version)-> tuple:
    major, minor, micro = re.search(r'(\d+)\.(\d+)\.(\d+)', version).groups()

    return int(major), int(minor), int(micro)

if __name__ == "__main__":
    URL = ""
    pkg_dir = str(pathlib.Path.home()) + "\\DoggoscriptPkgs"
    a = sys.argv

    if not os.path.exists(pkg_dir):
        os.umask(0)
        os.mkdir(pkg_dir)

    check_for_dirs()

    try:
        if a[1].lower() == "help":
            print("--- Nom Help ---")
            print("- Help: Help session.")
            print("- Install: Install a Doggoscript package.")
            print("- Upgrade: Upgrade a Doggoscript package.")
            print("- Uninstall: Uninstall a Doggoscript package.")
            print("- Show (info): Show info about a Doggoscript package.")
        elif a[1].lower() == "install":
            try:
                dirs = check_for_dirs()
                packages = []

                for _dir in dirs:
                    packages.append(_dir.split("\\")[-1].lower())

                if a[2].lower() in packages:
                    print(f"Package {a[2].lower()} is already installed.")
                    exit(0)
                
                print("Getting package...")
                res = requests.get(URL + f"/package/{a[2].lower()}")

                if res.status_code != 200:
                    print("Server returned a non 200 responce code while getting package info...")
                    exit(0)

                pkgs = res.json()

                if pkgs['error']:
                    print(pkgs['msg'])
                    exit(0)

                print("Getting package zip...")
                fres = requests.get(pkgs['package']['zip_url'])

                if fres.status_code != 200:
                    print("Server returned a non 200 responce code while getting package zip...")
                    exit(0)

                if not os.path.exists(pkg_dir):
                    os.umask(0)
                    os.mkdir(pkg_dir, mode=0o777)         

                print("Downloading package zip...")
                with open(pkg_dir + "\\temp\\" + a[2].lower() + ".zip", "wb") as f:
                    f.write(fres.content)

                print("Extracting zip content...")
                with zipfile.ZipFile(pkg_dir + "\\temp\\" + a[2].lower() + ".zip", "r") as zf:
                    zf.extractall(pkg_dir + "\\packages\\" + a[2].lower())

                os.remove(pkg_dir + "\\temp\\" + a[2].lower() + ".zip")
                print(f"Package {a[2].lower()} was successfully installed!")

            except IndexError:
                print("No package was specified!")
        elif a[1].lower() == "uninstall":
            try:
                dirs = check_for_dirs()
                packages = []

                for _dir in dirs:
                    packages.append(_dir.split("\\")[-1].lower())

                if a[2].lower() not in packages:
                    print(f"Package {a[2].lower()} is not installed.")
                    exit(0)
                
                print("Deleting folder...")
                os.umask(0)
                shutil.rmtree(pkg_dir + "\\packages\\" + a[2].lower())

                print(f"Package {a[2].lower()} was uninstalled successfully!")

            except IndexError:
                print("No package was specified!")
        elif a[1].lower() == "upgrade":
            check_for_dirs()

            print("Getting package...")
            res = requests.get(URL + f"/package/{a[2].lower()}")

            if res.status_code != 200:
                print("Server returned a non 200 responce code while getting package info...")
                exit(0)

            data_ = res.json()

            if data_['error']:
                print(data_['msg'])
                exit(0)

            latest = max(res.json()['package']['versions'], key=parse_version)

            with open(pkg_dir + f"\\packages\\{a[2].lower()}\\package.json", encoding="utf-8") as f:
                data = json.load(f)

            if data['version'] == latest:
                print(f"Package {a[2].lower()} was already at latest!")
                exit(0)

            temp_dir = random_string(25)
            temp_file = random_string(15)

            os.mkdir(pkg_dir + "\\packages\\" + temp_dir)

            resp = requests.get(res.json()['package']['zip_url'])

            with open(pkg_dir + "\\temp\\" + temp_file + ".zip", "wb") as f:
                f.write(resp.content)

            with zipfile.ZipFile(pkg_dir + "\\temp\\" + temp_file + ".zip", "r") as zf:
                zf.extractall(pkg_dir + "\\packages\\" + temp_dir)

            os.umask(0)
            shutil.rmtree(pkg_dir + "\\packages\\" + a[2].lower())
            os.rename(pkg_dir + "\\packages\\" + temp_dir, pkg_dir + "\\packages\\" + a[2].lower())

            print(f"Upgraded {a[2].title()} ver {data['version']} to {latest}")

        elif a[1].lower() == "show" or a[1].lower == "info":
            try:
                res = requests.get(URL + "/package/" + a[2].lower())

                if res.status_code != 200:
                    print("Server returned a non 200 responce code...")
                    exit(0)

                pkg = res.json()

                if(pkg['error']):
                    print(pkg['msg'])
                    exit(0)

                pkg = pkg['package']

                print(f"Package {pkg['name']}")
                print(f"Latest version: {pkg['latest_version']}")
                print(f"All versions: {', '.join(pkg['versions'])}")
            except IndexError:
                print("No package was specified!")

    except IndexError:
        print("No command was specified. For help, please use nom help")
