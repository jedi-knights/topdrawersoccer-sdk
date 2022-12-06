from invoke import task


@task(aliases=["u"])
def update(c):
    print("Updating dependencies...")
    c.run("poetry update")


@task(aliases=["c"])
def clean(c):
    print("Cleaning up...")
    c.run("rm -rf coverage")
    c.run("rm -rf dist")
    c.run("rm -f .coverage")
    c.run("rm -f coverage.xml")
    c.run("rm -rf htmlcov")
    c.run("rm -rf tests/htmlcov")
    c.run("rm -rf tests/.pytest_cache")
    c.run("rm -rf ./.pytest_cache")
    c.run("rm -f tests/coverage.xml")


@task(aliases=["t"])
def test(c):
    """Runs PyTest unit and integration tests."""
    c.run("pytest tests/unit")


@task(aliases=["v"])
def cover(c):
    """Runs PyTest unit and integration tests with coverage."""
    c.run("poetry run coverage run -m pytest")
    c.run("poetry run coverage lcov -o ./coverage/lcov.info")


@task(aliases=["l"])
def lint(c):
    print("Linting...")
    # c.run("poetry run black .")
    # c.run("poetry run isort .")
    # c.run(
    #     "poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place ."
    # )
    c.run(
        "poetry run flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics"
    )
    c.run(
        "poetry run flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics"
    )
    # c.run("poetry run mypy .")
    # c.run("poetry run safety check")
    # c.run("poetry run bandit -r .")
    # c.run("poetry run pyupgrade --py36-plus .")
    # c.run("poetry run pre-commit run --all-files")


@task(aliases=["version"])
def check_version(c):
    print("Checking version...")
    c.run("poetry run semantic-release version --noop")


@task(aliases=["b"], pre=[clean, lint, cover, check_version], default=True)
def build(c):
    print("Building the project")
    c.run("poetry build")
