from OpenGL.GLUT import *
from OpenGL.GL import *


def draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glutWireTeapot(0.5)
    glFlush()

def draw_rect():
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1., 1., 1.)
    glPushMatrix()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    glBegin(GL_POLYGON)
    glVertex3f(0.25, 0.25, 0.0)
    glVertex3f(0.75, 0.25, 0.0)
    glVertex3f(0.75, 0.75, 0.0)
    glVertex3f(0.25, 0.75, 0.0)
    glEnd()
    glPopMatrix()
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"My First OpenGL Program")
glutDisplayFunc(draw_rect)
glutMainLoop()
