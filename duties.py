"""Project Duties."""

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Tuple

from duty import duty
from duty.callables import mypy
from git_changelog.cli import build_and_render

if TYPE_CHECKING:
    from duty.context import Context
    from git_changelog import Changelog

CI = os.environ.get("CI", "0") in {"1", "true", "yes", ""}
WINDOWS = os.name == "nt"
PTY = not WINDOWS and not CI

MODULE_NAME = "recipe_scrapers_sage"


def _changelog() -> Tuple[Changelog, str]:
    """Update changelog in-place.

    Returns:
        Tuple[Changelog, str]: changelog object and contents
    """
    return build_and_render(
        repository=".",
        output="CHANGELOG.md",
        convention="conventional",
        template="keepachangelog",
        parse_trailers=True,
        parse_refs=False,
        bump="auto",
        in_place=True,
    )


@duty(aliases=["format"])
def fmt(ctx: Context):
    """Format source code.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run("isort --ca --profile=black .", title="Sorting imports (isort)")
    ctx.run("black .", title="Formatting code (black)")


@duty(aliases=["check_deps"])
def check_dependencies(ctx: Context):
    """Check for vulnerabilities in dependencies.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run(
        "poetry export --only main | safety check --stdin",
        title="Dependency checking (safety)",
    )


@duty
def check_types(ctx: Context):
    """Check that the code is correctly typed.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run(mypy.run(MODULE_NAME), title="Type checking (mypy)", pty=PTY)


@duty
def ruff(ctx: Context):
    """Run ruff code linting.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run("ruff check .", title="Code linting (ruff)")


@duty
def check_api(ctx: Context) -> None:
    """Check for API breaking changes.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    from griffe.cli import check as g_check

    ctx.run(
        lambda: g_check(MODULE_NAME),
        title="Checking for API breaking changes (griffe)",
        nofail=True,
    )


@duty(pre=["check_types", "ruff"])
def check(ctx: Context):
    """Check it all!

    Args:
        ctx (Context): the context instance (passed automatically).
    """


@duty
def test(ctx: Context):
    """Run the test suite.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run(f"pytest --cov={MODULE_NAME} --cov-report=xml", title="Testing (pytest)")


@duty
def changelog(ctx: Context):
    """Update the changelog in-place with latest commits.

    Args:
        ctx (Context): the context instance (passed automatically).
    """
    ctx.run(_changelog, title="Generating changelog (git-changelog)")


@duty()
def release(ctx: Context, version: str | None = None):
    """Release a new Python package.

    Args:
        ctx (Context): The context instance (passed automatically).
        version (str, optional): The new version number to use. Defaults to None.
    """
    if version is None:
        res: Tuple[Changelog, str] = _changelog()
        version: str = res[0].versions_list[0].planned_tag
    ctx.run(f"poetry version {version}", title="Bumping version (poetry)")
    ctx.run("git add pyproject.toml CHANGELOG.md", title="Staging files (git)")
    ctx.run(
        ["git", "commit", "-m", f"chore: Prepare release {version}"],
        title="Committing changes (git)",
        pty=PTY,
    )
    ctx.run("poetry publish --build", title="Publish package (poetry)")
    ctx.run(f"git tag {version}", title="Tagging commit (git)", pty=PTY)
    ctx.run("git push", title="Pushing commits (git)", pty=False)
    ctx.run("git push --tags", title="Pushing tags (git)", pty=False)
