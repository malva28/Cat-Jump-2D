"""
autor: Valentina Garrido
Main game module
"""

import glfw
from OpenGL.GL import *
import sys


import easy_shaders as es
from model import *
from controller import Controller

if __name__ == '__main__':

    if len(sys.argv) == 1:
        print("Using the csv platform file from the homework example.")
        csv_file = "ex_structure.csv"
    else:
        csv_file = sys.argv[1]


    # Initialize glfw
    if not glfw.init():
        sys.exit()

    width = 558
    height = 992

    window = glfw.create_window(width, height, 'Cat Jump Game', None, None)

    if not window:
        glfw.terminate()
        sys.exit()

    glfw.make_context_current(window)

    controlador = Controller()

    glfw.set_key_callback(window, controlador.on_key)

    # Assembling the shader program (pipeline) with both shaders
    #pipeline = es.SimpleTransformShaderProgram()
    pipeline = es.SimpleTextureTransformShaderProgram()

    # Telling OpenGL to use our shader program
    glUseProgram(pipeline.shaderProgram)

    # Setting up the clear screen color
    glClearColor(0.85, 0.85, 0.85, 1.0)

    # Our shapes here are always fully painted
    glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

    # Enabling transparencies
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # HACEMOS LOS OBJETOS

    world = TextureScrollableWorld(csv_file)
    world.fix_ratio()
    world.enable_game_over()

    controlador.set_model(world.mc)

    t0 = 0

    while not glfw.window_should_close(window):  # Dibujando --> 1. obtener el input

        # Calculamos el dt
        ti = glfw.get_time()
        dt = ti - t0
        t0 = ti

        glfw.poll_events()  # OBTIENE EL INPUT --> CONTROLADOR --> MODELOS

        # Clearing the screen in both, color and depth
        glClear(GL_COLOR_BUFFER_BIT)

        world.update(dt, ti)
        world.draw(pipeline)
        world.check_collisions()


        glfw.swap_buffers(window)

    glfw.terminate()