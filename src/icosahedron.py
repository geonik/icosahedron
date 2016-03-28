#!/usr/bin/env python3

import pyglet
from pyglet.gl import *
from ctypes import *
import math


# Direct OpenGL commands to this window.
window = pyglet.window.Window()

LIGHT_INDEX = 0
MATERIAL_INDEX = 0

ROTATION_SPEED = 1
X_ANGLE = 0
Y_ANGLE = 0

TRANSFER_SPEED = 1
X_TRANSFER = 0
Y_TRANSFER = 0

@window.event
def on_resize(width, height):
    print('on_resize')
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, width, 0, height, -1000, 1000)
    glMatrixMode(GL_MODELVIEW)
    return pyglet.event.EVENT_HANDLED


@window.event
def on_key_press(symbol, modifiers):
    global LIGHT_INDEX
    global MATERIAL_INDEX
    global X_TRANSFER
    global X_ANGLE
    global Y_ANGLE
    global X_TRANSFER
    global Y_TRANSFER

    if symbol == pyglet.window.key.L:
        LIGHT_INDEX += 1
    if symbol == pyglet.window.key.M:
        MATERIAL_INDEX += 1
    if symbol == pyglet.window.key.R:
        X_ANGLE = 0
        Y_ANGLE = 0
        X_TRANSFER = 0
        Y_TRANSFER = 0
        LIGHT_INDEX = 0
        MATERIAL_INDEX = 0


@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    global X_ANGLE
    global Y_ANGLE
    global X_TRANSFER
    global Y_TRANSFER
    global ROTATION_SPEED
    global TRANSFER_SPEED

    if modifiers & pyglet.window.key.MOD_SHIFT:
        Y_ANGLE += dx * ROTATION_SPEED
        X_ANGLE += dy * ROTATION_SPEED
    else:
        X_TRANSFER += dx * TRANSFER_SPEED
        Y_TRANSFER += dy * TRANSFER_SPEED

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glEnable(GL_DEPTH_TEST)
    light_scene()
    apply_transforms()
    draw_icosahedron()
    glFlush()


def apply_transforms():
    global X_ANGLE
    global Y_ANGLE
    global X_TRANSFER
    global Y_TRANSFER

    # Standard offset
    glTranslatef(100.0, 100.0, 100.0);

    # User input offsets
    glTranslatef(X_TRANSFER, Y_TRANSFER, 0.0)
    glRotatef(X_ANGLE, -1.0, 0.0, 0.0);
    glRotatef(Y_ANGLE, 0.0, 1.0, 0.0);

def light_scene():
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    global LIGHT_INDEX
    light_positions = [ 
            (GLfloat * 4)(0.0, 1.0, 0.0, 0.0),
            (GLfloat * 4)(0.0, -1.0, 0.0, 0.0),
            (GLfloat * 4)(1.0, 0.0, 0.0, 0.0),
            (GLfloat * 4)(-1.0, 0.0, 0.0, 0.0),
            (GLfloat * 4)(0.0, 0.0, 1.0, 0.0),
            (GLfloat * 4)(0.0, 0.0, -1.0, 0.0),
            (GLfloat * 4)(1.0, 1.0, 1.0, 0.0),
            (GLfloat * 4)(-1.0, -1.0, -1.0, 0.0),
            ]
    if LIGHT_INDEX >= len(light_positions):
        LIGHT_INDEX = 0
    glLightfv(GL_LIGHT0, GL_POSITION, light_positions[LIGHT_INDEX])

def draw_icosahedron():
    
    global MATERIAL_INDEX
    X = .525731112119133606 * 100
    Z = .850650808352039932 * 100
    vertices = [     
               [-X, 0.0, Z],
               [X, 0.0, Z],
               [-X, 0.0, -Z],
               [X, 0.0, -Z], 
               [0.0, Z, X],
               [0.0, Z, -X],
               [0.0, -Z, X],
               [0.0, -Z, -X], 
               [Z, X, 0.0,], 
               [-Z, X, 0.0,], 
               [Z, -X, 0.0,],
               [-Z, -X, 0.0]]
    tindices = [ 
               [0,4,1], [0,9,4], [9,5,4], [4,5,8], [4,8,1],    
               [8,10,1], [8,3,10], [5,3,8], [5,2,3], [2,7,3],    
               [7,10,3], [7,6,10], [7,11,6], [11,0,6], [0,1,6], 
               [6,1,10], [9,0,11], [9,11,2], [9,2,5], [7,2,11] ];
    materials = [
                (GLfloat * 4)(0.6, 0.6, 0.6,1.0),
                (GLfloat * 4)(0.6, 0.0, 0.0,1.0),
                (GLfloat * 4)(0.0, 0.6, 0.0,1.0),
                (GLfloat * 4)(0.0, 0.0, 0.6,1.0),
            ]
    if MATERIAL_INDEX >= len(materials):
        MATERIAL_INDEX = 0

    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, materials[MATERIAL_INDEX])

    glBegin(GL_TRIANGLES)
    for triangle in tindices:
        for vertex_index in triangle:
            glNormal3f(*vertices[vertex_index])
            glVertex3f(*vertices[vertex_index])
    glEnd()
    
angle = 0
draw_index = 0

pyglet.app.run()
