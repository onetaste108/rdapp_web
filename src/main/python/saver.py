import numpy as np
from PIL import Image, PngImagePlugin
import os
import json
def tostr(frame):
    return "00000"[:-len(str(frame))]+str(frame)

def save_frame(img, dir, name, type, frame):
    os.makedirs(dir, exist_ok=True)
    ext = ".png"
    filename = os.path.join(dir, name+"_"+type+"_"+tostr(frame)+ext)
    Image.fromarray(img).save(filename, compress_level=6)
    # Image.fromarray(img).save(filename, optimize=True)
    print(filename)

def save_snap(img, dir, name, type, frame):
    os.makedirs(dir, exist_ok=True)
    ext = ".png"
    filename = os.path.join(dir, name+"_"+tostr(frame)+"_"+type+ext)
    Image.fromarray(img).save(filename, compress_level=6)
    # Image.fromarray(img).save(filename, optimize=True)
    print(filename)

def save_web(imgs, info, dir):
    os.makedirs(dir, exist_ok=True)
    name = "RDWEBtmp"
    idx = get_idx(dir, name)
    path = os.path.join(dir, name+"_"+tostr(idx))
    os.makedirs(path, exist_ok=True)
    for img in imgs:
        shape = img.shape[:2][::-1]
        imgname_d = os.path.join(path, "DEPTH_"+str(shape[0])+"x"+str(shape[1])+".png")
        Image.fromarray(img).save(imgname_d, compress_level=8)
        print(imgname_d)
    infoname = os.path.join(path, "CONFIG.json")
    with open(infoname, "w") as f:
        f.write(json.dumps(info, indent=4))
    print(infoname)

def get_frame(dir, name):
    os.makedirs(dir, exist_ok=True)
    ext = ".png"
    files = os.listdir(dir)
    files = [os.path.splitext(f) for f in files]
    files = [f[0] for f in files if f[1].lower() == ext]
    files = [f.split("_") for f in files]
    files = [f for f in files if f[0] == name]
    files = [f[-1] for f in files if len(f) > 0]
    maxf = -1
    for f in files:
        if f.isdecimal():
            fi = int(f)
            maxf = max(maxf, fi)
    frame = maxf + 1
    return frame

def get_idx(dir, name):
    os.makedirs(dir, exist_ok=True)
    files = os.listdir(dir)
    files = [os.path.splitext(f)[0] for f in files]
    files = [f.split("_") for f in files]
    files = [f for f in files if f[0] == name]
    files = [f[1] for f in files if len(f) > 1]
    maxf = -1
    for f in files:
        if f.isdecimal():
            fi = int(f)
            maxf = max(maxf, fi)
    frame = maxf + 1
    return frame

def split_bits(img):
    high = img // 256
    low = img - high * 256
    return np.stack((np.uint8(high), np.uint8(low)), axis=-1)

def pack(img):
  fix = 255.0/256.0
  img = np.concatenate((img*fix*1.0, np.mod(img*fix*255.0, 1.0), np.zeros_like(img)), axis=-1)
  return np.uint8(img*255.0)
