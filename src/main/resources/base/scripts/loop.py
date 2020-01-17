loop_length = int(input("Loop Length: "))

import numpy as np

controller.set("Speed", 1/loop_length)
controller.signal.signal.emit("Speed")
freq = controller.values["Frequency"]
controller.set("Spd", [1/freq[i]*(i+1) for i in range(8)])
controller.set("Dir", [[np.random.randint(3)-1,np.random.randint(3)-1,np.random.randint(3)-1] for i in range(8)])
controller.set("Ren Frames", int(loop_length * 30))
controller.signal.signal.emit("Ren Frames")
