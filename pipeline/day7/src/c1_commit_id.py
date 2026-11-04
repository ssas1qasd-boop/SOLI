# Where does a commit ID like 84180e1 come from? Git hashes the file, then the folder, then the commit (SHA-1)
import hashlib


def git_hash(kind, data):
    header = (kind + " " + str(len(data)) + "\0").encode()
    return hashlib.sha1(header + data).hexdigest()


data = open("refactored.cpp", "rb").read()
blob = git_hash("blob", data)
print("blob   (the file)  :", blob)

entry = b"100644 refactored.cpp\0" + bytes.fromhex(blob)
tree = git_hash("tree", entry)
print("tree   (the folder):", tree)

who = "Student <student@example.com> 1793458800 +0200"
text = "tree " + tree + "\nauthor " + who + "\ncommitter " + who + "\n\nadd refactored polyline tool\n"
commit = git_hash("commit", text.encode())
print("commit             :", commit)
print("short ID           :", commit[:7])

data2 = data.replace(b"kPointSize = 10.0f", b"kPointSize = 12.0f")
print("one character changed -> new blob:", git_hash("blob", data2))
