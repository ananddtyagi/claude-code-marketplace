#!/usr/bin/env python3
"""
Skill Validation Utilities

Provides validation functions for skill structure, metadata, and registry entries.
Used by package_skill.py and repair_skill.py scripts.
"""

import json
import sys
from pathlib import Path
import yaml


def validate_skill_frontmatter(skill_path):
    """
    Validate SKILL.md YAML frontmatter format and required fields.

    Args:
        skill_path: Path to skill directory

    Returns:
        tuple: (is_valid, error_message)
    """
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    try:
        content = skill_md.read_text(encoding='utf-8')

        # Check for YAML frontmatter
        if not content.startswith('---'):
            return False, "SKILL.md must start with YAML frontmatter (---)"

        # Extract frontmatter
        try:
            frontmatter_end = content.find('---', 3)
            if frontmatter_end == -1:
                return False, "YAML frontmatter not properly closed"

            frontmatter_text = content[3:frontmatter_end].strip()
            frontmatter = yaml.safe_load(frontmatter_text)

        except yaml.YAMLError as e:
            return False, f"Invalid YAML in frontmatter: {e}"

        # Check required fields
        if not isinstance(frontmatter, dict):
            return False, "Frontmatter must be a dictionary"

        required_fields = ['name', 'description']
        for field in required_fields:
            if field not in frontmatter:
                return False, f"Missing required field: {field}"
            if not frontmatter[field] or not str(frontmatter[field]).strip():
                return False, f"Field '{field}' cannot be empty"

        # Validate skill name format
        name = frontmatter['name']
        if not isinstance(name, str):
            return False, "Field 'name' must be a string"

        if len(name) > 100:
            return False, "Skill name too long (max 100 characters)"

        # Validate description
        description = frontmatter['description']
        if not isinstance(description, str):
            return False, "Field 'description' must be a string"

        if len(description) < 10:
            return False, "Description too short (min 10 characters)"

        return True, "Frontmatter validation passed"

    except Exception as e:
        return False, f"Error reading SKILL.md: {e}"


def validate_skill_structure(skill_path):
    """
    Validate skill directory structure.

    Args:
        skill_path: Path to skill directory

    Returns:
        tuple: (is_valid, error_message)
    """
    if not skill_path.exists():
        return False, "Skill directory does not exist"

    if not skill_path.is_dir():
        return False, "Skill path is not a directory"

    # Check for SKILL.md
    skill_md = skill_path / "SKILL.md"
    if not skill_md.exists():
        return False, "SKILL.md not found"

    # Check for expected subdirectories (optional but common)
    optional_dirs = ['scripts', 'references', 'assets']
    for dir_name in optional_dirs:
        dir_path = skill_path / dir_name
        if dir_path.exists() and not dir_path.is_dir():
            return False, f"'{dir_name}' exists but is not a directory"

    return True, "Structure validation passed"


