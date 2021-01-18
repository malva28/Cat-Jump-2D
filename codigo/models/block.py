"""
autor: Valentina Garrido
"""

from models.quad import Quad
import scene_graph as sg
import transformations as tr
import easy_shaders as es
import basic_shapes as bs
from OpenGL.GL import *


class Block:
    def __init__(self, width, height, quadName="Quad"):
        self.width = width
        self.height = height
        self.name = quadName
        self.model = None

        self.delta = 0.001

        self.pos_x = 0.0
        self.pos_y = 0.0


    def copy(self):
        newBlock = Block(self.width, self.height, self.name)
        newBlock.model = sg.copyNode(self.model)
        newBlock.delta = self.delta
        newBlock.pos_x = self.pos_x
        newBlock.pos_y = self.pos_y
        return newBlock

    def set_model(self, gpu_quad):
        quad = sg.SceneGraphNode(self.name)

        quad.transform = tr.scale(self.width, self.height, 1)
        quad.children += [gpu_quad]

        self.model = sg.SceneGraphNode(self.name + "Tr")
        self.model.children += [quad]

    def set_model_color(self, color):
        gpu_quad = es.toGPUShape(bs.createColorQuad(*color))
        self.set_model(gpu_quad)

    def set_model_texture(self, texture_filename):
        gpu_quad = es.toGPUShape(bs.createTextureQuad(texture_filename, 1, 1), GL_REPEAT, GL_NEAREST)
        self.set_model(gpu_quad)

    def set_init_pos(self, ini_x, ini_y):
        # ini_pos = sg.findNode(self.model, self.name + "Tr")
        self.pos_x = ini_x
        self.pos_y = ini_y

    def update_translate_matrix(self):
        self.model.transform = tr.translate(self.pos_x, self.pos_y, 0)

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.model, pipeline, 'transform')

    def rightLim(self):
        return self.pos_x + self.width * 0.5

    def leftLim(self):
        return self.pos_x - self.width * 0.5

    def upperLim(self):
        return self.pos_y + self.height * 0.5

    def lowerLim(self):
        return self.pos_y - self.height * 0.5