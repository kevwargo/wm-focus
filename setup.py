from setuptools import find_packages, setup

setup(
    name="wm_focus",
    python_requires=">=3.8",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "wm-focus = wm_focus:run",
        ],
    },
)
