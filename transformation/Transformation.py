from OpenGL.GLUT import *
from OpenGL.GL import *

deg = 19.

def draw():
    global deg
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1., 1., 1.)
    glPushMatrix()
    glOrtho(0.0, 1.0, 0.0, 1.0, -1.0, 1.0)
    glLineWidth(1.)

    glTranslatef(-0.3, 0.15, 0)
    for i in range(19):
        # rect at (0.5, 0.5, 0.)
        glBegin(GL_LINE_LOOP)
        glVertex3f(0.50, 0.50, 0.0)
        glVertex3f(0.65, 0.50, 0.0)
        glVertex3f(0.65, 0.65, 0.0)
        glVertex3f(0.50, 0.65, 0.0)
        glEnd()

        # rotate 45 deg
        glPushMatrix()
        glTranslatef(0.47, 0.4, 0)  # T^-1
        glRotatef(deg, 0, 0, 1)  # R
        glTranslatef(-0.5, -0.5, 0)  # T        glPopMatrix()
        # end.

    glPopMatrix()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(250, 250)
glutInitWindowPosition(800, 200)
glutCreateWindow(b"My Second OpenGL Program")
glutDisplayFunc(draw)
glutMainLoop()