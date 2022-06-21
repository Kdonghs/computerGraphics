from OpenGL.GLUT import *
from OpenGL.GL import *
import colorsys


def draw_line(length, color):
    glBegin(GL_LINES)
    glColor3d(color[0], color[1], color[2])
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)
    glEnd()

def draw():
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1., 1., 1.)
    glPushMatrix()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    glLineWidth(4.)

    glTranslatef(0.1, 0.1, 0)
    lengths = [0.2, 0.2, 0.2, 0.2, 0.3, 0.3, 0.3]
    colors = [colorsys.hsv_to_rgb(i/len(lengths), 1, 1) for i in range(len(lengths))]
    thetas = [30., 40., -20., -40, 30., -120., -120]
    for l, c, t in zip(lengths, colors, thetas):
        glRotatef(t,0,0, 1)
        draw_line(l, c)
        glTranslatef(l, 0, 0)
    glPopMatrix()
    glFlush()

glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(500, 500)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"My Simple forward kinematics Program")
glutDisplayFunc(draw)
glutMainLoop()
