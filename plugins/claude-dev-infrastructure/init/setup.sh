#!/bin/bash

# Claude Dev Infrastructure Setup Script
# Usage: ./setup.sh /path/to/your/project [options]
#
# Options:
#   --all           Install all components (default)
#   --skills        Install only skills
#   --hooks         Install only hooks
#   --templates     Install only templates
#   --standards     Install only standards
#   --dev-manager   Install only dev-manager
#   --minimal       Install minimal set (templates + essential hooks)

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PLUGIN_DIR="$(dirname "$SCRIPT_DIR")"

# Parse arguments
TARGET_DIR=""
INSTALL_ALL=true
INSTALL_SKILLS=false
INSTALL_HOOKS=false
INSTALL_TEMPLATES=false
INSTALL_STANDARDS=false
INSTALL_DEV_MANAGER=false
INSTALL_MINIMAL=false

for arg in "$@"; do
  case $arg in
    --all)
      INSTALL_ALL=true
      ;;
    --skills)
      INSTALL_ALL=false
      INSTALL_SKILLS=true
      ;;
    --hooks)
      INSTALL_ALL=false
      INSTALL_HOOKS=true
      ;;
    --templates)
      INSTALL_ALL=false
      INSTALL_TEMPLATES=true
      ;;
    --standards)
      INSTALL_ALL=false
      INSTALL_STANDARDS=true
      ;;
    --dev-manager)
      INSTALL_ALL=false
      INSTALL_DEV_MANAGER=true
      ;;
    --minimal)
      INSTALL_ALL=false
      INSTALL_MINIMAL=true
      ;;
    -*)
      echo -e "${RED}Unknown option: $arg${NC}"
      exit 1
      ;;
    *)
      TARGET_DIR="$arg"
      ;;
  esac
done

# Validate target directory
if [ -z "$TARGET_DIR" ]; then
  echo -e "${RED}Error: Target directory required${NC}"
  echo "Usage: $0 /path/to/your/project [options]"
  exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
  echo -e "${YELLOW}Creating target directory: $TARGET_DIR${NC}"
  mkdir -p "$TARGET_DIR"
fi

# Convert to absolute path
TARGET_DIR="$(cd "$TARGET_DIR" && pwd)"

echo ""
echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║     Claude Dev Infrastructure - Setup Script           ║${NC}"
echo -e "${BLUE}╠════════════════════════════════════════════════════════╣${NC}"
echo -e "${BLUE}║  Plugin: ${PLUGIN_DIR}${NC}"
echo -e "${BLUE}║  Target: ${TARGET_DIR}${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Create .claude directory structure
mkdir -p "$TARGET_DIR/.claude/skills"
mkdir -p "$TARGET_DIR/.claude/hooks"
mkdir -p "$TARGET_DIR/.claude/locks"
mkdir -p "$TARGET_DIR/docs"

