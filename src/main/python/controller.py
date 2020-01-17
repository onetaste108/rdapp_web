from camera import Camera
import json
import numpy as np
import os
from saver import save_frame, get_frame, pack, save_web, get_idx, save_snap
import mcubes

# default = {
#     "Tex Src": None,

#     "Max Depth": 10,
#     "Stop Distance": 0.01,
#     "Time": 0,
#     "FOV": 2,
#     "Camera": (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -3.0, 1.0),
#     "Tex Mat": (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0),
#     "Camera Crop": 0.0,
#     "Camera Mode": 0,
#     "Texture Pos": (1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0),
#     "Octaves": 4,
#     "Amplitude": [0.6 for i in range(16)],
#     "Amplitude Value": 0.5,
#     "Amplitude Decay": -1,
#     "Amplitude Rand": 0,
#     "Amplitude Seed": 0,
#     "Frequency": [0.4 for i in range(16)],
#     "Frequency Value": 0.4,
#     "Frequency Decay": 1,
#     "Frequency Rand": 0,
#     "Frequency Seed": 0,
#     "Pos": [[0, 0, 0] for i in range(16)],
#     "Pos Rand": 1,
#     "Off": [[0, 0, 0] for i in range(16)],
#     "Off Seed": 0,
#     "Dir": [[0, 0, 0] for i in range(16)],
#     "Dir Seed": 0,
#     "Spd": [[0, 0, 0] for i in range(16)],
#     "Spd Seed": 0,

#     "Bump": 0,
#     "Bump Off": (0, 0, 0),
#     "Bump Off Value": (0, 0, 0),
#     "Bump Val": (0, 0, 0),
#     "Bump Val Value": (0, 0, 0),
#     "Bump Rand": 1,
#     "Bump Seed": 0,
#     "Speed": 0.1,
#     "Speed Random": 0,
#     "Offset Random": 0,
#     "Seed Random": 0,
#     "Mirror": False,
#     "Shape": 0,
#     "Material": 0,
#     "Tex Scale": 2,
#     "Material Value": 0,
#     "Material Seed": 0,
#     "Material Mix": (0, 0, 0),
#     "Refl": 0,
#     "Refl Metallic": 0,
#     "Refl Threshold": 0,
#     "Refl Border": 0.1,

#     "Diff Size": 10,
#     "Diff Blur": 8,
#     "Diff Blur Default": 16,
#     "Diff Blur K": 0,
#     "Diff Blur Radio": True,
#     "Refl Blur Radio": False,
#     "Refl Blur Default": 16,
#     "Refl Size": 4,
#     "Refl Blur": 2,
#     "Refl Blur K": 0,

#     "Prev Max Step": 1024,
#     "Prev Step Scale": 0.05,

#     "Rend Max Step": 1024*16,
#     "Rend Step Scale": 0.0005,

#     "Scan Size": 5.0,
#     "Rend Size": (1024, 1024),
#     "Web Sizes": [(1920*2, 1080*2), (1280*2, 720*2), (800*2, 600*2)],
#     "Rend Bounds": True,
#     "Rend AA": 1,
#     "Ren Frames": 1,
#     "Rend Max Patch": (1024, 1024),

#     "Snap Dir": "data/out/snaps/bin",
#     "Ren Dir": "data/out/render/bin",
#     "Web Dir": "data/out/web/bin",
#     "Mesh Dir": "data/out/mesh/bin",
#     "Rend Depth": True,
#     "Rend Normals": True,
#     "Rend Beauty": True,
#     "Rend UV": False,
#     "Rend Info": True,

#     "Camera Movement": (0, 0, 0),
#     "Tex Movement": (0, 0, 0),

#     "Video Play": False,
#     "Video Frame": 0,

#     "Random Cam": True
# }

