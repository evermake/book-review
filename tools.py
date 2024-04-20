from subprocess import run


def typecheck() -> None:
    run(["mypy", "."])


def lint() -> None:
    run(["ruff", "check"])


def format() -> None:
    run(["ruff", "format"])
