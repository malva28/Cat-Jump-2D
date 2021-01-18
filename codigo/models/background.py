"""
autor: Valentina Garrido
"""

import transformations as tr
import basic_shapes as bs
import scene_graph as sg
import easy_shaders as es
from OpenGL.GL import *


class Background:
    def __init__(self, window_width, window_height, max_scroll_y):
        self.b_width = 100
        self.b_height = 750
        self.max_scroll_y = max_scroll_y
        self.model = sg.SceneGraphNode("Background")
        self.set_normal_background()

    def set_single(self):
        # sets a single background image that adjusts to window width
        # no background  while going beyond its height
        gpu_background = es.toGPUShape(bs.createTextureQuad("../textures/background.png", 1, 1), GL_REPEAT, GL_NEAREST)
        self.model.children = [gpu_background]
        self.model.transform = tr.matmul([tr.translate(0, (self.b_height / self.b_width) - 1, 0),
                                          tr.scale(2, 2 * self.b_height / self.b_width, 1)])

    def set_repeating_background(self, filename):
        # sets a background image that adjusts to window width
        # backgrounds repeats to fit maximum scrollable size

        actual_y_scale = self.max_scroll_y+4
        y_ratio = actual_y_scale / (2*self.b_height/self.b_width)

        gpu_background = es.toGPUShape(bs.createTextureQuad(filename, 1, y_ratio), GL_REPEAT, GL_NEAREST)
        self.model.children = [gpu_background]
        self.model.transform = tr.matmul([tr.translate(0, 0.5* self.max_scroll_y+1, 0),
                                          tr.scale(2, actual_y_scale, 1)])

    def set_normal_background(self):
        filename = "textures/background.png"
        self.set_repeating_background(filename)

    def set_game_over_background(self):
        filename = "textures/darkerBackground.png"
        self.set_repeating_background(filename)