valueConfig = {
    "Tex Src": {
        "domain": "tex"
    },



    "Min Depth": {
        "domain": "shader",
        "_name": "u_min_depth",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.01
    },
    "Max Depth": {
        "domain": "shader",
        "_name": "u_max_depth",
        "dtype": "float",
        "min": 0,
        "max": 20,
        "step": 0.01
    },
    "Stop Distance": {
        "domain": "shader",
        "_name": "u_stop_dist",
        "dtype": "float",
        "min": 0,
        "max": 20,
        "step": 0.01
    },
    "Time": {
        "domain": "",
        "_name": "u_time",
        "dtype": "float",
        "min": 0,
        "max": 60,
        "step": 0.01
    },
    "FOV": {
        "domain": "shader",
        "_name": "u_cam_fov",
        "dtype": "float",
        "min": 0,
        "max": 5,
        "step": 0.01
    },
    "Camera": {
        "domain": "shader",
        "_name": "u_cam_mat"
    },
    "Camera Mode": {
        "domain": "shader",
        "_name": "u_cam_mode",
        "dtype": "combo",
        "map": ["Perspective", "Parallel"]
    },
    "Tex Mat": {
        "domain": "shader",
        "_name": "u_tex_mat"
    },
    "Camera Crop": {
        "domain": "shader",
        "_name": "u_cam_crop",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.0001
    },
    "Texture Pos": {
        "domain": "shader",
        "_name": "u_tex_mat"
    },
    "Iterations": {
        "domain": "shader",
        "_name": "u_it",
        "dtype": "float",
        "min": 0,
        "max": 8,
        "step": 1
    },


    "Octaves": {
        "domain": "shader",
        "_name": "u_octaves",
        "dtype": "float",
        "min": 1,
        "max": 8,
        "step": 1
    },


    "Amplitude": {
        "domain": "shader",
        "_name": "u_amp"
    },
    "Amplitude Value": {
        "domain": "amp",
        "dtype": "float",
        "min": 0,
        "max": 1.5,
        "step": 0.0001
    },
    "Amplitude Decay": {
        "domain": "amp",
        "dtype": "float",
        "min": -2,
        "max": 0,
        "step": 0.0001
    },
    "Amplitude Rand": {
        "domain": "amp",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Amplitude Seed": {
        "domain": "amp"
    },


    "Frequency": {
        "domain": "shader",
        "_name": "u_freq"
    },
    "Frequency Value": {
        "domain": "freq",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.0001
    },
    "Frequency Decay": {
        "domain": "freq",
        "dtype": "float",
        "min": 0,
        "max": 1.5,
        "step": 0.0001
    },
    "Frequency Rand": {
        "domain": "freq",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Frequency Seed": {
        "domain": "freq"
    },


    "Off": {
        "domain": ""
    },
    "Off Seed": {
        "domain": "off"
    },
    "Spd": {
        "domain": ""
    },
    "Spd Seed": {
        "domain": "spd"
    },
    "Dir": {
        "domain": ""
    },
    "Dir Seed": {
        "domain": "dir"
    },
    "Pos Rand": {
        "domain": "pos",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Pos": {
        "domain": "shader",
        "_name": "u_pos"
    },


    "Bump": {
        "domain": "shader",
        "_name": "u_bump",
        "dtype": "float",
        "min": 0,
        "max": 2,
        "step": 0.0001
    },
    "Bump Val": {
        "domain": "shader",
        "_name": "u_bump_val"
    },
    "Bump Val Value": {
        "domain": "bump",
        "dtype": "vec3",
        "min": -1,
        "max": 1,
        "step": 0.001
    },
    "Bump Off": {
        "domain": "shader",
        "_name": "u_bump_off"
    },
    "Bump Off Value": {
        "domain": "bump",
        "dtype": "vec3",
        "min": -0.5,
        "max": 0.5,
        "step": 0.001
    },
    "Bump Rand": {
        "domain": "bump",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Bump Seed": {
        "domain": "bump"
    },
    "Speed": {
        "domain": "shader",
        "_name": "u_speed",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Speed Random": {
        "domain": "shader",
        "_name": "u_speed_rand"
    },
    "Offset Random": {
        "domain": "shader",
        "_name": "u_rand_strength",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Seed Random": {
        "domain": "shader",
        "_name": "u_seed",
        "dtype": "float",
        "min": 0,
        "max": 1000,
        "step": 1
    },
    "Mirror": {
        "domain": "shader",
        "_name": "u_mirror",
        "dtype": "bool"
    },
    "Shape": {
        "domain": "shader",
        "_name": "u_shape",
        "dtype": "combo",
        "map": ["Inner Sphere", "Outer Sphere", "Combined Sphere", "Drop Sphere", "Plane"]
    },
    "Tex Scale": {
        "domain": "shader",
        "_name": "u_tex_scale",
        "dtype": "float",
        "min": 1,
        "max": 10,
        "step": 1
    },
    "Material": {
        "domain": "material",
        "dtype": "combo",
        "map": ["Plain", "Shiny", "Metallic", "Mixed"]
    },
    "Material Value": {
        "domain": "shader",
        "_name": "u_material",
        "dtype": "combo"
    },
    "Material Seed": {
        "domain": ""
    },
    "Material Mix": {
        "domain": "shader",
        "_name": "u_material_mix",
        "dtype": "vec3"
    },
    "Refl": {
        "domain": "shader",
        "_name": "u_ref_strength",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Refl Metallic": {
        "domain": "shader",
        "_name": "u_ref_metallic",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Refl Threshold": {
        "domain": "shader",
        "_name": "u_ref_point",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Refl Border": {
        "domain": "shader",
        "_name": "u_ref_smooth",
        "dtype": "float",
        "min": -1,
        "max": 1,
        "step": 0.001
    },


    "Diff Size": {
        "domain": "diff_size",
        "dtype": "float",
        "min": 6,
        "max": 12,
        "step": 1
    },
    "Diff Blur": {
        "domain": "app",
        "dtype": "float",
        "min": 0,
        "max": 64,
        "step": 1
    },
    "Diff Blur Default": {
        "domain": ""
    },
    "Refl Blur Default": {
        "domain": ""
    },
    "Diff Blur Radio": {
        "domain": "diff_blur",
        "dtype": "bool"
    },
    "Refl Blur Radio": {
        "domain": "refl_blur",
        "dtype": "bool"
    },
    "Diff Blur K": {
        "domain": "app",
        "dtype": "float",
        "min": 0,
        "max": 2,
        "step": 1
    },
    "Refl Size": {
        "domain": "refl_size",
        "dtype": "float",
        "min": 6,
        "max": 12,
        "step": 1
    },
    "Refl Blur": {
        "domain": "app",
        "dtype": "float",
        "min": 0,
        "max": 64,
        "step": 1
    },
    "Refl Blur K": {
        "domain": "app",
        "dtype": "float",
        "min": 0,
        "max": 2,
        "step": 1
    },


    "Prev Max Step": {
        "_name": "u_max_step",
        "domain": "shader",
        "dtype": "float",
        "min": 0,
        "max": 1024*256,
        "step": 1
    },
    "Prev Step Scale": {
        "_name": "u_step_scale",
        "domain": "shader",
        "dtype": "float",
        "min": 0.001,
        "max": 0.05,
        "step": 0.00001
    },

    "Rend Max Step": {
        "_name": "u_max_step",
        "domain": "shader",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Rend Step Scale": {
        "_name": "u_step_scale",
        "domain": "shader",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },


    "Scan Size": {
        "domain": "shader",
        "dtype": "float",
        "_name": "u_scan_size"
    },
    "Rend Size": {
        "domain": "shader",
        "dtype": "float",
        "_name": "u_ren_res"
    },
    "Rend Bounds": {
        "domain": "shader",
        "dtype": "bool",
        "_name": "u_ren_bounds"
    },
    "Rend AA": {
        "domain": "",
        "dtype": "float",
        "min": 1,
        "max": 8,
        "step": 1
    },
    "Rend Max Patch": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },

    "Web Dir": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Snap Dir": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Ren Dir": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Mesh Dir": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Ren Frames": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1000,
        "step": 1
    },
    "Rend Depth": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Rend Normals": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Rend Beauty": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Rend Info": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },
    "Rend UV": {
        "domain": "",
        "dtype": "float",
        "min": 0,
        "max": 1,
        "step": 0.001
    },


    "Camera Movement": {
        "domain": "",
        "dtype": "vec3",
        "min": -0.04,
        "max": 0.04,
        "step": 0.0001
    },
    "Tex Movement": {
        "domain": "",
        "dtype": "vec3",
        "min": -0.04,
        "max": 0.04,
        "step": 0.0001
    },

    "Video Play": {
        "domain": ""
    },
    "Video Frame": {
        "domain": "",
        "dtype": "float"
    },

    "Keyframes": {
        "domain": ""
    },

    "Frame": {
        "domain": ""
    }

}


