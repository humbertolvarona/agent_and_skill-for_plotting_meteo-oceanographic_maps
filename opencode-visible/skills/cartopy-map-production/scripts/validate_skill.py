from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


NAME_PATTERN = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
REQUIRED_FILES = (
    "SKILL.md",
    "references/map-specification.md",
    "templates/cartopy_map.py",
    "scripts/validate_skill.py",
)
REQUIRED_SKILL_SECTIONS = (
    "# Cartopy Map Production",
    "## Purpose",
    "## Activation rules",
    "## Scope",
    "## Inputs",
    "## Outputs",
    "## Deterministic workflow",
    "## Constraints",
    "## Dependencies",
    "## Error handling",
    "## Completion criteria",
)


def parse_frontmatter(text: str) -> dict[str, str]:
    if not text.startswith("---\n"):
        raise ValueError("SKILL.md must start with YAML frontmatter")
    end = text.find("\n---\n", 4)
    if end < 0:
        raise ValueError("SKILL.md frontmatter is not terminated")
    values: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if not line or line.startswith(" ") or ":" not in line:
            continue
        key, value = line.split(":", 1)
        values[key.strip()] = value.strip()
    return values


def validate_skill(skill_dir: Path) -> list[str]:
    errors: list[str] = []
    for relative_path in REQUIRED_FILES:
        if not (skill_dir / relative_path).is_file():
            errors.append(f"Missing required file: {relative_path}")
    skill_file = skill_dir / "SKILL.md"
    if not skill_file.is_file():
        return errors
    text = skill_file.read_text(encoding="utf-8")
    try:
        frontmatter = parse_frontmatter(text)
    except ValueError as exc:
        errors.append(str(exc))
        return errors
    name = frontmatter.get("name", "")
    description = frontmatter.get("description", "")
    if not NAME_PATTERN.fullmatch(name):
        errors.append(f"Invalid skill name: {name}")
    if name != skill_dir.name:
        errors.append(f"Skill name must match directory name: {skill_dir.name}")
    if not 1 <= len(description) <= 1024:
        errors.append("Description length must be between 1 and 1024 characters")
    for section in REQUIRED_SKILL_SECTIONS:
        if section not in text:
            errors.append(f"Missing required section: {section}")
    template_text = (skill_dir / "templates/cartopy_map.py").read_text(encoding="utf-8")
    required_fragments = (
        "ssl._create_default_https_context = ssl._create_unverified_context",
        "resolution=\"10m\"",
        "LongitudeFormatter(number_format=\".0f\"",
        "LatitudeFormatter(number_format=\".0f\"",
        "color=\"lightgray\"",
        "dpi=500",
        "format=\"png\"",
        "if config.show:",
    )
    for fragment in required_fragments:
        if fragment not in template_text:
            errors.append(f"Template missing required fragment: {fragment}")
    return errors


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("skill_dir", nargs="?", type=Path, default=Path(__file__).resolve().parents[1])
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    errors = validate_skill(args.skill_dir.resolve())
    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        return 1
    print("PASS: skill structure and required content are valid")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
