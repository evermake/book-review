from subprocess import run


def typecheck():
    run(["mypy", "."])


def lint():
    run(["ruff", "check"])


def format():
    run(["ruff", "format"])
