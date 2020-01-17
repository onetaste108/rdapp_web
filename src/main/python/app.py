import moderngl
import numpy as np
from numpy.random import rand

from blur import Blur
from renderer import Renderer
from camera import Camera

import imageio

class App:
    reader = None
    tex_src = None
    tex_fbo_blit = None
    tex_fbo_blur = None
    args = {}
    blit = None
    blur = None

    def __init__(self, ctx = None):
        self.tex_src = None

    def init(self, ctx, vs, fs, bvs, bfs):
        if ctx is None: self.ctx = moderngl.create_standalone_context()
        else: self.ctx = ctx
        # self.ctx.enable(moderngl.DEPTH_TEST)
        # self.ctx.enable(moderngl.BLEND)

        # Load Shaders
        with open(vs, 'r') as f:
            renderer_vs = f.read()
        with open(fs, 'r') as f:
            renderer_fs = f.read()
        with open(bvs, 'r') as f:
            blur_vs = f.read()
        with open(bfs, 'r') as f:
            blur_fs = f.read()

        self.renderer = Renderer(self.ctx, renderer_vs, renderer_fs)
        self.blit = Blur(self.ctx, blur_vs, blur_fs)
        self.blur = Blur(self.ctx, blur_vs, blur_fs)
        self.set("u_viewport", (0,0,1,1))


    def resize(self, w, h):
        self.renderer.build(w, h)
    def resize_blit(self, w, h=None):
        if h is None: h = w
        w, h = int(w), int(h)
        self.blit.build(w, h)
        if self.tex_fbo_blit is not None:
            self.tex_fbo_blit[0].release()
            self.tex_fbo_blit[1].release()
        self.tex_fbo_blit = self.blit.tex_fbo()
        self.renderer.set_tex("blit", self.tex_fbo_blit[0])
    def resize_blur(self, w, h=None):
        if h is None: h = w
        w, h = int(w), int(h)
        self.blur.build(w, h)
        if self.tex_fbo_blur is not None:
            self.tex_fbo_blur[0].release()
            self.tex_fbo_blur[1].release()
        self.tex_fbo_blur = self.blur.tex_fbo()
        self.renderer.set_tex("blur", self.tex_fbo_blur[0])

    # RENDER

    def render(self):
        self.renderer.use_textures()
        self.renderer.render("depth")
        self.renderer.render("norm")
        self.renderer.render("beauty")
        # self.renderer.render("uv_dif")
        # self.renderer.render("uv_ref")

    def scan(self, size):
        self.resize(size, size)
        self.renderer.use_textures()
        self.renderer.render("scan")
        out = self.get("scan")
        print(np.max(out))
        return out

    def render_preview(self):
        self.set("u_viewport", (0,0,1,1))
        self.set("u_render", False)
        self.render()

    def render_big(self, w, h, aa, maxw, maxh, get_depth=True, get_normals=True, get_beauty=True, get_uv=False, get_scan=False):
        # self.tex_fbo_blit[0].build_mipmaps()
        # self.tex_fbo_blit[0].anisotropy = 16
        # self.tex_fbo_blur[0].build_mipmaps()
        # self.tex_fbo_blur[0].anisotropy = 16


        patches = [1,1]
        maxw = maxw//aa
        maxh = maxh//aa
        patch_size = [w, h]
        while patch_size[0] > maxw:
            patches[0] += 1
            patch_size[0] = w//patches[0]
        while patch_size[1] > maxh:
            patches[1] += 1
            patch_size[1] = h//patches[1]
        patch_size[0] *= aa
        patch_size[1] *= aa
        patches[0]
        patches[1]

        self.resize(*patch_size)

        np_depth = None
        np_normals = None
        np_uv_dif = None
        np_uv_ref = None
        np_beauty = None
        np_scan = None

        for y in range(patches[1]):
            np_depth_x = None
            np_normals_x = None
            np_uv_dif_x = None
            np_uv_ref_x = None
            np_beauty_x = None

            self.set("u_render", True)
            for x in range(patches[0]):
                print("Rendering {}%".format(int((y*patches[0]+x)/(patches[0]*patches[1])*100)))
                self.set("u_viewport", (x/patches[0], y/patches[1], x/patches[0]+1/patches[0], y/patches[1]+1/patches[1]))

                self.render()

                if get_depth:
                    depth = self.get("depth")
                    if np_depth_x is not None: np_depth_x = np.concatenate((np_depth_x, depth), 1)
                    else: np_depth_x = depth
                if get_normals:
                    normals = self.get("norm")
                    if np_normals_x is not None: np_normals_x = np.concatenate((np_normals_x, normals), 1)
                    else: np_normals_x = normals
                if get_uv:
                    uv_dif = self.get("uv_dif")
                    if np_uv_dif_x is not None: np_uv_dif_x = np.concatenate((np_uv_dif_x, uv_dif), 1)
                    else: np_uv_dif_x = uv_dif
                    uv_ref = self.get("uv_ref")
                    if np_uv_ref_x is not None: np_uv_ref_x = np.concatenate((np_uv_ref_x, uv_ref), 1)
                    else: np_uv_ref_x = uv_ref
                if get_beauty:
                    beauty = self.get("beauty")
                    if np_beauty_x is not None: np_beauty_x = np.concatenate((np_beauty_x, beauty), 1)
                    else: np_beauty_x = beauty

            if get_depth:
                if np_depth is not None: np_depth = np.concatenate((np_depth, np_depth_x))
                else: np_depth = np_depth_x
            if get_normals:
                if np_normals is not None: np_normals = np.concatenate((np_normals, np_normals_x))
                else: np_normals = np_normals_x
            if get_beauty:
                if np_beauty is not None: np_beauty = np.concatenate((np_beauty, np_beauty_x))
                else: np_beauty = np_beauty_x
            if get_uv:
                if np_uv_dif is not None: np_uv_dif = np.concatenate((np_uv_dif, np_uv_dif_x))
                else: np_uv_dif = np_uv_dif_x
                if np_uv_ref is not None: np_uv_ref = np.concatenate((np_uv_ref, np_uv_ref_x))
                else: np_uv_ref = np_uv_ref_x

        if aa > 1 and get_beauty:
            _beauty = np.zeros((np_beauty.shape[0]//aa, np_beauty.shape[1]//aa, 4))
            for y in range(aa):
                print("Combining {}%".format(int(y/aa*100)))
                _beauty_x = np.zeros((np_beauty.shape[0], np_beauty.shape[1]//aa, 4))
                for x in range(aa):
                    _beauty_x += np_beauty[:,x::aa]
                _beauty += _beauty_x[y::aa]
            _beauty /= aa*aa
            np_beauty = _beauty

        if np_depth is not None: np_depth = np_depth[::-1]
        if np_normals is not None: np_normals = np_normals[::-1]
        if np_beauty is not None: np_beauty = np_beauty[::-1]
        if np_uv_dif is not None: np_uv_dif = np_uv_dif[::-1]
        if np_uv_ref is not None: np_uv_ref = np_uv_ref[::-1]

        return np_depth, np_normals, np_beauty, np_uv_dif, np_uv_ref

    def get(self, name):
        return self.renderer.get(name)

    def render_blit(self, name, fbo):
        return self.blur.blit(self.renderer.tex[name], fbo)

    # SETTINGS

    def set(self, name, val):
        try:
            self.renderer.set(name, val)
        except:
            print("Set prog value error: " + name)
            pass

    def add(self, name, val):
        if name in self.renderer.prog:
            self.renderer.set(name, self.renderer.prog[name].value + val)
        else:
            print("Not in program: " + name)

    def set_tex_src(self, path):
        try:
            if self.reader is not None:
                self.reader.close()
            self.reader = imageio.get_reader(path)
            shape = self.reader.get_data(0)[...,:3].shape
        except:
            return

        if self.tex_src is not None:
            self.tex_src.release()

        self.tex_src = self.ctx.texture(shape[:2][::-1], 3)
        self.tex_src.use(0)
        # self.set_tex_frame(0)

    def set_tex_frame(self, frame=0):
        if self.reader.get_length() > frame:
            self.tex_src.write(self.reader.get_data(frame)[...,:3].tobytes())
        self.blur_tex()

    def blur_tex(self):
        self.blit.blur(self.tex_src, self.tex_fbo_blit[1], int(self.args["Refl Blur"]), self.args["Refl Blur K"])
        # self.tex_fbo_blit[0].build_mipmaps()
        # self.tex_fbo_blit[0].anisotropy = 16
        self.blur.blur(self.tex_src, self.tex_fbo_blur[1], int(self.args["Diff Blur"]), self.args["Diff Blur K"])
        # self.tex_fbo_blur[0].build_mipmaps()
        # self.tex_fbo_blur[0].anisotropy = 16
