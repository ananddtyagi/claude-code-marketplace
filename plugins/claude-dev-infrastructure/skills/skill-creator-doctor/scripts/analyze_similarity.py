#!/usr/bin/env python3
"""
Skill Similarity Analyzer - Fixed Version

Analyzes skill inventory to identify merge candidates, trigger conflicts,
and obsolete skills using multiple similarity detection methods.
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict
import math
import re

def jaccard_similarity(set1: Set[str], set2: Set[str]) -> float:
    """Calculate Jaccard similarity between two sets."""
    if not set1 and not set2:
        return 1.0
    if not set1 or not set2:
        return 0.0

    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))

    return intersection / union if union > 0 else 0.0

def normalize_text(text: str) -> str:
    """Normalize text for comparison."""
    if not text:
        return ""

    # Convert to lowercase, remove punctuation, normalize whitespace
    text = text.lower()
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()

def extract_words(text: str) -> Set[str]:
    """Extract meaningful words from text."""
    if not text:
        return set()

    # Simple stop words to filter out
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'up', 'about', 'into', 'through', 'during',
        'before', 'after', 'above', 'below', 'between', 'among', 'under', 'over',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had',
        'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
        'must', 'can', 'shall', 'this', 'that', 'these', 'those', 'i', 'you',
        'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them',
        'my', 'your', 'our', 'their'
    }

    words = normalize_text(text).split()
    return {word for word in words if len(word) >= 3 and word not in stop_words}

def content_similarity(skill1: Dict, skill2: Dict) -> float:
    """Calculate content similarity between two skills."""
    # Get text content for comparison
    text1_parts = []
    text2_parts = []

    # Frontmatter content
    front1 = skill1.get('frontmatter', {})
    front2 = skill2.get('frontmatter', {})

    # Compare names and descriptions
    text1_parts.append(front1.get('name', ''))
    text1_parts.append(front1.get('description', ''))
    text2_parts.append(front2.get('name', ''))
    text2_parts.append(front2.get('description', ''))

    # Combine text
    text1 = ' '.join(filter(None, text1_parts))
    text2 = ' '.join(filter(None, text2_parts))

    # Extract word sets
    words1 = extract_words(text1)
    words2 = extract_words(text2)

    # Calculate Jaccard similarity
    return jaccard_similarity(words1, words2)

def trigger_similarity(skill1: Dict, skill2: Dict, registry: Dict) -> Tuple[float, List[str]]:
    """Calculate trigger similarity and identify conflicts."""
    name1, name2 = skill1['name'], skill2['name']

    # Get triggers from registry
    reg1 = registry.get('skills', {}).get(name1, {})
    reg2 = registry.get('skills', {}).get(name2, {})

    triggers1 = reg1.get('triggers', [])
    triggers2 = reg2.get('triggers', [])

    # Normalize to lists
    if isinstance(triggers1, str):
        triggers1 = [triggers1]
    if isinstance(triggers2, str):
        triggers2 = [triggers2]

    # Convert to sets of normalized text
    set1 = {normalize_text(t) for t in triggers1 if t}
    set2 = {normalize_text(t) for t in triggers2 if t}

    # Calculate similarity
    similarity = jaccard_similarity(set1, set2)

    # Find exact conflicts
    conflicts = list(set1.intersection(set2))

    return similarity, conflicts

def keyword_similarity(skill1: Dict, skill2: Dict, registry: Dict) -> float:
    """Calculate keyword similarity."""
    name1, name2 = skill1['name'], skill2['name']

    # Get keywords from registry
    reg1 = registry.get('skills', {}).get(name1, {})
    reg2 = registry.get('skills', {}).get(name2, {})

    keywords1 = reg1.get('keywords', [])
    keywords2 = reg2.get('keywords', [])

    # Normalize to lists
    if isinstance(keywords1, str):
        keywords1 = [keywords1]
    if isinstance(keywords2, str):
        keywords2 = [keywords2]

    # Convert to sets of normalized text
    set1 = {normalize_text(k) for k in keywords1 if k}
    set2 = {normalize_text(k) for k in keywords2 if k}

    return jaccard_similarity(set1, set2)

def category_match(skill1: Dict, skill2: Dict, registry: Dict) -> bool:
    """Check if skills are in the same category."""
    name1, name2 = skill1['name'], skill2['name']

    reg1 = registry.get('skills', {}).get(name1, {})
    reg2 = registry.get('skills', {}).get(name2, {})

    cat1 = reg1.get('category', '')
    cat2 = reg2.get('category', '')

    return cat1 == cat2 and cat1 != ''

def usage_similarity(skill1: Dict, skill2: Dict, registry: Dict) -> float:
    """Calculate usage pattern similarity."""
    name1, name2 = skill1['name'], skill2['name']

    reg1 = registry.get('skills', {}).get(name1, {})
    reg2 = registry.get('skills', {}).get(name2, {})

    # Get usage stats
    act1 = reg1.get('activation_count', 0)
    act2 = reg2.get('activation_count', 0)

    # Similar if both unused or both used
    if act1 == 0 and act2 == 0:
        return 1.0
    if act1 == 0 or act2 == 0:
        return 0.0

    # Calculate similarity based on usage ratio
    max_usage = max(act1, act2)
    min_usage = min(act1, act2)

    if max_usage == 0:
        return 1.0

    return min_usage / max_usage

def calculate_overall_similarity(skill1: Dict, skill2: Dict, registry: Dict) -> Dict[str, Any]:
    """Calculate overall similarity using multiple methods."""
    content_sim = content_similarity(skill1, skill2)
    trigger_sim, trigger_conflicts = trigger_similarity(skill1, skill2, registry)
    keyword_sim = keyword_similarity(skill1, skill2, registry)
    category_match_score = 1.0 if category_match(skill1, skill2, registry) else 0.0
    usage_sim = usage_similarity(skill1, skill2, registry)

    # Weighted average
    overall_sim = (
        content_sim * 0.30 +           # Content similarity
        trigger_sim * 0.35 +           # Trigger similarity (high weight due to conflict potential)
        keyword_sim * 0.20 +           # Keyword similarity
        category_match_score * 0.10 +  # Category match
        usage_sim * 0.05               # Usage pattern similarity
    )

    return {
        'overall': overall_sim,
        'content': content_sim,
        'triggers': trigger_sim,
        'keywords': keyword_sim,
        'category_match': category_match_score,
        'usage': usage_sim,
        'trigger_conflicts': trigger_conflicts,
        'details': {
            'has_content': content_sim > 0.3,
            'has_trigger_overlap': trigger_sim > 0.1,
            'has_keyword_overlap': keyword_sim > 0.2,
            'same_category': category_match_score > 0,
            'similar_usage': usage_sim > 0.7
        }
    }

def find_obsolete_skills(skills: List[Dict], registry: Dict) -> List[Dict]:
    """Identify obsolete skills based on usage patterns."""
    obsolete = []
    now = datetime.now()

    for skill in skills:
        name = skill['name']
        reg_data = registry.get('skills', {}).get(name, {})

        activation_count = reg_data.get('activation_count', 0)
        last_used = reg_data.get('last_used')

        reasons = []

        # Never used
        if activation_count == 0:
            reasons.append("Never used (0 activations)")

        # Not used recently
        if last_used:
            try:
                last_used_date = datetime.fromisoformat(last_used.replace('Z', '+00:00'))
                days_since_use = (now - last_used_date).days

                if days_since_use > 180:  # 6 months
                    reasons.append(f"Not used in {days_since_use} days")
            except:
                reasons.append("Invalid last_used date")
        else:
            reasons.append("No last_used date")

        # Check for outdated technology references
        description = reg_data.get('description', '').lower()
        outdated_tech = ['mongodb', 'angularjs', 'jquery', 'internet explorer', 'flash']
        for tech in outdated_tech:
            if tech in description:
                reasons.append(f"References outdated technology: {tech}")
                break

        # Check for deprecated features
        if any(word in description for word in ['deprecated', 'legacy', 'old', 'removed']):
            reasons.append("References deprecated features or legacy functionality")

        if reasons:
            obsolete.append({
                'skill': skill,
                'name': name,
                'reasons': reasons,
                'activation_count': activation_count,
                'last_used': last_used,
                'urgency': 'high' if len(reasons) >= 2 else 'medium'
            })

    # Sort by urgency and activation count
    obsolete.sort(key=lambda x: (x['urgency'] == 'high', x['activation_count']))

    return obsolete

def get_skill_display_name(skill_name: str, registry: Dict) -> str:
    """Get display name with emoji for a skill."""
    skill_data = registry.get('skills', {}).get(skill_name, {})
    emoji = skill_data.get('emoji', '')
    display_name = skill_data.get('name', skill_name.replace('-', ' ').title())

    if emoji:
        return f"{emoji} {display_name}"
    return display_name

def generate_simple_report(inventory: Dict, threshold: float = 0.65) -> str:
    """Generate simplified markdown consolidation report."""
    skills = inventory['skills']
    registry = inventory['registry']

    # Calculate similarities
    similar_pairs = []
    print("Analyzing skill similarities...")

    for i, skill1 in enumerate(skills):
        for j, skill2 in enumerate(skills[i+1:], i+1):
            similarity = calculate_overall_similarity(skill1, skill2, registry)
            if similarity['overall'] >= threshold:
                similar_pairs.append((skill1['name'], skill2['name'], similarity))

    # Sort by similarity (highest first)
    similar_pairs.sort(key=lambda x: x[2]['overall'], reverse=True)

    # Find obsolete skills
    obsolete = find_obsolete_skills(skills, registry)

    # Find trigger conflicts
    trigger_conflicts = []
    for skill1_name, skill2_name, similarity in similar_pairs:
        if similarity['trigger_conflicts']:
            trigger_conflicts.append((skill1_name, skill2_name, similarity['trigger_conflicts']))

    # Generate simplified report
    report_lines = [
        "# Skill Consolidation Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        f"**Skills Analyzed:** {len(skills)}",
        f"**Similarity Threshold:** {threshold:.2f}",
        "",
        "## Executive Summary",
        "",
        f"- **High Similarity Pairs (≥80%):** {len([p for p in similar_pairs if p[2]['overall'] >= 0.80])}",
        f"- **Medium Similarity Pairs (65-80%):** {len([p for p in similar_pairs if 0.65 <= p[2]['overall'] < 0.80])}",
        f"- **Trigger Conflicts:** {len(trigger_conflicts)}",
        f"- **Obsolete Skills:** {len(obsolete)}",
        "",
        "## High Priority Merge Candidates (≥80% Similarity)",
        ""
    ]

    # High priority merges
    high_priority = [p for p in similar_pairs if p[2]['overall'] >= 0.80]
    if high_priority:
        for skill1, skill2, similarity in high_priority:
            skill1_display = get_skill_display_name(skill1, registry)
            skill2_display = get_skill_display_name(skill2, registry)

            report_lines.extend([
                f"### {skill1_display} + {skill2_display}",
                f"- **Overall Similarity:** {similarity['overall']:.1%}",
                f"- **Content Similarity:** {similarity['content']:.1%}",
                f"- **Trigger Overlap:** {similarity['triggers']:.1%}",
                f"- **Keyword Overlap:** {similarity['keywords']:.1%}",
                f"- **Same Category:** {'Yes' if similarity['category_match'] > 0 else 'No'}",
            ])

            if similarity['trigger_conflicts']:
                report_lines.append(f"- **⚠️ Trigger Conflicts:** {', '.join(similarity['trigger_conflicts'])}")

            primary_skill = skill1 if len(skill1) <= len(skill2) else skill2
            primary_display = get_skill_display_name(primary_skill, registry)
            report_lines.extend([
                f"- **Recommendation:** Merge into `{primary_display}`",
                ""
            ])
    else:
        report_lines.extend([
            "✅ **No high-priority merge candidates found.**",
            ""
        ])

    # Medium priority merges
    report_lines.extend([
        "## Medium Priority Candidates (65-80% Similarity)",
        ""
    ])

    medium_priority = [p for p in similar_pairs if 0.65 <= p[2]['overall'] < 0.80]
    if medium_priority:
        for skill1, skill2, similarity in medium_priority:
            skill1_display = get_skill_display_name(skill1, registry)
            skill2_display = get_skill_display_name(skill2, registry)

            report_lines.extend([
                f"### {skill1_display} + {skill2_display} (Review Recommended)",
                f"- **Overall Similarity:** {similarity['overall']:.1%}",
                f"- **Content Similarity:** {similarity['content']:.1%}",
                f"- **Trigger Overlap:** {similarity['triggers']:.1%}",
            ])

            if similarity['trigger_conflicts']:
                report_lines.append(f"- **⚠️ Trigger Conflicts:** {', '.join(similarity['trigger_conflicts'])}")

            report_lines.append("")
    else:
        report_lines.extend([
            "✅ **No medium-priority candidates found.**",
            ""
        ])

    # Trigger conflicts
    report_lines.extend([
        "## Trigger Conflicts",
        ""
    ])

    if trigger_conflicts:
        for skill1, skill2, conflicts in trigger_conflicts:
            report_lines.extend([
                f"### Conflict: \"{', '.join(conflicts)}\"",
                f"Between: {skill1} + {skill2}",
                "**Recommendation:** Update triggers to be more specific",
                ""
            ])
    else:
        report_lines.extend([
            "✅ **No trigger conflicts found.**",
            ""
        ])

    # Obsolete skills
    report_lines.extend([
        "## Obsolete Skills",
        ""
    ])

    if obsolete:
        for item in obsolete[:10]:  # Limit to first 10
            skill = item['skill']
            reasons_str = '; '.join(item['reasons'])
            urgency_emoji = "🔴" if item['urgency'] == 'high' else "🟡"

            # Get display name with emoji
            skill_display = get_skill_display_name(item['name'], registry)

            report_lines.extend([
                f"### {urgency_emoji} {skill_display}",
                f"- **Activations:** {item['activation_count']}",
                f"- **Last Used:** {item['last_used'] or 'Never'}",
                f"- **Reasons:** {reasons_str}",
                f"- **Recommendation:** Archive skill",
                ""
            ])
    else:
        report_lines.extend([
            "✅ **No obsolete skills identified.**",
            ""
        ])

    # Recommendations
    report_lines.extend([
        "## Consolidation Recommendations",
        "",
        "### Immediate Actions (High Priority)",
        "1. **Review high-priority merge candidates** (80%+ similarity)",
        "2. **Resolve trigger conflicts** to prevent ambiguous activation",
        "3. **Archive high-urgency obsolete skills** that have never been used",
        "",
        "### Natural Language Commands for Execution",
        "```",
        "# Merge high-priority candidates:",
        '"Merge skill-a and skill-b based on the consolidation report"',
        "",
        "# Archive obsolete skills:",
        '"Archive old-skill because it was never used"',
        "",
        "# Fix trigger conflicts:",
        '"Fix the trigger conflicts for [trigger text]"',
        "```",
        "",
        "---",
        f"*Report generated by skill similarity analyzer v1.0.0*"
    ])

    return '\n'.join(report_lines)

def main():
    parser = argparse.ArgumentParser(description='Analyze skill inventory for consolidation opportunities')
    parser.add_argument('--inventory', '-i', required=True, help='Skill inventory JSON file')
    parser.add_argument('--threshold', '-t', type=float, default=0.65,
                       help='Similarity threshold (default: 0.65)')
    parser.add_argument('--output', '-o', default='skill_consolidation_report.md',
                       help='Output report file (default: skill_consolidation_report.md)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')

    args = parser.parse_args()

    # Validate threshold
    if not 0.0 <= args.threshold <= 1.0:
        print("Error: Threshold must be between 0.0 and 1.0")
        sys.exit(1)

    # Load inventory
    try:
        with open(args.inventory, 'r', encoding='utf-8') as f:
            inventory = json.load(f)
    except Exception as e:
        print(f"Error loading inventory: {e}")
        sys.exit(1)

    print(f"Analyzing {len(inventory['skills'])} skills with threshold {args.threshold:.2f}")

    # Generate report
    report = generate_simple_report(inventory, args.threshold)

    # Save report
    try:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)

        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report)

        print(f"\n✅ Report saved to: {output_path}")

    except Exception as e:
        print(f"Error saving report: {e}")
        sys.exit(1)

    if args.verbose:
        print("\n📊 Analysis Summary:")
        skills = inventory['skills']
        similar_count = 0
        for i, s1 in enumerate(skills):
            for s2 in skills[i+1:]:
                similarity = calculate_overall_similarity(s1, s2, inventory['registry'])
                if similarity['overall'] >= args.threshold:
                    similar_count += 1

        print(f"   Similar skill pairs found: {similar_count}")
        obsolete_count = len(find_obsolete_skills(skills, inventory['registry']))
        print(f"   Obsolete skills identified: {obsolete_count}")

if __name__ == '__main__':
    main()