import sys
from argparse import ArgumentParser
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

    focus_result = run_cmd(["xdotool", "search", "--desktop", "0", *search_args, "windowactivate"])
    if focus_result.returncode == 0:
        return

    if cmd:
        if auto_execute:
            Popen(cmd, shell=True)
        else:
            run_cmd(["qdbus", "org.kde.krunner", "/App", "org.kde.krunner.App.query", cmd])


def parse_args():
    parser = ArgumentParser()
    parser.add_argument("-c", "--class", dest="class_")
    parser.add_argument("-x", "--command")
    parser.add_argument("-y", "--auto-execute", action="store_true")
    parser.add_argument("alias", nargs="?")
    return parser.parse_args()
