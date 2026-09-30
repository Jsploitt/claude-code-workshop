#!/usr/bin/env bash
set -e
cd "$(dirname "$0")"
CLAUDE="$HOME/.local/bin/claude"
[ -x "$CLAUDE" ] || CLAUDE="claude"
"$CLAUDE" -p "/scout" --allowedTools "WebSearch,WebFetch,Read" --output-format json > last_run.json
python3 render.py last_run.json "$@"
