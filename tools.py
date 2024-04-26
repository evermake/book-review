import os
from subprocess import run as _run

CWD = os.path.dirname(os.path.abspath(__file__))


def run(command: str, *args: str) -> None:
    _args = [command, *args]

    print(f"+ {' '.join(_args)}")

    try:
        _run(_args, cwd=CWD)
    except KeyboardInterrupt:
        exit(0)


def serve() -> None:
    run("python", "book_review/main.py")


def test() -> None:
    run("pytest")


def security() -> None:
    run("bandit", "-r", "book_review", "-n", "3", "-lll", "-c", "pyproject.toml")


def typecheck() -> None:
    run("mypy", ".")


def lint() -> None:
    run("ruff", "check")


def check() -> None:
    def header(title: str) -> None:
        print(f"\x1b[4;1m{title}\x1b[0m")
        print()

    header("Lint")
    lint()

    print()

    header("Security")
    security()

    print()

    header("Typecheck")
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


def locust() -> None:
    run("locust")
