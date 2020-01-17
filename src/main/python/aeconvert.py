def convert(path):
    import numpy as np
    keys = open(path, "r").read()
    keys = keys.split("\n")
    keys = keys[10:-4]
    keys = [float(k.split("\t")[-2]) for k in keys]
    keys = np.float32(keys)
    return keys