from PySide2 import QtWidgets, QtCore, QtOpenGL
import moderngl
import sys
from PIL import Image
import numpy as np
import os


class SlidersWidget(QtWidgets.QWidget):
    def __init__(self, controller, name, label):
        super().__init__()
        self.controller = controller
        self.name = name
        self._label = label
        self.vc = controller.valconf[name]
        if self.vc["dtype"] == "float": n = 1
        if self.vc["dtype"] == "vec3": n = 3
        self.slidersGroup = SlidersGroup(n)
        for s in self.slidersGroup.sliders:
            s.setRange(self.norm(self.vc["min"]), self.norm(self.vc["max"]))
            s.valueChanged.connect(self.flush)
        self.label = QtWidgets.QLabel()
        self.label.setMinimumWidth(100)
        self.label.setMaximumWidth(100)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.slidersGroup)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        self.setLayout(self.layout)
        # self.set()
        controller.signal.signal.connect(self._set)
    def flush(self, value):
        val = ()
        for s in self.slidersGroup.sliders:
            val += (self.denorm(s.value()),)
        if len(val) == 1: val = val[0]
        self.controller.set(self.name, val)
        self.update_label()
    def update_label(self):
        text = self._label
        text = self._label+" "+str(self.controller.values[self.name])
        self.label.setText(text)
    def denorm(self, val):
        if type(val) == list:
            val = list(val)
            for i in range(len(val)):
                val[i] = val[i] / (1/self.vc["step"])
            return list(val)
        else:
            return val / (1/self.vc["step"])
    def norm(self, val):
        if type(val) == list:
            val = list(val)
            for i in range(len(val)):
                val[i] = int(val[i] / self.vc["step"])
            return list(val)
        else:
            return int(val / self.vc["step"])
    def _set(self, name):
        if name == self.name:
            if type(self.controller.values[self.name]) == list:
                for i in range(len(self.slidersGroup.sliders)):
                    self.slidersGroup.sliders[i].setValue(self.norm(self.controller.values[self.name][i]))
            else:
                self.slidersGroup.sliders[0].setValue(self.norm(self.controller.values[self.name]))
            self.update_label()
        


class ComboWidget(QtWidgets.QWidget):
    def __init__(self, controller, name, label):
        super().__init__()
        self.controller = controller
        self.name = name
        self._label = label
        self.vc = controller.valconf[name]
        self.combo = QtWidgets.QComboBox()
        for key in self.vc["map"]:
            self.combo.addItem(key)
        self.combo.activated.connect(self.set)
        self.label = QtWidgets.QLabel(label)
        self.label.setMinimumWidth(100)
        self.label.setMaximumWidth(100)

        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.combo)
        self.setLayout(self.layout)

        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        controller.signal.signal.connect(self._set)
    def set(self, val):
        self.controller.set(self.name, val)
    def _set(self, name):
        if name == self.name:
            self.combo.setCurrentIndex(self.controller.values[self.name])

class RadioWidget(QtWidgets.QWidget):
    def __init__(self, controller, name, label):
        super().__init__()
        self.controller = controller
        self.name = name
        self.vc = controller.valconf[name]
        self.checkbox = QtWidgets.QCheckBox(label)
        self.checkbox.stateChanged.connect(self.set)
        self.layout = QtWidgets.QHBoxLayout()
        self.layout.addWidget(self.checkbox)
        self.setLayout(self.layout)
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0,0,0,0)

        controller.signal.signal.connect(self._set)
    def set(self, val):
        self.controller.set(self.name, val!=0)
    def _set(self, name):
        if name == self.name:
            self.checkbox.setChecked(self.controller.values[self.name])



