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


def fk(center, lengths, thetas):
    points = [center]
    for i in range(len(lengths)):
        parent = points[i]
        length = lengths[i]
        theta = np.sum(thetas[:i + 1])
        point = parent + np.array([length * np.cos(theta), length * np.sin(theta), 0])
        points.append(point)

    return points


def build_jacobian(lengths, thetas):
    j = np.zeros([2, len(lengths)])  # 2 x n

    # build jacobian here
    for x in range(len(lengths)):
        j[0][0] += -lengths[x] * np.sin(sum(thetas[:x+1]))
        j[1][0] += lengths[x] * np.cos(sum(thetas[:x+1]))
        j[0][x] = -lengths[x] * np.sin(sum(thetas[:x+1]))
        j[1][x] = lengths[x] * np.cos(sum(thetas[:x+1]))
    return j


def ik(ef_point, center, lengths, thetas):
    points = fk(center, lengths, thetas)
    residual = (ef_point - points[-1])[:2]  # J dt = c - f(t)

    new_theta = thetas.copy()
    for _ in range(100):
        j = build_jacobian(lengths, new_theta)
        dt = np.linalg.solve(j.T @ j + 0.1 * np.eye(j.shape[1]), j.T @ residual)
        new_theta += 0.5 * dt
        points = fk(center, lengths, new_theta)
        residual = (ef_point - points[-1])[:2]

    return new_theta


center = np.array([0.25, 0.25, 1])
lengths = [[0.2], [0.1, 0.1], [0.0666, 0.0666, 0.0666], [0.05, 0.05, 0.05, 0.05]]
thetas = [np.array([np.pi / 20 for _ in length]) for length in lengths]
transs = [[0., 0., 0.], [0.5, 0., 0.], [0., -0.5, 0.], [0.5, -0.5, 0.]]


def draw():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1., 1., 1.)
    glPushMatrix()
    glLineWidth(2)

    glTranslatef(0., 0.5, 0.)

    # end effector pos
    ex = cx % 0.5
    ey = (1 - cy) % 0.5
    ef_point = np.array([ex, ey, 1])

    for i, (trans, length, theta) in enumerate(zip(transs, lengths, thetas)):
        glPushMatrix()
        glTranslatef(trans[0], trans[1], trans[2])
        print(theta)
        thetas[i] = ik(ef_point, center, length, theta)
        points = fk(center, length, theta)
        draw_lines(points, [1., 1., 1.])
        draw_points(points, [0., 1., 1.])
        # draw end effector
        draw_points([ef_point], [1., 0., 0.])

        glPopMatrix()

    glPopMatrix()
    glFlush()


cx = 0.
cy = 0.


def mouse(button, state, x, y):
    global cx, cy

    if button == GLUT_LEFT_BUTTON:
        leftMouseButtonDown = (state == GLUT_DOWN)
        if leftMouseButtonDown:
            print('Clicked')
            print(x / cw, y / ch)
            cx = x / cw
            cy = y / ch

    elif button == GLUT_RIGHT_BUTTON:
        rightMouseButtonDown = (state == GLUT_DOWN)

    mouseXPos = x
    mouseYPos = y
    # print(x/cw, y/ch)


cw = 1000
ch = 1000


def reshaped(w, h):
    global cw, ch
    cw = w
    ch = h
    glViewport(0, 0, w, h)


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(cw, ch)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"My Simple Inverse Kinematics")
glMatrixMode(GL_PROJECTION)
glOrtho(0, 1, 0, 1, 0, 20)
gluLookAt(0.0, 0.0, 10, 0.0, 0.0, 0, 0, 1, 0)
glutDisplayFunc(draw)
glutReshapeFunc(reshaped)
glutMouseFunc(mouse)
glutMainLoop()
