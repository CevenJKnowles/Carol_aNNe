#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Per-diagram render scale (Puppeteer scale factor -> higher-res PNG at the
# same layout/proportions). Default 1; override here for diagrams that need
# to be readable at a larger display size.
declare -A SCALE_OVERRIDES=(
    ["DOC-ARCH-003-cnn-training-pipeline-step-by-step"]=2
)

for INPUT in *.mmd; do
    BASE="${INPUT%.mmd}"
    OUTPUT="${BASE}.png"
    SCALE="${SCALE_OVERRIDES[$BASE]:-1}"
    npx -y @mermaid-js/mermaid-cli -i "$INPUT" -o "$OUTPUT" -b white -s "$SCALE"
    echo "Rendered $OUTPUT (scale=$SCALE)"
done