class Text2Widget(QtWidgets.QWidget):
    def __init__(self, controller, name, label):
        super().__init__()
        self.controller = controller
        self.name = name
        self.vc = controller.valconf[name]
        self.lines = [QtWidgets.QLineEdit() for i in range(2)]
        for l in self.lines: l.editingFinished.connect(self.set)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(label)
        self.label.setMinimumWidth(95)
        self.label.setMaximumWidth(95)
        self.layout.addWidget(self.label)
        for l in self.lines: self.layout.addWidget(l)
        self.setLayout(self.layout)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0,0,0,0)
        self.controller.signal.signal.connect(self._set)
    def set(self):
        vals = []
        for i in range(len(self.lines)):
            val = self.process(self.lines[i])
            if val is None:
                val = self.controller.values[self.name][i]
            vals.append(val)
            self.lines[i].setText(str(val))
        vals = tuple(vals)
        self.controller.set(self.name, vals)
    def process(self, line):
        val = line.text()
        try:
            val = int(val)
        except:
            val = None
        return val
    def _set(self, name):
        if name == self.name:
            for i in range(len(self.lines)):
                self.lines[i].setText(str(self.controller.values[self.name][i]))


class Text1Widget(QtWidgets.QWidget):
    def __init__(self, controller, name, label):
        super().__init__()
        self.controller = controller
        self.name = name
        self.vc = controller.valconf[name]
        self.lines = QtWidgets.QLineEdit()
        self.lines.editingFinished.connect(self.set)
        self.layout = QtWidgets.QHBoxLayout()
        self.label = QtWidgets.QLabel(label)
        self.label.setMinimumWidth(95)
        self.label.setMaximumWidth(95)
        self.layout.addWidget(self.label)
        self.layout.addWidget(self.lines)
        self.setLayout(self.layout)
        self.layout.setSpacing(5)
        self.layout.setContentsMargins(0,0,0,0)
        self.controller.signal.signal.connect(self._set)
    def set(self):
        val = self.process(self.lines)
        if val is None:
            val = self.controller.values[self.name]
            self.lines.setText(str(val))
        self.controller.set(self.name, val)
    def process(self, line):
        val = line.text()
        try:
            val = int(val)
        except:
            val = None
        return val
    def _set(self, name):
        if name == self.name:
            self.lines.setText(str(self.controller.values[self.name]))

class SlidersGroup(QtWidgets.QWidget):
    def __init__(self, n):
        super().__init__()
        self.sliders = []
        self.layout = QtWidgets.QHBoxLayout()
        for i in range(n):
            print(i)
            slider = QtWidgets.QSlider(QtCore.Qt.Horizontal)
            self.sliders.append(slider)
            self.layout.addWidget(slider)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)


class RenderWidget(QtOpenGL.QGLWidget):
    def __init__(self, controller):
        self.controller = controller
        fmt = QtOpenGL.QGLFormat()
        fmt.setVersion(3, 3)
        fmt.setProfile(QtOpenGL.QGLFormat.CoreProfile)
        fmt.setSampleBuffers(True)
        self.inited = False
        super().__init__(fmt, None)
    def initializeGL(self):
        self.ctx = moderngl.create_context()
        self.screen = self.ctx.detect_framebuffer()
        self.init()
    def init(self):
        self.controller.init(self.ctx)
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000/30)
        self.timer.timeout.connect(self.glDraw)
        self.timer.start()
        self.inited = True
    def get_screen(self):
        return self.screen
    def paintGL(self):
        if self.inited:
            self.controller.update()
            self.controller.render_preview(self.screen)


    def resizeGL(self, w, h):
        self.ctx.viewport = (0, 0, w, h)
        self.controller.resize(w, h)

    def mousePressEvent(self, e):
        self.dx = e.pos().x() / self.width()
        self.dy = e.pos().y() / self.width()

    def mouseMoveEvent(self, e):
        x = e.pos().x() / self.width()
        y = e.pos().y() / self.width()

        if e.modifiers() == QtCore.Qt.CTRL:
            if e.buttons() == QtCore.Qt.LeftButton:
                dt = 10
                self.controller.tex_cam.rotate_from(-(y-self.dy)*dt, -(x-self.dx)*dt, 0, 0,0,0)
        else:
            if e.buttons() == QtCore.Qt.LeftButton:
                if e.modifiers() == QtCore.Qt.SHIFT:
                    dt = 10
                    self.controller.cam.rotate(-(y-self.dy)*dt, -(x-self.dx)*dt, 0)
                else:
                    dt = 10
                    self.controller.cam.rotate_from(-(y-self.dy)*dt, -(x-self.dx)*dt, 0, 0,0,0)
            elif e.buttons() == QtCore.Qt.RightButton:
                dt = 10
                self.controller.cam.translate(0, 0, (-(y-self.dy)+(x-self.dx))*dt)
            elif e.buttons() == QtCore.Qt.MiddleButton:
                dt = 10
                self.controller.cam.translate(-(x-self.dx)*dt, (y-self.dy)*dt, 0)

        self.dx = x
        self.dy = y

