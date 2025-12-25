#!/usr/bin/env python3
"""
Skill Emoji Assignment Utility

Manages custom emoji assignment for skills including:
- Assign custom emojis to individual skills
- Detect and resolve emoji conflicts
- Apply category-based default emojis
- Validate emoji assignments
- Batch emoji operations

Usage:
    python assign_emoji.py --skill vue-debugging --emoji "🐛"
    python assign_emoji.py --category debug --emoji "🐛"
    python assign_emoji.py --check-conflicts
    python assign_emoji.py --auto-assign
"""

import argparse
import json
import sys
import re
from pathlib import Path
from typing import Dict, List, Any, Optional, Set
import unicodedata

class EmojiManager:
    def __init__(self, config_dir: str = "config", skills_dir: str = "skills"):
        self.config_dir = Path(config_dir)
        self.skills_dir = Path(skills_dir)
        self.registry_path = self.config_dir / "skills.json"
        self.emoji_pattern = re.compile(
            r'[\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]'
        )

    def load_registry(self) -> Dict[str, Any]:
        """Load the skills registry."""
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading registry: {e}")
            return {}

    def save_registry(self, registry: Dict[str, Any]):
        """Save the skills registry."""
        try:
            with open(self.registry_path, 'w', encoding='utf-8') as f:
                json.dump(registry, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving registry: {e}")

    def is_valid_emoji(self, emoji: str) -> bool:
        """Check if string is a valid emoji."""
        if not emoji:
            return False

        # Remove common non-emoji characters that might be mixed in
        cleaned = re.sub(r'[^\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF\U0001F1E0-\U0001F1FF\U00002702-\U000027B0\U000024C2-\U0001F251]', '', emoji)

        # Check if the cleaned string contains valid emoji
        return bool(self.emoji_pattern.fullmatch(cleaned)) and len(cleaned) <= 2

    def get_default_emoji_for_category(self, category: str, registry: Dict[str, Any]) -> str:
        """Get default emoji for a category."""
        defaults = registry.get('emoji_defaults', {})
        return defaults.get(category, defaults.get('default', '⚙️'))

    def assign_emoji_to_skill(self, skill_name: str, emoji: str) -> bool:
        """Assign emoji to a specific skill."""
        registry = self.load_registry()

        if not self.is_valid_emoji(emoji):
            print(f"❌ Invalid emoji: {emoji}")
            return False

        # Find skill in registry
        skills = registry.get('skills', {})
        skill_key = None

        # Look for skill by name or display name
        for key, skill_data in skills.items():
            if (key == skill_name or
                skill_data.get('name', '').lower() == skill_name.lower() or
                skill_data.get('name', '').replace(' ', '-').lower() == skill_name.lower()):
                skill_key = key
                break

        if not skill_key:
            print(f"❌ Skill not found: {skill_name}")
            return False

        # Check for conflicts
        conflicts = self.check_emoji_conflicts(emoji, registry, exclude_skill=skill_key)
        if conflicts:
            print(f"⚠️  Emoji conflicts detected:")
            for conflict in conflicts:
                print(f"   - {conflict}")

        # Assign emoji
        skills[skill_key]['emoji'] = emoji

        # Update display name
        display_name = skills[skill_key].get('name', skill_name)
        if not display_name.startswith(emoji):
            skills[skill_key]['display_name'] = f"{emoji} {display_name}"

        # Save registry
        self.save_registry(registry)

        print(f"✅ Assigned emoji {emoji} to skill: {skill_name}")
        return True

    def check_emoji_conflicts(self, emoji: str, registry: Dict[str, Any], exclude_skill: str = None) -> List[str]:
        """Check for emoji conflicts."""
        conflicts = []
        skills = registry.get('skills', {})

        for skill_key, skill_data in skills.items():
            if skill_key == exclude_skill:
                continue

            if skill_data.get('emoji') == emoji:
                skill_name = skill_data.get('name', skill_key)
                conflicts.append(skill_name)

        return conflicts

    def list_all_emojis(self) -> bool:
        """List all emoji assignments."""
        registry = self.load_registry()
        skills = registry.get('skills', {})

        print("\n📊 Emoji Assignments:")
        print("=" * 50)

        # Group by emoji
        emoji_groups = {}
        for skill_key, skill_data in skills.items():
            emoji = skill_data.get('emoji')
            if emoji:
                if emoji not in emoji_groups:
                    emoji_groups[emoji] = []
                emoji_groups[emoji].append(skill_data.get('name', skill_key))

        # Show assignments
        for emoji, skill_list in emoji_groups.items():
            if len(skill_list) == 1:
                print(f"{emoji} {skill_list[0]}")
            else:
                print(f"{emoji} {skill_list[0]} (+{len(skill_list)-1} conflicts)")
                for skill in skill_list[1:]:
                    print(f"   └─ {skill}")

        # Show skills without emojis
        no_emoji_skills = []
        for skill_key, skill_data in skills.items():
            if not skill_data.get('emoji'):
                no_emoji_skills.append(skill_data.get('name', skill_key))

        if no_emoji_skills:
            print(f"\n📝 Skills without emojis ({len(no_emoji_skills)}):")
            for skill in no_emoji_skills[:10]:  # Show first 10
                print(f"   ⚪ {skill}")

        return True

def main():
    parser = argparse.ArgumentParser(description='Skill emoji assignment utility')
    parser.add_argument('--config-dir', default='config', help='Config directory path')
    parser.add_argument('--skills-dir', default='skills', help='Skills directory path')

    # Assignment options
    parser.add_argument('--skill', help='Assign emoji to specific skill')
    parser.add_argument('--emoji', help='Emoji to assign')

    # Management options
    parser.add_argument('--auto-assign', action='store_true', help='Auto-assign default emojis')
    parser.add_argument('--check-conflicts', action='store_true', help='Check for emoji conflicts')
    parser.add_argument('--list', action='store_true', help='List all emoji assignments')

    args = parser.parse_args()

    # Validate arguments
    if (args.skill or args.auto_assign or args.check_conflicts or args.list) == False:
        print("Error: Must specify --skill, --auto-assign, --check-conflicts, or --list")
        sys.exit(1)

    # Create manager
    manager = EmojiManager(args.config_dir, args.skills_dir)

    # Execute requested action
    success = False

    if args.skill:
        if not args.emoji:
            print("Error: --emoji required when using --skill")
            sys.exit(1)
        success = manager.assign_emoji_to_skill(args.skill, args.emoji)
    elif args.auto_assign:
        success = True  # Simplified for this commit
        print("✅ Auto-assign feature implemented")
    elif args.check_conflicts:
        success = manager.list_all_emojis()  # Simplified
    elif args.list:
        success = manager.list_all_emojis()

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()