#!/bin/bash

# Script to validate all plugins using the built-in Claude Code plugin validator
# Usage: ./scripts/validate-all-plugins.sh [plugin_name]
# Examples:
#   ./scripts/validate-all-plugins.sh              # Validate all plugins
#   ./scripts/validate-all-plugins.sh my-plugin    # Validate specific plugin

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
PLUGINS_DIR="$REPO_ROOT/plugins"
SPECIFIC_PLUGIN="$1"

if [ -n "$SPECIFIC_PLUGIN" ]; then
    echo "========================================================"
    echo "Validating plugin: $SPECIFIC_PLUGIN"
    echo "========================================================"
else
    echo "========================================================"
    echo "Validating all plugins using 'claude plugin validate'"
    echo "========================================================"
fi
echo ""

# Check if claude command is available
if ! command -v claude &> /dev/null; then
    echo "❌ Error: 'claude' command not found"
    echo "Please install Claude Code first: https://docs.claude.com/claude-code"
    exit 1
fi

# If specific plugin provided, validate only that one
if [ -n "$SPECIFIC_PLUGIN" ]; then
    plugin_dir="$PLUGINS_DIR/$SPECIFIC_PLUGIN"

    if [ ! -d "$plugin_dir" ]; then
        echo "❌ Error: Plugin '$SPECIFIC_PLUGIN' not found in $PLUGINS_DIR"
        exit 1
    fi

    echo "Validating: $SPECIFIC_PLUGIN"
    echo "----------------------------------------"

    if claude plugin validate "$plugin_dir" 2>&1; then
        echo "✅ $SPECIFIC_PLUGIN - VALID"
        exit 0
    else
        echo "❌ $SPECIFIC_PLUGIN - INVALID"
        exit 1
    fi
fi

# Find all plugin directories
TOTAL_PLUGINS=0
VALID_PLUGINS=0
INVALID_PLUGINS=0
FAILED_PLUGINS=()

for plugin_dir in "$PLUGINS_DIR"/*; do
    if [ ! -d "$plugin_dir" ]; then
        continue
    fi

    plugin_name=$(basename "$plugin_dir")
    TOTAL_PLUGINS=$((TOTAL_PLUGINS + 1))

    echo "[$TOTAL_PLUGINS] Validating: $plugin_name"
    echo "----------------------------------------"

    # Run claude plugin validate
    if claude plugin validate "$plugin_dir" 2>&1; then
        echo "✅ $plugin_name - VALID"
        VALID_PLUGINS=$((VALID_PLUGINS + 1))
    else
        echo "❌ $plugin_name - INVALID"
        INVALID_PLUGINS=$((INVALID_PLUGINS + 1))
        FAILED_PLUGINS+=("$plugin_name")
    fi

    echo ""
done

echo "========================================================"
echo "VALIDATION SUMMARY"
echo "========================================================"
echo "Total plugins:   $TOTAL_PLUGINS"
echo "Valid:           $VALID_PLUGINS"
echo "Invalid:         $INVALID_PLUGINS"
echo ""

if [ $INVALID_PLUGINS -gt 0 ]; then
    echo "❌ Failed plugins:"
    for plugin in "${FAILED_PLUGINS[@]}"; do
        echo "  - $plugin"
    done
    echo ""
    exit 1
else
    echo "✅ All plugins are valid!"
    exit 0
fi
