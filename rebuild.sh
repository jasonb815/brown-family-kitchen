#!/usr/bin/env bash
# Manual rebuild helper for The Brown Family Kitchen site.
# Not automated on purpose -- Jason rebuilds by hand for now.
# Usage: ./rebuild.sh
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")"

git pull
source .venv/bin/activate
python3 scripts/generate_browse_pages.py
mkdocs build
