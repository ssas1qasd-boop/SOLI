# usage: python3 add.py "VIDEO_ID|channel|title" tid tid ...   (adds/overwrites the video for those topic ids)
import json, sys, os
f='/tmp/claude-0/yr/assign.json'
A=json.load(open(f)) if os.path.exists(f) else {}
vid, ch, ti = sys.argv[1].split('|', 2)
for t in sys.argv[2:]: A[t]={'id':vid,'channel':ch,'title':ti}
json.dump(A,open(f,'w'),ensure_ascii=False,indent=0); print(len(A))
