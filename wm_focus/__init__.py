import logging
from argparse import ArgumentParser
from pathlib import Path
from subprocess import Popen
from subprocess import run as run_cmd

CONFIG = {
    "slack": {
        "class": "slack",
        "command": "slack",
    },
    "konsole": {
        "class": "konsole",
        "command": "konsole",
        "auto": True,
    },
    "chrome": {
        "class": "chromium",
        "command": "chromium",
    },
    "firefox": {
        "class": "firefox",
        "command": "firefox",
    },
    "telegram": {
        "class": "TelegramDesktop",
        "command": "telegram-desktop",
    },
    "mocp": {
        "name": "mocp",
        "command": "konsole -e mocp",
        "auto": True,
    },
    "emacs": {
        "class": "emacs",
        "command": "emacs",
    },
    "audacity": {
        "class": "audacity",
        "command": "audacity",
    },
    "okular": {"class": "okular"},
    "gwenview": {"class": "gwenview"},
    "krusader": {
        "class": "krusader",
        "command": "krusader",
    },
    "dolphin": {
        "class": "dolphin",
        "command": "dolphin",
    },
}


logging.basicConfig(
    filename=Path("~/.wm-focus.log").expanduser(),
    filemode="a",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def run():
    args = parse_args()
    if alias := args.alias:
        window = CONFIG[alias]
        search_args = ("--class", window["class"]) if window.get("class") else ("--name", window["name"])
        cmd, auto_execute = window.get("command"), window.get("auto")
    elif cls := args.class_:
        search_args = ("--class", cls)
        cmd, auto_execute = args.command, args.auto_execute
    else:
        raise ValueError

    if not focus(search_args) and cmd:
        if auto_execute:
            Popen(cmd, shell=True)
        else:
            run_cmd(["qdbus", "org.kde.krunner", "/App", "org.kde.krunner.App.query", cmd])


def focus(args) -> bool:
    cmd = ["xdotool", "search", "--desktop", "0", *args, "windowactivate"]

    while True:
        result = run_cmd(cmd, capture_output=True)
        if result.returncode == 0:
            return True
        if result.returncode == 1 and not (result.stdout or result.stderr):
            return False

        if result.stderr.decode().startswith("X Error of failed request:  BadWindow"):
            logging.info(f"Retrying {cmd} ...")
        else:
            result.check_returncode()


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-c", "--class", dest="class_")
    parser.add_argument("-x", "--command")
    parser.add_argument("-y", "--auto-execute", action="store_true")
    parser.add_argument("alias", nargs="?")
    return parser.parse_args()
