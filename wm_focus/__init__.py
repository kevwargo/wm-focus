import sys
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
}


def run():
    window = CONFIG[sys.argv[1]]
    search_args = ["--class", window["class"]] if window.get("class") else ["--name", window["name"]]
    focus_result = run_cmd(["xdotool", "search", "--desktop", "0", *search_args, "windowactivate"])
    if focus_result.returncode == 0:
        return

    if cmd := window.get("command"):
        if window.get("auto"):
            run_cmd(cmd, shell=True)
        else:
            run_cmd(["qdbus", "org.kde.krunner", "/App", "org.kde.krunner.App.query", cmd])
