#!/bin/bash
# usage: run1.sh PID LAPS TITLE "callbacks" "clicks-json" srcfile...
PID=$1; LAPS=$2; TITLE=$3; CBS=$4; CLK=$5; shift 5
D=/home/claude/bench2/work/$PID; rm -rf $D; mkdir -p $D
for f in "$@"; do [ -d "$(dirname $f)/res" ] && cp -r "$(dirname $f)/res" $D/ ; done
CPPS=(); for f in "$@"; do case $f in *.cpp|*.c) CPPS+=("$f");; esac; done
CC=g++; ALLC=1; for f in "${CPPS[@]}"; do case $f in *.cpp) ALLC=0;; esac; done; [ $ALLC = 1 ] && CC=gcc
$CC -g3 -O0 "${CPPS[@]}" /home/claude/day1/full/glad.o -I/home/claude/day1/full/glad/include -lglfw -ldl -o $D/prog 2>$D/build.log || { cat $D/build.log; exit 1; }
SRCS=$(printf '"%s",' $(for f in "$@"; do readlink -f $f; done)); SRCS="[${SRCS%,}]"
CBJ=$(python3 -c "import json,sys;print(json.dumps([c for c in sys.argv[1].split(',') if c]))" "$CBS")
STDJ=""; [ -n "$STDIN_FILE" ] && STDJ=",\"stdin\":\"$STDIN_FILE\""
cat > $D/cfg.json <<J
{"out":"$D","srcs":$SRCS,"laps":$LAPS,"title":"$TITLE","callbacks":$CBJ,"clicks":$CLK$STDJ}
J
pgrep -x Xvfb >/dev/null || python3 -c "import subprocess;subprocess.Popen(['Xvfb',':84','-screen','0','1024x900x24'],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,start_new_session=True)"; sleep 1
cd $D && TRACE_CFG=$D/cfg.json timeout 600 gdb -q -batch -x /home/claude/bench2/gdbtrace.py --args ./prog 2>&1 | grep -v "^\[" | tail -5
