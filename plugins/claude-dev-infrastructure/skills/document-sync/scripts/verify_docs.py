#!/usr/bin/env python3
"""
Documentation Verification Script for Document Sync Skill

Verifies documentation against actual codebase to detect inconsistencies,
outdated information, and missing documentation.
"""

import os
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any, Tuple
import sys

class DocumentationVerifier:
    def __init__(self, root_dir: str = ".", system_state_file: str = "system_state.json"):
        self.root_dir = Path(root_dir).resolve()
        self.system_state_file = system_state_file
        self.system_state = self._load_system_state()
        self.verification_results = {
            "docs_inventory": [],
            "verification_report": [],
            "doc_trust_scores": {},
            "update_plan": [],
            "verification_metadata": {
                "timestamp": "",
                "root_directory": str(self.root_dir),
                "system_state_file": system_state_file,
                "total_docs": 0,
                "verified_sections": 0
            }
        }

    def _load_system_state(self) -> Dict[str, Any]:
        """Load system state JSON"""
        system_path = self.root_dir / self.system_state_file
        if not system_path.exists():
            raise FileNotFoundError(f"System state file not found: {system_path}")

        with open(system_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def find_documentation_files(self) -> List[Path]:
        """Find all documentation files in the project"""
        print("📚 Finding documentation files...")

        doc_patterns = [
            "**/*.md",
            "**/*.rst",
            "**/*.txt",
            "**/README*",
            "**/CHANGELOG*",
            "**/CONTRIBUTING*",
            "**/LICENSE*",
            "**/docs/**/*",
            "**/documentation/**/*",
            "**/.github/**/*.md"
        ]

        doc_files = set()

        for pattern in doc_patterns:
            try:
                for file_path in self.root_dir.glob(pattern):
                    if file_path.is_file() and not self._should_ignore_file(file_path):
                        doc_files.add(file_path)
            except Exception:
                continue

        # Also look for common documentation directories
        doc_dirs = ["docs", "documentation", "doc", "guides"]
        for doc_dir in doc_dirs:
            doc_path = self.root_dir / doc_dir
            if doc_path.exists() and doc_path.is_dir():
                for file_path in doc_path.rglob("*"):
                    if file_path.is_file() and not self._should_ignore_file(file_path):
                        doc_files.add(file_path)

        return sorted(list(doc_files))

    def _should_ignore_file(self, file_path: Path) -> bool:
        """Check if file should be ignored"""
        ignore_patterns = [
            "node_modules",
            ".git",
            "dist",
            "build",
            "coverage",
            ".next",
            ".nuxt",
            "__pycache__",
            ".pytest_cache"
        ]

        for pattern in ignore_patterns:
            if pattern in str(file_path):
                return True

        return False

    def analyze_documentation_content(self, doc_path: Path) -> Dict[str, Any]:
        """Analyze content of a documentation file"""
        try:
            with open(doc_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            return {"error": str(e)}

        # Extract different types of information
        analysis = {
            "file_path": str(doc_path.relative_to(self.root_dir)),
            "file_size": len(content),
            "line_count": len(content.split('\n')),
            "api_endpoints": self._extract_api_endpoints(content),
            "framework_mentions": self._extract_framework_mentions(content),
            "tech_stack_mentions": self._extract_tech_mentions(content),
            "config_variables": self._extract_config_variables(content),
            "features_mentioned": self._extract_features(content),
            "code_blocks": self._extract_code_blocks(content),
            "links": self._extract_links(content),
            "file_references": self._extract_file_references(content)
        }

        return analysis

    def _extract_api_endpoints(self, content: str) -> List[str]:
        """Extract API endpoint mentions from documentation"""
        endpoint_patterns = [
            r'`(GET|POST|PUT|DELETE|PATCH)\s+([^`]+)`',
            r'(GET|POST|PUT|DELETE|PATCH)\s+`([^`]+)`',
            r'/api/[^`\s\)]+',
            r'/v\d+/[^`\s\)]+',
            r'`/[^`\s\)]+`'
        ]

        endpoints = []
        for pattern in endpoint_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    endpoints.append(f"{match[0]} {match[1]}")
                else:
                    endpoints.append(match)

        return list(set(endpoints))  # Remove duplicates

    def _extract_framework_mentions(self, content: str) -> List[str]:
        """Extract framework mentions from documentation"""
        frameworks = [
            "react", "vue", "angular", "svelte", "next", "nuxt",
            "express", "fastify", "koa", "nestjs", "django", "flask",
            "redux", "vuex", "pinia", "mobx", "zustand",
            "jest", "vitest", "cypress", "playwright", "pytest"
        ]

        mentions = []
        content_lower = content.lower()
        for framework in frameworks:
            if framework in content_lower:
                mentions.append(framework)

        return mentions

    def _extract_tech_mentions(self, content: str) -> List[str]:
        """Extract technology mentions from documentation"""
        tech_keywords = [
            "mongodb", "postgresql", "mysql", "sqlite", "redis", "couchdb",
            "firebase", "supabase", "aws", "azure", "gcp",
            "docker", "kubernetes", "terraform", "ansible",
            "webpack", "vite", "rollup", "parcel", "esbuild",
            "typescript", "javascript", "python", "java", "go", "rust"
        ]

        mentions = []
        content_lower = content.lower()
        for tech in tech_keywords:
            if tech in content_lower:
                mentions.append(tech)

        return mentions

    def _extract_config_variables(self, content: str) -> List[str]:
        """Extract configuration variable mentions"""
        config_patterns = [
            r'[A-Z_]+_URL',
            r'[A-Z_]+_HOST',
            r'[A-Z_]+_PORT',
            r'[A-Z_]+_KEY',
            r'[A-Z_]+_SECRET',
            r'[A-Z_]+_TOKEN',
            r'[A-Z_]+_PATH',
            r'`[A-Z_]+`',
            r'\$\{[^}]+\}',
            r'process\.env\.[A-Z_]+'
        ]

        variables = []
        for pattern in config_patterns:
            matches = re.findall(pattern, content)
            variables.extend(matches)

        return list(set(variables))

    def _extract_features(self, content: str) -> List[str]:
        """Extract feature mentions"""
        feature_patterns = [
            r'feature[:\s]+([^\n,.)]+)',
            r'functionality[:\s]+([^\n,.)]+)',
            r'capability[:\s]+([^\n,.)]+)',
            r'\b(can|able to|supports|provides)\s+([^\n,.)]+)',
            r'\*\*([^\*]+)\*\*'  # Bold text that might be features
        ]

        features = []
        for pattern in feature_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    features.extend(match)
                else:
                    features.append(match)

        # Filter out common non-feature words
        stop_words = {'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        filtered_features = []
        for feature in features:
            feature = feature.strip()
            if len(feature) > 3 and feature.lower() not in stop_words:
                filtered_features.append(feature)

        return list(set(filtered_features))[:20]  # Limit output

    def _extract_code_blocks(self, content: str) -> List[Dict[str, str]]:
        """Extract code blocks from documentation"""
        code_block_patterns = [
            r'```(\w+)?\n(.*?)\n```',
            r'`([^`\n]+)`'  # Inline code
        ]

        code_blocks = []

        # Multi-line code blocks
        for match in re.finditer(r'```(\w+)?\n(.*?)\n```', content, re.DOTALL):
            language = match.group(1) or "text"
            code = match.group(2).strip()
            code_blocks.append({
                "type": "block",
                "language": language,
                "content": code,
                "lines": len(code.split('\n'))
            })

        # Inline code
        for match in re.finditer(r'`([^`\n]+)`', content):
            code = match.group(1).strip()
            if len(code) > 2:  # Filter out very short matches
                code_blocks.append({
                    "type": "inline",
                    "language": "text",
                    "content": code,
                    "lines": 1
                })

        return code_blocks

    def _extract_links(self, content: str) -> List[str]:
        """Extract links from documentation"""
        link_patterns = [
            r'\[([^\]]+)\]\(([^)]+)\)',  # Markdown links
            r'https?://[^\s\)]+',       # Direct URLs
            r'www\.[^\s\)]+'            # www URLs
        ]

        links = []
        for pattern in link_patterns:
            matches = re.findall(pattern, content)
            if isinstance(matches[0], tuple) if matches else False:
                links.extend([match[1] for match in matches])
            else:
                links.extend(matches)

        return links

    def _extract_file_references(self, content: str) -> List[str]:
        """Extract file path references"""
        file_patterns = [
            r'`([^`]+\.(js|ts|jsx|tsx|vue|py|java|cpp|c|h|cs|go|rs|rb|php|md|json|yaml|yml|toml))`',
            r'\./([^`\s\)]+)',
            r'/src/([^`\s\)]+)',
            r'./([^`\s\)]+\.(js|ts|vue|py|md))'
        ]

        files = []
        for pattern in file_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    files.append(match[0])
                else:
                    files.append(match)

        return list(set(files))

    def verify_against_system_state(self, doc_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Verify documentation claims against system state"""
        verification = {
            "file_path": doc_analysis.get("file_path", ""),
            "trust_score": 0,
            "issues_found": [],
            "missing_evidence": [],
            "outdated_claims": [],
            "confirmed_claims": [],
            "recommendations": []
        }

        # Initialize variables used in trust score calculation
        missing_endpoints = set()
        missing_frameworks = set()
        missing_tech = set()
        missing_files = set()
        existing_files = set()

        # Check API endpoints
        doc_endpoints = set(doc_analysis.get("api_endpoints", []))
        system_endpoints = set(self.system_state.get("architecture", {}).get("api_endpoints", []))

        if doc_endpoints:
            missing_endpoints = doc_endpoints - system_endpoints
            if missing_endpoints:
                verification["issues_found"].append({
                    "type": "missing_api_endpoints",
                    "severity": "high",
                    "description": f"API endpoints mentioned but not found in code: {list(missing_endpoints)}",
                    "evidence": "System scan did not detect these endpoints"
                })
                verification["missing_evidence"].extend(missing_endpoints)
            else:
                verification["confirmed_claims"].append({
                    "type": "api_endpoints_verified",
                    "description": f"All {len(doc_endpoints)} API endpoints found in code"
                })

        # Check framework mentions
        doc_frameworks = set(doc_analysis.get("framework_mentions", []))
        system_frameworks = set()

        # Extract frameworks from system state
        tech_stack = self.system_state.get("tech_stack", {})
        for file_name, tech_info in tech_stack.items():
            framework = tech_info.get("framework", "")
            if framework and framework != "Unknown":
                system_frameworks.add(framework.lower())

        if doc_frameworks:
            missing_frameworks = doc_frameworks - system_frameworks
            if missing_frameworks:
                verification["issues_found"].append({
                    "type": "missing_frameworks",
                    "severity": "medium",
                    "description": f"Frameworks mentioned but not detected in code: {list(missing_frameworks)}",
                    "evidence": "Tech stack scan did not detect these frameworks"
                })

        # Check technology mentions
        doc_tech = set(doc_analysis.get("tech_stack_mentions", []))
        system_tech = set()

        # Extract technologies from system state
        arch = self.system_state.get("architecture", {})
        system_tech.update(arch.get("database_usage", []))
        system_tech.update(arch.get("auth_methods", []))
        system_tech.update(arch.get("state_management", []))
        system_tech.update(arch.get("testing_framework", []))

        # Add from deployment config
        for deploy_file in arch.get("deployment_config", []):
            if "docker" in deploy_file.lower():
                system_tech.add("docker")
            if "kubernetes" in deploy_file.lower() or "k8s" in deploy_file.lower():
                system_tech.add("kubernetes")

        if doc_tech:
            missing_tech = doc_tech - system_tech
            if missing_tech:
                verification["issues_found"].append({
                    "type": "missing_technologies",
                    "severity": "medium",
                    "description": f"Technologies mentioned but not detected: {list(missing_tech)}",
                    "evidence": "System architecture scan did not detect these technologies"
                })

        # Check file references
        doc_files = set(doc_analysis.get("file_references", []))
        existing_files = set()

        # Check if referenced files exist
        for file_ref in doc_files:
            # Try different path resolutions
            possible_paths = [
                self.root_dir / file_ref,
                self.root_dir / "src" / file_ref,
                self.root_dir / "lib" / file_ref,
                self.root_dir / "app" / file_ref
            ]

            for path in possible_paths:
                if path.exists():
                    existing_files.add(file_ref)
                    break

        missing_files = doc_files - existing_files
        if missing_files:
            verification["issues_found"].append({
                "type": "missing_files",
                "severity": "high",
                "description": f"Files referenced but not found: {list(missing_files)}",
                "evidence": "File system check"
            })

        # Check configuration variables
        doc_configs = set(doc_analysis.get("config_variables", []))
        system_configs = set()

        # Extract config variables from system state
        config_files = self.system_state.get("configuration", {})
        for config_file, config_info in config_files.items():
            if "error" not in config_info:
                # This is a simplified check - real implementation would parse actual files
                system_configs.update(config_file)

        # Check code blocks
        code_blocks = doc_analysis.get("code_blocks", [])
        valid_code_blocks = 0
        for block in code_blocks:
            if block["type"] == "inline" or block["lines"] <= 50:  # Reasonable size check
                valid_code_blocks += 1

        # Calculate trust score
        total_checks = len(doc_endpoints) + len(doc_frameworks) + len(doc_tech) + len(doc_files) + len(code_blocks)
        passed_checks = len(doc_endpoints - set(verification["missing_evidence"])) + \
                       len(doc_frameworks - missing_frameworks) + \
                       len(doc_tech - missing_tech) + \
                       len(existing_files) + \
                       valid_code_blocks

        if total_checks > 0:
            verification["trust_score"] = round((passed_checks / total_checks) * 100)
        else:
            verification["trust_score"] = 50  # Neutral score for docs with no verifiable claims

        # Generate recommendations
        if verification["trust_score"] < 70:
            verification["recommendations"].append("Review and update outdated information")
        if missing_endpoints:
            verification["recommendations"].append("Update API endpoint documentation")
        if missing_files:
            verification["recommendations"].append("Update file path references or add missing files")
        if len(code_blocks) == 0:
            verification["recommendations"].append("Consider adding code examples for better documentation")

        return verification

    def generate_verification_report(self) -> str:
        """Generate comprehensive verification report"""
        report_lines = [
            "# Documentation Verification Report",
            f"*Generated on {self.verification_results['verification_metadata']['timestamp']}*",
            "",
            "## Summary",
            "",
            f"- **Total Documentation Files**: {self.verification_results['verification_metadata']['total_docs']}",
            f"- **Verified Sections**: {self.verification_results['verification_metadata']['verified_sections']}",
            f"- **Files with Issues**: {len([r for r in self.verification_results['verification_report'] if r['issues_found']])}",
            ""
        ]

        # Add trust score summary
        trust_scores = self.verification_results["doc_trust_scores"]
        if trust_scores:
            avg_trust = sum(trust_scores.values()) / len(trust_scores)
            report_lines.extend([
                f"- **Average Trust Score**: {avg_trust:.1f}%",
                f"- **High Trust Files**: {len([s for s in trust_scores.values() if s >= 80])}",
                f"- **Medium Trust Files**: {len([s for s in trust_scores.values() if 50 <= s < 80])}",
                f"- **Low Trust Files**: {len([s for s in trust_scores.values() if s < 50])}",
                ""
            ])

        # Add detailed file analysis
        report_lines.extend([
            "## Detailed Analysis",
            ""
        ])

        for verification in self.verification_results["verification_report"]:
            file_path = verification["file_path"]
            trust_score = verification["trust_score"]
            issues_count = len(verification["issues_found"])

            # Status emoji based on trust score
            if trust_score >= 80:
                status = "✅"
            elif trust_score >= 50:
                status = "⚠️"
            else:
                status = "❌"

            report_lines.extend([
                f"### {status} {file_path}",
                f"**Trust Score**: {trust_score}% | **Issues Found**: {issues_count}",
                ""
            ])

            if verification["confirmed_claims"]:
                report_lines.append("**✅ Verified Claims**:")
                for claim in verification["confirmed_claims"]:
                    report_lines.append(f"- {claim['description']}")
                report_lines.append("")

            if verification["issues_found"]:
                report_lines.append("**❌ Issues Found**:")
                for issue in verification["issues_found"]:
                    severity_emoji = {"high": "🔴", "medium": "🟡", "low": "🟢"}
                    emoji = severity_emoji.get(issue["severity"], "⚪")
                    report_lines.append(f"- {emoji} **{issue['type'].replace('_', ' ').title()}** ({issue['severity']}): {issue['description']}")
                report_lines.append("")

            if verification["recommendations"]:
                report_lines.append("**💡 Recommendations**:")
                for rec in verification["recommendations"]:
                    report_lines.append(f"- {rec}")
                report_lines.append("")

        # Add update plan section
        report_lines.extend([
            "## Update Plan",
            ""
        ])

        update_plan = self.verification_results["update_plan"]
        if update_plan:
            for action in update_plan:
                action_emoji = {"remove": "🗑️", "update": "✏️", "add": "➕", "review": "🔍"}
                emoji = action_emoji.get(action["action"], "📝")
                report_lines.append(f"{emoji} **{action['action'].title()}**: {action['description']}")
        else:
            report_lines.append("No specific actions required. Documentation is in good shape!")

        return "\n".join(report_lines)

    def generate_update_plan(self) -> List[Dict[str, str]]:
        """Generate prioritized update plan"""
        update_plan = []

        # Analyze verification results and create actions
        for verification in self.verification_results["verification_report"]:
            file_path = verification["file_path"]

            if verification["trust_score"] < 30:
                update_plan.append({
                    "action": "review",
                    "priority": "high",
                    "file": file_path,
                    "description": f"File has very low trust score ({verification['trust_score']}%)"
                })

            for issue in verification["issues_found"]:
                if issue["severity"] == "high":
                    if issue["type"] == "missing_files":
                        update_plan.append({
                            "action": "update",
                            "priority": "high",
                            "file": file_path,
                            "description": f"Fix file references: {issue['description']}"
                        })
                    elif issue["type"] == "missing_api_endpoints":
                        update_plan.append({
                            "action": "update",
                            "priority": "medium",
                            "file": file_path,
                            "description": f"Update API documentation: {issue['description']}"
                        })

        # Add recommendations for missing features
        system_features = [f["name"].lower() for f in self.system_state.get("features", [])]
        documented_features = set()

        for doc_analysis in self.verification_results["docs_inventory"]:
            documented_features.update([f.lower() for f in doc_analysis.get("features_mentioned", [])])

        missing_features = set(system_features) - documented_features
        if missing_features and len(missing_features) <= 10:  # Limit output
            update_plan.append({
                "action": "add",
                "priority": "medium",
                "file": "README.md",
                "description": f"Document missing features: {', '.join(list(missing_features)[:5])}"
            })

        return update_plan

    def run_verification(self):
        """Run complete verification process"""
        import datetime
        timestamp = datetime.datetime.now().isoformat()
        self.verification_results["verification_metadata"]["timestamp"] = timestamp

        print("🔍 Starting Documentation Verification")

        # Find all documentation files
        doc_files = self.find_documentation_files()
        self.verification_results["verification_metadata"]["total_docs"] = len(doc_files)

        print(f"📚 Found {len(doc_files)} documentation files")

        # Analyze each document
        for i, doc_path in enumerate(doc_files, 1):
            print(f"🔍 Analyzing ({i}/{len(doc_files)}): {doc_path.name}")

            # Analyze content
            doc_analysis = self.analyze_documentation_content(doc_path)
            self.verification_results["docs_inventory"].append(doc_analysis)

            # Verify against system state
            verification = self.verify_against_system_state(doc_analysis)
            self.verification_results["verification_report"].append(verification)
            self.verification_results["doc_trust_scores"][doc_analysis["file_path"]] = verification["trust_score"]

            self.verification_results["verification_metadata"]["verified_sections"] += 1

        # Generate update plan
        self.verification_results["update_plan"] = self.generate_update_plan()

        print("✅ Verification completed")

    def save_results(self, output_dir: str = "."):
        """Save verification results"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save verification report
        report_content = self.generate_verification_report()
        report_file = output_path / "doc_verification_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"📋 Verification report saved to: {report_file}")

        # Save update plan
        update_plan_file = output_path / "docs_update_plan.md"
        with open(update_plan_file, 'w', encoding='utf-8') as f:
            f.write("# Documentation Update Plan\n\n")

            plan = self.verification_results["update_plan"]
            if plan:
                # Group by priority
                high_priority = [p for p in plan if p.get("priority") == "high"]
                medium_priority = [p for p in plan if p.get("priority") == "medium"]
                low_priority = [p for p in plan if p.get("priority") == "low"]

                if high_priority:
                    f.write("## 🔴 High Priority\n\n")
                    for action in high_priority:
                        f.write(f"- **{action['action'].title()}** `{action['file']}`: {action['description']}\n")
                    f.write("\n")

                if medium_priority:
                    f.write("## 🟡 Medium Priority\n\n")
                    for action in medium_priority:
                        f.write(f"- **{action['action'].title()}** `{action['file']}`: {action['description']}\n")
                    f.write("\n")

                if low_priority:
                    f.write("## 🟢 Low Priority\n\n")
                    for action in low_priority:
                        f.write(f"- **{action['action'].title()}** `{action['file']}`: {action['description']}\n")
            else:
                f.write("No updates required! Your documentation is in excellent shape.\n")

        print(f"📝 Update plan saved to: {update_plan_file}")

        # Save detailed JSON results
        json_file = output_path / "verification_results.json"
        with open(json_file, 'w', encoding='utf-8') as f:
            json.dump(self.verification_results, f, indent=2, default=str)

        print(f"📊 Detailed results saved to: {json_file}")

        return report_file, update_plan_file

def main():
    parser = argparse.ArgumentParser(description="Verify documentation against codebase")
    parser.add_argument("--root", default=".", help="Root directory to analyze")
    parser.add_argument("--system-state", default="system_state.json", help="System state file path")
    parser.add_argument("--output", default=".", help="Output directory for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    try:
        verifier = DocumentationVerifier(args.root, args.system_state)
        verifier.run_verification()
        verifier.save_results(args.output)

        print("\n🎉 Documentation verification completed!")

    except Exception as e:
        print(f"\n❌ Verification failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()