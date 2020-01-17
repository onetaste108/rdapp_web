import numpy as np
import moderngl
class Blur:
    def __init__(self, ctx, vs, fs):

        self.ctx = ctx

        # Init Blur
        self.vbo = self.ctx.buffer(np.float32([-1,-1,1,-1,-1,1,-1,1,1,-1,1,1]))
        self.prog = self.ctx.program(
            vertex_shader = vs,
            fragment_shader = fs)
        self.vao = self.ctx.simple_vertex_array(self.prog, self.vbo, "a_pos")
        self.tex = [None for i in range(2)]
        self.fbo = [None for i in range(2)]

    def build(self, w, h, d = 3, dt = "f2"):
        self.w, self.h, self.d, self.dt = w, h, d, dt

        # Build Textures
        for i in range(2):
            if self.tex[i] is not None:
                self.tex[i].release()
            self.tex[i] = self.ctx.texture((w, h), d, dtype=dt)

        # Buld FBO's
        for i in range(2):
            if self.fbo[i] is not None:
                self.fbo[i].release()
            self.fbo[i] = self.ctx.framebuffer([self.tex[i]])

        self.prog["u_res"].value = self.fbo[0].size
        self.prog["u_tex"].value = 0

    def blur(self, tex, out, n=0, s=2):
        self.prog["u_size"].value = s

        self.blit(tex, self.fbo[0])
        for i in range(n):
            self.blur_once()
        self.blit(self.tex[0], out)

    def blur_once(self):
        self.tex[0].use(0)
        self.prog["u_mode"].value = 1
        self.fbo[1].use()
        self.vao.render()
        self.tex[1].use(0)
        self.prog["u_mode"].value = 2
        self.fbo[0].use()
        self.vao.render()

    def blit(self, tex, out):
        tex.use(0)
        out.use()
        self.prog["u_mode"].value = 0
        self.vao.render()

    def tex_fbo(self):
        tex = self.ctx.texture((self.w, self.h), self.d, dtype=self.dt)
        fbo = self.ctx.framebuffer([tex])
        return (tex, fbo)
