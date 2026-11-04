#!/bin/bash
# copy bench_days to the SOLI GitHub Pages repo, adding the page skeleton the claude.ai host normally adds
set -e
cd /home/claude/bench2
{ printf '%s\n' '<!doctype html><html lang="ar"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover"><style>:root{color-scheme:light;padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font:14px system-ui,sans-serif}img{max-width:100%}[hidden]{display:none!important}</style>'; cat bench_days.html; } > /home/claude/soli/bench/index.html
cp out_days/*.json out_days/maps_day*.html /home/claude/soli/bench/
cd /home/claude/soli && git add -A && git -c user.name="ssas1qasd-boop" -c user.email="noreply@anthropic.com" commit -qm "${1:-Update bench}

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_013kNpctVvWHKQmUD6uEjRyX" && git push 2>&1 | tail -1
