"""
autor: Valentina Garrido
"""

from models.block import Block
import scene_graph as sg

from withinEps import *



class Platform(Block):
    def __init__(self, width, height, quadName="Platform"):
        super().__init__(width, height, quadName)
        self.delta = 0.02

    def copy(self):
        newPlat = Platform(self.width, self.height, self.name)
        newPlat.model = sg.copyNode(self.model)
        newPlat.pos_x = self.pos_x
        newPlat.pos_y = self.pos_y
        return newPlat

    def upperCollide(self, cat):
        # print('cat lower lim: {}\nplatform upper lim: {}'.format(cat.lowerLim(), self.upperLim()))
        if within_eps(cat.lowerLim(), self.upperLim(), self.delta):
            if cat.rightLim() >= self.leftLim() and cat.leftLim() <= self.rightLim() \
                    and cat.jump_state() != 1:
                return True
        return False