# Function to copy skills
install_skills() {
  echo -e "${GREEN}Installing skills...${NC}"

  if [ -d "$PLUGIN_DIR/skills" ]; then
    for skill_dir in "$PLUGIN_DIR/skills"/*; do
      if [ -d "$skill_dir" ]; then
        skill_name=$(basename "$skill_dir")
        echo "  - $skill_name"
        cp -r "$skill_dir" "$TARGET_DIR/.claude/skills/"
      fi
    done
    echo -e "${GREEN}  ✓ Skills installed${NC}"
  else
    echo -e "${YELLOW}  ! Skills directory not found${NC}"
  fi
}

# Function to copy hooks
install_hooks() {
  echo -e "${GREEN}Installing hooks...${NC}"

  if [ -d "$PLUGIN_DIR/hooks" ]; then
    for hook_file in "$PLUGIN_DIR/hooks"/*.sh; do
      if [ -f "$hook_file" ]; then
        hook_name=$(basename "$hook_file")
        echo "  - $hook_name"
        cp "$hook_file" "$TARGET_DIR/.claude/hooks/"
        chmod +x "$TARGET_DIR/.claude/hooks/$hook_name"
      fi
    done
    echo -e "${GREEN}  ✓ Hooks installed${NC}"
  else
    echo -e "${YELLOW}  ! Hooks directory not found${NC}"
  fi
}

# Function to copy templates
install_templates() {
  echo -e "${GREEN}Installing templates...${NC}"

  if [ -d "$PLUGIN_DIR/templates" ]; then
    # Create MASTER_PLAN.md if it doesn't exist
    if [ ! -f "$TARGET_DIR/docs/MASTER_PLAN.md" ]; then
      echo "  - Creating docs/MASTER_PLAN.md from template"
      PROJECT_NAME=$(basename "$TARGET_DIR")
      DATE=$(date +%Y-%m-%d)
      sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
          -e "s/{{DATE}}/$DATE/g" \
          -e "s/{{STATUS}}/Active Development/g" \
          "$PLUGIN_DIR/templates/MASTER_PLAN.template.md" > "$TARGET_DIR/docs/MASTER_PLAN.md"
    else
      echo "  - docs/MASTER_PLAN.md already exists, skipping"
    fi

    # Create CLAUDE.md if it doesn't exist
    if [ ! -f "$TARGET_DIR/CLAUDE.md" ]; then
      echo "  - Creating CLAUDE.md from template"
      PROJECT_NAME=$(basename "$TARGET_DIR")
      DATE=$(date +%Y-%m-%d)
      sed -e "s/{{PROJECT_NAME}}/$PROJECT_NAME/g" \
          -e "s/{{DATE}}/$DATE/g" \
          -e "s/{{PROJECT_DESCRIPTION}}/A project scaffolded with Claude Dev Infrastructure/g" \
          "$PLUGIN_DIR/templates/CLAUDE.template.md" > "$TARGET_DIR/CLAUDE.md"
    else
      echo "  - CLAUDE.md already exists, skipping"
    fi

    # Copy template files to .claude for reference
    mkdir -p "$TARGET_DIR/.claude/templates"
    cp "$PLUGIN_DIR/templates"/*.md "$TARGET_DIR/.claude/templates/" 2>/dev/null || true
    cp "$PLUGIN_DIR/templates"/*.json "$TARGET_DIR/.claude/templates/" 2>/dev/null || true

    echo -e "${GREEN}  ✓ Templates installed${NC}"
  else
    echo -e "${YELLOW}  ! Templates directory not found${NC}"
  fi
}

# Function to copy standards
install_standards() {
  echo -e "${GREEN}Installing standards...${NC}"

  if [ -d "$PLUGIN_DIR/standards" ]; then
    mkdir -p "$TARGET_DIR/.claude/standards"
    for std_file in "$PLUGIN_DIR/standards"/*.md; do
      if [ -f "$std_file" ]; then
        std_name=$(basename "$std_file")
        echo "  - $std_name"
        cp "$std_file" "$TARGET_DIR/.claude/standards/"
      fi
    done
    echo -e "${GREEN}  ✓ Standards installed${NC}"
  else
    echo -e "${YELLOW}  ! Standards directory not found${NC}"
  fi
}

# Function to setup dev-manager
install_dev_manager() {
  echo -e "${GREEN}Setting up dev-manager...${NC}"

  if [ -d "$PLUGIN_DIR/dev-manager" ]; then
    mkdir -p "$TARGET_DIR/dev-manager"
    cp -r "$PLUGIN_DIR/dev-manager"/* "$TARGET_DIR/dev-manager/"

    echo "  - Copied server files"
    echo "  - Run 'cd dev-manager && npm install && npm start' to use"
    echo -e "${GREEN}  ✓ Dev-manager installed${NC}"
  else
    echo -e "${YELLOW}  ! Dev-manager directory not found${NC}"
  fi
}

# Function for minimal install
install_minimal() {
  echo -e "${GREEN}Installing minimal set...${NC}"
  install_templates

  # Copy only essential hooks
  if [ -d "$PLUGIN_DIR/hooks" ]; then
    echo -e "${GREEN}Installing essential hooks...${NC}"
    for hook in task-lock-enforcer.sh session-lock-awareness.sh session-lock-release.sh; do
      if [ -f "$PLUGIN_DIR/hooks/$hook" ]; then
        echo "  - $hook"
        cp "$PLUGIN_DIR/hooks/$hook" "$TARGET_DIR/.claude/hooks/"
        chmod +x "$TARGET_DIR/.claude/hooks/$hook"
      fi
    done
  fi
}

# Execute installation based on options
if [ "$INSTALL_ALL" = true ]; then
  install_skills
  install_hooks
  install_templates
  install_standards
  install_dev_manager
elif [ "$INSTALL_MINIMAL" = true ]; then
  install_minimal
else
  [ "$INSTALL_SKILLS" = true ] && install_skills
  [ "$INSTALL_HOOKS" = true ] && install_hooks
  [ "$INSTALL_TEMPLATES" = true ] && install_templates
  [ "$INSTALL_STANDARDS" = true ] && install_standards
  [ "$INSTALL_DEV_MANAGER" = true ] && install_dev_manager
fi

# Create/update settings.json with hook configuration
echo -e "${GREEN}Updating .claude/settings.json...${NC}"

SETTINGS_FILE="$TARGET_DIR/.claude/settings.json"

if [ ! -f "$SETTINGS_FILE" ]; then
  cat > "$SETTINGS_FILE" << 'EOF'
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "command": ".claude/hooks/task-lock-enforcer.sh"
      }
    ],
    "SessionStart": [
      {
        "command": ".claude/hooks/session-lock-awareness.sh"
      }
    ],
    "SessionEnd": [
      {
        "command": ".claude/hooks/session-lock-release.sh"
      }
    ]
  }
}
EOF
  echo -e "${GREEN}  ✓ Created settings.json with hook configuration${NC}"
else
  echo -e "${YELLOW}  ! settings.json already exists, please add hooks manually${NC}"
fi

echo ""
echo -e "${GREEN}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║              Installation Complete!                     ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════════════════════╝${NC}"
echo ""
echo "Next steps:"
echo "  1. Review the generated files in $TARGET_DIR"
echo "  2. Customize CLAUDE.md for your project"
echo "  3. Update docs/MASTER_PLAN.md with your tasks"
echo "  4. Start dev-manager: cd dev-manager && npm install && npm start"
echo ""
echo -e "${BLUE}Happy coding with Claude Code!${NC}"
