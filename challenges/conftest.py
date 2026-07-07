"""Shared test plumbing for all chapter challenges.

Each test file gets a `subject` fixture: the challenge module for its chapter.
Set COURSE_SOLUTIONS=1 to run the same tests against the reference solutions
(that's how the course itself is verified — every skeleton must fail these
tests unmodified, and every reference solution must pass them).
"""

import importlib.util
import os
import pathlib

import pytest

ROOT = pathlib.Path(__file__).resolve().parent.parent


def load_subject(chapter: str):
    if os.environ.get("COURSE_SOLUTIONS") == "1":
        path = ROOT / "solutions" / f"{chapter}.py"
    else:
        path = ROOT / "challenges" / chapter / "challenge.py"
    spec = importlib.util.spec_from_file_location(f"subject_{chapter}", path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def subject(request):
    chapter = pathlib.Path(request.fspath).parent.name
    return load_subject(chapter)
