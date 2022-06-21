from copy import deepcopy
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import numpy as np
import colorsys
from PIL import Image


def draw_lines(points, color):
    glColor3d(color[0], color[1], color[2])
    glBegin(GL_LINE_LOOP)
    for x, y, z in points:
        glVertex3f(x, y, z)
    glEnd()


def draw_points(points, color, size=10):
    glPointSize(size)
    glColor3d(color[0], color[1], color[2])
    glBegin(GL_POINTS)
    for x, y, z in points:
        glVertex3f(x, y, z)
    glEnd()


def draw_rainbow_points(points, size=10):
    glPointSize(size)
    glBegin(GL_POINTS)
    for i, (x, y, z) in enumerate(points):
        color = colorsys.hsv_to_rgb(i / len(points), 1, 1)
        glColor3d(color[0], color[1], color[2])
        glVertex3f(x, y, z)
    glEnd()


def draw_texture(points):
    glBegin(GL_QUADS)
    glTexCoord2f(0.0, 1.0)
    glVertex3f(*points[0])

    glTexCoord2f(0.0, 0.0)
    glVertex3f(*points[1])

    glTexCoord2f(1.0, 0.0)
    glVertex3f(*points[2])

    glTexCoord2f(1.0, 1.0)
    glVertex3f(*points[3])
    glEnd()


def get_texture():
    im = Image.open("../../../Desktop/nyan.png")
    # print(im.format, im.size, im.mode)
    w, h = im.size
    arr = np.array(im).astype(np.byte)
    textureid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, textureid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR);
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR);
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, w, h, 0, GL_RGB, GL_UNSIGNED_BYTE, arr)
    glGenerateMipmap(GL_TEXTURE_2D)

    return textureid


def get_affine_transform(src_points, tgt_points):
    # return 3x3 affine transform matrix
    # p'(tgt) = Ap(src)

    tgt = np.eye(3)
    tgt[0][0] = tgt_points[0][0]
    tgt[1][0] = tgt_points[0][1]
    tgt[0][1] = tgt_points[1][0]
    tgt[1][1] = tgt_points[1][1]
    tgt[0][2] = tgt_points[2][0]
    tgt[1][2] = tgt_points[2][1]
    tgt[2][0] = 1
    tgt[2][1] = 1
    tgt[2][2] = 1


    src = np.eye(3)
    src[0][0] = src_points[0][0]
    src[1][0] = src_points[0][1]
    src[0][1] = src_points[1][0]
    src[1][1] = src_points[1][1]
    src[0][2] = src_points[2][0]
    src[1][2] = src_points[2][1]
    src[2][0] = 1
    src[2][1] = 1
    src[2][2] = 1
    src = np.linalg.inv(src)

    affmat = tgt @ src
    return affmat


def get_perspective_transform(src_points, tgt_points):
    # return 3x3 perspective transform matrix
    # p'(tgt) = Mp(src)

    perspmat = np.eye(3)
    tgt = np.matrix([[src_points[0][0], src_points[0][1], 1, 0, 0, 0, -src_points[0][0] * tgt_points[0][0],
                      -src_points[0][1] * tgt_points[0][0]],
                     [src_points[1][0], src_points[1][1], 1, 0, 0, 0, -src_points[1][0] * tgt_points[1][0],
                      -src_points[1][1] * tgt_points[1][0]],
                     [src_points[2][0], src_points[2][1], 1, 0, 0, 0, -src_points[2][0] * tgt_points[2][0],
                      -src_points[2][1] * tgt_points[2][0]],
                     [src_points[3][0], src_points[3][1], 1, 0, 0, 0, -src_points[3][0] * tgt_points[3][0],
                      -src_points[3][1] * tgt_points[3][0]],
                     [0, 0, 0, src_points[0][0], src_points[0][1], 1, -src_points[0][0] * tgt_points[0][0],
                      -src_points[0][1] * tgt_points[0][1]],
                     [0, 0, 0, src_points[1][0], src_points[1][1], 1, -src_points[1][0] * tgt_points[1][1],
                      -src_points[1][1] * tgt_points[1][1]],
                     [0, 0, 0, src_points[2][0], src_points[2][1], 1, -src_points[2][0] * tgt_points[2][1],
                      -src_points[2][1] * tgt_points[2][1]],
                     [0, 0, 0, src_points[3][0], src_points[3][1], 1, -src_points[3][0] * tgt_points[3][1],
                      -src_points[3][1] * tgt_points[3][1]]])
    srt = np.matrix([[tgt_points[0][0]], [tgt_points[1][0]], [tgt_points[2][0]], [tgt_points[3][0]], [tgt_points[0][1]],
                     [tgt_points[1][1]], [tgt_points[2][1]], [tgt_points[3][1]]])
    tgt = np.linalg.inv(tgt)
    a = tgt @ srt
    perspmat[0][0] = a[0][0]
    perspmat[0][1] = a[1][0]
    perspmat[0][2] = a[2][0]
    perspmat[1][0] = a[3][0]
    perspmat[1][1] = a[4][0]
    perspmat[1][2] = a[5][0]
    perspmat[2][0] = a[6][0]
    perspmat[2][1] = a[7][0]
    return perspmat


