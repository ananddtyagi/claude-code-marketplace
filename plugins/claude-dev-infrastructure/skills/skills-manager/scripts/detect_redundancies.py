#!/usr/bin/env python3
"""
Skills Redundancy Detection Tool

Analyzes skills for overlaps, duplicates, and potential consolidation opportunities:
- Capability overlap analysis using semantic similarity
- Trigger conflict detection
- Merge candidate identification with confidence scoring
"""

import os
import re
import json
import math
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import defaultdict, Counter

@dataclass
class SkillOverlap:
    skill1: str
    skill2: str
    similarity: float
    shared_capabilities: List[str]
    unique_to_skill1: List[str]
    unique_to_skill2: List[str]
    recommendation: str
    confidence: float

@dataclass
class TriggerConflict:
    trigger: str
    conflicting_skills: List[str]
    conflict_type: str
    severity: str
    recommendation: str

@dataclass
class ConsolidationCandidate:
    skill_name: str
    action_type: str  # 'merge', 'archive', 'delete', 'keep'
    primary_skill: Optional[str]  # For merges
    merge_with: List[str]  # For merges
    reason: str
    confidence: float
    risk: str
    estimated_impact: str

class RedundancyDetector:
    def __init__(self, skills_data: Dict, config: Optional[Dict] = None):
        self.skills_data = skills_data
        self.config = config or self._default_config()
        self.stop_words = self._load_stop_words()

    def _default_config(self) -> Dict:
        return {
            'similarity_threshold': 0.7,
            'merge_threshold': 0.85,
            'archive_threshold': 0.3,
            'capability_weight': 0.4,
            'trigger_weight': 0.3,
            'description_weight': 0.3
        }

    def _load_stop_words(self) -> Set[str]:
        """Load common stop words for text analysis"""
        return {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
            'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have',
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
            'may', 'might', 'can', 'this', 'that', 'these', 'those', 'i', 'you',
            'he', 'she', 'it', 'we', 'they', 'what', 'which', 'who', 'when',
            'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
            'most', 'other', 'some', 'such', 'only', 'own', 'same', 'so', 'than',
            'too', 'very', 'just', 'now', 'use', 'used', 'using', 'skill',
            'skills', 'help', 'provides', 'enables', 'allows', 'supports'
        }

    def extract_keywords(self, text: str) -> Set[str]:
        """Extract meaningful keywords from text"""
        if not text:
            return set()

        # Convert to lowercase and extract words
        words = re.findall(r'\b[a-z]{3,}\b', text.lower())

        # Filter out stop words
        keywords = {word for word in words if word not in self.stop_words}

        return keywords

    def calculate_capability_overlap(self, skill1_data: Dict, skill2_data: Dict) -> Tuple[float, List[str], List[str], List[str]]:
        """Calculate capability overlap between two skills"""
        # Combine text sources
        skill1_text = f"{skill1_data.get('description', '')} {' '.join(skill1_data.get('capabilities', []))} {' '.join(skill1_data.get('triggers', []))}"
        skill2_text = f"{skill2_data.get('description', '')} {' '.join(skill2_data.get('capabilities', []))} {' '.join(skill2_data.get('triggers', []))}"

        # Extract keywords
        skill1_keywords = self.extract_keywords(skill1_text)
        skill2_keywords = self.extract_keywords(skill2_text)

        # Calculate Jaccard similarity
        if not skill1_keywords and not skill2_keywords:
            return 0.0, [], [], []

        intersection = skill1_keywords & skill2_keywords
        union = skill1_keywords | skill2_keywords

        similarity = len(intersection) / len(union) if union else 0.0

        # Find shared and unique capabilities
        skill1_caps = set(skill1_data.get('capabilities', []))
        skill2_caps = set(skill2_data.get('capabilities', []))

        shared_caps = list(skill1_caps & skill2_caps)
        unique1_caps = list(skill1_caps - skill2_caps)
        unique2_caps = list(skill2_caps - skill1_caps)

        return similarity, shared_caps, unique1_caps, unique2_caps

    def analyze_trigger_conflicts(self) -> List[TriggerConflict]:
        """Find skills with overlapping activation triggers"""
        print("🔍 Analyzing trigger conflicts...")

        trigger_map = defaultdict(list)
        conflicts = []

        for skill_name, skill_data in self.skills_data.items():
            triggers = skill_data.get('triggers', [])
            if isinstance(triggers, str):
                triggers = [triggers]

            for trigger in triggers:
                # Normalize trigger text for comparison
                normalized_trigger = self._normalize_trigger(trigger)
                if normalized_trigger:
                    trigger_map[normalized_trigger].append(skill_name)

        # Find conflicts
        for trigger, skills in trigger_map.items():
            if len(skills) > 1:
                # Determine severity based on number of conflicts
                severity = 'high' if len(skills) >= 3 else 'medium' if len(skills) == 2 else 'low'

                conflicts.append(TriggerConflict(
                    trigger=trigger,
                    conflicting_skills=skills,
                    conflict_type='exact_match',
                    severity=severity,
                    recommendation=self._generate_trigger_conflict_recommendation(skills, severity)
                ))

        print(f"  Found {len(conflicts)} trigger conflicts")
        return conflicts

    def _normalize_trigger(self, trigger: str) -> str:
        """Normalize trigger text for comparison"""
        if not trigger:
            return ""

        # Convert to lowercase and remove extra whitespace
        normalized = re.sub(r'\s+', ' ', trigger.lower().strip())

        # Remove common trigger prefixes/suffixes
        normalized = re.sub(r'^(when|if|for|to|use) ', '', normalized)
        normalized = re.sub(r' (needed|required|help)', '', normalized)

        return normalized

    def _generate_trigger_conflict_recommendation(self, skills: List[str], severity: str) -> str:
        """Generate recommendation for trigger conflicts"""
        if severity == 'high':
            return "High conflict - consider refining triggers to be more specific or merge skills"
        elif severity == 'medium':
            return "Medium conflict - review trigger specificity and skill differentiation"
        else:
            return "Low conflict - minor overlap, consider clarification"

    def detect_overlapping_skills(self) -> List[SkillOverlap]:
        """Find skills with high capability overlap"""
        print("🔍 Detecting overlapping skills...")

        overlaps = []
        skill_names = list(self.skills_data.keys())

        for i, skill1_name in enumerate(skill_names):
            for skill2_name in skill_names[i+1:]:
                skill1_data = self.skills_data[skill1_name]
                skill2_data = self.skills_data[skill2_name]

                similarity, shared_caps, unique1_caps, unique2_caps = self.calculate_capability_overlap(
                    skill1_data, skill2_data
                )

                if similarity >= self.config['similarity_threshold']:
                    # Determine recommendation and confidence
                    if similarity >= self.config['merge_threshold']:
                        recommendation = "Consider merging - very high overlap"
                        confidence = min(0.95, similarity + 0.1)
                    else:
                        recommendation = "Review for potential consolidation - high overlap"
                        confidence = similarity

                    overlaps.append(SkillOverlap(
                        skill1=skill1_name,
                        skill2=skill2_name,
                        similarity=similarity,
                        shared_capabilities=shared_caps,
                        unique_to_skill1=unique1_caps,
                        unique_to_skill2=unique2_caps,
                        recommendation=recommendation,
                        confidence=confidence
                    ))

        print(f"  Found {len(overlaps)} overlapping skill pairs")
        return overlaps

    def identify_consolidation_candidates(self, overlaps: List[SkillOverlap],
                                        usage_stats: Dict, necessity_scores: Dict) -> List[ConsolidationCandidate]:
        """Identify skills that are candidates for consolidation"""
        print("🔍 Identifying consolidation candidates...")

        candidates = []

        # Process overlapping skills for merges
        merge_groups = self._group_overlapping_skills(overlaps)

        for group in merge_groups:
            if len(group) >= 2:
                # Select primary skill (highest usage or necessity score)
                primary_skill = max(group, key=lambda s:
                    usage_stats.get(s, {}).get('uses_90_days', 0) +
                    necessity_scores.get(s, 0)
                )

                other_skills = [s for s in group if s != primary_skill]

                # Calculate confidence based on overlap and usage
                avg_overlap = sum(
                    o.similarity for o in overlaps
                    if (o.skill1 in group and o.skill2 in group)
                ) / len([o for o in overlaps if (o.skill1 in group and o.skill2 in group)])

                total_usage = sum(usage_stats.get(s, {}).get('uses_90_days', 0) for s in group)
                primary_usage = usage_stats.get(primary_skill, {}).get('uses_90_days', 0)

                confidence = avg_overlap
                if total_usage > 0:
                    confidence += (primary_usage / total_usage) * 0.2  # Boost if primary is most used

                risk = self._assess_merge_risk(primary_skill, other_skills, usage_stats)

                candidates.append(ConsolidationCandidate(
                    skill_name=primary_skill,
                    action_type='merge',
                    primary_skill=primary_skill,
                    merge_with=other_skills,
                    reason=f"High overlap ({avg_overlap:.1%}) with {len(other_skills)} other skills. {primary_skill} has highest usage.",
                    confidence=min(confidence, 0.95),
                    risk=risk,
                    estimated_impact=f"Combine {len(group)} skills into 1, reducing skill count by {len(group)-1}"
                ))

        # Identify archive candidates (low usage + low necessity)
        for skill_name, skill_data in self.skills_data.items():
            if skill_name in [c.skill_name for c in candidates]:  # Skip if already a merge candidate
                continue

            usage = usage_stats.get(skill_name, {})
            necessity = necessity_scores.get(skill_name, 0)

            # Archive criteria: no recent usage AND low necessity score
            if usage.get('uses_90_days', 0) == 0 and necessity < 30:
                candidates.append(ConsolidationCandidate(
                    skill_name=skill_name,
                    action_type='archive',
                    primary_skill=None,
                    merge_with=[],
                    reason=f"No recent usage and low necessity score ({necessity}/100).",
                    confidence=0.9,
                    risk='low',
                    estimated_impact="Move to archive - safe restoration possible"
                ))

        # Identify delete candidates (exact duplicates with very low usage)
        for overlap in overlaps:
            if overlap.similarity >= 0.95:  # Near-exact duplicates
                skill1_usage = usage_stats.get(overlap.skill1, {}).get('uses_90_days', 0)
                skill2_usage = usage_stats.get(overlap.skill2, {}).get('uses_90_days', 0)

                if max(skill1_usage, skill2_usage) <= 2:  # Both rarely used
                    # Delete the less used one
                    to_delete = overlap.skill1 if skill1_usage < skill2_usage else overlap.skill2

                    candidates.append(ConsolidationCandidate(
                        skill_name=to_delete,
                        action_type='delete',
                        primary_skill=None,
                        merge_with=[],
                        reason=f"Exact duplicate of another skill with minimal usage.",
                        confidence=0.95,
                        risk='low',
                        estimated_impact="Remove duplicate skill"
                    ))

        print(f"  Identified {len(candidates)} consolidation candidates")
        return candidates

    def _group_overlapping_skills(self, overlaps: List[SkillOverlap]) -> List[List[str]]:
        """Group overlapping skills into merge candidates"""
        # Simple clustering based on overlap threshold
        groups = []
        processed = set()

        for overlap in overlaps:
            if overlap.skill1 in processed or overlap.skill2 in processed:
                continue

            # Start new group
            group = {overlap.skill1, overlap.skill2}
            processed.update(group)

            # Find connected skills
            changed = True
            while changed:
                changed = False
                for other_overlap in overlaps:
                    if (other_overlap.skill1 in group or other_overlap.skill2 in group) and \
                       other_overlap.skill1 not in processed and other_overlap.skill2 not in processed:
                        group.add(other_overlap.skill1)
                        group.add(other_overlap.skill2)
                        processed.add(other_overlap.skill1)
                        processed.add(other_overlap.skill2)
                        changed = True

            if len(group) >= 2:
                groups.append(list(group))

        return groups

    def _assess_merge_risk(self, primary_skill: str, other_skills: List[str], usage_stats: Dict) -> str:
        """Assess the risk level of merging skills"""
        primary_usage = usage_stats.get(primary_skill, {}).get('uses_90_days', 0)
        other_usage = sum(usage_stats.get(s, {}).get('uses_90_days', 0) for s in other_skills)

        # Risk factors
        if primary_usage == 0 and other_usage == 0:
            return 'low'  # Neither skill is used
        elif primary_usage > other_usage * 3:
            return 'low'  # Primary skill is clearly dominant
        elif primary_usage < 5 and other_usage < 5:
            return 'medium'  # Both skills rarely used
        else:
            return 'medium'  # Both have some usage

    def run_redundancy_analysis(self) -> Dict:
        """Run complete redundancy analysis"""
        print("🔍 Running redundancy detection analysis...")

        # Extract usage stats and necessity scores from skills data
        usage_stats = self.skills_data.get('usage_stats', {})
        necessity_scores = self.skills_data.get('necessity_scores', {})

        # Convert skills_inventory.skills to simple dict format for processing
        skills_simple = {}
        for name, skill_data in self.skills_data.get('skills_inventory', {}).get('skills', {}).items():
            skills_simple[name] = skill_data

        # Analyze overlaps
        overlaps = self.detect_overlapping_skills()

        # Analyze trigger conflicts
        trigger_conflicts = self.analyze_trigger_conflicts()

        # Identify consolidation candidates
        candidates = self.identify_consolidation_candidates(overlaps, usage_stats, necessity_scores)

        # Generate summary
        summary = {
            'total_skills': len(skills_simple),
            'overlap_pairs': len(overlaps),
            'trigger_conflicts': len(trigger_conflicts),
            'consolidation_candidates': len(candidates),
            'merge_candidates': len([c for c in candidates if c.action_type == 'merge']),
            'archive_candidates': len([c for c in candidates if c.action_type == 'archive']),
            'delete_candidates': len([c for c in candidates if c.action_type == 'delete'])
        }

        print(f"\n=== Redundancy Analysis Summary ===")
        print(f"Total skills analyzed: {summary['total_skills']}")
        print(f"Overlapping skill pairs: {summary['overlap_pairs']}")
        print(f"Trigger conflicts: {summary['trigger_conflicts']}")
        print(f"Consolidation candidates: {summary['consolidation_candidates']}")
        print(f"  - Merge candidates: {summary['merge_candidates']}")
        print(f"  - Archive candidates: {summary['archive_candidates']}")
        print(f"  - Delete candidates: {summary['delete_candidates']}")

        return {
            'overlapping_skills': [asdict(overlap) for overlap in overlaps],
            'trigger_conflicts': [asdict(conflict) for conflict in trigger_conflicts],
            'consolidation_candidates': [asdict(candidate) for candidate in candidates],
            'summary': summary,
            'config_used': self.config
        }

