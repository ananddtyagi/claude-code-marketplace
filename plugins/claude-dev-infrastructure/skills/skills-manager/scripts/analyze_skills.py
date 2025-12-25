#!/usr/bin/env python3
"""
Skills Analysis Tool for Skills Manager

Comprehensive analysis of Claude Code skills including:
- System reality detection (project type, tech stack)
- Skills inventory with metadata extraction
- Usage pattern analysis from git history
- Necessity scoring and redundancy detection
"""

import os
import re
import json
import yaml
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter
import datetime

@dataclass
class SkillMetadata:
    name: str
    description: str
    category: str
    triggers: List[str]
    capabilities: List[str]
    file_size: int
    last_modified: str
    file_path: str

@dataclass
class SystemReality:
    project_type: str
    primary_technologies: List[str]
    databases: List[str]
    frameworks: List[str]
    build_tools: List[str]
    directory_structure: Dict[str, int]
    relevance_domains: List[str]

@dataclass
class UsageStats:
    uses_90_days: int
    last_used: Optional[str]
    git_commits_mentioned: int
    dependencies: List[str]

class SkillsAnalyzer:
    def __init__(self, project_root: str = ".", skills_dir: str = ".claude/skills"):
        self.project_root = Path(project_root)
        self.skills_dir = Path(skills_dir)
        self.config_dir = self.project_root / ".claude/config"

    def detect_system_reality(self) -> SystemReality:
        """Analyze project structure and dependencies"""
        print("🔍 Detecting system reality...")

        # Detect project type and technologies
        technologies = set()
        frameworks = set()
        databases = set()
        build_tools = set()

        # Parse dependency files
        dependency_files = [
            "package.json", "package-lock.json", "yarn.lock",
            "requirements.txt", "requirements-dev.txt", "Pipfile", "poetry.lock",
            "Cargo.toml", "go.mod", "go.sum",
            "pom.xml", "build.gradle", "build.gradle.kts",
            "composer.json", "Gemfile", "mix.exs"
        ]

        for dep_file in dependency_files:
            file_path = self.project_root / dep_file
            if file_path.exists():
                print(f"  📦 Analyzing: {dep_file}")
                techs = self._parse_dependency_file(file_path)
                technologies.update(techs['technologies'])
                frameworks.update(techs['frameworks'])
                databases.update(techs['databases'])
                build_tools.update(techs['build_tools'])

        # Analyze directory structure
        directory_structure = {}
        important_dirs = ["src", "lib", "app", "components", "services", "docs", "k8s", "docker"]

        for dir_name in important_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists() and dir_path.is_dir():
                file_count = len(list(dir_path.rglob("*")))
                directory_structure[f"{dir_name}/"] = file_count

        # Determine project type and relevance domains
        project_type = self._determine_project_type(technologies, frameworks, directory_structure)
        relevance_domains = self._extract_relevance_domains(project_type, technologies, frameworks)

        return SystemReality(
            project_type=project_type,
            primary_technologies=list(technologies),
            databases=list(databases),
            frameworks=list(frameworks),
            build_tools=list(build_tools),
            directory_structure=directory_structure,
            relevance_domains=relevance_domains
        )

    def _parse_dependency_file(self, file_path: Path) -> Dict[str, Set[str]]:
        """Parse dependency file for technology detection"""
        techs = {
            'technologies': set(),
            'frameworks': set(),
            'databases': set(),
            'build_tools': set()
        }

        try:
            if file_path.name == "package.json":
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)

                deps = {}
                for dep_type in ['dependencies', 'devDependencies', 'peerDependencies']:
                    if dep_type in data:
                        deps.update(data[dep_type])

                for dep_name in deps.keys():
                    # Technology detection
                    if any(tech in dep_name.lower() for tech in ['react', 'vue', 'angular', 'svelte']):
                        techs['frameworks'].add(dep_name)
                    elif any(tech in dep_name.lower() for tech in ['express', 'fastify', 'koa', 'nest']):
                        techs['frameworks'].add(dep_name)
                    elif any(tech in dep_name.lower() for tech in ['pg', 'postgres', 'mysql', 'mongodb', 'redis', 'sqlite']):
                        techs['databases'].add(dep_name)
                    elif any(tech in dep_name.lower() for tech in ['webpack', 'vite', 'rollup', 'parcel', 'esbuild']):
                        techs['build_tools'].add(dep_name)
                    else:
                        techs['technologies'].add(dep_name)

            elif file_path.name.startswith("requirements"):
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()

                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        package = line.split('=')[0].split('>')[0].split('<')[0].strip()

                        if any(tech in package.lower() for tech in ['django', 'flask', 'fastapi', 'starlette']):
                            techs['frameworks'].add(package)
                        elif any(tech in package.lower() for tech in ['psycopg2', 'mysql', 'pymongo', 'redis', 'sqlite']):
                            techs['databases'].add(package)
                        else:
                            techs['technologies'].add(package)

        except (json.JSONDecodeError, FileNotFoundError, UnicodeDecodeError):
            pass

        return techs

    def _determine_project_type(self, technologies: Set[str], frameworks: Set[str],
                               directory_structure: Dict[str, int]) -> str:
        """Determine project type based on detected technologies"""

        if any(fw in str(frameworks) for fw in ['react', 'vue', 'angular', 'svelte']):
            if 'src/' in directory_structure and 'components/' in directory_structure:
                return "Frontend Framework Application"

        if any(fw in str(frameworks) for fw in ['django', 'flask', 'fastapi', 'express']):
            return "Backend API Application"

        if any(fw in str(frameworks) for fw in ['react', 'vue']) and any(fw in str(frameworks) for fw in ['django', 'flask', 'express']):
            return "Full-Stack Application"

        if 'Cargo.toml' in [f.name for f in self.project_root.rglob("Cargo.toml")]:
            return "Rust Application"

        if 'go.mod' in [f.name for f in self.project_root.rglob("go.mod")]:
            return "Go Application"

        if 'src/' in directory_structure:
            return "Software Development Project"

        return "General Project"

    def _extract_relevance_domains(self, project_type: str, technologies: Set[str],
                                 frameworks: Set[str]) -> List[str]:
        """Extract relevance domains based on project characteristics"""
        domains = []

        # Technology-based domains
        tech_lower = ' '.join(list(technologies) + list(frameworks)).lower()

        if any(tech in tech_lower for tech in ['vue', 'react', 'angular', 'svelte']):
            domains.append('frontend')

        if any(tech in tech_lower for tech in ['node', 'python', 'java', 'go', 'rust']):
            domains.append('backend')

        if any(tech in tech_lower for tech in ['postgresql', 'mysql', 'mongodb', 'redis']):
            domains.append('database')

        if any(tech in tech_lower for tech in ['docker', 'kubernetes', 'k8s']):
            domains.append('devops')

        if any(tech in tech_lower for tech in ['jest', 'pytest', 'cypress', 'playwright']):
            domains.append('testing')

        # Project type-based domains
        if 'Frontend' in project_type:
            domains.extend(['ui', 'components', 'styling'])

        if 'Backend' in project_type or 'API' in project_type:
            domains.extend(['api', 'services', 'authentication'])

        # Default domains
        if not domains:
            domains = ['general', 'productivity']

        return list(set(domains))

    def extract_skill_metadata(self, skill_file: Path) -> Optional[SkillMetadata]:
        """Extract metadata from skill markdown file"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()
        except (UnicodeDecodeError, FileNotFoundError):
            return None

        # Extract YAML frontmatter
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        metadata = {}

        if frontmatter_match:
            try:
                metadata = yaml.safe_load(frontmatter_match.group(1)) or {}
            except yaml.YAMLError:
                metadata = {}

        # Extract capabilities from content
        capabilities = []
        capability_patterns = [
            r'## Capabilities\n\n(.*?)(?:\n##|\Z)',
            r'### \d+\. .*?\n\n(.*?)(?:\n###|\n##|\Z)',
            r'[*-]\s*(.*(?:debug|fix|create|analyze|optimize|manage|build|test).*)',
        ]

        for pattern in capability_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                lines = match.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#') and len(line) > 10:
                        # Clean up bullet points and formatting
                        clean_line = re.sub(r'^[*-]\s*', '', line)
                        clean_line = re.sub(r'^\d+\.\s*', '', clean_line)
                        clean_line = clean_line.strip()
                        if clean_line:
                            capabilities.append(clean_line)

        # Extract activation triggers
        triggers = []
        if 'triggers' in metadata:
            if isinstance(metadata['triggers'], list):
                triggers = metadata['triggers']
            elif isinstance(metadata['triggers'], str):
                triggers = [metadata['triggers']]

        # Also look for trigger-like patterns in content
        trigger_patterns = [
            r'(?:triggers|activates?|when to use):\s*(.*?)(?:\n\n|\Z)',
            r'[*-]\s*(.*(?:when|if|for).*)',
        ]

        for pattern in trigger_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                for line in match.strip().split('\n'):
                    line = line.strip()
                    if line and not line.startswith('#'):
                        clean_line = re.sub(r'^[*-]\s*', '', line)
                        clean_line = clean_line.strip()
                        if clean_line and len(clean_line) > 5:
                            triggers.append(clean_line)

        # Get file modification info
        last_modified = self._get_git_last_modified(skill_file)

        return SkillMetadata(
            name=metadata.get('name', skill_file.stem),
            description=metadata.get('description', ''),
            category=metadata.get('category', 'general'),
            triggers=list(set(triggers)),  # Remove duplicates
            capabilities=list(set(capabilities)),  # Remove duplicates
            file_size=len(content),
            last_modified=last_modified,
            file_path=str(skill_file)
        )

    def _get_git_last_modified(self, file_path: Path) -> str:
        """Get last git modification date for a file"""
        try:
            result = subprocess.run(
                ['git', 'log', '-1', '--format="%ci"', str(file_path)],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip().strip('"')
        except (subprocess.CalledProcessError, FileNotFoundError):
            return "unknown"

    def analyze_usage_patterns(self, skill_name: str) -> UsageStats:
        """Analyze usage patterns from git history"""
        try:
            # Calculate date 90 days ago
            since_date = (datetime.datetime.now() - datetime.timedelta(days=90)).strftime("%Y-%m-%d")

            # Count commits mentioning this skill
            commit_count_result = subprocess.run(
                ['git', 'log', '--since', since_date, '--grep', skill_name, '--oneline'],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            commit_count = len(commit_count_result.stdout.strip().split('\n')) if commit_count_result.stdout.strip() else 0

            # Get last used date
            last_used_result = subprocess.run(
                ['git', 'log', '-1', '--format="%ci"', '--grep', skill_name],
                cwd=self.project_root,
                capture_output=True,
                text=True,
                check=True
            )
            last_used = last_used_result.stdout.strip().strip('"') if last_used_result.stdout.strip() else None

            # Analyze dependencies (references to other skills)
            dependencies = self._analyze_skill_dependencies(skill_name)

            return UsageStats(
                uses_90_days=commit_count,
                last_used=last_used,
                git_commits_mentioned=commit_count,
                dependencies=dependencies
            )

        except (subprocess.CalledProcessError, FileNotFoundError):
            return UsageStats(
                uses_90_days=0,
                last_used=None,
                git_commits_mentioned=0,
                dependencies=[]
            )

    def _analyze_skill_dependencies(self, skill_name: str) -> List[str]:
        """Analyze which other skills reference this skill"""
        try:
            dependencies = []
            skill_pattern = re.compile(r'\b' + re.escape(skill_name) + r'\b', re.IGNORECASE)

            for other_skill_file in self.skills_dir.glob("*.md"):
                if other_skill_file.stem == skill_name:
                    continue

                try:
                    with open(other_skill_file, 'r', encoding='utf-8') as f:
                        content = f.read()

                    if skill_pattern.search(content):
                        dependencies.append(other_skill_file.stem)

                except (UnicodeDecodeError, FileNotFoundError):
                    continue

            return dependencies
        except Exception:
            return []

    def calculate_necessity_score(self, skill: SkillMetadata, system_reality: SystemReality,
                                usage_stats: UsageStats) -> int:
        """Calculate necessity score for a skill (0-100)"""
        score = 0

        # Base score from recent usage (40 points max)
        usage_score = min(usage_stats.uses_90_days * 2, 40)  # 2 points per use, max 40
        score += usage_score

        # Project relevance score (30 points max)
        skill_domains = self._extract_domains_from_skill(skill)
        project_domains = system_reality.relevance_domains

        domain_overlap = len(set(skill_domains) & set(project_domains))
        relevance_score = min(domain_overlap * 10, 30)  # 10 points per matching domain
        score += relevance_score

        # Category importance score (20 points max)
        important_categories = ['debug', 'create', 'fix', 'meta']
        if skill.category in important_categories:
            score += 20
        elif skill.category in ['optimize', 'analyze', 'implement']:
            score += 15
        elif skill.category in ['test', 'documentation']:
            score += 12
        else:
            score += 8

        # Dependency score (10 points max)
        dependency_score = min(len(usage_stats.dependencies) * 3, 10)
        score += dependency_score

        return min(score, 100)

    def _extract_domains_from_skill(self, skill: SkillMetadata) -> List[str]:
        """Extract domains from skill description and capabilities"""
        text = f"{skill.description} {' '.join(skill.capabilities)} {' '.join(skill.triggers)}".lower()

        domains = []
        domain_keywords = {
            'frontend': ['vue', 'react', 'component', 'ui', 'frontend', 'javascript', 'typescript'],
            'backend': ['api', 'server', 'backend', 'database', 'service', 'node', 'python'],
            'debug': ['debug', 'fix', 'error', 'issue', 'problem', 'troubleshoot'],
            'create': ['create', 'build', 'generate', 'make', 'develop', 'implement'],
            'test': ['test', 'testing', 'validate', 'verify', 'check'],
            'productivity': ['productivity', 'workflow', 'automate', 'efficiency'],
            'vue.js': ['vue', 'vuex', 'pinia', 'vue-router'],
            'typescript': ['typescript', 'ts', 'type'],
            'documentation': ['documentation', 'docs', 'readme', 'guide'],
            'git': ['git', 'version control', 'commit', 'branch', 'merge']
        }

        for domain, keywords in domain_keywords.items():
            if any(keyword in text for keyword in keywords):
                domains.append(domain)

        return domains

    def run_full_analysis(self) -> Dict:
        """Run complete skills analysis"""
        print("🔍 Running comprehensive skills analysis...")

        # Phase 1: System Reality Detection
        print("\n=== Phase 1: System Reality Detection ===")
        system_reality = self.detect_system_reality()
        print(f"✅ Project type: {system_reality.project_type}")
        print(f"✅ Technologies detected: {len(system_reality.primary_technologies)}")
        print(f"✅ Relevance domains: {len(system_reality.relevance_domains)}")

        # Phase 2: Skills Inventory
        print("\n=== Phase 2: Skills Inventory ===")
        skills = {}
        skill_files = list(self.skills_dir.glob("*.md"))

        print(f"📁 Found {len(skill_files)} skill files")

        for skill_file in skill_files:
            skill_metadata = self.extract_skill_metadata(skill_file)
            if skill_metadata:
                skills[skill_metadata.name] = skill_metadata
                print(f"  ✅ {skill_metadata.name} - {skill_metadata.category} - {skill_metadata.file_size} lines")

        # Phase 3: Usage Analysis
        print("\n=== Phase 3: Usage Pattern Analysis ===")
        usage_stats = {}
        for skill_name in skills.keys():
            stats = self.analyze_usage_patterns(skill_name)
            usage_stats[skill_name] = stats
            if stats.uses_90_days > 0:
                print(f"  📊 {skill_name} - {stats.uses_90_days} uses (last 90 days)")
            else:
                print(f"  ⚠️  {skill_name} - No recent usage")

        # Phase 4: Necessity Scoring
        print("\n=== Phase 4: Necessity Scoring ===")
        necessity_scores = {}
        for skill_name, skill in skills.items():
            score = self.calculate_necessity_score(skill, system_reality, usage_stats[skill_name])
            necessity_scores[skill_name] = score
            if score >= 70:
                print(f"  🔥 {skill_name} - {score} (High necessity)")
            elif score >= 40:
                print(f"  📈 {skill_name} - {score} (Medium necessity)")
            else:
                print(f"  📉 {skill_name} - {score} (Low necessity)")

        # Generate summary
        print("\n=== Analysis Summary ===")
        total_skills = len(skills)
        high_necessity = len([s for s in necessity_scores.values() if s >= 70])
        medium_necessity = len([s for s in necessity_scores.values() if 40 <= s < 70])
        low_necessity = len([s for s in necessity_scores.values() if s < 40])

        print(f"Total skills: {total_skills}")
        print(f"High necessity: {high_necessity}")
        print(f"Medium necessity: {medium_necessity}")
        print(f"Low necessity: {low_necessity}")

        return {
            'system_reality': asdict(system_reality),
            'skills_inventory': {
                'total_skills': total_skills,
                'categories': dict(Counter([skill.category for skill in skills.values()])),
                'skills': {name: asdict(skill) for name, skill in skills.items()}
            },
            'usage_stats': {name: asdict(stats) for name, stats in usage_stats.items()},
            'necessity_scores': necessity_scores,
            'summary': {
                'total_skills': total_skills,
                'high_necessity': high_necessity,
                'medium_necessity': medium_necessity,
                'low_necessity': low_necessity,
                'analysis_timestamp': datetime.datetime.now().isoformat()
            }
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Analyze Claude Code skills')
    parser.add_argument('--project-root', default='.', help='Project root directory')
    parser.add_argument('--skills-dir', default='.claude/skills', help='Skills directory')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON output')

    args = parser.parse_args()

    analyzer = SkillsAnalyzer(args.project_root, args.skills_dir)
    result = analyzer.run_full_analysis()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2 if args.pretty else None, ensure_ascii=False)
        print(f"\n✅ Results saved to: {args.output}")
    else:
        print("\n" + "="*50)
        print("ANALYSIS RESULTS")
        print("="*50)
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))

if __name__ == "__main__":
    main()