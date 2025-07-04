import nox

# Configure Nox to reuse virtual environments by default
nox.options.reuse_existing_virtualenvs = True
nox.options.error_on_missing_interpreters = False

@nox.session(python="3.11")
def tests(session):
    """Run all tests."""
    session.env["PYTHONPATH"] = "."
    # Install all dev dependencies
    session.install("-r", "dev-requirements.txt")
    session.run("pytest", "-v", "--capture=no", "tests")

@nox.session(python="3.11")
def integration_tests(session):
    """Run only integration tests."""
    session.env["PYTHONPATH"] = "."
    session.install("-r", "dev-requirements.txt")
    session.run("pytest", "-v", "--capture=no", "-m", "integration", "tests")

@nox.session(python="3.11")
def coverage(session):
    """Run tests with coverage."""
    session.env["PYTHONPATH"] = "."
    session.install("-r", "dev-requirements.txt")
    session.install("pytest-cov")
    session.run(
        "pytest",
        "--capture=no",
        "--cov=invoice_processor",
        "--cov=main",
        "--cov-report=term",
        "--cov-report=xml",
        "tests"
    )

@nox.session(python="3.11")
def lint(session):
    """Run linting checks."""
    session.install("flake8")
    session.run("flake8", "invoice_processor", "tests", "main.py")

@nox.session(python="3.11")
def typecheck(session):
    """Run type checking."""
    session.install("mypy")
    session.install("-r", "requirements.txt")
    session.run("mypy", "invoice_processor", "main.py")

@nox.session(python="3.11")
def format(session):
    """Format code with black."""
    session.install("black")
    session.run("black", "invoice_processor", "tests", "main.py")

@nox.session(python="3.11")
def clean(session):
    """Remove temporary files and directories."""
    import shutil
    import os
    import glob
    
    # Define patterns for files/directories to remove
    patterns = [
        # Python cache files
        "**/__pycache__",
        "**/*.pyc",
        "**/*.pyo",
        "**/*.pyd",
        "**/.pytest_cache",
        ".coverage",
        ".nox",
        # Build artifacts
        "build",
        "dist",
        "**/*.egg-info",
        # Coverage reports
        "htmlcov",
        "coverage.xml",
        # Temporary files
        "**/.tmp",
        "**/.temp",
    ]
    
    # Use Python's built-in file operations instead of shell commands
    for pattern in patterns:
        for path in glob.glob(pattern, recursive=True):
            if os.path.isdir(path):
                print(f"Removing directory: {path}")
                try:
                    shutil.rmtree(path)
                except Exception as e:
                    print(f"Error removing {path}: {e}")
            elif os.path.isfile(path):
                print(f"Removing file: {path}")
                try:
                    os.unlink(path)
                except Exception as e:
                    print(f"Error removing {path}: {e}")

@nox.session(python="3.11")
def ci(session):
    """Run all CI checks in the correct order."""
    # Run sessions sequentially to avoid memory issues
    session.notify("lint")
    session.notify("typecheck")
    session.notify("tests")
    # Skip more memory-intensive sessions for local development
    # Uncomment these for CI environments with more resources
    # session.notify("integration_tests")
    # session.notify("coverage")


