"""
autor: Valentina Garrido
"""

import transformations as tr
import scene_graph as sg
import numpy as np

from OpenGL.GL import glClearColor
import random
from typing import List

from models.platformList import PlatformList
from models.movingQuad import MovingQuad
from models.walls import Walls
from models.background import Background
from models.base import Base
from models.platform import Platform
from models.cat import Cat
from models.yarn import Yarn


class ScrollableWorld:
    def __init__(self, platform_filename, y_sep, window_width= 558, window_height = 992):
        self.window_w = window_width
        self.window_h = window_height
        self.platform_filename = platform_filename

        self.mc = None
        self.base = None
        self.yarn = None

        self.platforms = None
        self.walls = Walls(-1, 1)

        self.world = sg.SceneGraphNode("World")
        self.not_moving = sg.SceneGraphNode("StaticObjs")
        self.world.children += [self.not_moving]
        self.update_list = []

        self.y_sep = y_sep
        self.min_scroll_y = 0.0
        self.max_scroll_y = 1.0
        self.scrolling = -1
        self.fixed_ratio = False

    def set_mc(self, mc):
        self.mc = mc
        self.world.children += [self.mc.model]

    def platform_row_mc_is_near_to(self):
        y = self.mc.lowerLim()
        i_row = int(np.ceil((y+0.5)/self.y_sep))
        return i_row

    def set_platforms(self, platform_list):
        self.platforms = platform_list
        self.platforms.read_from_csv(self.platform_filename)
        self.platforms.position_platforms(self.platforms.presence)

        self.platforms.update_model_tree()
        self.max_scroll_y = self.platforms.maximum_height() - 2

    def add_platforms_to_model(self):
        self.not_moving.children += [self.platforms.model]

    def set_yarn(self, yarn):
        yarn_pos_y = self.platforms.maximum_height() + self.y_sep-1
        yarn.set_init_pos(0.0, yarn_pos_y)
        yarn.update_translate_matrix()

        self.yarn = yarn
        self.not_moving.children += [yarn.model]

    def dummy_platform_test(self, platform_list):
        self.platforms = platform_list

        ones = np.array([[1, 0, 0] for i in range(30)], dtype=int)
        self.platforms.read_platforms(ones)
        self.platforms.position_platforms(ones)

        self.platforms.update_model_tree()
        self.max_scroll_y = self.platforms.maximum_height() - 2

    def fix_ratio(self):
        if self.window_h > self.window_w:
            factor = self.window_w/self.window_h
            self.world.transform = tr.matmul([tr.translate(0,-(1-factor),0),
                tr.scale(1, factor, 1)])
            self.fixed_ratio = True

    def update_mc(self, dt):
        # updates mc's position and
        # sets scrolling to 1 if it should scroll, -1 if mc is mc is under
        # scrolling limits and 0 if mc it's over scrolling limits

        self.mc.update_positions(dt)
        if self.mc.pos_y > self.min_scroll_y and self.mc.pos_y < self.max_scroll_y:
            self.scrolling = 1
        elif self.mc.pos_y > self.max_scroll_y:
            self.scrolling = 0
        else:
            self.scrolling = -1

    def visible_slabs(self):
        w_range = self.get_current_y_view()
        row_min = int(np.ceil((w_range[0] + 1) / self.y_sep))
        row_max = int(np.ceil((w_range[1] + 1) / self.y_sep))
        return [row_min, row_max]

    def update(self, dt, t):
        self.update_mc(dt)
        self.yarn.grow_and_shrink(dt)

        [o.update(t) for o in self.update_list]

        slab_range = self.visible_slabs()
        self.platforms.update_model_tree(slab_range[0], slab_range[1])

        if self.scrolling == 1:
            self.verticalScroll()
        else:
            self.no_scroll()

    def get_current_y_view(self):
        factor = self.window_h/self.window_w
        lower_y = -1
        upper_y = 1
        if self.scrolling == -1:
            if self.fixed_ratio:
                return [lower_y,upper_y+2*(factor-1)]
            else:
                return [lower_y, upper_y]
        elif self.scrolling == 1:
            if self.fixed_ratio:
                return [lower_y+self.mc.pos_y,
                        upper_y+self.mc.pos_y+2*(factor-1)]
            else:
                return [lower_y+self.mc.pos_y, upper_y+self.mc.pos_y]
        else:
            if self.fixed_ratio:
                return [self.max_scroll_y+lower_y,
                        self.max_scroll_y+upper_y+2*(factor-1)]
            else:
                return [self.max_scroll_y+lower_y,
                        self.max_scroll_y+upper_y]

    def no_scroll(self):
        if self.scrolling == -1:
            self.mc.update_translate_matrix()
        elif self.scrolling == 0:
            self.mc.model.transform = tr.translate(self.mc.pos_x, self.mc.pos_y - self.max_scroll_y, 0)
            self.not_moving.transform = tr.translate(0, -self.max_scroll_y, 0)

    def verticalScroll(self):
        self.mc.model.transform = tr.translate(self.mc.pos_x, 0, 0)
        self.not_moving.transform = tr.translate(0,-self.mc.pos_y,0)

    def draw(self, pipeline):
        sg.drawSceneGraphNode(self.world, pipeline, 'transform')

    def check_collisions(self):

        self.mc.horizontalCollide(self.walls)
        row_i = self.platform_row_mc_is_near_to()

        stepped_into_row_i = self.mc.efficientVerticalCollide(self.platforms, row_i)

        if row_i >= self.platforms.len_p:
            self.yarn.update_winning_status(self.mc)
        # stepped_into_row        print(row_i)_i = self.mc.verticalCollide(self.platforms)

        self.mc.update_losing_status(self.platforms, stepped_into_row_i)

    def enable_game_over(self):
        self.base.enable_game_over = True
        self.yarn.enable_game_over = True