def main():
    import argparse

    parser = argparse.ArgumentParser(description='Detect skill redundancies')
    parser.add_argument('--skills-data', required=True, help='Path to skills analysis JSON file')
    parser.add_argument('--output', help='Output JSON file path')
    parser.add_argument('--pretty', action='store_true', help='Pretty print JSON output')
    parser.add_argument('--similarity-threshold', type=float, default=0.7, help='Similarity threshold for overlap detection')
    parser.add_argument('--merge-threshold', type=float, default=0.85, help='Similarity threshold for merge recommendations')

    args = parser.parse_args()

    # Load skills data
    with open(args.skills_data, 'r', encoding='utf-8') as f:
        skills_data = json.load(f)

    # Configure detector
    config = {
        'similarity_threshold': args.similarity_threshold,
        'merge_threshold': args.merge_threshold
    }

    detector = RedundancyDetector(skills_data, config)
    result = detector.run_redundancy_analysis()

    if args.output:
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(result, f, indent=2 if args.pretty else None, ensure_ascii=False)
        print(f"\n✅ Results saved to: {args.output}")
    else:
        print("\n" + "="*50)
        print("REDUNDANCY ANALYSIS RESULTS")
        print("="*50)
        print(json.dumps(result, indent=2 if args.pretty else None, ensure_ascii=False))

if __name__ == "__main__":
    main()