from subprocess import run


def check():
    run(["ruff", "check"])


def format():
    run(["ruff", "format"])
