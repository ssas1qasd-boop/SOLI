import os
import subprocess
import tempfile

ENV = dict(os.environ, GIT_AUTHOR_NAME="Student", GIT_AUTHOR_EMAIL="student@example.com",
           GIT_COMMITTER_NAME="Student", GIT_COMMITTER_EMAIL="student@example.com",
           GIT_AUTHOR_DATE="2026-11-07T12:00:00", GIT_COMMITTER_DATE="2026-11-07T12:00:00")


def git(*args):
    result = subprocess.run(["git", *args], capture_output=True, text=True, env=ENV)
    return (result.stdout + result.stderr).strip()


def save(text):
    with open("site.css", "w") as f:
        f.write(text)


folder = tempfile.mkdtemp()
os.chdir(folder)
print(git("init", "-q", "-b", "main") or "git init: empty repository made")

save("body { color: blue; }\n")
print("status:", git("status", "--short"))
git("add", "site.css")
print("after add:", git("status", "--short"))
git("commit", "-q", "-m", "v1: blue")

for version, color in [("v2", "pink"), ("v3", "green"), ("v4", "orange")]:
    save("body { color: " + color + "; }\n")
    if version == "v2":
        print("changed, not added:", git("status", "--short"))
        print(git("diff", "--unified=0").splitlines()[-2:])
    git("commit", "-q", "-a", "-m", version + ": " + color)

print("log:")
print(git("log", "--oneline"))
first = git("rev-list", "--max-parents=0", "HEAD")
git("checkout", "-q", first, "--", "site.css")
print("client wants the original. site.css now:", open("site.css").read().strip())
print("files in the folder:", sorted(f for f in os.listdir(".") if f != ".git"))