class NoTextureScrollableWorld(ScrollableWorld):
    def __init__(self, platform_filename, y_sep=0.8, window_width= 558, window_height = 992):
        super().__init__(platform_filename,y_sep, window_width, window_height)

        mc = MovingQuad(0.2, 0.2, "Quad")
        mc.set_model_color((0.0, 0.0, 0.0))

        base = Base()
        base.set_model_color((0.0, 1.0, 1.0))
        self.base = base

        slab_pattern = Platform(0.4,  0.1)
        slab_pattern.set_model_color((1.0, 0.0, 0.0))

        platform_list = PlatformList(base,slab_pattern,y_sep)

        yarn = Yarn(0.3)
        yarn.set_model_color((1.0, 1.0, 0.0))

        self.set_mc(mc)
        self.set_platforms(platform_list)
        self.add_platforms_to_model()
        self.set_yarn(yarn)


class TextureScrollableWorld(ScrollableWorld):
    def __init__(self, platform_filename, y_sep=0.8, window_width= 558, window_height = 992):
        super().__init__(platform_filename, y_sep, window_width, window_height)

        mc = Cat(0.2, 0.2)

        base = Base()
        base.set_model_texture("textures/base.png")
        self.base = base

        slab_pattern = Platform(0.4, 0.1)
        slab_pattern.set_model_texture("textures/platform.png")

        platform_list = PlatformList(base,slab_pattern,y_sep)

        yarn = Yarn(0.3)
        yarn.set_model_texture("textures/lana.png")

        self.set_mc(mc)
        self.set_platforms(platform_list)

        self.background = None
        self.set_background()
        self.add_platforms_to_model()
        self.set_yarn(yarn)

        self.yarn.set_bg(self.background)
        self.yarn.set_world_model(self.world)
        self.yarn.set_update_list(self.update_list)

        self.base.set_bg(self.background)
        self.base.set_world_model(self.world)
        self.base.set_update_list(self.update_list)

    def set_background(self):
        self.background = Background(self.window_w, self.window_h, self.max_scroll_y)
        self.not_moving.children += [self.background.model]
