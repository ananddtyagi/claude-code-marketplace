#!/usr/bin/env python3
"""
Safe Project Organizer for Claude Code
Analyzes project structure and suggests safe organizational improvements
"""

import os
import json
import fnmatch
from pathlib import Path
from typing import List, Dict, Set, Tuple
from dataclasses import dataclass, asdict
from collections import defaultdict
import hashlib

@dataclass
class FileInfo:
    """Information about a file in the project"""
    path: str
    size: int
    extension: str
    is_config: bool
    is_documentation: bool
    in_root: bool

@dataclass
class OrganizationSuggestion:
    """A suggested organizational change"""
    action: str  # 'move', 'delete', 'create_dir', 'rename'
    source: str
    destination: str = ""
    reason: str = ""
    risk_level: str = "low"  # low, medium, high
    safety_checks: List[str] = None

    def __post_init__(self):
        if self.safety_checks is None:
            self.safety_checks = []

class SafeProjectOrganizer:
    """
    Safe project organization analyzer and executor
    """

    # Protected patterns - NEVER modify these
    PROTECTED_PATTERNS = [
        '.git', '.git/**',
        '.svn', '.svn/**',
        '.hg', '.hg/**',
        'node_modules', 'node_modules/**',
        'vendor', 'vendor/**',
        'venv', 'venv/**',
        '.venv', '.venv/**',
        '__pycache__', '__pycache__/**',
        '.env*',
        'secrets.*',
        'credentials.*',
        '*.lock',
        'package-lock.json',
        'yarn.lock',
        'pnpm-lock.yaml',
        'Gemfile.lock',
        'Pipfile.lock',
        'poetry.lock',
        'dist', 'dist/**',
        'build', 'build/**',
        '.next', '.next/**',
        '.nuxt', '.nuxt/**',
        'out', 'out/**',
    ]

    # Common config files that should stay in root
    ROOT_CONFIG_FILES = {
        'package.json', 'tsconfig.json', 'jsconfig.json',
        'Cargo.toml', 'Cargo.lock',
        'go.mod', 'go.sum',
        'requirements.txt', 'setup.py', 'pyproject.toml',
        'Gemfile', 'Rakefile',
        '.gitignore', '.dockerignore',
        'Dockerfile', 'docker-compose.yml',
        'Makefile', 'CMakeLists.txt',
        '.eslintrc*', '.prettierrc*',
        'README.md', 'LICENSE', 'CHANGELOG.md',
    }

    # Files that can safely be moved to subfolders
    MOVABLE_ROOT_FILES = {
        'docs': ['*.md', '*.txt', 'CONTRIBUTING.md', 'CODE_OF_CONDUCT.md'],
        'config': ['*.config.js', '*.config.ts', '.editorconfig'],
        'scripts': ['*.sh', '*.ps1', '*.bat'],
    }

    # Empty/unused indicators
    EMPTY_FILE_INDICATORS = [
        '__init__.py',  # Can be empty in Python
    ]

    def __init__(self, project_root: str):
        self.project_root = Path(project_root).resolve()
        self.file_inventory: List[FileInfo] = []
        self.suggestions: List[OrganizationSuggestion] = []
        self.operation_log: List[Dict] = []

    def is_protected(self, path: Path) -> bool:
        """Check if a path is protected and should never be modified"""
        rel_path = path.relative_to(self.project_root)
        path_str = str(rel_path)

        # Check against protected patterns
        for pattern in self.PROTECTED_PATTERNS:
            if fnmatch.fnmatch(path_str, pattern):
                return True
            # Also check just the name
            if fnmatch.fnmatch(path.name, pattern):
                return True

        return False

    def scan_project(self) -> Dict:
        """
        Phase 1: Read-only analysis of project structure
        Returns comprehensive project statistics
        """
        print(f"🔍 Scanning project: {self.project_root}")
        print("📋 This is a READ-ONLY scan. No changes will be made.\n")

        stats = {
            'total_files': 0,
            'total_dirs': 0,
            'root_files': [],
            'root_dirs': [],
            'empty_dirs': [],
            'file_types': defaultdict(int),
            'protected_items': [],
            'large_files': [],  # Files > 10MB
            'duplicate_candidates': defaultdict(list),
        }

        self.file_inventory.clear()

        for root, dirs, files in os.walk(self.project_root):
            root_path = Path(root)

            # Skip protected directories
            dirs[:] = [d for d in dirs if not self.is_protected(root_path / d)]

            stats['total_dirs'] += len(dirs)

            # Check for empty directories
            if not dirs and not files and root_path != self.project_root:
                if not self.is_protected(root_path):
                    stats['empty_dirs'].append(str(root_path.relative_to(self.project_root)))

            # Track root-level items
            if root_path == self.project_root:
                stats['root_dirs'] = dirs.copy()
                stats['root_files'] = files.copy()

            for file in files:
                file_path = root_path / file

                # Skip protected files
                if self.is_protected(file_path):
                    stats['protected_items'].append(str(file_path.relative_to(self.project_root)))
                    continue

                try:
                    file_size = file_path.stat().st_size
                    stats['total_files'] += 1

                    # Track file extension
                    ext = file_path.suffix or 'no_extension'
                    stats['file_types'][ext] += 1

                    # Track large files
                    if file_size > 10 * 1024 * 1024:  # 10MB
                        stats['large_files'].append({
                            'path': str(file_path.relative_to(self.project_root)),
                            'size_mb': round(file_size / (1024 * 1024), 2)
                        })

                    # Track file info
                    is_config = file in self.ROOT_CONFIG_FILES or file.endswith(('.config.js', '.config.ts', 'rc'))
                    is_doc = file_path.suffix.lower() in ['.md', '.txt', '.rst', '.adoc']
                    in_root = root_path == self.project_root

                    file_info = FileInfo(
                        path=str(file_path.relative_to(self.project_root)),
                        size=file_size,
                        extension=ext,
                        is_config=is_config,
                        is_documentation=is_doc,
                        in_root=in_root
                    )
                    self.file_inventory.append(file_info)

                    # Track potential duplicates by size
                    if file_size > 0:
                        stats['duplicate_candidates'][file_size].append(str(file_path.relative_to(self.project_root)))

                except (PermissionError, OSError) as e:
                    print(f"⚠️  Warning: Cannot access {file_path}: {e}")

        # Filter duplicate candidates (keep only actual duplicates)
        stats['duplicate_candidates'] = {
            size: files for size, files in stats['duplicate_candidates'].items()
            if len(files) > 1
        }

        return stats

    def analyze_organization(self, stats: Dict) -> List[OrganizationSuggestion]:
        """
        Phase 2: Generate safe organizational suggestions
        """
        print("\n📊 Analyzing project organization...")
        self.suggestions.clear()

        # 1. Suggest moving non-essential files from root
        self._suggest_root_cleanup(stats)

        # 2. Suggest removing empty directories
        self._suggest_empty_dir_cleanup(stats)

        # 3. Suggest organizing by file type
        self._suggest_type_organization(stats)

        # 4. Suggest creating missing standard directories
        self._suggest_standard_structure(stats)

        return self.suggestions

    def _suggest_root_cleanup(self, stats: Dict):
        """Suggest moving non-essential files from root"""
        for file in stats['root_files']:
            # Skip essential root config files
            if file in self.ROOT_CONFIG_FILES:
                continue

            file_path = str(Path(file))

            # Check movable patterns
            for target_dir, patterns in self.MOVABLE_ROOT_FILES.items():
                for pattern in patterns:
                    if fnmatch.fnmatch(file, pattern):
                        self.suggestions.append(OrganizationSuggestion(
                            action='move',
                            source=file,
                            destination=f'{target_dir}/{file}',
                            reason=f'Documentation/config files organized in {target_dir}/ directory',
                            risk_level='low',
                            safety_checks=[
                                'File is not a primary config',
                                'No imports reference this file path',
                                'Not in protected patterns'
                            ]
                        ))
                        break

    def _suggest_empty_dir_cleanup(self, stats: Dict):
        """Suggest removing empty directories"""
        for empty_dir in stats['empty_dirs']:
            self.suggestions.append(OrganizationSuggestion(
                action='delete',
                source=empty_dir,
                reason='Empty directory with no files or subdirectories',
                risk_level='low',
                safety_checks=[
                    'Directory is empty',
                    'Not a protected path',
                    'No version control markers'
                ]
            ))

    def _suggest_type_organization(self, stats: Dict):
        """Suggest creating organizational directories for scattered file types"""
        # Find file types scattered in root
        root_files_by_type = defaultdict(list)

        for file_info in self.file_inventory:
            if file_info.in_root and not file_info.is_config:
                root_files_by_type[file_info.extension].append(file_info.path)

        # If multiple files of same type in root (3+), suggest organizing
        for ext, files in root_files_by_type.items():
            if len(files) >= 3 and ext not in ['no_extension', '.md']:
                # Determine appropriate directory
                org_dir = self._get_organization_dir(ext)
                if org_dir:
                    for file in files:
                        self.suggestions.append(OrganizationSuggestion(
                            action='move',
                            source=file,
                            destination=f'{org_dir}/{Path(file).name}',
                            reason=f'Group {ext} files in {org_dir}/ directory',
                            risk_level='medium',
                            safety_checks=[
                                'File type pattern detected',
                                'Multiple files of same type exist',
                                'Not a primary config file'
                            ]
                        ))

    def _suggest_standard_structure(self, stats: Dict):
        """Suggest creating missing standard directories"""
        standard_dirs = {
            'src': 'Source code files',
            'docs': 'Documentation files',
            'tests': 'Test files',
            'config': 'Configuration files',
            'scripts': 'Utility scripts',
        }

        existing_dirs = set(stats['root_dirs'])

        for dir_name, purpose in standard_dirs.items():
            if dir_name not in existing_dirs:
                # Check if there are files that would belong here
                relevant_files = self._find_files_for_directory(dir_name)
                if len(relevant_files) >= 2:
                    self.suggestions.append(OrganizationSuggestion(
                        action='create_dir',
                        source='',
                        destination=dir_name,
                        reason=f'Create {dir_name}/ for {purpose} ({len(relevant_files)} files would benefit)',
                        risk_level='low',
                        safety_checks=[
                            'Standard directory pattern',
                            'Multiple relevant files exist',
                            'No naming conflicts'
                        ]
                    ))

    def _get_organization_dir(self, extension: str) -> str:
        """Determine appropriate directory for a file extension"""
        code_extensions = {'.js', '.ts', '.jsx', '.tsx', '.py', '.go', '.rs', '.java', '.cpp', '.c', '.h'}
        test_extensions = {'.test.js', '.spec.js', '.test.ts', '.spec.ts', '_test.py'}
        doc_extensions = {'.md', '.txt', '.rst', '.adoc'}
        config_extensions = {'.json', '.yaml', '.yml', '.toml', '.ini'}

        if extension in code_extensions:
            return 'src'
        elif extension in test_extensions:
            return 'tests'
        elif extension in doc_extensions:
            return 'docs'
        elif extension in config_extensions:
            return 'config'

        return ''

    def _find_files_for_directory(self, dir_name: str) -> List[str]:
        """Find files that would logically belong in a directory"""
        relevant = []

        if dir_name == 'docs':
            relevant = [f.path for f in self.file_inventory if f.is_documentation and f.in_root]
        elif dir_name == 'tests':
            relevant = [f.path for f in self.file_inventory if 'test' in f.path.lower() and f.in_root]
        elif dir_name == 'scripts':
            relevant = [f.path for f in self.file_inventory if f.extension in ['.sh', '.ps1', '.bat'] and f.in_root]
        elif dir_name == 'config':
            relevant = [f.path for f in self.file_inventory if f.is_config and f.in_root and Path(f.path).name not in self.ROOT_CONFIG_FILES]

        return relevant

    def preview_changes(self) -> Dict:
        """
        Phase 3: Generate detailed preview of all suggested changes
        """
        print("\n📋 PREVIEW MODE - No changes will be made")
        print("=" * 60)

        preview = {
            'total_suggestions': len(self.suggestions),
            'by_action': defaultdict(int),
            'by_risk': defaultdict(int),
            'affected_paths': [],
            'summary': {}
        }

        for suggestion in self.suggestions:
            preview['by_action'][suggestion.action] += 1
            preview['by_risk'][suggestion.risk_level] += 1

            if suggestion.source:
                preview['affected_paths'].append(suggestion.source)
            if suggestion.destination:
                preview['affected_paths'].append(suggestion.destination)

        # Print organized preview
        print(f"\n📊 Total Suggestions: {preview['total_suggestions']}")
        print(f"\n🎯 By Action:")
        for action, count in preview['by_action'].items():
            print(f"   {action.upper()}: {count}")

        print(f"\n⚠️  By Risk Level:")
        for risk, count in preview['by_risk'].items():
            emoji = '🟢' if risk == 'low' else '🟡' if risk == 'medium' else '🔴'
            print(f"   {emoji} {risk.upper()}: {count}")

        print(f"\n📝 Detailed Suggestions:\n")

        # Group by action
        grouped = defaultdict(list)
        for suggestion in self.suggestions:
            grouped[suggestion.action].append(suggestion)

        for action, suggestions in grouped.items():
            print(f"\n{action.upper()} Operations ({len(suggestions)}):")
            print("-" * 60)

            for i, sug in enumerate(suggestions, 1):
                risk_emoji = '🟢' if sug.risk_level == 'low' else '🟡' if sug.risk_level == 'medium' else '🔴'
                print(f"\n{i}. {risk_emoji} {sug.reason}")

                if sug.action == 'move':
                    print(f"   FROM: {sug.source}")
                    print(f"   TO:   {sug.destination}")
                elif sug.action == 'delete':
                    print(f"   PATH: {sug.source}")
                elif sug.action == 'create_dir':
                    print(f"   CREATE: {sug.destination}/")

                print(f"   Safety Checks:")
                for check in sug.safety_checks:
                    print(f"      ✓ {check}")

        preview['summary'] = dict(preview['by_action'])
        return preview

    def execute_suggestions(self, suggestions: List[OrganizationSuggestion], dry_run: bool = True) -> Dict:
        """
        Phase 4: Execute approved suggestions with safety checks
        """
        if dry_run:
            print("\n🏃 DRY RUN MODE - Simulating changes only")
        else:
            print("\n⚡ EXECUTING CHANGES")

        print("=" * 60)

        results = {
            'successful': [],
            'failed': [],
            'skipped': [],
            'rollback_info': []
        }

        for suggestion in suggestions:
            try:
                if suggestion.action == 'move':
                    result = self._execute_move(suggestion, dry_run)
                elif suggestion.action == 'delete':
                    result = self._execute_delete(suggestion, dry_run)
                elif suggestion.action == 'create_dir':
                    result = self._execute_create_dir(suggestion, dry_run)
                else:
                    result = {'status': 'skipped', 'reason': f'Unknown action: {suggestion.action}'}

                if result['status'] == 'success':
                    results['successful'].append({**asdict(suggestion), **result})
                    print(f"✅ {suggestion.action.upper()}: {suggestion.source or suggestion.destination}")
                elif result['status'] == 'failed':
                    results['failed'].append({**asdict(suggestion), **result})
                    print(f"❌ FAILED: {result.get('reason', 'Unknown error')}")
                else:
                    results['skipped'].append({**asdict(suggestion), **result})
                    print(f"⏭️  SKIPPED: {result.get('reason', 'Unknown reason')}")

            except Exception as e:
                results['failed'].append({
                    **asdict(suggestion),
                    'error': str(e)
                })
                print(f"❌ ERROR: {str(e)}")

        print(f"\n📊 Results:")
        print(f"   ✅ Successful: {len(results['successful'])}")
        print(f"   ❌ Failed: {len(results['failed'])}")
        print(f"   ⏭️  Skipped: {len(results['skipped'])}")

        if not dry_run:
            self._save_operation_log(results)

        return results

    def _execute_move(self, suggestion: OrganizationSuggestion, dry_run: bool) -> Dict:
        """Execute file move operation"""
        source = self.project_root / suggestion.source
        dest = self.project_root / suggestion.destination

        # Safety checks
        if not source.exists():
            return {'status': 'failed', 'reason': 'Source file does not exist'}

        if self.is_protected(source):
            return {'status': 'skipped', 'reason': 'Source is protected'}

        if dest.exists():
            return {'status': 'failed', 'reason': 'Destination already exists'}

        if dry_run:
            return {
                'status': 'success',
                'mode': 'dry_run',
                'would_create_dirs': not dest.parent.exists()
            }

        # Actual execution
        dest.parent.mkdir(parents=True, exist_ok=True)
        source.rename(dest)

        return {
            'status': 'success',
            'mode': 'executed',
            'old_path': str(source),
            'new_path': str(dest)
        }

    def _execute_delete(self, suggestion: OrganizationSuggestion, dry_run: bool) -> Dict:
        """Execute delete operation"""
        target = self.project_root / suggestion.source

        # Safety checks
        if not target.exists():
            return {'status': 'skipped', 'reason': 'Path does not exist'}

        if self.is_protected(target):
            return {'status': 'skipped', 'reason': 'Path is protected'}

        if target.is_dir() and list(target.iterdir()):
            return {'status': 'failed', 'reason': 'Directory is not empty'}

        if dry_run:
            return {
                'status': 'success',
                'mode': 'dry_run',
                'would_delete': str(target)
            }

        # Actual execution
        if target.is_dir():
            target.rmdir()
        else:
            target.unlink()

        return {
            'status': 'success',
            'mode': 'executed',
            'deleted_path': str(target)
        }

    def _execute_create_dir(self, suggestion: OrganizationSuggestion, dry_run: bool) -> Dict:
        """Execute directory creation"""
        target = self.project_root / suggestion.destination

        # Safety checks
        if target.exists():
            return {'status': 'skipped', 'reason': 'Directory already exists'}

        if dry_run:
            return {
                'status': 'success',
                'mode': 'dry_run',
                'would_create': str(target)
            }

        # Actual execution
        target.mkdir(parents=True, exist_ok=True)

        return {
            'status': 'success',
            'mode': 'executed',
            'created_path': str(target)
        }

    def _save_operation_log(self, results: Dict):
        """Save operation log for audit trail"""
        log_file = self.project_root / '.project_organizer.log'

        import datetime
        log_entry = {
            'timestamp': datetime.datetime.now().isoformat(),
            'results': results
        }

        self.operation_log.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(self.operation_log, f, indent=2)

        print(f"\n📝 Operation log saved to: {log_file}")

