from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np



def draw_lines(points, color):
    glColor3d(color[0], color[1], color[2])
    glBegin(GL_LINE_STRIP)
    for x, y, z in points:
        glVertex3f(x, y, z)
    glEnd()


def draw_points(points, color):
    glPointSize(10)
    glColor3d(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    for x, y, z in points:
        glVertex3f(x, y, z)
    glEnd()


def natural_cubic(points, t=30):
    ts = np.linspace(0, 1, t)

    # 10.Keyframe Animation Smooth Curves.pdf page 40.
    # Keyframe interpolation.pdf page 8.

    ta = np.array([
        [t ** 3, t ** 2, t, 1] for t in [0, 1 / 3, 2 / 3, 1]
    ])
    coeffs = np.linalg.solve(ta, points)

    results = []
    for t in ts:
        tv = np.array([t ** 3, t ** 2, t, 1])
        results.append(tv @ coeffs)

    return results


def hermite(points, t=30):
    ts = np.linspace(0, 1, t)

    # 10.Keyframe Animation Smooth Curves.pdf page 68.
    # Keyframe interpolation.pdf page 11.

    permute_mat = np.array([
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [0, 1, 0, 0],
        [0, 0, 1, 0],
    ])

    mat = np.array([
        [2, -2, 1, 1],
        [-3, 3, -2, -1],
        [0, 0, 1, 0],
        [1, 0, 0, 0],
    ])

    results = []

    for t in ts:
        # some codes here
        tv = np.array([t ** 3, t ** 2, t, 1])
        results.append(tv @ mat @ permute_mat @ points)

    return results


def bezier(points, t=30):
    ts = np.linspace(0, 1, t)

    # 10.Keyframe Animation Smooth Curves.pdf page 77.
    # Keyframe interpolation.pdf page 25.
    mat =np.array([
        [-1, 3, -3, 1],
        [3, -6, 3, 0],
        [-3, 3, 0, 0],
        [1, 0, 0, 0],
    ])

    results = []

    for t in ts:
        # some codes here
        tv = np.array([t ** 3, t ** 2, t, 1])
        results.append(tv @ mat @ points)
        pass

    return results


p1s = np.array([[-1.5, 0.5, 1], [-0.5, 1.5, 1], [0.5, 1.5, 1], [1.5, 0.5, 1]])
p2s = np.array([[-1.5, 1.5, 1], [-0.5, 0.5, 1], [0.5, 1.5, 1], [1.5, 0.5, 1]])


def draw():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1., 1., 1.)
    glPushMatrix()
    glLineWidth(4.)

    glTranslatef(0, -1, 0)

    glPushMatrix()
    glTranslatef(-2, 2.5, 0)
    lns = natural_cubic(p1s)
    # draw cubic lines
    draw_lines(lns, [0., 0.5, 0.5])
    # draw interpolation points
    draw_points(p1s, [1., 0., 0.])
    # draw (0, 0) point
    draw_points([[0., 0., 0.]], [0., 0., 1.])
    glPopMatrix()
    glPushMatrix()
    glTranslatef(2, 2.5, 0)
    lns = natural_cubic(p2s)
    draw_lines(lns, [0., 0.5, 0.5])
    draw_points(p2s, [1., 0., 0.])
    draw_points([[0., 0., 0.]], [0., 0., 1.])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2, 0, 0)
    lns = hermite(p1s)
    draw_lines(lns, [0., 0.5, 0.5])
    draw_points(p1s, [1., 0., 0.])
    draw_points([[0., 0., 0.]], [0., 0., 1.])
    glPopMatrix()
    glPushMatrix()
    glTranslatef(2, 0, 0)
    lns = hermite(p2s)
    draw_lines(lns, [0., 0.5, 0.5])
    draw_points(p2s, [1., 0., 0.])
    draw_points([[0., 0., 0.]], [0., 0., 1.])
    glPopMatrix()

    glPushMatrix()
    glTranslatef(-2, -2.5, 0)
    lns = bezier(p1s)
    draw_lines(lns, [0., 0.5, 0.5])
    draw_points(p1s, [1., 0., 0.])
    draw_points([[0., 0., 0.]], [0., 0., 1.])
    glPopMatrix()
    glPushMatrix()
    glTranslatef(2, -2.5, 0)
    lns = bezier(p2s)
    draw_lines(lns, [0., 0.5, 0.5])
    draw_points(p2s, [1., 0., 0.])
    draw_points([[0., 0., 0.]], [0., 0., 1.])
    glPopMatrix()

    glPopMatrix()
    glFlush()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"My Simple Splines")
glMatrixMode(GL_PROJECTION)
glOrtho(-4, 4, -4, 4, 0, 20)
gluLookAt(0, 0, 10, 0, 0, 0, 0, 1, 0)
glutDisplayFunc(draw)
glutMainLoop()
