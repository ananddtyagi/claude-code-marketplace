#!/usr/bin/env python3
"""
Skills Merge Tool

Safely merges two or more skills while preserving all unique functionality.
Handles frontmatter merging, capability consolidation, and trigger optimization.
"""

import os
import re
import json
import yaml
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime

@dataclass
class MergeConflict:
    field: str
    primary_value: str
    secondary_values: List[str]
    resolution_strategy: str
    recommended_value: str

class SkillsMerger:
    def __init__(self, dry_run: bool = False):
        self.dry_run = dry_run
        self.conflicts = []

    def load_skill_data(self, skill_file: Path) -> Dict:
        """Load and parse skill markdown file"""
        try:
            with open(skill_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Extract YAML frontmatter
            frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
            frontmatter = {}
            body_content = content

            if frontmatter_match:
                try:
                    frontmatter = yaml.safe_load(frontmatter_match.group(1)) or {}
                    body_content = content[frontmatter_match.end():].strip()
                except yaml.YAMLError as e:
                    print(f"⚠️  Warning: YAML parsing error in {skill_file}: {e}")

            return {
                'file_path': str(skill_file),
                'frontmatter': frontmatter,
                'body': body_content,
                'full_content': content
            }

        except (UnicodeDecodeError, FileNotFoundError) as e:
            print(f"❌ Error loading {skill_file}: {e}")
            return {}

    def merge_frontmatter(self, primary_frontmatter: Dict, secondary_frontmatters: List[Dict]) -> Tuple[Dict, List[MergeConflict]]:
        """Merge YAML frontmatter from multiple skills"""
        print("🔧 Merging frontmatter...")
        merged = {}
        conflicts = []

        # Start with primary frontmatter
        merged.update(primary_frontmatter)

        # Process secondary frontmatters
        for i, secondary in enumerate(secondary_frontmatters):
            for key, value in secondary.items():
                if key not in merged:
                    merged[key] = value
                elif key in merged and merged[key] != value:
                    # Conflict detected
                    conflict = MergeConflict(
                        field=key,
                        primary_value=str(merged[key]),
                        secondary_values=[str(value)],
                        resolution_strategy=self._determine_resolution_strategy(key, merged[key], value),
                        recommended_value=self._resolve_conflict(key, merged[key], value)
                    )
                    conflicts.append(conflict)
                    merged[key] = conflict.recommended_value

        return merged, conflicts

    def _determine_resolution_strategy(self, key: str, primary: any, secondary: any) -> str:
        """Determine how to resolve a specific conflict"""
        if key == 'description':
            return 'combine'  # Combine descriptions
        elif key == 'triggers':
            return 'merge_lists'  # Merge trigger lists
        elif key == 'capabilities':
            return 'merge_lists'  # Merge capability lists
        elif key in ['name', 'category']:
            return 'keep_primary'  # Keep primary value
        else:
            return 'manual_review'  # Requires manual review

    def _resolve_conflict(self, key: str, primary: any, secondary: any) -> str:
        """Resolve a specific conflict based on strategy"""
        strategy = self._determine_resolution_strategy(key, primary, secondary)

        if strategy == 'combine':
            # Combine descriptions
            return f"{primary} {secondary}"
        elif strategy == 'merge_lists':
            # Convert to lists and merge
            primary_list = primary if isinstance(primary, list) else [primary]
            secondary_list = secondary if isinstance(secondary, list) else [secondary]
            merged_list = list(set(primary_list + secondary_list))  # Remove duplicates
            return merged_list
        elif strategy == 'keep_primary':
            return primary
        else:
            # Default to primary with manual review note
            return str(primary)

    def merge_body_content(self, primary_body: str, secondary_bodies: List[str], skill_name: str) -> str:
        """Merge body content from multiple skills"""
        print("🔧 Merging body content...")

        # Parse sections from primary skill
        primary_sections = self._parse_sections(primary_body)

        # Collect unique sections from all skills
        all_sections = {}
        section_sources = {}  # Track which skill contributed each section

        # Add primary sections
        for section_name, section_content in primary_sections.items():
            all_sections[section_name] = section_content
            section_sources[section_name] = 'primary'

        # Add unique sections from secondary skills
        for i, secondary_body in enumerate(secondary_bodies):
            secondary_sections = self._parse_sections(secondary_body)
            for section_name, section_content in secondary_sections.items():
                if section_name not in all_sections:
                    all_sections[section_name] = section_content
                    section_sources[section_name] = f'secondary-{i+1}'
                else:
                    # Section exists in both - check if content is significantly different
                    if not self._sections_similar(all_sections[section_name], section_content):
                        # Create subsections for different content
                        new_section_name = f"{section_name} (from secondary skill {i+1})"
                        all_sections[new_section_name] = section_content
                        section_sources[new_section_name] = f'secondary-{i+1}'

        # Reconstruct merged body
        merged_body = self._reconstruct_body(all_sections, skill_name)

        return merged_body

    def _parse_sections(self, content: str) -> Dict[str, str]:
        """Parse markdown content into sections"""
        sections = {}

        # Split by markdown headers (##, ###, etc.)
        lines = content.split('\n')
        current_section = "Introduction"
        current_content = []

        for line in lines:
            # Check for section headers
            header_match = re.match(r'^(#{2,6})\s+(.+)$', line)
            if header_match:
                # Save previous section
                if current_content:
                    sections[current_section] = '\n'.join(current_content).strip()

                # Start new section
                current_section = header_match.group(2).strip()
                current_content = [line]
            else:
                current_content.append(line)

        # Save last section
        if current_content:
            sections[current_section] = '\n'.join(current_content).strip()

        return sections

    def _sections_similar(self, content1: str, content2: str, threshold: float = 0.8) -> bool:
        """Check if two sections are similar enough to be considered the same"""
        if not content1 or not content2:
            return False

        # Simple similarity check based on word overlap
        words1 = set(re.findall(r'\b\w+\b', content1.lower()))
        words2 = set(re.findall(r'\b\w+\b', content2.lower()))

        if not words1 or not words2:
            return content1.strip() == content2.strip()

        intersection = len(words1 & words2)
        union = len(words1 | words2)

        similarity = intersection / union if union > 0 else 0
        return similarity >= threshold

    def _reconstruct_body(self, sections: Dict[str, str], skill_name: str) -> str:
        """Reconstruct merged body from sections"""
        # Define preferred section order
        preferred_order = [
            "Overview",
            "Core Capabilities",
            "Capabilities",
            "Activation Triggers",
            "When to Use",
            "Usage Examples",
            "Quick Start",
            "Implementation",
            "Configuration",
            "Examples",
            "Resources",
            "Related Skills",
            "Notes"
        ]

        # Sort sections: preferred order first, then alphabetical
        sorted_sections = []
        processed = set()

        # Add sections in preferred order
        for section_name in preferred_order:
            if section_name in sections:
                sorted_sections.append((section_name, sections[section_name]))
                processed.add(section_name)

        # Add remaining sections alphabetically
        for section_name in sorted(sections.keys()):
            if section_name not in processed:
                sorted_sections.append((section_name, sections[section_name]))

        # Reconstruct content
        content_parts = []

        for section_name, section_content in sorted_sections:
            if section_content.strip():
                content_parts.append(f"## {section_name}")
                content_parts.append(section_content)
                content_parts.append("")  # Empty line between sections

        return '\n'.join(content_parts).strip()

    def merge_skills(self, primary_skill_file: Path, secondary_skill_files: List[Path], output_file: Optional[Path] = None) -> Dict:
        """Merge multiple skills into one"""
        print(f"🔀 Merging {len(secondary_skill_files) + 1} skills...")

        if self.dry_run:
            print("🔍 DRY RUN MODE - No files will be modified")

        # Load all skill data
        primary_data = self.load_skill_data(primary_skill_file)
        if not primary_data:
            return {'success': False, 'error': f'Failed to load primary skill: {primary_skill_file}'}

        secondary_data_list = []
        for secondary_file in secondary_skill_files:
            secondary_data = self.load_skill_data(secondary_file)
            if secondary_data:
                secondary_data_list.append(secondary_data)

        if not secondary_data_list:
            return {'success': False, 'error': 'No valid secondary skills found'}

        # Determine output file
        if not output_file:
            output_file = primary_skill_file

        # Merge frontmatter
        merged_frontmatter, frontmatter_conflicts = self.merge_frontmatter(
            primary_data['frontmatter'],
            [data['frontmatter'] for data in secondary_data_list]
        )

        # Update frontmatter with merge metadata
        merged_frontmatter['merged_from'] = [primary_skill_file.stem] + [Path(data['file_path']).stem for data in secondary_data_list]
        merged_frontmatter['merge_date'] = datetime.now().isoformat()
        merged_frontmatter['merge_type'] = 'consolidation'

        # Merge body content
        merged_body = self.merge_body_content(
            primary_data['body'],
            [data['body'] for data in secondary_data_list],
            merged_frontmatter.get('name', 'merged-skill')
        )

        # Construct complete merged content
        merged_content = self._construct_merged_content(merged_frontmatter, merged_body)

        # Add merge summary at the beginning
        merge_summary = self._generate_merge_summary(
            primary_skill_file, secondary_skill_files, frontmatter_conflicts
        )
        merged_content = f"{merge_summary}\n\n{merged_content}"

        # Validate merged content
        validation_result = self._validate_merged_skill(merged_content)
        if not validation_result['valid']:
            return {
                'success': False,
                'error': 'Merged skill validation failed',
                'validation_errors': validation_result['errors']
            }

        # Write merged content
        if not self.dry_run:
            try:
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(merged_content)
                print(f"✅ Merged skill written to: {output_file}")
            except Exception as e:
                return {'success': False, 'error': f'Failed to write merged skill: {e}'}
        else:
            print(f"🔍 Would write merged skill to: {output_file}")
            print(f"📊 Merged content length: {len(merged_content)} characters")

        return {
            'success': True,
            'output_file': str(output_file),
            'conflicts': [vars(conflict) for conflict in frontmatter_conflicts],
            'validation': validation_result,
            'dry_run': self.dry_run
        }

    def _construct_merged_content(self, frontmatter: Dict, body: str) -> str:
        """Construct complete merged content from frontmatter and body"""
        # Convert frontmatter to YAML
        frontmatter_yaml = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False)

        return f"---\n{frontmatter_yaml}---\n\n{body}"

    def _generate_merge_summary(self, primary_file: Path, secondary_files: List[Path], conflicts: List[MergeConflict]) -> str:
        """Generate a summary of the merge operation"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        summary_lines = [
            f"<!--",
            f"Skill Merge Summary",
            f"Generated: {timestamp}",
            f"",
            f"Primary skill: {primary_file.name}",
            f"Merged skills: {', '.join([f.name for f in secondary_files])}",
            f""
        ]

        if conflicts:
            summary_lines.extend([
                f"Conflicts resolved: {len(conflicts)}",
                ""
            ])
            for conflict in conflicts:
                summary_lines.append(f"- {conflict.field}: {conflict.resolution_strategy}")

        summary_lines.extend([
            f"",
            f"Total skills consolidated: {len(secondary_files) + 1}",
            f"-->"
        ])

        return '\n'.join(summary_lines)

    def _validate_merged_skill(self, content: str) -> Dict:
        """Validate the merged skill content"""
        errors = []

        # Check for YAML frontmatter
        if not content.startswith('---'):
            errors.append("Missing YAML frontmatter")
        else:
            # Check if frontmatter is valid YAML
            try:
                frontmatter_end = content.find('---', 3)
                if frontmatter_end == -1:
                    errors.append("Unclosed YAML frontmatter")
                else:
                    frontmatter_content = content[3:frontmatter_end]
                    yaml.safe_load(frontmatter_content)
            except yaml.YAMLError as e:
                errors.append(f"Invalid YAML frontmatter: {e}")

        # Check for required fields
        frontmatter_match = re.match(r'^---\n(.*?)\n---', content, re.DOTALL)
        if frontmatter_match:
            try:
                frontmatter = yaml.safe_load(frontmatter_match.group(1))
                required_fields = ['name', 'description']

                for field in required_fields:
                    if field not in frontmatter:
                        errors.append(f"Missing required field: {field}")

            except yaml.YAMLError:
                pass  # Already caught above

        # Check for basic markdown structure
        if '##' not in content:
            errors.append("No markdown sections found (no ## headers)")

        return {
            'valid': len(errors) == 0,
            'errors': errors
        }

def main():
    parser = argparse.ArgumentParser(description='Merge Claude Code skills')
    parser.add_argument('--primary', required=True, help='Primary skill file (keeps this name/metadata)')
    parser.add_argument('--secondary', nargs='+', required=True, help='Secondary skill files to merge')
    parser.add_argument('--output', help='Output file path (default: overwrite primary)')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be merged without writing files')
    parser.add_argument('--json-output', help='Output merge results to JSON file')

    args = parser.parse_args()

    # Convert file paths to Path objects
    primary_file = Path(args.primary)
    secondary_files = [Path(f) for f in args.secondary]
    output_file = Path(args.output) if args.output else None

    # Validate input files
    if not primary_file.exists():
        print(f"❌ Primary skill file not found: {primary_file}")
        return 1

    for sec_file in secondary_files:
        if not sec_file.exists():
            print(f"❌ Secondary skill file not found: {sec_file}")
            return 1

    # Create merger and run merge
    merger = SkillsMerger(dry_run=args.dry_run)
    result = merger.merge_skills(primary_file, secondary_files, output_file)

    # Output results
    if args.json_output:
        with open(args.json_output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"📊 Merge results written to: {args.json_output}")

    if result['success']:
        print("✅ Skill merge completed successfully")
        if result.get('conflicts'):
            print(f"⚠️  Resolved {len(result['conflicts'])} conflicts during merge")
        return 0
    else:
        print(f"❌ Skill merge failed: {result['error']}")
        if 'validation_errors' in result:
            for error in result['validation_errors']:
                print(f"  - {error}")
        return 1

if __name__ == "__main__":
    exit(main())