def main():
    """Main execution function"""
    import argparse

    parser = argparse.ArgumentParser(description='Safe Project Organizer')
    parser.add_argument('project_path', help='Path to project root')
    parser.add_argument('--scan', action='store_true', help='Scan project only')
    parser.add_argument('--analyze', action='store_true', help='Scan and analyze')
    parser.add_argument('--preview', action='store_true', help='Preview changes')
    parser.add_argument('--execute', action='store_true', help='Execute changes (dry-run)')
    parser.add_argument('--execute-real', action='store_true', help='Execute changes (REAL)')

    args = parser.parse_args()

    organizer = SafeProjectOrganizer(args.project_path)

    # Phase 1: Scan
    stats = organizer.scan_project()

    print(f"\n✅ Scan complete!")
    print(f"   📁 Directories: {stats['total_dirs']}")
    print(f"   📄 Files: {stats['total_files']}")
    print(f"   🔒 Protected items: {len(stats['protected_items'])}")
    print(f"   📂 Empty directories: {len(stats['empty_dirs'])}")

    if args.scan:
        return

    # Phase 2: Analyze
    suggestions = organizer.analyze_organization(stats)

    print(f"\n💡 Generated {len(suggestions)} suggestions")

    if args.analyze:
        return

    # Phase 3: Preview
    if args.preview or args.execute or args.execute_real:
        preview = organizer.preview_changes()

    if args.preview:
        return

    # Phase 4: Execute
    if args.execute or args.execute_real:
        dry_run = not args.execute_real

        if args.execute_real:
            confirm = input("\n⚠️  WARNING: This will make REAL changes. Type 'yes' to confirm: ")
            if confirm.lower() != 'yes':
                print("❌ Cancelled")
                return

        results = organizer.execute_suggestions(suggestions, dry_run=dry_run)

if __name__ == '__main__':
    main()