def validate_skill_registry_entry(skills_json_path, skill_name):
    """
    Validate that a skill is properly registered in skills.json.

    Args:
        skills_json_path: Path to skills.json file
        skill_name: Name of the skill to check

    Returns:
        tuple: (is_registered, details_dict)
    """
    if not skills_json_path.exists():
        return False, {"error": "skills.json not found"}

    try:
        with open(skills_json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        skills = data.get('skills', {})

        if skill_name not in skills:
            return False, {
                "error": f"Skill '{skill_name}' not found in registry",
                "suggestion": "Add skill entry to skills.json"
            }

        skill_entry = skills[skill_name]

        # Check required fields in registry entry
        required_fields = ['name', 'category', 'triggers', 'keywords']
        missing_fields = [field for field in required_fields if field not in skill_entry]

        if missing_fields:
            return False, {
                "error": f"Missing registry fields: {missing_fields}",
                "entry": skill_entry
            }

        # Check if category exists
        categories = data.get('categories', {})
        category = skill_entry.get('category')
        if category and category not in categories:
            return False, {
                "error": f"Category '{category}' not defined in categories",
                "entry": skill_entry
            }

        return True, {"entry": skill_entry, "categories": categories}

    except json.JSONDecodeError as e:
        return False, {"error": f"Invalid JSON in skills.json: {e}"}
    except Exception as e:
        return False, {"error": f"Error reading skills.json: {e}"}


def validate_skill(skill_path):
    """
    Comprehensive skill validation including structure and registry check.

    Args:
        skill_path: Path to skill directory

    Returns:
        tuple: (is_valid, message)
    """
    skill_path = Path(skill_path).resolve()
    skill_name = skill_path.name

    # Validate structure
    structure_valid, structure_msg = validate_skill_structure(skill_path)
    if not structure_valid:
        return False, f"Structure error: {structure_msg}"

    # Validate frontmatter
    frontmatter_valid, frontmatter_msg = validate_skill_frontmatter(skill_path)
    if not frontmatter_valid:
        return False, f"Frontmatter error: {frontmatter_msg}"

    # Validate registry entry (warning only for packaging)
    skills_json_path = skill_path.parent.parent / "config" / "skills.json"
    registry_valid, registry_info = validate_skill_registry_entry(skills_json_path, skill_name)

    if not registry_valid:
        if "error" in registry_info and "suggestion" in registry_info:
            return False, f"Registry error: {registry_info['error']}. {registry_info['suggestion']}"
        else:
            return False, f"Registry error: {registry_info['error']}"

    return True, "Skill validation passed"


def diagnose_skill_issues(skill_path):
    """
    Comprehensive diagnostic for skill issues.

    Args:
        skill_path: Path to skill directory

    Returns:
        dict: Diagnostic report with issues and suggestions
    """
    skill_path = Path(skill_path).resolve()
    skill_name = skill_path.name

    diagnosis = {
        "skill_name": skill_name,
        "skill_path": str(skill_path),
        "issues": [],
        "warnings": [],
        "suggestions": []
    }

    # Check basic existence
    if not skill_path.exists():
        diagnosis["issues"].append({
            "type": "critical",
            "category": "existence",
            "message": "Skill directory does not exist",
            "solution": f"Create skill directory at {skill_path}"
        })
        return diagnosis

    # Validate structure
    structure_valid, structure_msg = validate_skill_structure(skill_path)
    if not structure_valid:
        diagnosis["issues"].append({
            "type": "critical",
            "category": "structure",
            "message": structure_msg,
            "solution": "Fix skill directory structure"
        })

    # Validate frontmatter
    frontmatter_valid, frontmatter_msg = validate_skill_frontmatter(skill_path)
    if not frontmatter_valid:
        diagnosis["issues"].append({
            "type": "critical",
            "category": "frontmatter",
            "message": frontmatter_msg,
            "solution": "Fix SKILL.md YAML frontmatter"
        })

    # Validate registry entry
    skills_json_path = skill_path.parent.parent.parent / "config" / "skills.json"
    registry_valid, registry_info = validate_skill_registry_entry(skills_json_path, skill_name)

    if not registry_valid:
        if "not found in registry" in registry_info.get("error", ""):
            diagnosis["issues"].append({
                "type": "critical",
                "category": "registry",
                "message": registry_info["error"],
                "solution": registry_info.get("suggestion", "Add skill to skills.json registry")
            })
        else:
            diagnosis["issues"].append({
                "type": "error",
                "category": "registry",
                "message": registry_info["error"],
                "solution": "Fix registry entry in skills.json"
            })
    else:
        diagnosis["warnings"].append("Skill is properly registered")

    # Add suggestions based on what's missing
    if not diagnosis["issues"]:
        diagnosis["suggestions"].append("Skill appears to be healthy")

    return diagnosis


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python quick_validate.py <path/to/skill>")
        sys.exit(1)

    skill_path = sys.argv[1]
    is_valid, message = validate_skill(skill_path)

    if is_valid:
        print(f"✅ {message}")
        sys.exit(0)
    else:
        print(f"❌ {message}")
        sys.exit(1)