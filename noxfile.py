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
        session, "flake8", "flake8-isort", "flake8-bugbear", "flake8-bandit"
    )
    session.run("flake8", *args)


@nox.session(python=PYTHON_VERSIONS)
def black(session):
    args = session.posargs or locations
    install_with_constraints(session, "black")
    session.run("black", *args)


nox.options.sessions = ("lint", "safety")