def draw():
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0., 0., 0., 0.)
    glClear(GL_COLOR_BUFFER_BIT)
    glColor3f(1., 1., 1.)

    glPushMatrix()
    glLineWidth(2)

    # draw 2 lines
    draw_lines([[0.0, 0.5, 1], [1., 0.5, 1]], [1., 1., 1.])
    draw_lines([[0.5, 0.0, 1], [0.5, 1.0, 1]], [1., 1., 1.])

    # draw current points
    glTranslate(0., 0.5, 0.)

    glEnable(GL_TEXTURE_2D)

    if (len(affine_source_points_clicked) == 3) and (len(affine_target_points_clicked) == 3):
        affmat = get_affine_transform(affine_source_points_clicked, affine_target_points_clicked)
        imgq = deepcopy(quads)
        imgq = list(map(lambda x: affmat @ x, imgq))
        trans = translations[1]
        glPushMatrix()
        glTranslatef(trans[0], trans[1], 0)
        draw_texture(imgq)
        glPopMatrix()

    if (len(perspective_source_points_clicked) == 4) and (len(perspective_target_points_clicked) == 4):
        perspmat = get_perspective_transform(perspective_source_points_clicked, perspective_target_points_clicked)
        imgq = deepcopy(quads)
        imgq = list(map(lambda x: x / x[-1], map(lambda x: perspmat @ x, imgq)))
        trans = translations[3]
        glPushMatrix()
        glTranslatef(trans[0], trans[1], 0)
        draw_texture(imgq)
        glPopMatrix()

    for trans in translations[::2]:
        glPushMatrix()
        glTranslatef(trans[0], trans[1], 0)
        draw_texture(quads)
        glPopMatrix()
    glDisable(GL_TEXTURE_2D)

    for i, (point, trans) in enumerate(zip(points, translations)):
        glPushMatrix()
        glTranslatef(trans[0], trans[1], 0)
        draw_lines(point, [1., 0., 0.])
        if i % 2 == 0:
            draw_points(point, [0., 1., 1.])
        else:
            draw_rainbow_points(point)
        glPopMatrix()

    glPopMatrix()
    glFlush()


affine_source_points_clicked = []
affine_target_points_clicked = [np.array([0.1, 0.1, 1]), np.array([0.4, 0.4, 1]), np.array([0.4, 0.1, 1])]
perspective_source_points_clicked = []
perspective_target_points_clicked = [np.array([0.1, 0.1, 1]), np.array([0.1, 0.4, 1]), np.array([0.4, 0.4, 1]),
                                     np.array([0.4, 0.1, 1])]
translations = [(0, 0), (0.5, 0), (0, -0.5), (0.5, -0.5)]
quads = [np.array([0.1, 0.1, 1]), np.array([0.1, 0.4, 1]), np.array([0.4, 0.4, 1]), np.array([0.4, 0.1, 1])]
points = [affine_source_points_clicked, affine_target_points_clicked,
          perspective_source_points_clicked, perspective_target_points_clicked]


def mouse(button, state, x, y):
    cx = x / cw
    cy = y / ch

    if button == GLUT_LEFT_BUTTON:
        leftMouseButtonDown = (state == GLUT_DOWN)
        if leftMouseButtonDown:

            if cx < 0.5 and cy < 0.5:
                if len(affine_source_points_clicked) < 3:
                    ex = cx
                    ey = (0.5 - cy)
                    ef_point = np.array([ex, ey, 1])
                    affine_source_points_clicked.append(ef_point)

            if cx >= 0.5 and cy < 0.5:
                if len(affine_target_points_clicked) < 3:
                    ex = cx - 0.5
                    ey = (0.5 - cy)
                    ef_point = np.array([ex, ey, 1])
                    affine_target_points_clicked.append(ef_point)

            if cx < 0.5 and cy >= 0.5:
                if len(perspective_source_points_clicked) < 4:
                    ex = cx
                    ey = (1 - cy)
                    ef_point = np.array([ex, ey, 1])
                    perspective_source_points_clicked.append(ef_point)

            if cx >= 0.5 and cy >= 0.5:
                if len(perspective_target_points_clicked) < 4:
                    ex = cx - 0.5
                    ey = (1 - cy)
                    ef_point = np.array([ex, ey, 1])
                    perspective_target_points_clicked.append(ef_point)
        glutPostRedisplay()
    elif button == GLUT_RIGHT_BUTTON:
        rightMouseButtonDown = (state == GLUT_DOWN)
        if rightMouseButtonDown:
            if cx < 0.5 and cy < 0.5:
                affine_source_points_clicked.clear()
            if cx >= 0.5 and cy < 0.5:
                affine_target_points_clicked.clear()
            if cx < 0.5 and cy >= 0.5:
                perspective_source_points_clicked.clear()
            if cx >= 0.5 and cy >= 0.5:
                perspective_target_points_clicked.clear()
        glutPostRedisplay()


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
glutCreateWindow(b"My Simple Affine, Perspective transform")
glMatrixMode(GL_PROJECTION)
glOrtho(0, 1, 0, 1, 0, 20)
gluLookAt(0.0, 0.0, 10, 0.0, 0.0, 0, 0, 1, 0)
texid = get_texture()
glutDisplayFunc(draw)
glutReshapeFunc(reshaped)
glutMouseFunc(mouse)
glutMainLoop()
