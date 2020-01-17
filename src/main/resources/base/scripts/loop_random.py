loop_length = int(input("Loop Length: "))
nloops = int(input("Num Loops: "))
from PySide2 import QtWidgets
imgdir = QtWidgets.QFileDialog.getExistingDirectory()
import os
files = os.listdir(imgdir)
olddir = controller.values["Ren Dir"]
for j, f in enumerate(files):
    for i in range(nloops):
        import numpy as np
        controller.set("Ren Dir", olddir+"/randloop"+str(j)+"_"+str(i))
        controller.rand()
        controller.set("Speed", 1/loop_length)
        controller.set("Tex Src", imgdir+"/"+f)
        controller.signal.signal.emit("Speed")
        freq = controller.values["Frequency"]
        controller.set("Spd", [1/freq[i]*(i+1) for i in range(8)])
        controller.set("Dir", [[np.random.randint(3)-1,np.random.randint(3)-1,np.random.randint(3)-1] for i in range(8)])
        controller.set("Ren Frames", int(loop_length * 30))
        controller.signal.signal.emit("Ren Frames")
        controller.update()
        controller.render()
