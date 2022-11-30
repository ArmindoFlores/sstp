import os

os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

import json
import math
import os
import socket

import numpy as np
import pygame
import pyrr
from camera import Camera
from ObjLoader import ObjLoader
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from TextureLoader import load_texture_pygame

basedir = os.path.dirname(os.path.abspath(__file__))

# CAMERA settings
cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True

SIZES = {'mercury': 2439.7, 'venus': 6051.8, 'earth': 6378, 'mars': 3389.5, 'jupiter': 69911, 'saturn': 58232, 'uranus': 25362, 'neptune': 246222}


vertex_src = """
# version 330

layout(location = 0) in vec3 a_position;
layout(location = 1) in vec2 a_texture;
layout(location = 2) in vec3 a_normal;
layout(location = 3) in vec3 a_color;

uniform mat4 model;
uniform mat4 projection;
uniform mat4 view;

out vec3 v_color;
out vec2 v_texture;

void main()
{
    vec4 pos = view * model * vec4(a_position, 1.0);
    gl_Position = projection * view * model * vec4(a_position, 1.0);
    v_texture = a_texture;
    v_color = a_color;
}
"""

fragment_src = """
# version 330

in vec2 v_texture;
in vec3 v_color;

out vec4 out_color;
uniform int switcher;

uniform sampler2D s_texture;

void main()
{
    if (switcher == 0){
        out_color = texture(s_texture, v_texture);
    }
    else if (switcher == 1){
        out_color = vec4(1.0, 1.0, 0, 1.0);   
    }
    else if (switcher == 2){
        out_color = vec4(1.0, 0, 0, 1.0);   
    }
    
}
"""

def drawElipse(cx, cy, rx, ry, num_segments, amplify=1.0):
    vertices = []
    indices = []
    theta = 2 * math.pi / float(num_segments)
    c = math.cos(theta)
    s = math.sin(theta);
    t = 0

    x = 1
    y = 0

    for ii in range(num_segments):
        # vertex position 
        vertices.append((x * rx + cx)*amplify)
        vertices.append(0)
        vertices.append((y * ry + cy)*amplify) 
        # colour
        """ vertices.append(1.0)
        vertices.append(0.0)
        vertices.append(0.0) """
        # index
        indices.append(ii)
        indices.append((ii+1)%num_segments)
        # indices.append((ii+2)%num_segments)

        t = x
        x = c * x - s * y
        y = s * t + c * y

    return indices, vertices

def mouse_look(xpos, ypos, maxX, maxY):
    global first_mouse, lastX, lastY, lastXOffset

    if first_mouse:
        lastX = xpos
        lastY = ypos
        first_mouse = False
        lastXOffset = 0

    if xpos == maxX-1 and xpos == lastX:
        if lastXOffset > 0.5:
            lastXOffset = 0.5
        xoffset = lastXOffset
    elif xpos == 0 and xpos == lastX:
        if lastXOffset < -0.5:
            lastXOffset = -0.5
        xoffset = lastXOffset
    else:
        xoffset = xpos - lastX
        lastXOffset = xoffset

    """ if ypos == maxY-1 and ypos == lastY:
        yoffset = 1
    elif ypos == 0 and ypos == lastY:
        yoffset = -1
    else: """
    yoffset = lastY - ypos

    lastX = xpos
    lastY = ypos

    cam.process_mouse_movement(xoffset, yoffset)

def get_positions():
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    sock.connect("/tmp/sstp_socket")
    sock.sendall(b'{"type": "get_planet_positions"}\x00')
    data = sock.recv(4096)
    positions = np.array(json.loads(data))
    return positions

