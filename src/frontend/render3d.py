import os
os.environ['SDL_VIDEO_WINDOW_POS'] = '400,200'

import pygame
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import pyrr
from TextureLoader import load_texture_pygame
from ObjLoader import ObjLoader

from camera import Camera
import os
import math
import numpy as np

basedir = os.path.dirname(os.path.abspath(__file__))

# CAMERA settings
cam = Camera()
WIDTH, HEIGHT = 1280, 720
lastX, lastY = WIDTH / 2, HEIGHT / 2
first_mouse = True


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
        out_color = vec4(v_color, 1.0);   
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
        vertices.append(1.0)
        vertices.append(0.0)
        vertices.append(0.0) 
        # index
        indices.append(ii)
        indices.append((ii+1)%num_segments)
        indices.append((ii+2)%num_segments)

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




pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF | pygame.RESIZABLE) # |pygame.FULLSCREEN
pygame.mouse.set_visible(False)
pygame.event.set_grab(True)

# load here the 3d meshes
earth_indices, earth_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), False, True)
sun_indices, sun_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "sphere.obj"), True, True, 5.0)
floor_indices, floor_buffer = ObjLoader.load_model(os.path.join(basedir, "..", "..", "objects", "floor.obj"))
elipse_indices, elipse_vertices = drawElipse(0, 0, 0.5, 1, 20, 5)
elipse_vertices = np.array(elipse_vertices, dtype=np.float32)
elipse_indices = np.array(elipse_indices, dtype=np.uint32)

shader = compileProgram(compileShader(vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

# VAO and VBO
VAO = glGenVertexArrays(3)
VBO = glGenBuffers(3)
EBO = glGenBuffers(1)

# earth VAO
glBindVertexArray(VAO[0])
# earth Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[0])
glBufferData(GL_ARRAY_BUFFER, earth_buffer.nbytes, earth_buffer, GL_STATIC_DRAW)

glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, earth_indices.nbytes, earth_indices, GL_STATIC_DRAW)

# earth vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, earth_buffer.itemsize * 8, ctypes.c_void_p(0))
# earth textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, earth_buffer.itemsize * 8, ctypes.c_void_p(12))
# earth normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, earth_buffer.itemsize * 8, ctypes.c_void_p(20))
glEnableVertexAttribArray(2)

# sun VAO
glBindVertexArray(VAO[1])
# sun Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[1])
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

# floor VAO
glBindVertexArray(VAO[2])
# floor Vertex Buffer Object
glBindBuffer(GL_ARRAY_BUFFER, VBO[2])
glBufferData(GL_ARRAY_BUFFER, floor_buffer.nbytes, floor_buffer, GL_STATIC_DRAW)

# floor vertices
glEnableVertexAttribArray(0)
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(0))
# floor textures
glEnableVertexAttribArray(1)
glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(12))
# floor normals
glVertexAttribPointer(2, 3, GL_FLOAT, GL_FALSE, floor_buffer.itemsize * 8, ctypes.c_void_p(20))
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
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, elipse_vertices.itemsize * 6, ctypes.c_void_p(0))

glEnableVertexAttribArray(1)
glVertexAttribPointer(3, 3, GL_FLOAT, GL_FALSE, elipse_vertices.itemsize * 6, ctypes.c_void_p(12))


textures = glGenTextures(3)
load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_earth.jpg"), textures[0])
load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_sun.jpg"), textures[1])
load_texture_pygame(os.path.join(basedir, "..", "..", "textures", "2k_uranus.jpg"), textures[2])

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

projection = pyrr.matrix44.create_perspective_projection_matrix(45, 1280 / 720, 0.1, 100)
earth_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([6, 0, 0]))
sun_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([-4, 0, -4]))
floor_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0, 0]))
elipse_pos = pyrr.matrix44.create_from_translation(pyrr.Vector3([0, 0.1, 0.1]))

model_loc = glGetUniformLocation(shader, "model")
proj_loc = glGetUniformLocation(shader, "projection")
view_loc = glGetUniformLocation(shader, "view")

glUniformMatrix4fv(proj_loc, 1, GL_FALSE, projection)

running = True

while running:
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
        cam.process_keyboard("LEFT", 0.01)
    if keys_pressed[pygame.K_d]:
        cam.process_keyboard("RIGHT", 0.01)
    if keys_pressed[pygame.K_w]:
        cam.process_keyboard("FORWARD", 0.01)
    if keys_pressed[pygame.K_s]:
        cam.process_keyboard("BACKWARD", 0.01)
    if keys_pressed[pygame.K_SPACE]:
        cam.process_keyboard("UP", 0.01)
    if keys_pressed[pygame.K_LCTRL]:
        cam.process_keyboard("DOWN", 0.01)


    mouse_pos = pygame.mouse.get_pos()
    mouse_look(mouse_pos[0], mouse_pos[1], WIDTH, HEIGHT)

    # to been able to look around 360 degrees, still not perfect


    ct = pygame.time.get_ticks() / 1000

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    view = cam.get_view_matrix()
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)

    rot_y = pyrr.Matrix44.from_y_rotation(0.8 * ct)
    rot_elipse_y = pyrr.Matrix44.from_y_rotation(0.1 * ct)
    rot_elipse_x = pyrr.Matrix44.from_x_rotation(0.8 * ct)
    model = pyrr.matrix44.multiply(rot_y, earth_pos)

    # draw the earth
    glBindVertexArray(VAO[0])
    glBindTexture(GL_TEXTURE_2D, textures[0])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawElements(GL_TRIANGLES, len(earth_indices), GL_UNSIGNED_INT, None)

    # draw the sun
    glBindVertexArray(VAO[1])
    glBindTexture(GL_TEXTURE_2D, textures[1])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, sun_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(sun_indices))

    # draw the floor
    glBindVertexArray(VAO[2])
    glBindTexture(GL_TEXTURE_2D, textures[2])
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, floor_pos)
    glDrawArrays(GL_TRIANGLES, 0, len(floor_indices))

    # draw the elipse
    model = pyrr.matrix44.multiply(rot_elipse_x, elipse_pos)
    model = pyrr.matrix44.multiply(rot_elipse_y, model)
    glBindVertexArray(elipse_VAO)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)
    glDrawElements(GL_TRIANGLES, len(elipse_indices), GL_UNSIGNED_INT, None)


    pygame.display.flip()

pygame.quit()
