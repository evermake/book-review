import subprocess


def format():
    subprocess.run(["ruff", "format"])
