import os
def rename(dir, name):
    files = os.listdir(dir)
    count = len(files)
    print("{} files found.".format(count))
    def getnum(num):
        return "00000"[:-len(str(num))] + str(num)
    tempfiles = []
    for i, f in enumerate(files):
        ext = os.path.splitext(f)[-1]
        os.rename(os.path.join(dir, f), os.path.join(dir, "tempfile_"+getnum(i)+ext))
        tempfiles.append(os.path.join(dir, "tempfile_"+getnum(i)+ext))
    for i, f in enumerate(tempfiles):
        ext = os.path.splitext(f)[-1]
        os.rename(f, os.path.join(dir, name+"_"+getnum(i)+ext))
    return len(files)
cwd = os.getcwd()
SRC_NUM = rename(os.path.join(cwd, "src"), "SRC")
RDWEB_NUM = rename(os.path.join(cwd, "rdweb"), "RDWEB")
import json
with open(os.path.join(cwd, "config.txt"), "w") as f:
    f.write(json.dumps({
        "SRC_NUM": SRC_NUM,
        "RDWEB_NUM": RDWEB_NUM
    }))
print("Done")
