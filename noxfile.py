import nox

locations = "app", "noxfile.py"

PYTHON_VERSIONS = ["3.7"]


@nox.session(python=PYTHON_VERSIONS)
def isort(session):
    args = session.posargs or locations
    session.install("isort")
    session.run("isort", *args)


@nox.session(python=PYTHON_VERSIONS)
def lint(session):
    args = session.posargs or locations
    session.install("flake8", "flake8-isort", "flake8-bugbear", "flake8-bandit")
    session.run("flake8", *args)


@nox.session(python=PYTHON_VERSIONS)
def black(session):
    args = session.posargs or locations
    session.install("black")
    session.run("black", *args)


nox.options.sessions = ("lint",)
