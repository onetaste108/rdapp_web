import numpy as np
import moderngl

class Renderer:
    def __init__(self, ctx, vs, fs):
        self.ctx = ctx
        # Init Renderer
        self.vbo = self.ctx.buffer(np.float32([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]))
        self.prog = self.ctx.program(
            vertex_shader = vs,
            fragment_shader = fs)
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, "a_pos")

        self.tex_empty = self.ctx.texture((1,1), 1, dtype="f1")
        self.tex_blit = None
        self.tex_blur = None

        self.tex_map = {
            "blit": 0,
            "blur": 1,
            "depth": 2,
            "norm": 3,
            "beauty": 4,
            "uv_dif": 5,
            "uv_ref": 6,

            "scan": 7
        }

        self.tex = {
            "blit": None,
            "blur": None,
            "depth": None,
            "norm": None,
            "beauty": None,
            "uv_dif": None,
            "uv_ref": None,

            "scan": None
        }

        self.fbo = {
            "depth": None,
            "norm": None,
            "beauty": None,
            "uv_dif": None,
            "uv_ref": None,

            "scan": None,
        }

        for tex in self.tex_map:
            self.set("u_tex_"+tex, self.tex_map[tex])

    def set_tex(self, name, tex):
        self.tex[name] = tex

    def use_textures(self):
        for tex in self.tex:
            self.tex[tex].use(self.tex_map[tex])

    def build(self, w, h, dn_dt="f4", beauty_dt="f2", scale = 1):
        self.width = w
        self.height = h
        self.scale = scale
        self.set("u_res", (w, h))

        if self.tex["depth"] is not None: self.tex["depth"].release()
        if self.tex["beauty"] is not None: self.tex["beauty"].release()
        if self.tex["scan"] is not None: self.tex["scan"].release()
        if self.tex["uv_dif"] is not None: self.tex["uv_dif"].release()
        if self.tex["uv_ref"] is not None: self.tex["uv_ref"].release()

        if self.fbo["depth"] is not None: self.fbo["depth"].release()
        if self.fbo["beauty"] is not None: self.fbo["beauty"].release()
        if self.fbo["scan"] is not None: self.fbo["scan"].release()
        if self.fbo["uv_dif"] is not None: self.fbo["uv_dif"].release()
        if self.fbo["uv_ref"] is not None: self.fbo["uv_ref"].release()

        self.tex["depth"] = self.ctx.texture((w, h), 1, dtype=dn_dt)
        self.tex["depth"].filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.tex["norm"] = self.ctx.texture((w, h), 3, dtype=beauty_dt)
        self.tex["norm"].filter = (moderngl.NEAREST, moderngl.NEAREST)
        self.tex["beauty"] = self.ctx.texture((w, h), 4, dtype="f2")
        self.tex["uv_dif"] = self.ctx.texture((w, h), 4, dtype="f4")
        self.tex["uv_ref"] = self.ctx.texture((w, h), 4, dtype="f2")
        self.tex["scan"] = self.ctx.texture((w, h), 4, dtype="f2")

        self.fbo["depth"] = self.ctx.framebuffer([self.tex["depth"]])
        self.fbo["norm"] = self.ctx.framebuffer([self.tex["norm"]])
        self.fbo["beauty"] = self.ctx.framebuffer([self.tex["beauty"]])
        self.fbo["uv_dif"] = self.ctx.framebuffer([self.tex["uv_dif"]])
        self.fbo["uv_ref"] = self.ctx.framebuffer([self.tex["uv_ref"]])
        self.fbo["scan"] = self.ctx.framebuffer([self.tex["scan"]])

    def render(self, name):
        self.set("u_tex_mode", self.tex_map[name])
        self.tex_empty.use(self.tex_map[name])
        self.fbo[name].use()
        self.vao.render()
        self.tex[name].use(self.tex_map[name])

    def get(self, name):
        tex = self.tex[name]
        npt =  np.frombuffer(tex.read(), dtype=tex.dtype).reshape(tex.height, tex.width, tex.components)
        return npt

    def set(self, name, value):
        if name in self.prog:
            self.prog[name].value = value
        else:
            print("Not in program: "+name)
