from lib2to3.fixer_util import p1, p2

from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import time
import math


def rx(theta):
    r = np.zeros([4, 4])
    c = np.cos(theta)
    s = np.sin(theta)
    r[0, 0] = 1
    r[1, 1] = c
    r[1, 2] = -s
    r[2, 1] = s
    r[2, 2] = c
    r[3, 3] = 1

    return r


def ry(theta):
    r = np.zeros([4, 4])
    c = np.cos(theta)
    s = np.sin(theta)
    r[1, 1] = 1
    r[0, 0] = c
    r[0, 2] = s
    r[2, 0] = -s
    r[2, 2] = c
    r[3, 3] = 1

    return r


def rz(theta):
    r = np.zeros([4, 4])
    c = np.cos(theta)
    s = np.sin(theta)
    r[0, 0] = c
    r[0, 1] = -s
    r[1, 0] = s
    r[1, 1] = c
    r[2, 2] = 1
    r[3, 3] = 1

    return r


def q_to_transform(q, tx=0, ty=0, tz=0):
    qw = q[0]
    qx = q[1]
    qy = q[2]
    qz = q[3]

    x2 = qx + qx;
    y2 = qy + qy;
    z2 = qz + qz
    xx = qx * x2;
    yy = qy * y2;
    wx = qw * x2
    xy = qx * y2;
    yz = qy * z2;
    wy = qw * y2
    xz = qx * z2;
    zz = qz * z2;
    wz = qw * z2

    m = [0 for _ in range(16)]
    m[0 * 4 + 0] = 1.0 - (yy + zz)
    m[0 * 4 + 1] = xy - wz
    m[0 * 4 + 2] = xz + wy
    m[1 * 4 + 0] = xy + wz
    m[1 * 4 + 1] = 1.0 - (xx + zz)
    m[1 * 4 + 2] = yz - wx
    m[2 * 4 + 0] = xz - wy
    m[2 * 4 + 1] = yz + wx
    m[2 * 4 + 2] = 1.0 - (xx + yy)
    m[3] = tx
    m[7] = ty
    m[11] = tz
    m[15] = 1.

    # transpose for gl
    nm = [0 for _ in range(16)]
    for i in range(4):
        for j in range(4):
            nm[j * 4 + i] = m[i * 4 + j]

    return nm


def draw_axis(length, linewidth):
    glBegin(GL_POLYGON)
    # xy plane
    glColor3f(1, 1, 0)
    glVertex3f(0.25, 0.25, 0.0)
    glVertex3f(0.75, 0.25, 0.0)
    glVertex3f(0.75, 0.75, 0.0)
    glVertex3f(0.25, 0.75, 0.0)

    glEnd()

    glBegin(GL_POLYGON)
    # yz plane
    glColor3f(0, 1, 1)
    glVertex3f(0.0, 0.25, 0.25)
    glVertex3f(0.0, 0.75, 0.25)
    glVertex3f(0.0, 0.75, 0.75)
    glVertex3f(0.0, 0.25, 0.75)
    glEnd()

    glBegin(GL_POLYGON)
    # zx plane
    glColor3f(1, 0, 1)
    glVertex3f(0.25, 0.0, 0.25)
    glVertex3f(0.75, 0.0, 0.25)
    glVertex3f(0.75, 0.0, 0.75)
    glVertex3f(0.25, 0.0, 0.75)

    glEnd()

    glLineWidth(linewidth)
    glBegin(GL_LINES)
    # draw x
    glColor3f(1, 0, 0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(length, 0.0, 0.0)

    # draw y
    glColor3f(0, 1, 0)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, length, 0.0)

    # draw z
    glColor3f(0, 0, 1)
    glVertex3f(0.0, 0.0, 0.0)
    glVertex3f(0.0, 0.0, length)
    glEnd()


timestep = 0.
frame = 1 / 60.
repeat_intv = 4.

