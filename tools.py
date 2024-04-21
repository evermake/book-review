import os
from subprocess import run as _run

CWD = os.path.dirname(os.path.abspath(__file__))


def run(command: str, *args: str) -> None:
    _run([command, *args], cwd=CWD)


def test() -> None:
    run("pytest")


def typecheck() -> None:
    run("mypy", ".")


def lint() -> None:
    run("ruff", "check")


def check() -> None:
    print("--- Lint")
    lint()

    print()

    print("--- Typecheck")
    typecheck()


def format() -> None:
    run("ruff", "check", "--fix")
    run("ruff", "format")


def migrations_apply() -> None:
    run("yoyo", "apply", "-b")


def migrations_rollback() -> None:
    run("yoyo", "rollback", "-b")


def migrations_list() -> None:
    run("yoyo", "list")


def migrations_new() -> None:
    run("yoyo", "new", "--sql")
