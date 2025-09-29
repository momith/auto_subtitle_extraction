#!/bin/bash
# usage: ./extract_subs.sh input.mkv

INPUT="$1"
DIRNAME="$(dirname "$INPUT")"
BASENAME="$(basename "$INPUT" .mkv)"

# list all subtitle streams with index, language and name
mapfile -t SUBS < <(ffprobe -v error -select_streams s \
  -show_entries stream=index:stream_tags=language,title \
  -of csv=p=0 "$INPUT")

if [ ${#SUBS[@]} -eq 0 ]; then
  echo "No subtitles found."
  exit 1
fi

for SUB in "${SUBS[@]}"; do
  IDX=$(echo "$SUB" | cut -d',' -f1)
  LANG=$(echo "$SUB" | cut -d',' -f2)
  TITLE=$(echo "$SUB" | cut -d',' -f3)

  # fallbacks in case fields are empty
  [ -z "$LANG" ] && LANG="und" # undetermined
  [ -z "$TITLE" ] && TITLE="track$IDX"

  OUTFILE="${DIRNAME}/${BASENAME}_${LANG}_${TITLE}.srt"

  echo "Extract stream $IDX ($LANG, $TITLE) -> $OUTFILE"

  ffmpeg -y -i "$INPUT" -map 0:$IDX -c:s srt "$OUTFILE"
done