q_source = np.array([0.44496884, 0.52699965, -0.33075, -0.64411065])
q_target = -np.array([0.54443759, -0.53286634, -0.14169922, 0.63210957])
q_src_euler = np.array([1.32373404, 0.39471518, -1.6234128])
q_tgt_euler = np.array([-1.09430823, 0.54611012, 1.38159701])


def euler_lerp(rxo, ryo, rzo, rxt, ryt, rzt, ts, ox, oy, oz, tx, ty, tz):
    ts = (ts % repeat_intv) / repeat_intv
    # lerp code here ;)
    rxo = (1 - ts) * rxo + ts * rxt
    ryo = (1 - ts) * ryo + ts * ryt
    rzo = (1 - ts) * rzo + ts * rzt

    t = rz(rzo) @ ry(ryo) @ rx(rxo)
    t[0, 3] = (1 - ts) * ox + ts * tx
    t[1, 3] = (1 - ts) * oy + ts * ty
    t[2, 3] = (1 - ts) * oz + ts * tz

    return t.T


def q_slerp(qo, qt, ts, ox, oy, oz, tx, ty, tz):
    ts = (ts % repeat_intv) / repeat_intv
    # slerp code here ;)
    a = np.arccos(qo * qt)
    qo = (np.sin((1 - ts) * a) / np.sin(a)) * qo + (np.sin(ts * a) / np.sin(a)) * qt

    q = qo
    return q_to_transform(q, (1 - ts) * ox + ts * tx, (1 - ts) * oy + ts * ty, (1 - ts) * oz + ts * tz)


def draw():
    global timestep
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    # glColor3f(1., 1., 1.)

    # draw source
    # lerp origin
    glLoadMatrixf(q_to_transform(q_source, -5, 5))
    draw_axis(2, 3)
    # slerp origin
    glLoadMatrixf(q_to_transform(q_source, -5, 0))
    draw_axis(2, 3)
    # slerp, lerp both origin
    glLoadMatrixf(q_to_transform(q_source, -5, -5))
    draw_axis(2, 3)

    # draw target
    # lerp target
    glLoadMatrixf(q_to_transform(q_target, 5, 5))
    draw_axis(2, 3)
    # slerp target
    glLoadMatrixf(q_to_transform(q_target, 5, 0))
    draw_axis(2, 3)
    # slerp, lerp both target
    glLoadMatrixf(q_to_transform(q_target, 5, -5))
    draw_axis(2, 3)

    # draw interpolation
    # lerp interpolation
    glLoadMatrixf(euler_lerp(*q_src_euler, *q_tgt_euler, timestep, -5, 5, 0, 5, 5, 0))
    draw_axis(2, 3)
    # slerp target
    glLoadMatrixf(q_slerp(q_source, q_target, timestep, -5, 0, 0, 5, 0, 0))
    draw_axis(2, 3)
    # slerp, lerp both target
    glLoadMatrixf(euler_lerp(*q_src_euler, *q_tgt_euler, timestep, -5, -5, 0, 5, -5, 0))
    draw_axis(2, 3)
    glLoadMatrixf(q_slerp(q_source, q_target, timestep, -5, -5, 0, 5, -5, 0))
    draw_axis(2, 3)

    timestep += frame
    glFlush()
    time.sleep(frame)
    glutPostRedisplay()


glutInit()
glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
glutInitWindowSize(1000, 1000)
glutInitWindowPosition(100, 100)
glutCreateWindow(b"My Simple lerp, slerp Program")
glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
glMatrixMode(GL_PROJECTION)
# gluPerspective(45, 1, 0.1, 100.) # perspective?
glOrtho(-10, 10, -10, 10, 0.1, 100)  # or ortho?
glEnable(GL_DEPTH_TEST)
gluLookAt(0, 0, 20, 0, 0, 0, 0, 1, 0)
glutDisplayFunc(draw)
glutMainLoop()
