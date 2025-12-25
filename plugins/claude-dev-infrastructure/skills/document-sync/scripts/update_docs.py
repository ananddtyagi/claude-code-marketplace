#!/usr/bin/env python3
"""
Document Update Script for Document Sync Skill

Automatically updates documentation based on verification results.
Supports dry-run, suggest, and auto-update modes with safety controls.
"""

import os
import json
import re
import argparse
import shutil
from pathlib import Path
from typing import Dict, List, Set, Any, Optional, Tuple
import sys
from datetime import datetime

class DocumentUpdater:
    def __init__(self, root_dir: str = ".", verification_file: str = "verification_results.json"):
        self.root_dir = Path(root_dir).resolve()
        self.verification_file = verification_file
        self.verification_results = self._load_verification_results()
        self.mode = "suggest"  # Default mode
        self.backup_dir = None
        self.updates_applied = []

    def _load_verification_results(self) -> Dict[str, Any]:
        """Load verification results JSON"""
        verification_path = self.root_dir / self.verification_file
        if not verification_path.exists():
            raise FileNotFoundError(f"Verification results file not found: {verification_path}")

        with open(verification_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def create_backup(self):
        """Create backup of all documentation files before updating"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_dir = self.root_dir / "doc_sync_backups" / timestamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        self.backup_dir = backup_dir

        print(f"💾 Creating backup in: {backup_dir}")

        for verification in self.verification_results["verification_report"]:
            file_path = self.root_dir / verification["file_path"]
            if file_path.exists():
                backup_path = backup_dir / verification["file_path"]
                backup_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, backup_path)

        print(f"✅ Backed up {len(self.verification_results['verification_report'])} files")

    def load_config(self) -> Dict[str, Any]:
        """Load document sync configuration"""
        config_path = self.root_dir / ".claude" / "document-sync-skill.yml"
        default_config = {
            "mode": "suggest",
            "protected_docs": ["README.md", "docs/security.md"],
            "review_required_for": ["section_removal", "breaking_changes"],
            "output_reports": ["doc_verification_report.md", "docs_update_plan.md"]
        }

        if config_path.exists():
            try:
                import yaml
                with open(config_path, 'r', encoding='utf-8') as f:
                    config = yaml.safe_load(f)
                return {**default_config, **config}
            except ImportError:
                print("⚠️ PyYAML not installed, using default configuration")
            except Exception as e:
                print(f"⚠️ Error loading config file: {e}")

        return default_config

    def generate_update_suggestions(self) -> List[Dict[str, Any]]:
        """Generate update suggestions based on verification results"""
        suggestions = []

        for verification in self.verification_results["verification_report"]:
            file_path = verification["file_path"]
            issues = verification["issues_found"]
            trust_score = verification["trust_score"]

            # Generate suggestions for each issue
            for issue in issues:
                suggestion = self._create_suggestion_for_issue(file_path, issue, verification)
                if suggestion:
                    suggestions.append(suggestion)

            # Generate suggestions for missing features
            if trust_score < 70:
                missing_features_suggestion = self._suggest_missing_features(file_path, verification)
                if missing_features_suggestion:
                    suggestions.append(missing_features_suggestion)

        # Sort suggestions by priority and severity
        priority_order = {"high": 3, "medium": 2, "low": 1}
        suggestions.sort(key=lambda x: (priority_order.get(x.get("priority", "low"), 0), x.get("severity_score", 0)), reverse=True)

        return suggestions

    def _create_suggestion_for_issue(self, file_path: str, issue: Dict[str, Any], verification: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Create update suggestion for a specific issue"""
        issue_type = issue["type"]
        severity = issue["severity"]

        suggestions_map = {
            "missing_api_endpoints": self._suggest_api_endpoint_fix,
            "missing_frameworks": self._suggest_framework_fix,
            "missing_technologies": self._suggest_technology_fix,
            "missing_files": self._suggest_file_reference_fix,
            "missing_config_variables": self._suggest_config_fix
        }

        if issue_type in suggestions_map:
            return suggestions_map[issue_type](file_path, issue, verification)

        return None

    def _suggest_api_endpoint_fix(self, file_path: str, issue: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest fix for missing API endpoints"""
        description = issue["description"]
        missing_endpoints = re.findall(r'([A-Z]+\s+/[^\]]+)', description)

        suggestion = {
            "type": "update_api_endpoints",
            "file": file_path,
            "priority": "medium",
            "severity": issue["severity"],
            "description": f"Update API endpoints documentation in {file_path}",
            "issue": issue,
            "action": "replace_missing_endpoints",
            "search_pattern": r'(GET|POST|PUT|DELETE|PATCH)\s+/[^\s\)]+',
            "replacement": f"# TODO: Update these endpoints with current API\n# Missing: {', '.join(missing_endpoints)}",
            "confidence": 0.8
        }

        return suggestion

    def _suggest_framework_fix(self, file_path: str, issue: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest fix for missing framework mentions"""
        description = issue["description"]
        missing_frameworks = re.findall(r'([a-z]+(?:js)?)', description.lower())

        suggestion = {
            "type": "update_framework_mentions",
            "file": file_path,
            "priority": "low",
            "severity": issue["severity"],
            "description": f"Update framework documentation in {file_path}",
            "issue": issue,
            "action": "verify_framework_claims",
            "search_pattern": r'\b(' + '|'.join(missing_frameworks) + r')\b',
            "replacement": f"# TODO: Verify framework claims for: {', '.join(missing_frameworks)}",
            "confidence": 0.6
        }

        return suggestion

    def _suggest_technology_fix(self, file_path: str, issue: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest fix for missing technology mentions"""
        description = issue["description"]
        missing_tech = re.findall(r'([a-z]+(?:db|sql|aws|gcp|azure))', description.lower())

        suggestion = {
            "type": "update_technology_mentions",
            "file": file_path,
            "priority": "low",
            "severity": issue["severity"],
            "description": f"Update technology documentation in {file_path}",
            "issue": issue,
            "action": "verify_technology_claims",
            "search_pattern": r'\b(' + '|'.join(missing_tech) + r')\b',
            "replacement": f"# TODO: Verify technology claims for: {', '.join(missing_tech)}",
            "confidence": 0.6
        }

        return suggestion

    def _suggest_file_reference_fix(self, file_path: str, issue: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest fix for missing file references"""
        description = issue["description"]
        missing_files = re.findall(r'([^`\]]+\.(js|ts|jsx|tsx|vue|py|md|json|yaml|yml))', description)

        suggestion = {
            "type": "fix_file_references",
            "file": file_path,
            "priority": "high",
            "severity": issue["severity"],
            "description": f"Fix file path references in {file_path}",
            "issue": issue,
            "action": "update_file_paths",
            "search_patterns": missing_files,
            "replacement": "# TODO: Update file path references",
            "confidence": 0.9
        }

        return suggestion

    def _suggest_config_fix(self, file_path: str, issue: Dict[str, Any], verification: Dict[str, Any]) -> Dict[str, Any]:
        """Suggest fix for missing config variables"""
        suggestion = {
            "type": "update_config_documentation",
            "file": file_path,
            "priority": "medium",
            "severity": issue["severity"],
            "description": f"Update configuration documentation in {file_path}",
            "issue": issue,
            "action": "verify_config_variables",
            "replacement": "# TODO: Update configuration variables",
            "confidence": 0.7
        }

        return suggestion

    def _suggest_missing_features(self, file_path: str, verification: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Suggest addition of missing features documentation"""
        # This is a placeholder - in real implementation, would compare
        # system features with documented features

        if file_path == "README.md" and verification["trust_score"] < 60:
            return {
                "type": "add_missing_features",
                "file": file_path,
                "priority": "medium",
                "severity": "low",
                "description": f"Add missing features documentation to {file_path}",
                "action": "add_features_section",
                "replacement": "\n## Features\n\nTODO: Add documented features based on codebase analysis\n",
                "confidence": 0.5
            }

        return None

    def apply_suggestion(self, suggestion: Dict[str, Any]) -> bool:
        """Apply a single update suggestion"""
        file_path = self.root_dir / suggestion["file"]

        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            return False

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            original_content = content
            updated_content = self._apply_suggestion_to_content(content, suggestion)

            if updated_content != original_content:
                if self.mode == "auto-update":
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(updated_content)

                    self.updates_applied.append({
                        "file": suggestion["file"],
                        "type": suggestion["type"],
                        "timestamp": datetime.now().isoformat(),
                        "backup_path": str(self.backup_dir / suggestion["file"]) if self.backup_dir else None
                    })

                    print(f"✅ Applied update to {suggestion['file']}")
                    return True
                elif self.mode == "suggest":
                    print(f"💡 Suggested update for {suggestion['file']}: {suggestion['description']}")
                    return True

        except Exception as e:
            print(f"❌ Error applying suggestion to {suggestion['file']}: {e}")
            return False

        return False

    def _apply_suggestion_to_content(self, content: str, suggestion: Dict[str, Any]) -> str:
        """Apply suggestion to file content"""
        action = suggestion.get("action", "")
        search_pattern = suggestion.get("search_pattern", "")
        replacement = suggestion.get("replacement", "")

        if action == "replace_missing_endpoints" and search_pattern:
            # Add comment about missing endpoints
            updated_content = re.sub(
                search_pattern,
                lambda match: f"{match.group(0)}  # TODO: Verify this endpoint exists",
                content
            )
            return updated_content

        elif action == "update_file_paths":
            search_patterns = suggestion.get("search_patterns", [])
            for pattern in search_patterns:
                if isinstance(pattern, tuple):
                    pattern = pattern[0]
                # Replace with comment
                content = re.sub(
                    re.escape(pattern),
                    f"{pattern}  # TODO: Update file path",
                    content
                )
            return content

        elif action == "add_features_section":
            # Add features section if not present
            if "## Features" not in content:
                return content + "\n" + replacement
            return content

        else:
            # Generic replacement
            if search_pattern:
                return re.sub(search_pattern, replacement, content)
            return content + "\n" + replacement

    def generate_diff_report(self) -> str:
        """Generate a report showing what changes would be made"""
        suggestions = self.generate_update_suggestions()

        if not suggestions:
            return "# Document Update Report\n\nNo updates needed! Your documentation is in good shape.\n"

        report_lines = [
            "# Document Update Report",
            f"*Generated on {datetime.now().isoformat()}*",
            "",
            f"## Summary",
            f"- **Total Suggestions**: {len(suggestions)}",
            f"- **High Priority**: {len([s for s in suggestions if s.get('priority') == 'high'])}",
            f"- **Medium Priority**: {len([s for s in suggestions if s.get('priority') == 'medium'])}",
            f"- **Low Priority**: {len([s for s in suggestions if s.get('priority') == 'low'])}",
            ""
        ]

        # Group by file
        suggestions_by_file = {}
        for suggestion in suggestions:
            file_path = suggestion["file"]
            if file_path not in suggestions_by_file:
                suggestions_by_file[file_path] = []
            suggestions_by_file[file_path].append(suggestion)

        for file_path, file_suggestions in suggestions_by_file.items():
            priority_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}

            report_lines.extend([
                f"## 📄 {file_path}",
                ""
            ])

            for suggestion in file_suggestions:
                priority = suggestion.get("priority", "low")
                emoji = priority_emoji.get(priority, "⚪")
                confidence = suggestion.get("confidence", 0)

                report_lines.extend([
                    f"### {emoji} {suggestion.get('type', 'unknown').replace('_', ' ').title()}",
                    f"**Priority**: {priority} | **Confidence**: {confidence:.0%}",
                    f"**Description**: {suggestion['description']}",
                    ""
                ])

                if suggestion.get("search_pattern"):
                    report_lines.extend([
                        "**Search Pattern**:",
                        f"```regex",
                        suggestion["search_pattern"],
                        "```",
                        ""
                    ])

                if suggestion.get("replacement"):
                    report_lines.extend([
                        "**Suggested Replacement**:",
                        f"```",
                        suggestion["replacement"],
                        "```",
                        ""
                    ])

        return "\n".join(report_lines)

    def run_update_process(self, mode: str = "suggest"):
        """Run the update process"""
        self.mode = mode
        config = self.load_config()

        print(f"🚀 Starting document update process (mode: {mode})")

        if mode in ["auto-update", "suggest"]:
            # Create backup for safety
            self.create_backup()

        # Generate suggestions
        suggestions = self.generate_update_suggestions()
        print(f"💡 Generated {len(suggestions)} update suggestions")

        # Apply suggestions based on mode
        applied_count = 0
        for i, suggestion in enumerate(suggestions, 1):
            print(f"📝 Processing suggestion {i}/{len(suggestions)}: {suggestion['description']}")

            # Check if file is protected
            if suggestion["file"] in config.get("protected_docs", []):
                print(f"⚠️  Skipping protected file: {suggestion['file']}")
                continue

            # Check if action requires review
            action = suggestion.get("action", "")
            if action in config.get("review_required_for", []) and mode == "auto-update":
                print(f"⚠️  Skipping action requiring review: {action}")
                continue

            if self.apply_suggestion(suggestion):
                applied_count += 1

        # Generate report
        if mode in ["dry-run", "suggest"]:
            diff_report = self.generate_diff_report()
            report_file = self.root_dir / "document_update_report.md"
            with open(report_file, 'w', encoding='utf-8') as f:
                f.write(diff_report)

            print(f"📋 Update report saved to: {report_file}")

        # Summary
        print(f"\n📊 Update Summary:")
        print(f"- Mode: {mode}")
        print(f"- Suggestions generated: {len(suggestions)}")
        print(f"- Updates applied: {applied_count}")

        if self.backup_dir:
            print(f"- Backup created: {self.backup_dir}")

        if self.updates_applied:
            print(f"- Modified files: {len(set(u['file'] for u in self.updates_applied))}")

        return applied_count

def main():
    parser = argparse.ArgumentParser(description="Update documentation based on verification results")
    parser.add_argument("--root", default=".", help="Root directory to analyze")
    parser.add_argument("--verification", default="verification_results.json", help="Verification results file path")
    parser.add_argument("--mode", choices=["dry-run", "suggest", "auto-update"], default="suggest",
                       help="Update mode: dry-run (show only), suggest (show and backup), auto-update (apply changes)")
    parser.add_argument("--output", default=".", help="Output directory for reports")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        updater = DocumentUpdater(args.root, args.verification)
        updates_count = updater.run_update_process(args.mode)

        if args.mode == "auto-update" and updates_count > 0:
            print(f"\n✅ Successfully applied {updates_count} updates")
        elif args.mode == "suggest":
            print(f"\n💡 Generated {updates_count} suggestions for review")
        elif args.mode == "dry-run":
            print(f"\n📋 Dry run completed - {updates_count} potential updates identified")

    except Exception as e:
        print(f"\n❌ Update process failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()