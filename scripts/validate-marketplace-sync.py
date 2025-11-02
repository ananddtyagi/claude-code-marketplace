#!/usr/bin/env python3
"""
Marketplace Sync Validator

Validates that the marketplace documentation files (README.md, plugins.md)
are kept in sync with the actual plugins in the repository.

This ensures that when new plugins are added or updated, the marketplace
catalog is also updated.
"""

import json
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set

class MarketplaceSyncValidator:
    def __init__(self, repo_root: Path):
        self.repo_root = repo_root
        self.plugins_dir = repo_root / "plugins"
        self.readme_path = repo_root / "README.md"
        self.plugins_md_path = repo_root / "plugins.md"
        self.errors: List[str] = []
        self.warnings: List[str] = []
        self.is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
    
    def github_error(self, message: str, file_path: str = None):
        """Output a GitHub Actions error annotation."""
        if self.is_github_actions:
            if file_path:
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
    
    def get_plugin_list(self) -> Dict[str, Dict]:
        """Get list of plugins from the plugins directory."""
        plugins = {}
        
        if not self.plugins_dir.exists():
            return plugins
        
        for plugin_dir in self.plugins_dir.iterdir():
            if not plugin_dir.is_dir():
                continue
            
            plugin_json_path = plugin_dir / ".claude-plugin" / "plugin.json"
            
            # Skip plugins without plugin.json (they haven't been migrated yet)
            if not plugin_json_path.exists():
                continue
            
            try:
                with open(plugin_json_path, 'r', encoding='utf-8') as f:
                    plugin_data = json.load(f)
                
                plugins[plugin_dir.name] = {
                    "name": plugin_data.get("name", plugin_dir.name),
                    "description": plugin_data.get("description", ""),
                    "version": plugin_data.get("version", ""),
                    "path": plugin_dir
                }
            except (json.JSONDecodeError, Exception) as e:
                self.warnings.append(f"Could not read plugin.json for {plugin_dir.name}: {e}")
        
        return plugins
    
    def extract_plugin_names_from_markdown(self, content: str) -> Set[str]:
        """Extract plugin names mentioned in markdown content."""
        plugin_names = set()
        
        # Look for plugin names in code blocks and command examples
        # Pattern: /plugin install <plugin-name>
        install_patterns = re.findall(r'/plugin install ([a-z0-9-]+)', content, re.IGNORECASE)
        plugin_names.update(install_patterns)
        
        # Pattern: plugin-name@ in examples
        at_patterns = re.findall(r'([a-z0-9-]+)@', content, re.IGNORECASE)
        plugin_names.update(at_patterns)
        
        # Pattern: **Plugin Name** in featured sections
        bold_patterns = re.findall(r'\*\*([A-Za-z0-9 -]+)\*\*\s*-', content)
        # Convert to kebab-case for comparison
        for name in bold_patterns:
            kebab_name = name.lower().replace(' ', '-')
            plugin_names.add(kebab_name)
        
        # Remove common false positives
        false_positives = {'claude-code-marketplace', 'marketplace', 'your-org', 'test', 
                          'my-first-plugin', 'my-plugin', 'dev-marketplace', 'plugin-name'}
        plugin_names = plugin_names - false_positives
        
        return plugin_names
    
    def validate_marketplace_sync(self) -> bool:
        """Validate that marketplace files are in sync with actual plugins."""
        print("Validating marketplace synchronization...")
        print("=" * 60)
        
        # Get actual plugins with plugin.json
        plugins = self.get_plugin_list()
        
        if not plugins:
            print("No plugins with plugin.json found (this is okay for repos without migrated plugins)")
            return True
        
        print(f"Found {len(plugins)} plugin(s) with plugin.json:\n")
        for plugin_name in sorted(plugins.keys()):
            print(f"  - {plugin_name}")
        print()
        
        # Check README.md
        readme_valid = True
        if self.readme_path.exists():
            with open(self.readme_path, 'r', encoding='utf-8') as f:
                readme_content = f.read()
            
            readme_plugins = self.extract_plugin_names_from_markdown(readme_content)
            print(f"Plugins mentioned in README.md: {len(readme_plugins)}")
            
            # Check for missing plugins
            missing_in_readme = set(plugins.keys()) - readme_plugins
            if missing_in_readme:
                self.warnings.append(
                    f"README.md may be missing these plugins: {', '.join(sorted(missing_in_readme))}"
                )
                readme_valid = False
        else:
            self.warnings.append("README.md not found")
        
        # Check plugins.md (if it exists and is supposed to be a catalog)
        plugins_md_valid = True
        if self.plugins_md_path.exists():
            with open(self.plugins_md_path, 'r', encoding='utf-8') as f:
                plugins_md_content = f.read()
            
            # Only validate if it looks like a catalog (not documentation)
            if "# Plugins" in plugins_md_content and not "## Quickstart" in plugins_md_content:
                plugins_md_plugins = self.extract_plugin_names_from_markdown(plugins_md_content)
                print(f"Plugins mentioned in plugins.md: {len(plugins_md_plugins)}")
                
                missing_in_plugins_md = set(plugins.keys()) - plugins_md_plugins
                if missing_in_plugins_md:
                    self.warnings.append(
                        f"plugins.md may be missing these plugins: {', '.join(sorted(missing_in_plugins_md))}"
                    )
                    plugins_md_valid = False
        
        return readme_valid and plugins_md_valid
    
    def validate_on_pr(self) -> bool:
        """Validate marketplace sync specifically for PR changes."""
        import subprocess
        import os
        
        # Check if we're in a GitHub Actions environment
        is_github_actions = os.environ.get('GITHUB_ACTIONS') == 'true'
        
        if not is_github_actions:
            print("Not in GitHub Actions environment, skipping PR-specific validation")
            return True
        
        try:
            # Get list of changed files in the PR
            result = subprocess.run(
                ['git', 'diff', '--name-only', 'origin/main...HEAD'],
                capture_output=True,
                text=True,
                cwd=self.repo_root
            )
            
            if result.returncode != 0:
                print("Could not get changed files, skipping PR validation")
                return True
            
            changed_files = result.stdout.strip().split('\n')
            if not changed_files or changed_files == ['']:
                print("No changed files detected")
                return True
            
            # Check if new plugin directories were ADDED (not just modified)
            # Get list of added files (A = added)
            result_status = subprocess.run(
                ['git', 'diff', '--name-status', 'origin/main...HEAD'],
                capture_output=True,
                text=True,
                cwd=self.repo_root
            )
            
            if result_status.returncode != 0:
                print("Could not get file status, skipping PR validation")
                return True
            
            # Parse git diff output (format: "STATUS\tFILENAME")
            new_plugin_dirs = set()
            for line in result_status.stdout.strip().split('\n'):
                if not line:
                    continue
                parts = line.split('\t')
                if len(parts) < 2:
                    continue
                status, filepath = parts[0], parts[1]
                
                # Check if this is a new plugin.json file (indicates new plugin)
                if status == 'A' and filepath.startswith('plugins/') and filepath.endswith('.claude-plugin/plugin.json'):
                    # Extract plugin directory name (e.g., "plugins/my-plugin/")
                    plugin_dir = filepath.split('/')[1]
                    new_plugin_dirs.add(plugin_dir)
            
            if not new_plugin_dirs:
                print("No new plugins added, skipping marketplace sync check")
                return True
            
            print(f"New plugins detected: {', '.join(sorted(new_plugin_dirs))}")
            
            # Check if .claude-plugin/marketplace.json was updated
            marketplace_json_updated = '.claude-plugin/marketplace.json' in changed_files
            
            if not marketplace_json_updated:
                error_msg = (
                    f"New plugin(s) added ({', '.join(sorted(new_plugin_dirs))}) but .claude-plugin/marketplace.json was not updated. "
                    "Please add the new plugin(s) to the marketplace.json file."
                )
                self.errors.append(error_msg)
                self.github_error(error_msg, ".claude-plugin/marketplace.json")
                return False
            
            print("✓ Marketplace.json updated for new plugins")
            return True
            
        except Exception as e:
            print(f"Could not validate PR changes: {e}")
            return True  # Don't fail on validation errors
    
    def print_summary(self):
        """Print validation summary."""
        print("\n" + "=" * 60)
        print("MARKETPLACE SYNC SUMMARY")
        print("=" * 60)
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
                # Output warnings to GitHub Actions
                if self.is_github_actions and "may be missing" in warning:
                    self.github_warning(warning, "README.md")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
        else:
            print("\n✅ Marketplace appears to be in sync!")
        
        # Generate GitHub Actions Job Summary
        if self.is_github_actions:
            self.generate_github_summary()
    
    def generate_github_summary(self):
        """Generate a GitHub Actions job summary."""
        summary_file = os.environ.get('GITHUB_STEP_SUMMARY')
        if not summary_file:
            return
        
        with open(summary_file, 'a') as f:
            f.write("## 📚 Marketplace Sync Validation\n\n")
            
            if not self.errors:
                f.write("### ✅ Marketplace Documentation In Sync!\n\n")
                if not self.warnings:
                    f.write("All marketplace documentation files are properly synchronized with plugin changes.\n\n")
                else:
                    f.write("Marketplace files are in sync, but there are some warnings to review.\n\n")
            else:
                f.write("### ❌ Sync Check Failed\n\n")
                f.write("**Action Required:** Update marketplace documentation when adding or modifying plugins.\n\n")
                
                f.write("#### Errors\n\n")
                for error in self.errors:
                    f.write(f"- ❌ {error}\n")
                f.write("\n")
            
            if self.warnings:
                f.write("#### ⚠️ Warnings\n\n")
                # Show only first few warnings if there are many
                warnings_to_show = self.warnings[:5]
                for warning in warnings_to_show:
                    f.write(f"- {warning}\n")
                if len(self.warnings) > 5:
                    f.write(f"- ... and {len(self.warnings) - 5} more warnings\n")
                f.write("\n")
            
            f.write("#### 📝 How to Fix\n\n")
            f.write("1. Update `README.md` to include new/modified plugins in the featured sections\n")
            f.write("2. Update `plugins.md` if it contains a plugin catalog\n")
            f.write("3. Ensure plugin names match the directory names\n\n")
            f.write("---\n")


def main():
    """Main entry point."""
    script_dir = Path(__file__).parent
    repo_root = script_dir.parent
    
    validator = MarketplaceSyncValidator(repo_root)
    
    # Run general sync validation
    sync_valid = validator.validate_marketplace_sync()
    
    # Run PR-specific validation
    pr_valid = validator.validate_on_pr()
    
    validator.print_summary()
    
    # Only fail on errors, not warnings
    if validator.errors:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == "__main__":
    main()


