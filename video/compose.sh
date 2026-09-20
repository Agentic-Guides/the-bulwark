#!/bin/bash
# THE BULWARK — compose narration onto the PURE video track. mono-aware.
cd /c/Users/hohoh/Desktop/the-mast/video || exit 1
set -e
A="C:/Users/hohoh/Desktop/the-bulwark/video/audio"
V="out/bulwark-video-only.mp4"
O="out/the-bulwark-final.mp4"

FILES=( title problem attack demo_good demo_bad demo_ledger arch impact close )
DELAYS=( 0 12000 24000 36000 44000 55000 66000 86000 100000 )

INPUT_PARTS=""; for i in "${!FILES[@]}"; do INPUT_PARTS="$INPUT_PARTS -i $A/${FILES[i]}.mp3"; done

FILTER=""; MIX=""
for i in "${!FILES[@]}"; do
  d=${DELAYS[i]}
  FILTER="$FILTER [$i:a]adelay=${d}:all=1[a${i}];"
  MIX="$MIX[a${i}]"
done
FILTER="$FILTER ${MIX}amix=inputs=${#FILES[@]}:normalize=0[aout]"

# audio inputs first (0..8), video input LAST (index 9)
ffmpeg -y $INPUT_PARTS -i "$V" -filter_complex "$FILTER" \
  -map 9:v:0 -map "[aout]" -c:v copy -c:a aac -b:a 128k -shortest "$O" 2>&1 | tail -6
echo "MUX exit=$?"
