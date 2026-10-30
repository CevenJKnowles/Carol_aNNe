#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# A4 width in points (210mm). Each diagram becomes a single continuous page
# at this width, height scaled to fit the whole diagram - no pagination, so
# a PDF viewer scrolls through it instead of flipping pages.
A4_WIDTH_PT=595.2756

for INPUT in *.mmd; do
    BASE="${INPUT%.mmd}"
    RAW="$(mktemp --suffix=.pdf)"
    OUTPUT="${BASE}.pdf"

    npx -y @mermaid-js/mermaid-cli -i "$INPUT" -o "$RAW" -b white

    read -r W H < <(pdfinfo "$RAW" | grep "Page size" | sed -E 's/Page size:[[:space:]]+([0-9.]+) x ([0-9.]+) pts.*/\1 \2/')
    NEW_H=$(awk -v h="$H" -v w="$W" -v tw="$A4_WIDTH_PT" 'BEGIN{printf "%.4f", h*tw/w}')

    gs -q -o "$OUTPUT" -sDEVICE=pdfwrite \
       -dDEVICEWIDTHPOINTS="$A4_WIDTH_PT" -dDEVICEHEIGHTPOINTS="$NEW_H" \
       -dPDFFitPage -dFIXEDMEDIA "$RAW"

    rm -f "$RAW"
    echo "Rendered $OUTPUT (${A4_WIDTH_PT} x ${NEW_H} pt, 1 page)"
done
