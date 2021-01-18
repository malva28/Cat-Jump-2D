"""
autor: Valentina Garrido
"""

from models.movingQuad import MovingQuad

import scene_graph as sg
import transformations as tr
import easy_shaders as es
import basic_shapes as bs
import numpy as np
from OpenGL.GL import *



class Cat(MovingQuad):
    def __init__(self, width, height):
        super().__init__(width, height, "Cat")

        self.moving_sprites = []
        self.jumping_sprites = []
        self.idle_sprite = []

        self.load_sprites()
        self.set_model(self.idle_sprite[0])

        self.current_idle_sprite = 0
        self.current_jump_sprite = 0
        self.current_mov_sprite = 0
        self.t = 0

    def set_sprite(self, gpu_sprite):
        cat = sg.findNode(self.model, self.name)
        cat.children = [gpu_sprite]

    def load_moving_sprites(self):
        filenames = []
        name_base = "textures/catRunning{}{}.png"
        for i in range(1, 13):
            u = i % 10
            d = i // 10
            filenames.append(name_base.format(str(d), str(u)))
        self.moving_sprites = [es.toGPUShape(bs.createTextureCube(texture), GL_REPEAT, GL_NEAREST) for texture in
                               filenames]

    def load_jumping_sprites(self):
        filenames = ["textures/catJumping01.png",
                     "textures/catRunning04.png",
                     "textures/catRunning05.png",
                     "textures/catRunning06.png",
                     "textures/catJumping02.png"]
        self.jumping_sprites = [es.toGPUShape(bs.createTextureCube(texture), GL_REPEAT, GL_NEAREST) for texture in
                               filenames]

    def load_sprites(self):
        self.load_moving_sprites()
        self.load_jumping_sprites()
        self.idle_sprite = [es.toGPUShape(bs.createTextureCube("textures/catIdle.png"), GL_REPEAT, GL_NEAREST)]

    def set_model(self, gpu_quad):
        super().set_model(gpu_quad)

        direc = sg.SceneGraphNode(self.name+"Direc")
        cat = sg.findNode(self.model, self.name)
        self.model.children = [direc]
        direc.children = [cat]

    def set_direc(self, facing_left=True):
        direc = sg.findNode(self.model, self.name+"Direc")
        if facing_left:
            direc.transform = tr.identity()
        else:
            direc.transform = tr.horizontalReflection()

    def update_positions(self, dt):
        if self.vx < -self.dv:
            self.set_direc(True)
        elif self.vx > self.dv:
            self.set_direc(False)
        self.update_sprite(dt)
        super().update_positions(dt)

    def update_jump_sprite(self, dt):
        if self.jump_state() == 0:
            return
        if self.jump_state() == 2:
            self.t += dt
            if self.vy > self.maxVy/10:
                self.current_jump_sprite = 1
            elif self.vy < -self.maxVy/10:
                self.current_jump_sprite = 3
            else:
                self.current_jump_sprite = 2
        else:
            self.t = 0
            if self.jump_state() == 1:
                self.current_jump_sprite = 0
            elif self.jump_state() == 3:
                self.current_jump_sprite = 4

    def update_moving_sprite(self, dt):
        self.t += dt
        if np.fabs(self.vx) > 0 and self.t > np.fabs(0.03/self.vx):
            self.current_mov_sprite = (self.current_mov_sprite + 1) % 12
            self.t = 0

    def update_sprite(self, dt):
        if self.is_idle():
            self.set_sprite(self.idle_sprite[self.current_idle_sprite])
        else:
            if self.midair:
                self.update_jump_sprite(dt)
                self.set_sprite(self.jumping_sprites[self.current_jump_sprite])
            else:
                self.update_moving_sprite(dt)
                self.set_sprite(self.moving_sprites[self.current_mov_sprite])
