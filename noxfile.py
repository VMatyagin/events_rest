import tempfile

import nox

locations = "app", "noxfile.py"

PYTHON_VERSIONS = ["3.7"]


@nox.session(python=PYTHON_VERSIONS)
def safety(session):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        install_with_constraints(session, "safety")
        session.run("safety", "check", f"--file={requirements.name}", "--full-report")


def install_with_constraints(session, *args, **kwargs):
    with tempfile.NamedTemporaryFile() as requirements:
        session.run(
            "poetry",
            "export",
            "--dev",
            "--format=requirements.txt",
            "--without-hashes",
            f"--output={requirements.name}",
            external=True,
        )
        session.install(f"--constraint={requirements.name}", *args, **kwargs)


@nox.session(python=PYTHON_VERSIONS)
def isort(session):
    args = session.posargs or locations
    install_with_constraints(session, "isort")
    session.run("isort", *args)


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    args = session.posargs or locations
    install_with_constraints(
        session,
        "flake8",
        "flake8-isort",
        "flake8-bugbear",
        "flake8-bandit",
        "flake8-builtins",
        "flake8-comprehensions",
        "flake8-django",
        "flake8-simplify",
        "flake8-cognitive-complexity",
    )
    session.run("flake8", *args)


@nox.session(python=PYTHON_VERSIONS)
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


@nox.session(python=PYTHON_VERSIONS)
def pytype(session):
    """Run the static type checker."""
    args = session.posargs or ["--disable=import-error", *locations]
    install_with_constraints(session, "pytype")
    session.run("pytype", *args)


@nox.session(python=PYTHON_VERSIONS)
def mypy(session):
    args = session.posargs or locations
    install_with_constraints(session, "mypy")
    session.run("mypy", *args)


nox.options.sessions = ("lint", "mypy", "pytype", "safety")
