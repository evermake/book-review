from subprocess import run


def typecheck() -> None:
    run(["mypy", "."])


def lint() -> None:
    run(["ruff", "check"])


def format() -> None:
    run(["ruff", "format"])


def migrations_apply() -> None:
    run(["yoyo", "apply", "-b"])


def migrations_rollback() -> None:
    run(["yoyo", "rollback", "-b"])


def migrations_list() -> None:
    run(["yoyo", "list"])


def migrations_new() -> None:
    run(["yoyo", "new", "--sql"])
