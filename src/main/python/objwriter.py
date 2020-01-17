def write(path, vertices, faces, attributes):
    import os
    dir, name = os.path.split(path)
    os.makedirs(dir, exist_ok = True)
    with open(path, "w") as file:
        for v in vertices:
            file.write("v {} {} {}\n".format(v[0], v[1], v[2]))
        for f in faces:
            file.write("f {} {} {}\n".format(f[0]+1, f[1]+1, f[2]+1))
        for key in attributes:
            val = attributes[key]
            for _val in val:
                txt = key
                for v in _val:
                    txt += " {}".format(v)
                file.write(txt+"\n")