def main():
    pygame.init()
    pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE) # |pygame.FULLSCREEN
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    minimum = SIZES["mercury"]

    # load here the 3d meshes 
    mercury_indices, mercury_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["mercury"]/minimum)
    venus_indices, venus_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["venus"]/minimum)
    earth_indices, earth_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["earth"]/minimum)
    mars_indices, mars_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["mars"]/minimum)
    jupiter_indices, jupiter_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["jupiter"]/minimum)
    saturn_indices, saturn_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["saturn"]/minimum)
    uranus_indices, uranus_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["uranus"]/minimum)
    neptune_indices, neptune_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["neptune"]/minimum)
    sun_indices, sun_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, SIZES["jupiter"]/minimum * 2)
    elipse_indices, elipse_vertices = drawElipse(0, 0, 0.5, 1, 200, 5)
    elipse_vertices = np.array(elipse_vertices, dtype=np.float32)
    elipse_indices = np.array(elipse_indices, dtype=np.uint32)

    shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

    # VAO and VBO
    VAO = glGenVertexArrays(9)
    VBO = glGenBuffers(9)
    #EBO = glGenBuffers(1)

    # mercury VAO
    glBindVertexArray(VAO[0])
    # mercury Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
    glBufferData(GL_ARRAY_BUFFER, mercury_buffer.nbytes, mercury_buffer, GL_STATIC_DRAW)

    # mercury vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, mercury_buffer.itemsize * 8, ctypes.c_void_p(0))
    # mercury textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, mercury_buffer.itemsize * 8, ctypes.c_void_p(12))
    # mercury normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, mercury_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # venus VAO
    glBindVertexArray(VAO[1])
    # venus Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
    glBufferData(GL_ARRAY_BUFFER, venus_buffer.nbytes, venus_buffer, GL_STATIC_DRAW)

    # venus vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, venus_buffer.itemsize * 8, ctypes.c_void_p(0))
    # venus textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, venus_buffer.itemsize * 8, ctypes.c_void_p(12))
    # venus normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, venus_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # earth VAO
    glBindVertexArray(VAO[2])
    # earth Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
    glBufferData(GL_ARRAY_BUFFER, earth_buffer.nbytes, earth_buffer, GL_STATIC_DRAW)

    # earth vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, earth_buffer.itemsize * 8, ctypes.c_void_p(0))
    # earth textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, earth_buffer.itemsize * 8, ctypes.c_void_p(12))
    # earth normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, earth_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # mars VAO
    glBindVertexArray(VAO[3])
    # mars Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[3])
    glBufferData(GL_ARRAY_BUFFER, mars_buffer.nbytes, mars_buffer, GL_STATIC_DRAW)

    # mars vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, mars_buffer.itemsize * 8, ctypes.c_void_p(0))
    # mars textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, mars_buffer.itemsize * 8, ctypes.c_void_p(12))
    # mars normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, mars_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # jupiter VAO
    glBindVertexArray(VAO[4])
    # jupiter Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[4])
    glBufferData(GL_ARRAY_BUFFER, jupiter_buffer.nbytes, jupiter_buffer, GL_STATIC_DRAW)

    # jupiter vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, jupiter_buffer.itemsize * 8, ctypes.c_void_p(0))
    # jupiter textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, jupiter_buffer.itemsize * 8, ctypes.c_void_p(12))
    # jupiter normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, jupiter_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # saturn VAO
    glBindVertexArray(VAO[5])
    # saturn Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[5])
    glBufferData(GL_ARRAY_BUFFER, saturn_buffer.nbytes, saturn_buffer, GL_STATIC_DRAW)

    # saturn vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, saturn_buffer.itemsize * 8, ctypes.c_void_p(0))
    # saturn textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, saturn_buffer.itemsize * 8, ctypes.c_void_p(12))
    # saturn normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, saturn_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # uranus VAO
    glBindVertexArray(VAO[6])
    # uranus Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[6])
    glBufferData(GL_ARRAY_BUFFER, uranus_buffer.nbytes, uranus_buffer, GL_STATIC_DRAW)

    # uranus vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, uranus_buffer.itemsize * 8, ctypes.c_void_p(0))
    # uranus textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, uranus_buffer.itemsize * 8, ctypes.c_void_p(12))
    # uranus normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, uranus_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # neptune VAO
    glBindVertexArray(VAO[7])
    # neptune Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[7])
    glBufferData(GL_ARRAY_BUFFER, neptune_buffer.nbytes, neptune_buffer, GL_STATIC_DRAW)

    # neptune vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, neptune_buffer.itemsize * 8, ctypes.c_void_p(0))
    # neptune textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, neptune_buffer.itemsize * 8, ctypes.c_void_p(12))
    # neptune normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, neptune_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    ########################################################

    # sun VAO
    glBindVertexArray(VAO[8])
    # sun Vertex Buffer Object
    glBindBuffer(GL_ARRAY_BUFFER, VBO[8])
    glBufferData(GL_ARRAY_BUFFER, sun_buffer.nbytes, sun_buffer, GL_STATIC_DRAW)

    # sun vertices
    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, sun_buffer.itemsize * 8, ctypes.c_void_p(0))
    # sun textures
    glEnableVertexAttribArray(1)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, sun_buffer.itemsize * 8, ctypes.c_void_p(12))
    # sun normals
    glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, sun_buffer.itemsize * 8, ctypes.c_void_p(20))
    glEnableVertexAttribArray(2)

    # elipse VAO
    elipse_VAO = glGenVertexArrays(1)
    glBindVertexArray(elipse_VAO)

    # elipse Vertex Buffer Object
    elipse_VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, elipse_VBO)
    glBufferData(GL_ARRAY_BUFFER, elipse_vertices.nbytes, elipse_vertices, GL_STATIC_DRAW)

    # elipse Element Buffer Object
    elipse_EBO = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, elipse_EBO)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, elipse_indices.nbytes, elipse_indices, GL_STATIC_DRAW)

    glEnableVertexAttribArray(0)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, elipse_vertices.itemsize * 3, ctypes.c_void_p(0))

    """ glEnableVertexAttribArray(1)
    glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, elipse_vertices.itemsize * 6, ctypes.c_void_p(12)) """


    textures = glGenTextures(9)
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_mercury.jpg"), textures[0])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_venus.jpg"), textures[1])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_earth.jpg"), textures[2])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_mars.jpg"), textures[3])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_jupiter.jpg"), textures[4])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_saturn.jpg"), textures[5])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_uranus.jpg"), textures[6])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_neptune.jpg"), textures[7])
    load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_sun.jpg"), textures[8])

    glUseProgram(shader)
    glClearColor(0, 0.1, 0.1, 1)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 1000)
    mercury_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-15, 0, 0]))
    venus_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-30, 0, 0]))
    earth_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-45, 0, 0]))
    mars_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-60, 0, 0]))
    jupiter_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-75, 0, 0]))
    saturn_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-90, 0, 0]))
    uranus_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-105, 0, 0]))
    neptune_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-130, 0, 0]))
    sun_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
    elipse_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0.0, 0.0]))

    model_loc = glGetUniformLocation(shader, "model")
    proj_loc = glGetUniformLocation(shader, "projection")
    view_loc = glGetUniformLocation(shader, "view")
    switcher_loc = glGetUniformLocation(shader, "switcher")

    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

    running = True

    i = 0
    speed = 0.04

    while running:
        i+=1
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif  event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

            if event.type == pygame.VIDEORESIZE:
                glViewport(0, 0, event.w, event.h)
                projection = pyrr.matrix44.create_perspective_projection_matrix(45, event.w / event.h, 0.1, 100)
                glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_a]:
            cam.process_keyboard("LEFT", speed)
        if keys_pressed[pygame.K_d]:
            cam.process_keyboard("RIGHT", speed)
        if keys_pressed[pygame.K_w]:
            cam.process_keyboard("FORWARD", speed)
        if keys_pressed[pygame.K_s]:
            cam.process_keyboard("BACKWARD", speed)
        if keys_pressed[pygame.K_SPACE]:
            cam.process_keyboard("UP", speed)
        if keys_pressed[pygame.K_LCTRL]:
            cam.process_keyboard("DOWN", speed)


        mouse_pos = pygame.mouse.get_pos()
        mouse_look(mouse_pos[0], mouse_pos[1], WIDTH, HEIGHT)



        ct = pygame.time.get_ticks() / 1000

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        glUniform1i(switcher_loc, 0)

        view = cam.get_view_matrix()
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

        rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)
        rot_elipse_y = pyrr.Matrix44.from_y_rotation(0.1 * ct)
        rot_elipse_x = pyrr.Matrix44.from_x_rotation(0.8 * ct)

        #model = pyrr.matrix44.multiply(rot_y, earth_pos)

        positions = 5*get_positions() / 1e7

        
        # draw mercury
        glBindVertexArray(VAO[0])
        glBindTexture(GL_TEXTURE_2D, textures[0])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[0]))
        glDrawArrays(GL_TRIANGLES, 0, len(mercury_indices))

        # draw the venus
        glBindVertexArray(VAO[1])
        glBindTexture(GL_TEXTURE_2D, textures[1])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[1]))
        glDrawArrays(GL_TRIANGLES, 0, len(venus_indices))

        # draw the earth
        glBindVertexArray(VAO[2])
        glBindTexture(GL_TEXTURE_2D, textures[2])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[2]))
        glDrawArrays(GL_TRIANGLES, 0, len(earth_indices))

        # draw the mars
        glBindVertexArray(VAO[3])
        glBindTexture(GL_TEXTURE_2D, textures[3])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[3]))
        glDrawArrays(GL_TRIANGLES, 0, len(mars_indices))

        # draw the jupiter
        glBindVertexArray(VAO[4])
        glBindTexture(GL_TEXTURE_2D, textures[4])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[4]))
        glDrawArrays(GL_TRIANGLES, 0, len(jupiter_indices))

        # draw the saturn
        glBindVertexArray(VAO[5])
        glBindTexture(GL_TEXTURE_2D, textures[5])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[5]))
        glDrawArrays(GL_TRIANGLES, 0, len(saturn_indices))

        # draw the uranus
        glBindVertexArray(VAO[6])
        glBindTexture(GL_TEXTURE_2D, textures[6])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[6]))
        glDrawArrays(GL_TRIANGLES, 0, len(uranus_indices))

        # draw the neptune
        glBindVertexArray(VAO[7])
        glBindTexture(GL_TEXTURE_2D, textures[7])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, pyrr.matrix44.create_from_translation(positions[7]))
        glDrawArrays(GL_TRIANGLES, 0, len(neptune_indices))

        # draw the sun
        glBindVertexArray(VAO[8])
        glBindTexture(GL_TEXTURE_2D, textures[8])
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, sun_pos)
        glDrawArrays(GL_TRIANGLES, 0, len(sun_indices))

        # draw the elipse
        model = pyrr.matrix44.multiply(rot_elipse_x, elipse_pos)
        model = pyrr.matrix44.multiply(rot_elipse_y, model)
        glBindVertexArray(elipse_VAO)
        glUniform1i(switcher_loc, 2)
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
        glDrawElements(GL_LINES, len(elipse_indices), GL_UNSIGNED_INT, None)


        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    try:
        main()
    except RuntimeError as err:
        print(err.args[0])
    