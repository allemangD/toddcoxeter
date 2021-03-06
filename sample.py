import math
from typing import List

import util
from mirrors import PlaneAngles
from toddcox import solve
from util import schlafli, Vec, V


def apply(point, word, mirrors):
    point = Vec(point)

    for gen in word:
        mirror = mirrors[gen]
        point = point.reflect(mirror)

    return point


def make_all(gens, subgens, coeffs):
    angles = PlaneAngles(gens)
    for (x, y), a in zip(util.pairwise(gens), coeffs):
        angles[x, y] = a

    mirrors = angles.normals
    cosets = solve(*schlafli(gens, subgens, coeffs))
    elements = solve(*schlafli(subgens, '', coeffs[:len(subgens) - 1]))

    return mirrors, cosets.words, elements.words


def proj(point):
    x, y, z = point[:3] * 300
    return V(x + .2 * z, y + .1 * z)


def draw_all(gens, subgens, rels, P, pen):
    mirrors, cos_words, el_words = make_all(gens, subgens, rels)

    for cos in cos_words:
        pen.penup()
        for el in el_words:
            p = apply(P, el + cos, mirrors)
            if p[2] > 0:
                pen.color('lightgray')
            else:
                pen.color('black')
            pen.setpos(*proj(p))
            pen.pendown()
    pen.penup()
    pen.setpos(0, 0)


def gram_schmidt(vecs) -> List[Vec]:
    vecs = [Vec(v) for v in vecs]
    for i in range(len(vecs)):
        for j in range(i):
            vecs[i] -= vecs[i].project(vecs[j])
    return [v.normalized for v in vecs]


def main():
    import turtle
    pen = turtle.Turtle()
    pen.speed(0)
    pen.penup()

    mults = (5, 3)
    # C = V(2, .05, .05)  # dodecahedron
    C = V(.05, 2, .05)  # icosidodecahedron
    # C = V(.05, .05, 2)  # icosihedron

    # mults = (4, 3)
    # C = V(2, .05, .05)  # cube
    # C = V(.05, 2, .05)  # cuboctahedron
    # C = V(.05, .05, 2)  # octahedron

    # mults = (3, 3)
    # C = V(2, .05, .05)  # tetrahedron
    # C = V(.05, 2, .05)  # octahedron
    # C = V(.05, .05, 2)  # tetrahedron

    planes = PlaneAngles('rgb', **dict(zip(('rg', 'gb'), mults)))
    norm = planes.normals
    r = norm['r']
    g = norm['g']
    b = norm['b']

    Pr = gram_schmidt([g, b, r])[-1]
    Pg = gram_schmidt([b, r, g])[-1]
    Pb = gram_schmidt([r, g, b])[-1]

    P = (Pr * C[0] + Pg * C[1] + Pb * C[2]).normalized

    # pen.color('red')
    draw_all('rgb', 'r', mults, P, pen)
    # pen.color('green')
    draw_all('rgb', 'g', mults, P, pen)
    # pen.color('blue')
    draw_all('rgb', 'b', mults, P, pen)

    turtle.done()


if __name__ == '__main__':
    main()
