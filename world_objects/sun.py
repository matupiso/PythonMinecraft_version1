from meshes.cube_mesh import CubeMesh
from settings import *
from utils import sun_value


class Sun:
    def __init__(self, app):
        self.mesh = CubeMesh(app, app.shader_program.sun)
        self.mesh.position = glm.vec3(WORLD_W * CHUNK_H_SIZE,  WORLD_Y, WORLD_D * CHUNK_H_SIZE)
        self.app = app
        self.angle = START_SUN_ANGLE


    def render(self):
        self.mesh.render()


    def update(self):
        self.angle += SUN_SPEED
        self.app.sky_color = glm.vec4(sun_value(self.angle)) * BG_COLOR
        self.angle %= 361
    



    @property
    def light(self):
        return sun_value(self.angle)
