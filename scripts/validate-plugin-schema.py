#!/usr/bin/env python3
"""
Plugin Schema Validator

Validates that all plugins in the plugins/ directory conform to the expected schema:

Required:
  - .claude-plugin/plugin.json (JSON manifest with name, version, description)

Optional:
  - commands/          (command definitions as .md files)
  - agents/            (agent definitions as .md files)
  - skills/            (agent skills with SKILL.md files)
  - hooks/             (hook configurations as .json files)
  - scripts/           (hook and utility scripts)
  - .mcp.json          (MCP server definitions)
  - LICENSE            (license file)
  - CHANGELOG.md       (version history)
  - README.md          (documentation)
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Set

# Define the expected schema
REQUIRED_FILES = {
    ".claude-plugin/plugin.json": "Plugin manifest file"
}

OPTIONAL_DIRS = {
    "commands": "Command definitions",
    "agents": "Agent definitions",
    "skills": "Agent skills",
    "hooks": "Hook configurations",
    "scripts": "Scripts and utilities"
}

OPTIONAL_FILES = {
    ".mcp.json": "MCP server definitions",
    "LICENSE": "License file",
    "CHANGELOG.md": "Version history",
    "README.md": "Documentation"
}

# Required fields in plugin.json
PLUGIN_JSON_REQUIRED_FIELDS = ["name", "version", "description"]

# Optional fields in plugin.json with their expected types
PLUGIN_JSON_OPTIONAL_FIELDS = {
    "author": dict,
    "homepage": str,
    "repository": str,
    "license": str,
    "keywords": list,
    "commands": (list, str),  # Can be list or string
    "agents": str,
    "hooks": str,
    "mcpServers": str
}

# Required fields in author object
AUTHOR_REQUIRED_FIELDS = ["name"]
AUTHOR_OPTIONAL_FIELDS = ["email", "url"]


class PluginValidator:
    def __init__(self, plugins_dir: Path):
        self.plugins_dir = plugins_dir
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.validated_plugins: Set[str] = set()
        self.is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
    
    def github_error(self, message: str, file_path: str = None, line: int = None):
        """Output a GitHub Actions error annotation."""
        if self.is_github_actions:
            if file_path and line:
                print(f"::error file={file_path},line={line}::{message}")
            elif file_path:
                print(f"::error file={file_path}::{message}")
            else:
                print(f"::error::{message}")
    
    def github_warning(self, message: str, file_path: str = None):
        """Output a GitHub Actions warning annotation."""
        if self.is_github_actions:
            if file_path:
                print(f"::warning file={file_path}::{message}")
            else:
                print(f"::warning::{message}")
    
    def validate_all_plugins(self) -> bool:
        """Validate all plugins in the plugins directory."""
        if not self.plugins_dir.exists():
            self.errors.append(f"Plugins directory not found: {self.plugins_dir}")
            return False
        
        plugin_dirs = [d for d in self.plugins_dir.iterdir() if d.is_dir()]
        
        if not plugin_dirs:
            self.warnings.append("No plugin directories found")
            return True
        
        print(f"Found {len(plugin_dirs)} plugin(s) to validate\n")
        
        all_valid = True
        for plugin_dir in sorted(plugin_dirs):
            if not self.validate_plugin(plugin_dir):
                all_valid = False
        
        return all_valid
    
    def validate_plugin(self, plugin_dir: Path) -> bool:
        """Validate a single plugin directory."""
        plugin_name = plugin_dir.name
        print(f"Validating plugin: {plugin_name}")
        print("-" * 60)
        
        plugin_valid = True
        
        # Check required files
        for req_file, description in REQUIRED_FILES.items():
            file_path = plugin_dir / req_file
            if not file_path.exists():
                error_msg = f"[{plugin_name}] Missing required file: {req_file} ({description})"
                self.errors.append(error_msg)
                self.github_error(error_msg, str(plugin_dir.relative_to(self.plugins_dir.parent)))
                plugin_valid = False
            else:
                # Validate plugin.json content
                if req_file == ".claude-plugin/plugin.json":
                    if not self.validate_plugin_json(file_path, plugin_name):
                        plugin_valid = False
                print(f"  ✓ {req_file}")
        
        # Check optional directories
        for opt_dir, description in OPTIONAL_DIRS.items():
            dir_path = plugin_dir / opt_dir
            if dir_path.exists():
                print(f"  ✓ {opt_dir}/ ({description})")
                
                # Validate content based on directory type
                if opt_dir == "commands" and not self.validate_markdown_files(dir_path, plugin_name, "command"):
                    plugin_valid = False
                elif opt_dir == "agents" and not self.validate_markdown_files(dir_path, plugin_name, "agent"):
                    plugin_valid = False
                elif opt_dir == "skills" and not self.validate_skills(dir_path, plugin_name):
                    plugin_valid = False
                elif opt_dir == "hooks" and not self.validate_json_files(dir_path, plugin_name):
                    plugin_valid = False
        
        # Check optional files
        for opt_file, description in OPTIONAL_FILES.items():
            file_path = plugin_dir / opt_file
            if file_path.exists():
                print(f"  ✓ {opt_file} ({description})")
                
                # Validate .mcp.json if present
                if opt_file == ".mcp.json" and not self.validate_mcp_json(file_path, plugin_name):
                    plugin_valid = False
        
        if plugin_valid:
            self.validated_plugins.add(plugin_name)
            print(f"  ✅ Plugin '{plugin_name}' is valid\n")
        else:
            print(f"  ❌ Plugin '{plugin_name}' has validation errors\n")
        
        return plugin_valid
    
    def validate_plugin_json(self, file_path: Path, plugin_name: str) -> bool:
        """Validate the plugin.json manifest file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Check required fields
            missing_fields = []
            for field in PLUGIN_JSON_REQUIRED_FIELDS:
                if field not in data:
                    missing_fields.append(field)
            
            if missing_fields:
                error_msg = f"[{plugin_name}] plugin.json missing required fields: {', '.join(missing_fields)}"
                self.errors.append(error_msg)
                self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)))
                return False
            
            is_valid = True
            
            # Validate required field types
            if not isinstance(data.get("name"), str) or not data["name"]:
                error_msg = f"[{plugin_name}] plugin.json 'name' must be a non-empty string"
                self.errors.append(error_msg)
                self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)), 2)
                is_valid = False
            
            if not isinstance(data.get("version"), str) or not data["version"]:
                error_msg = f"[{plugin_name}] plugin.json 'version' must be a non-empty string"
                self.errors.append(error_msg)
                self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)), 3)
                is_valid = False
            
            if not isinstance(data.get("description"), str) or not data["description"]:
                error_msg = f"[{plugin_name}] plugin.json 'description' must be a non-empty string"
                self.errors.append(error_msg)
                self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)), 4)
                is_valid = False
            
            # Validate optional fields
            if "author" in data:
                if not self.validate_author_field(data["author"], plugin_name):
                    is_valid = False
            
            if "homepage" in data:
                if not isinstance(data["homepage"], str) or not data["homepage"]:
                    self.errors.append(f"[{plugin_name}] plugin.json 'homepage' must be a non-empty string")
                    is_valid = False
            
            if "repository" in data:
                if not isinstance(data["repository"], str) or not data["repository"]:
                    self.errors.append(f"[{plugin_name}] plugin.json 'repository' must be a non-empty string")
                    is_valid = False
            
            if "license" in data:
                if not isinstance(data["license"], str) or not data["license"]:
                    self.errors.append(f"[{plugin_name}] plugin.json 'license' must be a non-empty string")
                    is_valid = False
            
            if "keywords" in data:
                if not isinstance(data["keywords"], list):
                    self.errors.append(f"[{plugin_name}] plugin.json 'keywords' must be an array")
                    is_valid = False
                elif not all(isinstance(k, str) for k in data["keywords"]):
                    self.errors.append(f"[{plugin_name}] plugin.json 'keywords' must contain only strings")
                    is_valid = False
            
            # Check for disallowed fields that cause plugin loading failures
            # These directories/files are auto-discovered by Claude Code
            disallowed_fields = ["agents", "commands", "hooks", "mcpServers"]
            for field in disallowed_fields:
                if field in data:
                    error_msg = (
                        f"[{plugin_name}] plugin.json must NOT contain '{field}' field. "
                        f"Claude Code automatically discovers the {field}/ directory or .mcp.json file. "
                        f"Remove this field to fix plugin loading failures."
                    )
                    self.errors.append(error_msg)
                    self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)))
                    is_valid = False
            
            return is_valid
            
        except json.JSONDecodeError as e:
            error_msg = f"[{plugin_name}] Invalid JSON in plugin.json: {e}"
            self.errors.append(error_msg)
            self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)), getattr(e, 'lineno', 1))
            return False
        except Exception as e:
            error_msg = f"[{plugin_name}] Error reading plugin.json: {e}"
            self.errors.append(error_msg)
            self.github_error(error_msg, str(file_path.relative_to(self.plugins_dir.parent)))
            return False
    
    def validate_author_field(self, author: any, plugin_name: str) -> bool:
        """Validate the author field in plugin.json."""
        if not isinstance(author, dict):
            self.errors.append(f"[{plugin_name}] plugin.json 'author' must be an object")
            return False
        
        # Check required author fields
        if "name" not in author:
            self.errors.append(f"[{plugin_name}] plugin.json 'author' must have a 'name' field")
            return False
        
        if not isinstance(author["name"], str) or not author["name"]:
            self.errors.append(f"[{plugin_name}] plugin.json 'author.name' must be a non-empty string")
            return False
        
        # Validate optional author fields
        is_valid = True
        if "email" in author:
            if not isinstance(author["email"], str) or not author["email"]:
                self.errors.append(f"[{plugin_name}] plugin.json 'author.email' must be a non-empty string")
                is_valid = False
        
        if "url" in author:
            if not isinstance(author["url"], str) or not author["url"]:
                self.errors.append(f"[{plugin_name}] plugin.json 'author.url' must be a non-empty string")
                is_valid = False
        
        return is_valid
    
    def validate_mcp_json(self, file_path: Path, plugin_name: str) -> bool:
        """Validate the .mcp.json file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                json.load(f)
            return True
        except json.JSONDecodeError as e:
            self.errors.append(f"[{plugin_name}] Invalid JSON in .mcp.json: {e}")
            return False
        except Exception as e:
            self.warnings.append(f"[{plugin_name}] Error reading .mcp.json: {e}")
            return True
    
    def validate_markdown_files(self, dir_path: Path, plugin_name: str, file_type: str) -> bool:
        """Validate that directory contains .md files."""
        md_files = list(dir_path.glob("*.md"))
        if not md_files:
            self.warnings.append(
                f"[{plugin_name}] {dir_path.name}/ directory exists but contains no .md files"
            )
        return True
    
    def validate_skills(self, skills_dir: Path, plugin_name: str) -> bool:
        """Validate skills directory structure."""
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir()]
        
        if not skill_dirs:
            self.warnings.append(f"[{plugin_name}] skills/ directory exists but contains no skill directories")
            return True
        
        for skill_dir in skill_dirs:
            skill_md = skill_dir / "SKILL.md"
            if not skill_md.exists():
                self.warnings.append(
                    f"[{plugin_name}] Skill directory '{skill_dir.name}' missing SKILL.md"
                )
        
        return True
    
    def validate_json_files(self, dir_path: Path, plugin_name: str) -> bool:
        """Validate JSON files in directory."""
        json_files = list(dir_path.glob("*.json"))
        
        if not json_files:
            self.warnings.append(
                f"[{plugin_name}] {dir_path.name}/ directory exists but contains no .json files"
            )
            return True
        
        all_valid = True
        for json_file in json_files:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                self.errors.append(
                    f"[{plugin_name}] Invalid JSON in {json_file.name}: {e}"
                )
                all_valid = False
        
        return all_valid
    
    def print_summary(self):
        """Print validation summary."""
        print("=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Validated plugins: {len(self.validated_plugins)}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ All plugins are valid!")
        
        # Generate GitHub Actions Job Summary
        if self.is_github_actions:
            self.generate_github_summary()
    
    def generate_github_summary(self):
        """Generate a GitHub Actions job summary."""
        summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
        if not summary_file:
            return
        
        with open(summary_file, 'a') as f:
            f.write("## 🔍 Plugin Schema Validation Results\n\n")
            
            if not self.errors:
                f.write("### ✅ All Plugins Valid!\n\n")
                f.write(f"Successfully validated **{len(self.validated_plugins)}** plugins.\n\n")
            else:
                f.write("### ❌ Validation Failed\n\n")
                f.write(f"Found **{len(self.errors)}** error(s) in {len(self.validated_plugins)} plugins.\n\n")
                
                f.write("#### Errors\n\n")
                f.write("| Plugin | Error |\n")
                f.write("|--------|-------|\n")
                for error in self.errors:
                    # Extract plugin name and error message
                    if error.startswith('['):
                        plugin = error[1:error.index(']')]
                        msg = error[error.index(']')+2:]
                    else:
                        plugin = "Unknown"
                        msg = error
                    f.write(f"| `{plugin}` | {msg} |\n")
                f.write("\n")
            
            if self.warnings:
                f.write("#### ⚠️ Warnings\n\n")
                for warning in self.warnings:
                    f.write(f"- {warning}\n")
                f.write("\n")
            
            f.write("---\n")
            f.write("*See [PLUGIN_SCHEMA.md](../PLUGIN_SCHEMA.md) for schema requirements.*\n")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    plugins_dir = repo_root / "plugins"

    validator = PluginValidator(plugins_dir)
    validator.validate_all_plugins()
    validator.print_summary()

    # Only fail on actual errors, not warnings
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()

