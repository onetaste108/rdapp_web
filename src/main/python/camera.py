from pyrr import Matrix33, Matrix44, Quaternion, Vector3
import numpy as np

class Camera:
    def __init__(self, mat = None):
        if mat is None:
            self.position = Matrix44.identity()
        else:
            self.position = Matrix44(np.float32(mat))
    def translate(self, x=0, y=0, z=0):
        self.position = self.position * Matrix44.from_translation([x,y,z])
    def rotate(self, x=0, y=0, z=0):
        if x != 0: self.position = self.position * Quaternion.from_x_rotation(x)
        if y != 0: self.position = self.position * Quaternion.from_y_rotation(y)
        if z != 0: self.position = self.position * Quaternion.from_z_rotation(z)
    def rotate_from(self, x=0, y=0, z=0, x0=1, y0=0, z0=0):
        rotation = Matrix44.identity()
        if x != 0: rotation = rotation * Quaternion.from_x_rotation(x)
        if y != 0: rotation = rotation * Quaternion.from_y_rotation(y)
        if z != 0: rotation = rotation * Quaternion.from_z_rotation(z)

        r0 = Matrix44.identity() * Quaternion.from_matrix(self.position)
        pivot = self.position * Vector3([0,0,0])
        eye = Vector3([x0, y0, z0])
        eye_to_pivot = pivot - eye
        eye_to_pivot = ~r0 * eye_to_pivot

        translation = Matrix44.from_translation(-eye_to_pivot)
        self.position = self.position * translation
        self.position = self.position * rotation
        self.position = self.position * ~translation

    def get(self):
        return tuple(np.float64(self.position).ravel())
