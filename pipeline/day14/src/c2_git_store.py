import hashlib
import os
import subprocess
import tempfile


def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True)
    return (result.stdout + result.stderr).strip()


content = b"body { color: blue; }\n"
header = b"blob " + str(len(content)).encode() + b"\0"
by_hand = hashlib.sha1(header + content).hexdigest()
print("content:", len(content), "bytes")
print("sha1 by hand :", by_hand)

folder = tempfile.mkdtemp()
os.chdir(folder)
git("init", "-q")
with open("a.css", "wb") as f:
    f.write(content)
print("git hash-object:", git("hash-object", "a.css"))

with open("copy_v2.css", "wb") as f:
    f.write(content)
with open("pink.css", "wb") as f:
    f.write(b"body { color: pink; }\n")
git("add", ".")
blobs = git("ls-files", "-s").splitlines()
for line in blobs:
    mode, sha, stage, name = line.split(maxsplit=3)
    print(name.ljust(12), sha[:7])
objects = [f for d in os.listdir(".git/objects") if len(d) == 2 for f in os.listdir(".git/objects/" + d)]
print("3 files, but", len(objects), "objects stored (same content = same hash = stored once)")
print("inside", by_hand[:7] + ":", git("cat-file", "-p", by_hand).strip())
