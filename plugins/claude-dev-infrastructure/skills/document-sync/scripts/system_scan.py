#!/usr/bin/env python3
"""
System Scan Script for Document Sync Skill

Performs comprehensive analysis of codebase, tech stack, and architecture.
Generates system_state.json and code_features_report.md
"""

import os
import json
import re
import argparse
from pathlib import Path
from typing import Dict, List, Set, Any
import subprocess
import sys

class SystemScanner:
    def __init__(self, root_dir: str = "."):
        self.root_dir = Path(root_dir).resolve()
        self.system_state = {
            "tech_stack": {},
            "project_structure": {},
            "architecture": {},
            "dependencies": {},
            "features": [],
            "configuration": {},
            "scan_metadata": {
                "timestamp": "",
                "root_directory": str(self.root_dir),
                "scanner_version": "1.0.0"
            }
        }

    def scan_tech_stack(self):
        """Analyze package files and detect technologies"""
        print("🔍 Scanning tech stack...")

        tech_patterns = {
            "package.json": self._parse_package_json,
            "requirements.txt": self._parse_requirements_txt,
            "package-lock.json": self._parse_package_lock,
            "yarn.lock": self._parse_yarn_lock,
            "pom.xml": self._parse_pom_xml,
            "build.gradle": self._parse_gradle,
            "Cargo.toml": self._parse_cargo_toml,
            "composer.json": self._parse_composer_json,
            "Gemfile": self._parse_gemfile,
            "go.mod": self._parse_go_mod,
        }

        for file_name, parser in tech_patterns.items():
            file_path = self.root_dir / file_name
            if file_path.exists():
                try:
                    tech_info = parser(file_path)
                    self.system_state["tech_stack"][file_name] = tech_info
                    print(f"  ✅ Found {file_name}")
                except Exception as e:
                    print(f"  ❌ Error parsing {file_name}: {e}")

    def _parse_package_json(self, file_path: Path) -> Dict[str, Any]:
        """Parse Node.js package.json"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            "framework": self._detect_framework(data),
            "dependencies": data.get("dependencies", {}),
            "dev_dependencies": data.get("devDependencies", {}),
            "scripts": data.get("scripts", {}),
            "engines": data.get("engines", {}),
            "bundler": self._detect_bundler(data)
        }

    def _detect_framework(self, package_data: Dict) -> str:
        """Detect frontend/backend framework from dependencies"""
        deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

        frameworks = {
            "react": "React",
            "vue": "Vue.js",
            "angular": "Angular",
            "svelte": "Svelte",
            "next": "Next.js",
            "nuxt": "Nuxt.js",
            "express": "Express.js",
            "fastify": "Fastify",
            "koa": "Koa.js",
            "nestjs": "NestJS",
            "django": "Django",
            "flask": "Flask"
        }

        for dep, framework in frameworks.items():
            if dep in deps:
                return framework

        return "Unknown"

    def _detect_bundler(self, package_data: Dict) -> str:
        """Detect build tool/bundler"""
        deps = {**package_data.get("dependencies", {}), **package_data.get("devDependencies", {})}

        bundlers = {
            "vite": "Vite",
            "webpack": "Webpack",
            "rollup": "Rollup",
            "parcel": "Parcel",
            "esbuild": "ESBuild"
        }

        for dep, bundler in bundlers.items():
            if dep in deps:
                return bundler

        return "None detected"

    def _parse_requirements_txt(self, file_path: Path) -> Dict[str, Any]:
        """Parse Python requirements.txt"""
        requirements = []
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    requirements.append(line)

        return {
            "framework": self._detect_python_framework(requirements),
            "requirements": requirements,
            "count": len(requirements)
        }

    def _detect_python_framework(self, requirements: List[str]) -> str:
        """Detect Python framework from requirements"""
        frameworks = {
            "django": "Django",
            "flask": "Flask",
            "fastapi": "FastAPI",
            "pytest": "Testing",
            "requests": "HTTP Client"
        }

        for req in requirements:
            req_lower = req.lower()
            for framework_name, framework_display in frameworks.items():
                if framework_name in req_lower:
                    return framework_display

        return "Unknown"

    def _parse_package_lock(self, file_path: Path) -> Dict[str, Any]:
        """Parse package-lock.json for exact versions"""
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return {
            "lockfile_version": data.get("lockfileVersion"),
            "dependencies_count": len(data.get("dependencies", {})),
            "packages_count": len(data.get("packages", {}))
        }

    def _parse_yarn_lock(self, file_path: Path) -> Dict[str, Any]:
        """Parse yarn.lock"""
        return {
            "type": "Yarn lockfile",
            "note": "Exact version parsing not implemented"
        }

    def _parse_pom_xml(self, file_path: Path) -> Dict[str, Any]:
        """Parse Maven pom.xml"""
        return {
            "type": "Maven project",
            "note": "XML parsing not implemented"
        }

    def _parse_gradle(self, file_path: Path) -> Dict[str, Any]:
        """Parse Gradle build file"""
        return {
            "type": "Gradle project",
            "note": "Gradle parsing not implemented"
        }

    def _parse_cargo_toml(self, file_path: Path) -> Dict[str, Any]:
        """Parse Rust Cargo.toml"""
        return {
            "type": "Rust project",
            "note": "TOML parsing not implemented"
        }

    def _parse_composer_json(self, file_path: Path) -> Dict[str, Any]:
        """Parse PHP composer.json"""
        return {
            "type": "PHP project",
            "note": "Composer parsing not implemented"
        }

    def _parse_gemfile(self, file_path: Path) -> Dict[str, Any]:
        """Parse Ruby Gemfile"""
        return {
            "type": "Ruby project",
            "note": "Gemfile parsing not implemented"
        }

    def _parse_go_mod(self, file_path: Path) -> Dict[str, Any]:
        """Parse Go go.mod"""
        return {
            "type": "Go project",
            "note": "Go module parsing not implemented"
        }

    def scan_project_structure(self):
        """Analyze directory structure and key files"""
        print("📁 Scanning project structure...")

        important_dirs = ["src", "lib", "app", "config", "public", "tests", "docs"]
        structure = {}

        for dir_name in important_dirs:
            dir_path = self.root_dir / dir_name
            if dir_path.exists() and dir_path.is_dir():
                structure[dir_name] = self._analyze_directory(dir_path)
                print(f"  ✅ Found {dir_name}/")

        self.system_state["project_structure"] = structure

    def _analyze_directory(self, dir_path: Path) -> Dict[str, Any]:
        """Analyze directory contents"""
        files = []
        subdirs = []

        try:
            for item in dir_path.iterdir():
                if item.is_file():
                    files.append(item.name)
                elif item.is_dir() and not item.name.startswith('.'):
                    subdirs.append(item.name)
        except PermissionError:
            return {"error": "Permission denied"}

        return {
            "files": files[:20],  # Limit to prevent huge outputs
            "subdirectories": subdirs[:20],
            "file_count": len(files),
            "subdir_count": len(subdirs)
        }

    def scan_architecture(self):
        """Detect architectural patterns and components"""
        print("🏗️  Scanning architecture...")

        architecture = {
            "api_endpoints": self._find_api_endpoints(),
            "database_usage": self._detect_database_usage(),
            "auth_methods": self._detect_auth_methods(),
            "state_management": self._detect_state_management(),
            "testing_framework": self._detect_testing_framework(),
            "deployment_config": self._find_deployment_config()
        }

        self.system_state["architecture"] = architecture

    def _find_api_endpoints(self) -> List[str]:
        """Find API endpoint definitions"""
        endpoints = []
        api_patterns = [
            r'app\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)',
            r'router\.(get|post|put|delete|patch)\s*\(\s*[\'"]([^\'"]+)',
            r'@([A-Z]+)\s*\(\s*[\'"]([^\'"]+)',  # Decorators
            r'\.route\s*\(\s*[\'"]([^\'"]+)'
        ]

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        for pattern in api_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                if isinstance(match, tuple) and len(match) >= 2:
                                    endpoints.append(f"{match[0].upper()} {match[1]}")
                except Exception:
                    continue

        return endpoints[:10]  # Limit output

    def _detect_database_usage(self) -> List[str]:
        """Detect database technologies and patterns"""
        db_indicators = []

        db_patterns = {
            'mongodb': ['mongoose', 'mongodb', 'mongo_client'],
            'postgresql': ['pg', 'postgres', 'postgresql'],
            'mysql': ['mysql', 'mysql2'],
            'sqlite': ['sqlite', 'sqlite3'],
            'redis': ['redis', 'ioredis'],
            'couchdb': ['couchdb', 'nano', 'pouchdb'],
            'firebase': ['firebase', '@firebase'],
            'supabase': ['supabase', '@supabase']
        }

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for db, patterns in db_patterns.items():
                            if any(pattern in content for pattern in patterns):
                                if db not in db_indicators:
                                    db_indicators.append(db)
                except Exception:
                    continue

        return db_indicators

    def _detect_auth_methods(self) -> List[str]:
        """Detect authentication methods"""
        auth_methods = []

        auth_patterns = {
            'JWT': ['jwt', 'jsonwebtoken', 'jose'],
            'OAuth': ['oauth', 'passport', 'auth0'],
            'Session': ['session', 'express-session', 'cookie-session'],
            'Basic Auth': ['basic-auth', 'http-basic'],
            'API Key': ['api-key', 'x-api-key'],
            'Firebase Auth': ['firebase/auth', 'firebase/auth'],
            'Cognito': ['cognito', 'aws-sdk'],
            'Auth0': ['auth0', '@auth0']
        }

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for auth, patterns in auth_patterns.items():
                            if any(pattern in content for pattern in patterns):
                                if auth not in auth_methods:
                                    auth_methods.append(auth)
                except Exception:
                    continue

        return auth_methods

    def _detect_state_management(self) -> List[str]:
        """Detect state management solutions"""
        state_management = []

        state_patterns = {
            'Redux': ['redux', '@reduxjs'],
            'Vuex': ['vuex'],
            'Pinia': ['pinia'],
            'MobX': ['mobx'],
            'Zustand': ['zustand'],
            'Context API': ['createcontext', 'usecontext'],
            'Recoil': ['recoil'],
            'Valtio': ['valtio'],
            'Jotai': ['jotai']
        }

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for state, patterns in state_patterns.items():
                            if any(pattern in content for pattern in patterns):
                                if state not in state_management:
                                    state_management.append(state)
                except Exception:
                    continue

        return state_management

    def _detect_testing_framework(self) -> List[str]:
        """Detect testing frameworks"""
        testing_frameworks = []

        test_patterns = {
            'Jest': ['jest', '@jest'],
            'Vitest': ['vitest'],
            'Mocha': ['mocha'],
            'Jasmine': ['jasmine'],
            'Pytest': ['pytest'],
            'Unittest': ['unittest'],
            'Cypress': ['cypress'],
            'Playwright': ['playwright', '@playwright'],
            'Testing Library': ['testing-library', '@testing-library']
        }

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read().lower()
                        for framework, patterns in test_patterns.items():
                            if any(pattern in content for pattern in patterns):
                                if framework not in testing_frameworks:
                                    testing_frameworks.append(framework)
                except Exception:
                    continue

        return testing_frameworks

    def _find_deployment_config(self) -> List[str]:
        """Find deployment configuration files"""
        deployment_files = []

        deployment_patterns = [
            'dockerfile', 'docker-compose.yml', 'docker-compose.yaml',
            '.dockerignore', 'kubernetes', 'k8s', 'helm',
            'vercel.json', '.vercel', 'netlify.toml',
            '.github/workflows', '.gitlab-ci.yml',
            'azure-pipelines.yml', 'jenkinsfile',
            'terraform', 'ansible', 'puppet',
            'serverless.yml', '.serverless',
            'buildspec.yml', 'amplify.yml'
        ]

        for pattern in deployment_patterns:
            for file_path in self.root_dir.rglob("*"):
                if pattern.lower() in file_path.name.lower():
                    rel_path = file_path.relative_to(self.root_dir)
                    deployment_files.append(str(rel_path))

        return list(set(deployment_files))  # Remove duplicates

    def _is_code_file(self, file_path: Path) -> bool:
        """Check if file is a code file"""
        code_extensions = {
            '.js', '.ts', '.jsx', '.tsx', '.vue', '.svelte',
            '.py', '.java', '.cpp', '.c', '.h', '.cs',
            '.go', '.rs', '.rb', '.php', '.swift', '.kt',
            '.scala', '.clj', '.hs', '.ml', '.dart'
        }

        return file_path.suffix.lower() in code_extensions

    def extract_features(self):
        """Extract key features from the codebase"""
        print("✨ Extracting features...")

        features = []

        # Look for common feature patterns
        feature_patterns = [
            r'export\s+(?:async\s+)?function\s+(\w+)',
            r'export\s+(?:const|let|var)\s+(\w+)\s*=',
            r'class\s+(\w+)',
            r'interface\s+(\w+)',
            r'type\s+(\w+)\s*=',
            r'component\s+(\w+)',
            r'def\s+(\w+)\s*\(',  # Python
            r'func\s+(\w+)\s*\(',  # Go
        ]

        feature_files = {}

        for file_path in self.root_dir.rglob("*"):
            if file_path.is_file() and self._is_code_file(file_path):
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        file_features = []

                        for pattern in feature_patterns:
                            matches = re.findall(pattern, content, re.IGNORECASE)
                            for match in matches:
                                if len(match) > 2:  # Skip very short matches
                                    file_features.append(match)

                        if file_features:
                            rel_path = file_path.relative_to(self.root_dir)
                            feature_files[str(rel_path)] = file_features[:10]  # Limit per file

                except Exception:
                    continue

        # Convert to feature list
        for file_path, file_features in feature_files.items():
            for feature in file_features:
                features.append({
                    "name": feature,
                    "file": file_path,
                    "type": self._classify_feature_name(feature)
                })

        # Sort by name and deduplicate
        seen = set()
        unique_features = []
        for feature in sorted(features, key=lambda x: x['name']):
            key = (feature['name'], feature['file'])
            if key not in seen:
                seen.add(key)
                unique_features.append(feature)

        self.system_state["features"] = unique_features[:50]  # Limit total output

    def _classify_feature_name(self, name: str) -> str:
        """Classify feature type based on name"""
        name_lower = name.lower()

        if any(word in name_lower for word in ['test', 'spec', 'mock']):
            return 'testing'
        elif any(word in name_lower for word in ['config', 'setting', 'env']):
            return 'configuration'
        elif any(word in name_lower for word in ['api', 'route', 'endpoint', 'handler']):
            return 'api'
        elif any(word in name_lower for word in ['component', 'view', 'page']):
            return 'ui'
        elif any(word in name_lower for word in ['service', 'service', 'business']):
            return 'business'
        elif any(word in name_lower for word in ['model', 'entity', 'schema']):
            return 'data'
        elif any(word in name_lower for word in ['util', 'helper', 'common']):
            return 'utility'
        else:
            return 'general'

    def scan_configuration(self):
        """Scan configuration files"""
        print("⚙️  Scanning configuration...")

        config_files = [
            '.env', '.env.example', '.env.sample',
            'config.js', 'config.json', 'config.yaml', 'config.yml',
            'settings.py', 'settings.yaml', 'settings.yml',
            'application.properties', 'application.yml',
            'tsconfig.json', 'jsconfig.json',
            'vite.config.js', 'vite.config.ts',
            'webpack.config.js', 'rollup.config.js',
            '.babelrc', 'babel.config.js',
            'tailwind.config.js', 'postcss.config.js'
        ]

        found_configs = {}

        for config_file in config_files:
            config_path = self.root_dir / config_file
            if config_path.exists():
                found_configs[config_file] = self._analyze_config_file(config_path)

        self.system_state["configuration"] = found_configs

    def _analyze_config_file(self, file_path: Path) -> Dict[str, Any]:
        """Analyze a configuration file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count configuration keys/variables
            if file_path.suffix == '.json':
                try:
                    data = json.loads(content)
                    keys_count = len(self._count_json_keys(data))
                except:
                    keys_count = len(re.findall(r'["\']([^"\']+)["\']:', content))
            elif file_path.suffix in ['.yaml', '.yml']:
                keys_count = len(re.findall(r'^\s*\w+\s*:', content, re.MULTILINE))
            elif file_path.suffix in ['.js', '.ts']:
                keys_count = len(re.findall(r'["\']([^"\']+)["\']\s*:', content))
            else:  # .env, .properties, etc.
                keys_count = len([line for line in content.split('\n') if '=' in line and not line.strip().startswith('#')])

            return {
                "file_size": len(content),
                "keys_count": keys_count,
                "lines": len(content.split('\n'))
            }

        except Exception as e:
            return {"error": str(e)}

    def _count_json_keys(self, obj, count=0):
        """Recursively count keys in JSON object"""
        if isinstance(obj, dict):
            for key, value in obj.items():
                count += 1
                count = self._count_json_keys(value, count)
        elif isinstance(obj, list):
            for item in obj:
                count = self._count_json_keys(item, count)
        return count

    def generate_report(self):
        """Generate code features report"""
        print("📝 Generating report...")

        report_lines = [
            "# Code Features Report",
            f"*Generated on {self.system_state['scan_metadata']['timestamp']}*",
            "",
            "## Tech Stack Summary"
        ]

        # Add tech stack info
        for file_name, tech_info in self.system_state["tech_stack"].items():
            report_lines.append(f"\n### {file_name}")
            framework = tech_info.get("framework", "Unknown")
            report_lines.append(f"- **Framework**: {framework}")

            if file_name == "package.json":
                bundler = tech_info.get("bundler", "None detected")
                report_lines.append(f"- **Bundler**: {bundler}")
                deps_count = len(tech_info.get("dependencies", {}))
                dev_deps_count = len(tech_info.get("dev_dependencies", {}))
                report_lines.append(f"- **Dependencies**: {deps_count} runtime, {dev_deps_count} dev")

        # Add architecture info
        report_lines.extend([
            "",
            "## Architecture Components"
        ])

        arch = self.system_state["architecture"]
        if arch["database_usage"]:
            report_lines.append(f"- **Databases**: {', '.join(arch['database_usage'])}")
        if arch["auth_methods"]:
            report_lines.append(f"- **Authentication**: {', '.join(arch['auth_methods'])}")
        if arch["state_management"]:
            report_lines.append(f"- **State Management**: {', '.join(arch['state_management'])}")
        if arch["testing_framework"]:
            report_lines.append(f"- **Testing**: {', '.join(arch['testing_framework'])}")

        # Add features summary
        features_by_type = {}
        for feature in self.system_state["features"]:
            ftype = feature["type"]
            if ftype not in features_by_type:
                features_by_type[ftype] = []
            features_by_type[ftype].append(feature)

        report_lines.extend([
            "",
            "## Features by Type"
        ])

        for ftype, features in sorted(features_by_type.items()):
            report_lines.append(f"\n### {ftype.title()} ({len(features)} features)")
            for feature in features[:10]:  # Limit per type
                report_lines.append(f"- **{feature['name']}** in `{feature['file']}`")
            if len(features) > 10:
                report_lines.append(f"- *... and {len(features) - 10} more*")

        # Add deployment info
        if arch["deployment_config"]:
            report_lines.extend([
                "",
                "## Deployment Configuration",
                ""
            ])
            for deploy_file in arch["deployment_config"]:
                report_lines.append(f"- `{deploy_file}`")

        return "\n".join(report_lines)

    def save_results(self, output_dir: str = "."):
        """Save scan results to files"""
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save system state as JSON
        system_state_file = output_path / "system_state.json"
        with open(system_state_file, 'w', encoding='utf-8') as f:
            json.dump(self.system_state, f, indent=2, default=str)

        print(f"✅ System state saved to: {system_state_file}")

        # Save features report as Markdown
        report_content = self.generate_report()
        report_file = output_path / "code_features_report.md"
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(report_content)

        print(f"✅ Features report saved to: {report_file}")

        return system_state_file, report_file

def main():
    parser = argparse.ArgumentParser(description="Scan codebase for document sync analysis")
    parser.add_argument("--root", default=".", help="Root directory to scan")
    parser.add_argument("--output", default=".", help="Output directory for results")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")

    args = parser.parse_args()

    print("🚀 Starting System Scan for Document Sync")
    print(f"📂 Scanning directory: {Path(args.root).resolve()}")

    # Update timestamp
    import datetime
    timestamp = datetime.datetime.now().isoformat()

    scanner = SystemScanner(args.root)
    scanner.system_state["scan_metadata"]["timestamp"] = timestamp

    try:
        # Run all scans
        scanner.scan_tech_stack()
        scanner.scan_project_structure()
        scanner.scan_architecture()
        scanner.extract_features()
        scanner.scan_configuration()

        # Save results
        system_file, report_file = scanner.save_results(args.output)

        print("\n🎉 Scan completed successfully!")
        print(f"📊 System state: {system_file}")
        print(f"📋 Features report: {report_file}")

    except KeyboardInterrupt:
        print("\n❌ Scan interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Scan failed: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()