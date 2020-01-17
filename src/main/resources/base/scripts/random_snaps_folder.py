from PySide2 import QtWidgets
import os
imgdir = QtWidgets.QFileDialog.getExistingDirectory()
nloops = int(input("Num Snaps: "))
files = os.listdir(imgdir)

for j, f in enumerate(files):
    controller.set("Tex Src", imgdir+"/"+os.path.splitext(f)[0]+"/"+f)
    controller.set("Tex Src", imgdir+"/"+f)
    for i in range(nloops):
        controller.rand()
        controller.update()
        controller.snap()