class DisplayWidget(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.layout = QtWidgets.QVBoxLayout()
        self.renderWidget = RenderWidget(controller)
        toolbar = QtWidgets.QToolBar()
        self.layout.addWidget(self.renderWidget)
        self.layout.addWidget(toolbar)
        self.layout.setContentsMargins(0,0,0,0)
        self.setLayout(self.layout)

        depth = toolbar.addAction("Depth")
        normals = toolbar.addAction("Normals")
        beauty = toolbar.addAction("Beauty")
        uv_dif = toolbar.addAction("UV Dif")
        uv_ref = toolbar.addAction("UV Ref")
        def set_depth(): controller.set_render("depth")
        def set_normals(): controller.set_render("norm")
        def set_beauty(): controller.set_render("beauty")
        def set_uv_dif(): controller.set_render("uv_dif")
        def set_uv_ref(): controller.set_render("uv_ref")
        depth.triggered.connect(set_depth)
        normals.triggered.connect(set_normals)
        beauty.triggered.connect(set_beauty)
        uv_dif.triggered.connect(set_uv_dif)
        uv_ref.triggered.connect(set_uv_ref)

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setWindowTitle("Radugadesign")
        centralWidget = MainWidget(controller)
        self.setCentralWidget(centralWidget)
    def closeEvent(self, event):
        print("Bye...")

class MainWidget(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        renderer = DisplayWidget(controller)
        self.layout = QtWidgets.QHBoxLayout()
        control = ControlWidget(controller)
        self.layout.addWidget(renderer, 2)
        self.layout.addWidget(control, 1)
        self.setLayout(self.layout)

def HGroup(*widgets):
    w = QtWidgets.QWidget()
    l = QtWidgets.QHBoxLayout()
    w.setLayout(l)
    for wi in widgets:
        l.addWidget(wi)
    l.setContentsMargins(0,0,0,0)
    l.setSpacing(10)
    return w

class Sign(QtCore.QObject):
    signal = QtCore.Signal(str)

class ControlWidget(QtWidgets.QWidget):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        controller.signal = Sign()

        self.layout = QtWidgets.QVBoxLayout()


        amp_group = QtWidgets.QGroupBox("Amplitude")
        self.layout.addWidget(amp_group)
        amp_group.layout = QtWidgets.QVBoxLayout()
        amp_group.setLayout(amp_group.layout)
        amp_group.layout.addWidget(SlidersWidget(controller, "Amplitude Value", "Value"))
        amp_group.layout.addWidget(SlidersWidget(controller, "Amplitude Decay", "Decay"))

        freq_group = QtWidgets.QGroupBox("Frequency")
        self.layout.addWidget(freq_group)
        freq_group.layout = QtWidgets.QVBoxLayout()
        freq_group.setLayout(freq_group.layout)
        freq_group.layout.addWidget(SlidersWidget(controller, "Frequency Value", "Value"))
        freq_group.layout.addWidget(SlidersWidget(controller, "Frequency Decay", "Decay"))

        self.layout.addWidget(SlidersWidget(controller, "Octaves", "Octaves"))
        self.layout.addWidget(SlidersWidget(controller, "Speed", "Speed"))
        self.layout.addWidget(SlidersWidget(controller, "Bump", "Displace"))


        shape_group = QtWidgets.QWidget()
        self.layout.addWidget(shape_group)
        shape_group.layout = QtWidgets.QHBoxLayout()
        shape_group.layout.setContentsMargins(0,0,0,0)
        shape_group.layout.setSpacing(10)
        shape_group.setLayout(shape_group.layout)
        shape_group.layout.addWidget(ComboWidget(controller, "Shape", "Shape"), 3)
        shape_group.layout.addWidget(RadioWidget(controller, "Mirror", "Mirror"), 1)





        tex_group = QtWidgets.QGroupBox("Material")
        self.layout.addWidget(tex_group)
        tex_group.layout = QtWidgets.QVBoxLayout()
        tex_group.setLayout(tex_group.layout)

        tex_group.layout.addWidget(HGroup(
            ComboWidget(controller, "Material", "Material"),
            SlidersWidget(controller, "Tex Scale", "Scale")))
        tex_group.layout.addWidget(HGroup(
            SlidersWidget(controller, "Diff Size", "Diff Size"),
            RadioWidget(controller, "Diff Blur Radio", "Blur")))
        tex_group.layout.addWidget(HGroup(
            SlidersWidget(controller, "Refl Size", "Refl Size"),
            RadioWidget(controller, "Refl Blur Radio", "Blur")))
        c = SlidersWidget(controller, "Tex Movement", "Move")
        b = QtWidgets.QPushButton("Reset"); b.clicked.connect(lambda x:
            (
                controller.set("Tex Movement", (0,0,0)),
                c.set(),
                controller.set("Tex Movement", (0,0,0)),
                c.set(),
                controller.set("Tex Movement", (0,0,0)),
                c.set(),
            ))
        tex_group.layout.addWidget(HGroup(c, b))
        load_tex_button = QtWidgets.QPushButton("Load Image")
        load_tex_button.clicked.connect(self.load_tex)
        tex_group.layout.addWidget(load_tex_button)

        vid_play = QtWidgets.QPushButton("Vid Play")
        vid_play.setCheckable(True)
        # vid_play.setChecked(controller.values["Video Play"])
        vid_play.clicked.connect(lambda: controller.set("Video Play", not controller.values["Video Play"]))
        def vid_play_connect(name):
            if name == "Video Play":
                vid_play.setChecked(controller.values["Video Play"])
        controller.signal.signal.connect(vid_play_connect)
        vid_reset = QtWidgets.QPushButton("Vid Reset")
        vid_reset.clicked.connect(lambda: (controller.set("Video Frame", 0), controller.set("Frame", 0)))
        tex_group.layout.addWidget(HGroup(vid_play, vid_reset))

        cam_group = QtWidgets.QGroupBox("Camera")
        self.layout.addWidget(cam_group)
        cam_group.layout = QtWidgets.QVBoxLayout()
        cam_group.setLayout(cam_group.layout)

        cm = SlidersWidget(controller, "Camera Movement", "Move")
        bm = QtWidgets.QPushButton("Reset"); bm.clicked.connect(lambda x:
            (
                controller.set("Camera Movement", (0,0,0)),
                cm.set(),
                controller.set("Camera Movement", (0,0,0)),
                cm.set(),
                controller.set("Camera Movement", (0,0,0)),
                cm.set(),
            ))
        cam_group.layout.addWidget(HGroup(cm, bm))
        setZ = QtWidgets.QPushButton("Set Z"); setZ.clicked.connect(controller.set_cam_z)
        set0 = QtWidgets.QPushButton("Set 0"); set0.clicked.connect(controller.set_cam_0)
        cam_group.layout.addWidget(HGroup(SlidersWidget(controller, "FOV", "FOV"), setZ, set0))
        cam_group.layout.addWidget(HGroup(
            ComboWidget(controller, "Camera Mode", "Camera Mode"),
            SlidersWidget(controller, "Camera Crop", "Clip")
            ))


        ren_group = QtWidgets.QGroupBox("Render")
        self.layout.addWidget(ren_group)
        ren_group.layout = QtWidgets.QVBoxLayout()
        ren_group.setLayout(ren_group.layout)

        ren_group.layout.addWidget(HGroup(
            Text2Widget(controller, "Rend Size", "Render Size"),
            SlidersWidget(controller, "Rend AA", "AA")))

        web_dir = QtWidgets.QLineEdit("../out")
        web_dir.editingFinished.connect(lambda: self.controller.set("Web Dir", web_dir.text()))
        web_button = QtWidgets.QPushButton("Web")
        web_button.clicked.connect(self.controller.save_web)
        snap_dir = QtWidgets.QLineEdit("../out")
        snap_dir.editingFinished.connect(lambda: self.controller.set("Snap Dir", snap_dir.text()))
        snap_button = QtWidgets.QPushButton("Snap")
        snap_button.clicked.connect(self.controller.snap)
        ren_dir = QtWidgets.QLineEdit("../out")
        ren_dir.editingFinished.connect(lambda: self.controller.set("Ren Dir", ren_dir.text()))
        ren_button = QtWidgets.QPushButton("Render")
        ren_button.clicked.connect(self.controller.render)
        mesh_dir = QtWidgets.QLineEdit("../out")
        mesh_button = QtWidgets.QPushButton("Mesh")
        mesh_button.clicked.connect(self.controller.save_mesh)
        ren_group.layout.addWidget(HGroup(web_button, web_dir))
        ren_group.layout.addWidget(HGroup(snap_button, snap_dir))
        ren_group.layout.addWidget(HGroup(ren_button, ren_dir))
        ren_group.layout.addWidget(HGroup(mesh_button, mesh_dir))
        ren_frames = Text1Widget(controller, "Ren Frames", "Frames")
        ren_group.layout.addWidget(ren_frames)

        ren_group.layout.addWidget(HGroup(
            RadioWidget(controller, "Rend Depth", "Depth"),
            RadioWidget(controller, "Rend Normals", "Normals"),
            RadioWidget(controller, "Rend Beauty", "Beauty"),
        ))

        ren_group.layout.addWidget(SlidersWidget(controller, "Prev Step Scale", "Preview Q"))

        self.save_name = QtWidgets.QLineEdit("default")
        self.render_name = QtWidgets.QLineEdit("default")
        rand_button = QtWidgets.QPushButton("Random")
        save_button = QtWidgets.QPushButton("Save Project")
        load_button = QtWidgets.QPushButton("Load Project")
        def_button = QtWidgets.QPushButton("Default")
        rand_button.clicked.connect(self.controller.rand)
        save_button.clicked.connect(self.save)
        load_button.clicked.connect(self.load)
        def_button.clicked.connect(lambda: controller.load(controller.appctx.get_resource("default.rd")))

        self.layout.addWidget(rand_button)
        self.layout.addWidget(HGroup(save_button, load_button, def_button))

        script_button = QtWidgets.QPushButton("Run Script")
        script_button.clicked.connect(self.run_script)
        self.layout.addWidget(script_button)

        self.layout.addStretch()
        self.layout.setSpacing(10)
        self.setLayout(self.layout)

    def run_script(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Save Project", self.controller.appctx.get_resource("scripts"), "Python (*.py)")
        print(fileName)
        with open(fileName[0], "r") as f:
            script = f.read()
        exec(script, {"controller": self.controller})

    def save(self):
        fileName = QtWidgets.QFileDialog.getSaveFileName(self, "Save Project", "/data/projects/", "Rd Files (*.rd)")
        print(fileName)
        self.controller.save(fileName[0])
    def load(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Load Project", "/data/projects/", "Rd Files (*.rd)")
        print(fileName)
        self.controller.load(fileName[0])
    def load_tex(self):
        fileName = QtWidgets.QFileDialog.getOpenFileName(self, "Open Image", "/data/in/", "All Files (*.*)")
        print(fileName)
        self.controller.set("Tex Src", fileName[0])

    def makeValueWidget(self, name):
        if self.controller.valconf[name]["dtype"] == "float":
            widget = SlidersWidget(self.controller, name, "Label")
        if self.controller.valconf[name]["dtype"] == "vec2":
            widget = SlidersWidget(self.controller, name, "Label")
        if self.controller.valconf[name]["dtype"] == "vec3":
            widget = SlidersWidget(self.controller, name, "Label")
        if self.controller.valconf[name]["dtype"] == "combo":
            widget = ComboWidget(self.controller, name, "Label")
        if self.controller.valconf[name]["dtype"] == "bool":
            widget = RadioWidget(self.controller, name, "Label")
        return widget

class QtApp:
    def run(self, controller):
        qtapp = QtWidgets.QApplication([])
        qtapp.setStyle('Fusion')
        window = MainWindow(controller)
        window.resize(1920,1080)
        window.show()
        sys.exit(qtapp.exec_())
