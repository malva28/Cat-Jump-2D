import glfw
import sys

class Controller:
    def __init__(self):
        self.mc = None

    def set_model(self, m):
        self.mc = m

    def on_key(self, window, key, scancode, action, mods):
        if self.mc.game_over:
            print("The game is over!"
                  "\nRerun the program to start again")
            return

        if not (action == glfw.PRESS or action == glfw.RELEASE):
            return

        if key == glfw.KEY_ESCAPE:
            sys.exit()

        elif key == glfw.KEY_A and action == glfw.PRESS:
            self.mc.direc = -1

        elif key == glfw.KEY_D and action == glfw.PRESS:
            self.mc.direc = 1

        elif (key == glfw.KEY_A or key == glfw.KEY_D) and action == glfw.RELEASE:
            self.mc.direc = 0

        elif key == glfw.KEY_W:
            self.mc.jump()

        else:
            print('Unknown key')