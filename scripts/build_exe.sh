#!/usr/bin/env bash
set -euo pipefail

python -m pip install -r requirements.txt
pyinstaller --clean --noconfirm study_nudge.spec

echo "Built executable at: dist/study_nudge"
