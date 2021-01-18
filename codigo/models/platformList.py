"""
autor: Valentina Garrido
"""

import csv
import numpy as np

import scene_graph as sg


class PlatformList:
    def __init__(self, base, slab, y_sep=0.5, name="Platforms"):
        self.y_sep = y_sep  # platform to platform separation in y axis

        self.slab_pattern = slab

        base.update_init_pos()
        self.platforms = [[base]]
        self.len_p = 1
        self.presence = []
        self.x_positions = [-0.7, 0.0, 0.7]
        self.name = name

        platform_list = sg.SceneGraphNode(self.name)
        self.model = platform_list

    def read_from_csv(self, structure_csv):
        with open(structure_csv, newline='') as fout:
            reader = csv.reader(fout)
            arr = np.array([row for row in reader], dtype=int)
            self.presence = arr
            self.read_platforms(arr)

    def read_platforms(self, presence_array):
        len_p = 1
        for rows in presence_array:
            platform_row = []
            for present in rows:
                if present:
                    slab_copy = self.slab_pattern.copy()
                    platform_row += [slab_copy]

            self.platforms += [platform_row]
            len_p += 1
        self.len_p = len_p

    def update_model_tree(self, row_min=0, row_max=None):
        if not row_max or row_max > self.len_p:
            row_max = self.len_p

        if row_min < 0:
            row_min = 0

        self.model.children = []

        for i in range(row_min, row_max):
            row = self.platforms[i]
            self.model.children += [p.model for p in row]

    def position_platforms(self, presence):
        for i in range(1,self.len_p):
            k = 0
            for j in range(3):  # lenght of a row
                if presence[i-1][j]:
                    self.platforms[i][k].set_init_pos(self.x_positions[j], -1 + self.y_sep*i)
                    self.platforms[i][k].update_translate_matrix()
                    k += 1

    def get_platforms(self):
        return [p for row in self.platforms for p in row]

    def maximum_height(self):
        return (self.len_p-1)*self.y_sep

    def draw(self, pipeline):
        for row in self.platforms:
            for p in row:
                p.draw(pipeline)