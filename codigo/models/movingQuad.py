"""
autor: Valentina Garrido
"""

from models.block import Block
from withinEps import *


class MovingQuad(Block):
    def __init__(self, width, height, quadName="Quad"):
        super().__init__(width, height, quadName)

        self.direc = 0
        # direc 0 indica que no se mueve, direc -1 indica que se mueve a la izquierda
        # y direc 1 indica que se mueve a la derecha
        self.vx = 0
        self.maxVel = 1
        self.dv = 1 / 40

        self.midair = False
        self.vy = 0
        self.maxVy = 2.5
        self.gravity = 1 / 20

        self.might_lose = False
        self.game_over = False
        self.won = False

    def clamp_lower_lim_to(self, py):
        self.pos_y = py+self.width*0.5

    def update_positions(self, dt):
        self.move()
        self.pos_x += (self.vx * dt)
        # print(self.pos_y)
        self.moveDown()
        self.pos_y += (self.vy * dt)

    def is_idle(self):
        return not self.midair and within_eps(self.vx, 0, self.dv)

    def move(self):
        if self.direc == 1:
            self.move_right()
        elif self.direc == -1:
            self.move_left()
        elif self.direc == 0:
            self.decelerate()

    def move_left(self):
        if self.vx >= - self.maxVel:
            self.vx -= self.dv

    def move_right(self):
        if self.vx <= self.maxVel:
            self.vx += self.dv

    def decelerate(self):
        if self.vx >= self.dv:
            self.vx -= self.dv
        elif self.vx <= -self.dv:
            self.vx += self.dv
        else:
            self.vx = 0.0

    def horizontalCollide(self, walls):
        if (walls.leftCollide(self) and self.vx < 0.0) or \
                (walls.rightCollide(self) and self.vx > 0.0):
            self.direc = 0
            self.vx = 0.0

        # else:
        #    self.allowLeftMove = True
        #    self.allowRightMove =True

    def jump(self):
        if not self.midair:
            self.midair = True
            self.vy = self.maxVy

    def jump_state(self):
        # returns 1 if it's going up, 2 if it's floating
        # 3 if it's going down, and 0 if neither of them
        if not self.midair:
            return 0
        else:
            if self.vy > self.maxVy/5:
                return 1
            elif self.vy < self.maxVy/5 and self.vy > -self.maxVy/5:
                return 2
            else:
                return 3

    def moveDown(self):
        if self.midair:
            self.vy -= self.gravity

    def verticalCollide(self, platforms):
        for i in range(platforms.len_p):
            print(i)
            row = platforms.platforms[i]
            for p in row:
                if p.upperCollide(self):
                    self.midair = False
                    self.vy = 0.0
                    self.clamp_lower_lim_to(p.upperLim())
                    return i
                else:
                    self.midair = True
        return None

    def efficientVerticalCollide(self, platforms, i_row):
        if i_row < 0:
            i_row = 0
        if i_row >= platforms.len_p:
            i_row = platforms.len_p-1

        row = platforms.platforms[i_row]
        for p in row:
            if p.upperCollide(self):
                self.midair = False
                self.vy = 0.0
                self.clamp_lower_lim_to(p.upperLim())
                return i_row
            else:
                self.midair = True
        return None

    def update_losing_status(self, platforms, recent_i_row):
        if not self.might_lose:
            if platforms.len_p == 0 or not recent_i_row :
                return
            if platforms.len_p < 1:
                if recent_i_row == platforms.len_p:
                    self.might_lose = True
            else:
                if recent_i_row > 1:
                    self.might_lose = True

