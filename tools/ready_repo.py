"""Schemas' checks for `tools/ready.py`: ruff, then every example and test case validated."""

from ready import Check

RUFF = "ruff==0.16.10"

CHECKS = [
    Check("ready's tests", ["python3", "tools/test-ready.py"], covers=("tools/*ready*",)),
    Check("ruff", ["ruff", "check", "."], covers=("*.py", "ruff.toml"), tool=RUFF),
    Check("format", ["ruff", "format", "--check"], covers=("*.py",), tool=RUFF, on_paths=True),
    Check(
        "valid cases pass",
        ["sh", "-c", "python3 tools/validate.py examples/* tests/valid/*"],
        covers=("schema/*", "examples/*", "tests/*", "tools/validate.py"),
        tool="jsonschema",
        waits=True,
    ),
    Check(
        "invalid cases fail",
        ["sh", "-c", "python3 tools/validate.py --expect-invalid tests/invalid/*"],
        covers=("schema/*", "examples/*", "tests/*", "tools/validate.py"),
        tool="jsonschema",
        waits=True,
    ),
]
