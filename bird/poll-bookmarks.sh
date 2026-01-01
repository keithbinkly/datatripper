#!/bin/bash
#
# Bookmark polling script for cron
#
# Add to crontab for continuous polling:
#   * * * * * /path/to/data-centered/bird/poll-bookmarks.sh
#
# Or run manually:
#   ./poll-bookmarks.sh
#   ./poll-bookmarks.sh --simple  # Use heuristic classifier (no LLM)
#

set -e

# Get script directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

# Change to project directory
cd "$PROJECT_DIR"

# Check if bird is installed
if ! command -v bird &> /dev/null; then
    echo "Error: bird CLI not found"
    echo "Install with: npm install -g @steipete/bird"
    exit 1
fi

# Check if bird is authenticated
if ! bird whoami &> /dev/null; then
    echo "Error: bird not authenticated"
    echo "Run: bird auth"
    exit 1
fi

# Parse arguments
EXTRA_ARGS=""
if [[ "$1" == "--simple" ]]; then
    EXTRA_ARGS="--simple"
fi

# Run the poll command
python -m bird.cli poll $EXTRA_ARGS

echo "Poll complete at $(date)"
