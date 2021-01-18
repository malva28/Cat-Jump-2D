"""
autor: Valentina Garrido
"""

import scene_graph as sg
import easy_shaders as es
import basic_shapes as bs
import transformations as tr
import numpy as np

from OpenGL.GL import GL_REPEAT, GL_NEAREST


class GameOverCG:
    def __init__(self):
        gameOverPic = sg.SceneGraphNode("GameOverPic")
        gameOverPic.transform = tr.matmul([tr.translate(0, 0.5, 0),
                                           tr.scale(1.8, 1.8 * 200 / 150, 1)])

        gameOverText = sg.SceneGraphNode("GameOverText")
        gameOverText.transform = tr.scale(1.8, 1.8 * 15 / 100, 1)

        gameOverTextRot = sg.SceneGraphNode("GameOverTextRot")
        gameOverTextRot.children += [gameOverText]

        gameOverTextTR = sg.SceneGraphNode("GameOverTextTR")
        gameOverTextTR.transform = tr.translate(0, 2, 0)
        gameOverTextTR.children += [gameOverTextRot]

        gameOver = sg.SceneGraphNode("GameOver")
        gameOver.children += [gameOverPic, gameOverTextTR]

        self.pause = 1.0
        self.model = gameOver

    def soft_rotate(self, t, min_angle=-np.pi / 4, max_angle=np.pi / 4):
        resulting_angle = min_angle + (max_angle - min_angle) * np.sin(t)
        return resulting_angle

    def update(self, t):
        resulting_angle = self.soft_rotate(t)
        gameOverTextRot = sg.findNode(self.model, "GameOverTextRot")
        gameOverTextRot.transform = tr.rotationZ(resulting_angle)

    def set_picture(self, filename):
        gpu_pic = es.toGPUShape(bs.createTextureQuad(filename, 1, 1), GL_REPEAT, GL_NEAREST)
        gameOverPic = sg.findNode(self.model, "GameOverPic")
        gameOverPic.children += [gpu_pic]

    def set_text(self, filename):
        gpu_pic = es.toGPUShape(bs.createTextureQuad(filename, 1, 1), GL_REPEAT, GL_NEAREST)
        gameOverText = sg.findNode(self.model, "GameOverText")
        gameOverText.children += [gpu_pic]


class WinCG(GameOverCG):
    def __init__(self):
        super().__init__()
        self.set_picture("textures/gameWonPic.png")
        self.set_text("textures/youWinText.png")

    def update(self, t):
        resulting_angle = self.soft_rotate(t, 0, np.pi / 4)
        soft_factor = (1 + 0.2 * np.sin(5 * t))

        gameOverTextRot = sg.findNode(self.model, "GameOverTextRot")
        gameOverTextRot.transform = tr.matmul([tr.rotationZ(resulting_angle),
                                               tr.uniformScale(soft_factor)])


class LoseCG(GameOverCG):
    def __init__(self):
        super().__init__()
        self.set_picture("textures/gameOverPic.png")
        self.set_text("textures/youLostText.png")
