import numpy as np
from numpy.random import rand, randint

class Distort:

    pos = [
        # Pos("x"),
        # Pos("y"),
        # Pos("z"),
        Pos("xyz"),
        # Pos("zxy"),
        # Pos("yzx"),
        # Pos("zyx"),
        # Pos("yxz"),
        # Pos("zyx"),

    ]

    val = [
        Val("u_time"),
        # Val("vec3(0.0,0.0,0.0)"),
        Tex(),
        Rval(),
        # Rval(),
        # Rval(),

    ]

    math = [
        Math("+"),
        Math("-"),
        Math("*"),
    ]

    func = [
        Func("sin", 1),
        Func("cos", 1),
        # Func("rot", 2),
        Func("normalize", 1),
        # Func("length", 1),

        # Func("abs", 1),
        # Func("fract", 1),
    ]

    all = pos+val+math+func
    const = pos+val
    op = func+math

    depth = 2

    def __init__(self, fs):
        f = open(fs, 'r')
        self.fs = f.read()
        f.close()
        self.fs = self.fs.split("// DISTFUNC")
        self.tree = None
        self.trees = []
        self.build()

    def get(self):
        self.build()
        return self.fs[0] + self.write() + self.fs[1]

    def build(self):
        self.trees = []
        for i in range(4):
            self.trees.append(self._build())

    def _build(self):
        tree = Node(self.rand_op(), 0)
        for i in range(tree.val.n):
            self.add_rand_node(tree)
        return tree

    def write(self):
        text = ""
        for t in self.trees:
            text += self._write(t)
        return text

    def _write(self, t):
        return "\np-="+t.write()+";\n"

    def add_rand_node(self, n):
        if rand() > n.d / self.depth:
            v = self.rand_op()
        else:
            v = self.rand_const()
        nn = n.add_child(v)
        for i in range(v.n):
            self.add_rand_node(nn)


    def rand_all(self):
        return self.all[randint(len(self.all))]

    def rand_const(self):
        return self.const[randint(len(self.const))]

    def rand_op(self):
        return self.op[randint(len(self.op))]