class Controller:
    def __init__(self, app, appctx):
        self.app = app
        self.appctx = appctx
        self.valconf = valueConfig
        self.values = {}
        self.blit_tex = "beauty"
        self.max_octaves = 8
        self.inited = False
        self.size = (100, 100)
        self.signal = None
        self.frame = 0

    def init(self, ctx):
        self.app.init(ctx,
                      self.appctx.get_resource("renderer_vs.glsl"),
                      self.appctx.get_resource("renderer_fs.glsl"),
                      self.appctx.get_resource("blur_vs.glsl"),
                      self.appctx.get_resource("blur_fs.glsl"))
        self.inited = True
        # self.apply_all()
        # try:
        #     self.load("autosave.rd")
        # except:
        # self.values = default
        self.load(self.appctx.get_resource("default.rd"))

    def apply_all(self):
        for key in self.values:
            self.apply(key)
            self.signal.signal.emit(key)

    def apply(self, name):
        if name in self.valconf:
            domain = self.valconf[name]["domain"]
            if domain == "shader":
                val = self.values[name]
                _name = self.valconf[name]["_name"]
                self.app.set(_name, val)
            if domain == "tex":
                val = self.values[name]
                self.set("Video Frame", 0)
                if val is None:
                    val = self.appctx.get_resource("default.jpg")
                self.app.set_tex_src(val)
            if domain == "refl_size":
                val = pow(2, int(self.values[name]))
                self.app.resize_blit(val)
            if domain == "refl_blur":
                val = self.values[name]
                if val:
                    self.set("Refl Blur", self.values["Refl Blur Default"])
                else:
                    self.set("Refl Blur", 0)
            if domain == "diff_size":
                val = pow(2, int(self.values[name]))
                self.app.resize_blur(val)
            if domain == "diff_blur":
                val = self.values[name]
                if val:
                    self.set("Diff Blur", self.values["Diff Blur Default"])
                else:
                    self.set("Diff Blur", 0)
            if domain == "app":
                val = self.values[name]
                self.app.args[name] = val

            if domain == "amp":
                self.set_amp()
            if domain == "freq":
                self.set_freq()
            if domain == "off":
                self.set_off()
                self.set_pos()
            if domain == "dir":
                self.set_dir()
                self.set_pos()
            if domain == "spd":
                self.set_spd()
                self.set_pos()
            if domain == "pos":
                self.set_pos()
            if domain == "bump":
                self.set_bump()

            if domain == "material":
                val = self.values[name]
                self.set("Material Value", val)

    def resize(self, w, h):
        self.size = (w, h)
        self.app.resize(w, h)

    def set(self, name, val):
        self.values[name] = val
        if self.inited:
            self.apply(name)

    def render_preview(self, target):
        # self.apply("Prev Max Step")
        self.apply("Prev Step Scale")
        self.app.render_preview()
        self.app.render_blit(self.blit_tex, target)

    def snap(self):
        imgs = self.render_frame()
        self.save_snap(imgs, self.values["Snap Dir"], "RDSNAP", None)
        self.resize(*self.size)

    def render_frame(self):
        # self.apply("Rend Max Step")
        self.apply("Rend Step Scale")
        # self.apply("Prev Max Step")
        # self.apply("Prev Step Scale")
        out = self.app.render_big(
            *self.values["Rend Size"],
            int(self.values["Rend AA"]),
            *self.values["Rend Max Patch"],
            self.values["Rend Depth"],
            self.values["Rend Normals"],
            self.values["Rend Beauty"],
            self.values["Rend UV"]
        )
        return out

    def render(self):
        self.set("Frame", 0)
        self.set("Video Frame", 0)
        for i in range(self.values["Ren Frames"]):
            imgs = self.render_frame()
            self.save_frame(imgs, self.values["Ren Dir"], "RDREN", i)
            self.update()
        self.resize(*self.size)

    def save_frame(self, img, dir, name, frame=None):
        if frame is None:
            frame = get_frame(dir, name)
        if img[0] is not None:
            out = img[0][:, :, 0]
            min = np.min(out)
            max = np.max(out)
            out = (out-min)/(max-min)
            out = np.uint16(out*(2**16))
            save_frame(out, dir, name, "DEPTH", frame)
        if img[1] is not None:
            out = img[1]
            out = np.uint8((out/2+0.5) * 255)
            save_frame(out, dir, name, "NORMALS", frame)
        if img[2] is not None:
            out = img[2]
            out = np.uint8(out * 255)
            save_frame(out, dir, name, "BEAUTY", frame)
        if img[3] is not None:
            out = img[3]
            out = np.uint8(out * 255)
            save_frame(out, dir, name, "UVDIF", frame)
        if img[4] is not None:
            out = img[4]
            out = np.uint8(out * 255)
            save_frame(out, dir, name, "UVREF", frame)

    def save_snap(self, img, dir, name, frame=None):
        if frame is None:
            frame = get_idx(dir, name)
        if img[0] is not None:
            out = img[0][:, :, 0]
            min = np.min(out)
            max = np.max(out)
            out = (out-min)/(max-min)
            out = np.uint16(out*(2**16))
            save_snap(out, dir, name, "DEPTH", frame)
        if img[1] is not None:
            out = img[1]
            out = np.uint8((out/2+0.5) * 255)
            save_snap(out, dir, name, "NORMALS", frame)
        if img[2] is not None:
            out = img[2]
            out = np.uint8(out * 255)
            save_snap(out, dir, name, "BEAUTY", frame)
        if img[3] is not None:
            out = img[3]
            out = np.uint8(out * 255)
            save_snap(out, dir, name, "UVDIF", frame)
        if img[4] is not None:
            out = img[4]
            out = np.uint8(out * 255)
            save_snap(out, dir, name, "UVREF", frame)

    def save_web(self):
        self.apply("Rend Step Scale")
        imgs = []
        outs = []
        sizes = self.values["Web Sizes"]
        rsize = self.values["Rend Size"]
        for size in sizes:
            self.set("Rend Size", tuple(size))
            out = self.app.render_big(
                *size,
                1,
                *self.values["Rend Max Patch"],
                True,
                True,
                False,
                False
            )
            outs.append(out[0])
        newsizes = []
        for out in outs:
            imgs.append(pack(out))
            newsizes.append(out.shape[:2][::-1])
        save_web(imgs, self.get_webconfig(newsizes), self.values["Web Dir"])
        self.resize(*self.size)
        self.set("Rend Size", rsize)

    def get_webconfig(self, sizes):
        return {
            "u_max_depth": self.values["Max Depth"],
            "u_amp": self.values["Amplitude"],
            "u_freq": self.values["Frequency"],
            "u_pos": self.values["Pos"],
            "u_octaves": self.values["Octaves"],
            "u_cam_mat": self.values["Camera"],
            "u_fov": self.values["FOV"],
            "u_mirror": self.values["Mirror"],
            "sizes": sizes
        }

    def save_mesh(self):
        size = 512
        out = None
        for i in range(size):
            self.app.set("u_scan_pos", i / size)
            print(i/size)
            ren = self.app.scan(size)
            _out = np.uint8(ren[:, :, :1]*255)
            _uv = np.expand_dims(ren[:, :, 1:], -2)
            if out is None:
                out = _out
            else:
                out = np.concatenate([out, _out], -1)

        print(out.shape)
        print(np.min(out), np.max(out))
        out = np.transpose(out, (2, 0, 1))
        vertices, triangles = mcubes.marching_cubes(out, 128)
        import trimesh
        mesh = trimesh.Trimesh(vertices=vertices, faces=triangles)
        mesh.process()
        mesh.fix_normals()
        vertices, triangles = mesh.vertices, mesh.faces
        print(vertices.shape, triangles.shape)
        import objwriter
        objwriter.write("../data/rdapp/meshes/mesh.obj", (vertices/size-0.5)*4, triangles, {})
        # mesh.export("data/mesh.obj")
        self.resize(*self.size)

    def update(self):
        for key in self.values["Keyframes"]:
            val = self.values["Keyframes"][key]
            idx = self.values["Frame"] % len(val)
            self.set(key, val[idx])

        self.set("Time", self.values["Time"]+self.values["Speed"]/30)
        self.set_pos()
        self.tex_cam.rotate_from(
            self.values["Tex Movement"][0],
            self.values["Tex Movement"][1],
            self.values["Tex Movement"][2], 0, 0, 0)
        self.cam.rotate_from(
            self.values["Camera Movement"][0],
            self.values["Camera Movement"][1],
            self.values["Camera Movement"][2], 0, 0, 0)
        self.set("Camera", self.cam.get())
        self.set("Tex Mat", self.tex_cam.get())
        self.app.set_tex_frame(self.values["Video Frame"])



        self.values["Frame"] += 1
        if self.values["Video Play"]:
            self.set("Video Frame", self.values["Video Frame"] + 1)
        pass

    def set_render(self, name):
        print(name)
        self.blit_tex = name

    def rand(self):
        self.rand_pos()
        self.rand_amp()
        self.rand_freq()
        self.rand_bump()
        self.rand_material_mix()
        if self.values["Random Cam"]:
            np.random.seed()
            self.cam.rotate_from(
                np.random.rand()-0.5*2, np.random.rand()-0.5*2, np.random.rand()-0.5*2, 0, 0, 0)
            cam_speed = np.float32(self.values["Camera Movement"])
            cam_spd = np.sqrt(np.sum(cam_speed * cam_speed))
            new_speed = np.random.rand(3)-0.5
            new_speed /= np.sqrt(np.sum(new_speed * new_speed))
            new_speed *= cam_spd
            self.set("Camera Movement", (float(new_speed[0]), float(
                new_speed[1]), float(new_speed[2])))

    def rand_material_mix(self):
        np.random.seed()
        self.set("Material Seed", np.random.randint(2**16))
        self.set_material_mix()

    def set_material_mix(self):
        seed = self.values["Material Seed"]
        np.random.seed(seed)
        val = (np.random.rand()*2-1, np.random.rand()
               * 2-1, np.random.rand()*2-1)
        self.set("Material Mix", val)

    def set_bump(self):
        bump_val = np.float64(self.values["Bump Val Value"])
        bump_off = np.float64(self.values["Bump Off Value"])
        bump_val_min = self.valconf["Bump Val Value"]["min"]
        bump_val_max = self.valconf["Bump Val Value"]["max"]
        bump_off_min = self.valconf["Bump Off Value"]["min"]
        bump_off_max = self.valconf["Bump Off Value"]["max"]
        bump_rand = self.values["Bump Rand"]
        bump_seed = self.values["Bump Seed"]
        np.random.seed(bump_seed)
        val = bump_val + bump_rand * \
            (np.random.rand()-0.5)*(bump_val_max-bump_val_min)
        off = bump_off + bump_rand * \
            (np.random.rand()-0.5)*(bump_off_max-bump_off_min)
        self.set("Bump Val", tuple(val))
        self.set("Bump Off", tuple(off))

    def rand_bump(self):
        np.random.seed()
        self.set("Bump Seed", np.random.randint(2**16))
        self.set_amp()

    def set_amp(self):
        amp_val = self.values["Amplitude Value"]
        amp_min = self.valconf["Amplitude Value"]["min"]
        amp_max = self.valconf["Amplitude Value"]["max"]
        amp_decay = self.values["Amplitude Decay"]
        amp_seed = self.values["Amplitude Seed"]
        amp_rand = self.values["Amplitude Rand"]
        amp = []
        np.random.seed(amp_seed)
        for i in range(self.max_octaves):
            _amp = amp_val + amp_rand*(np.random.rand()-0.5)*(amp_max-amp_min)
            _amp *= pow(2, amp_decay*i)
            amp.append(_amp)
        self.set("Amplitude", amp)

    def rand_amp(self):
        np.random.seed()
        self.set("Amplitude Seed", np.random.randint(2**16))
        self.set_amp()

    def set_freq(self):
        freq_val = self.values["Frequency Value"]
        freq_min = self.valconf["Frequency Value"]["min"]
        freq_max = self.valconf["Frequency Value"]["max"]
        freq_decay = self.values["Frequency Decay"]
        freq_seed = self.values["Frequency Seed"]
        freq_rand = self.values["Frequency Rand"]
        freq = []
        np.random.seed(freq_seed)
        for i in range(self.max_octaves):
            _freq = freq_val + freq_rand * \
                (np.random.rand()-0.5)*(freq_max-freq_min)
            _freq *= pow(2, freq_decay*i)
            freq.append(_freq)
        self.set("Frequency", freq)

    def rand_freq(self):
        np.random.seed()
        self.set("Frequency Seed", np.random.randint(2**16))
        self.set_freq()

    def set_dir(self):
        dir_seed = self.values["Dir Seed"]
        dir = []
        np.random.seed(dir_seed)
        for i in range(self.max_octaves):
            _d = np.random.rand(3)
            _d /= np.linalg.norm(_d)
            _dir = list(np.random.rand(3))
            dir.append(_dir)
        self.set("Dir", dir)

    def rand_pos(self):
        np.random.seed()
        self.set("Dir Seed", np.random.randint(2**16))
        self.set_dir()
        self.set("Spd Seed", np.random.randint(2**16))
        self.set_spd()
        self.set("Off Seed", np.random.randint(2**16))
        self.set_off()

    def set_off(self):
        off_seed = self.values["Off Seed"]
        off = []
        np.random.seed(off_seed)
        for i in range(self.max_octaves):
            _off = list(np.random.rand(3)*2-1)
            off.append(_off)
        self.set("Off", off)

    def set_spd(self):
        spd_seed = self.values["Spd Seed"]
        spd = []
        np.random.seed(spd_seed)
        for i in range(self.max_octaves):
            _spd = np.random.rand()
            spd.append(_spd)
        self.set("Spd", spd)

    def set_pos(self):
        pos_rand = self.values["Pos Rand"]
        time = self.values["Time"]
        off = self.values["Off"]
        dir = self.values["Dir"]
        spd = self.values["Spd"]
        pos = []
        for i in range(self.max_octaves):
            _pos = pos_rand * \
                (np.float64(off[i]) + np.float64(dir[i])
                 * np.float64(spd[i]) * time)
            _pos = tuple(_pos)
            pos.append(_pos)
        self.set("Pos", pos)

    def set_cam_z(self):
        self.cam = Camera((1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                           0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, -3.0, 1.0))

    def set_cam_0(self):
        self.cam = Camera((1.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0,
                           0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 1.0))

    def flush_config(self):
        return json.dumps(self.values, indent=4)

    def save(self, path):
        head, tail = os.path.split(path)
        os.makedirs(head, exist_ok=True)
        config = self.flush_config()
        with open(path, "w") as f:
            f.write(config)
        print(path)

    def load(self, path):
        with open(path) as f:
            config = f.read()
        config = json.loads(config)
        self.values = config
        self.cam = Camera(self.values["Camera"])
        self.tex_cam = Camera(self.values["Tex Mat"])
        self.apply_all()

        print(path)


def lerp(a, b, c):
    return (b-a)*c+a


def correct(a, b, c):
    return c
