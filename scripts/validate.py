#!/usr/bin/env python3
"""Validate the distributable packages and run host-only regression tests."""

import ast
import os
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
NAMES = (
    "pd-disaggregation-design",
    "pd-disaggregation-serving",
    "pd-disaggregation-accuracy-debug",
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def main():
    try:
        license_bytes = (ROOT / "LICENSE").read_bytes()
        for name in NAMES:
            package = ROOT / "skills" / name
            entry = package / "SKILL.md"
            content = entry.read_text(encoding="utf-8")
            match = re.match(r"\A---\n(.*?)\n---\n", content, re.DOTALL)
            require(match, f"{entry}: missing frontmatter")
            # The collection deliberately uses simple one-line scalar fields.
            fields = {}
            for line in match.group(1).splitlines():
                key, separator, value = line.partition(":")
                require(separator and key not in fields, f"{entry}: invalid or duplicate field")
                fields[key] = value.strip()
            require(fields.get("name") == name, f"{entry}: name mismatch")
            description = fields.get("description", "")
            require(0 < len(description) <= 1024, f"{entry}: invalid description length")
            require(fields.get("license") == "MIT", f"{entry}: license mismatch")
            require((package / "LICENSE").read_bytes() == license_bytes,
                    f"{package}: bundled license differs")
            require((package / "agents" / "openai.yaml").is_file(),
                    f"{package}: missing interface metadata")
            for path in package.rglob("*"):
                require(not path.is_symlink(), f"{path}: package must not depend on symlinks")
                if path.is_file() and path.suffix in (".md", ".py", ".yaml"):
                    text = path.read_text(encoding="utf-8")
                    require(not re.search(r"[\u4e00-\u9fff]", text),
                            f"{path}: keep skill instructions in English")

        for path in ROOT.rglob("*"):
            relative = path.relative_to(ROOT)
            if any(part.startswith(".") or part == "__pycache__" for part in relative.parts):
                continue
            if not path.is_file() or path.suffix not in (".md", ".py", ".yaml", ".txt"):
                continue
            text = path.read_text(encoding="utf-8")
            require(all(line == line.rstrip() for line in text.splitlines()),
                    f"{relative}: trailing whitespace")
            if path.suffix == ".py":
                ast.parse(text, filename=str(relative))
            if path.suffix != ".md":
                continue
            for target in re.findall(r"\]\(([^)]+)\)", text):
                if urlsplit(target).scheme or target.startswith("#"):
                    continue
                local_path = unquote(target.split("#", 1)[0])
                resolved = (path.parent / local_path).resolve()
                require(resolved.is_relative_to(ROOT), f"{relative}: link escapes repository")
                require(resolved.exists(), f"{relative}: missing link {target}")
                if relative.parts[0] == "skills":
                    package = ROOT / "skills" / relative.parts[1]
                    require(resolved.is_relative_to(package),
                            f"{relative}: link depends on another package")

        for reference in ("official-docs.md", "runtime-integration.md", "skill-reuse.md"):
            copies = {(ROOT / "skills" / name / "references" / reference).read_bytes()
                      for name in NAMES}
            require(len(copies) == 1, f"Shared reference drift: {reference}")
    except (OSError, UnicodeError, ValueError, SyntaxError) as error:
        print(f"Validation failed: {error}", file=sys.stderr)
        return 1

    print("PASS: 3 skill packages, local links, licenses and shared references", flush=True)
    environment = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")
    return subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests", "-v"],
        cwd=ROOT, env=environment, check=False,
    ).returncode


if __name__ == "__main__":
    raise SystemExit(main())
