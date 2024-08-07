from sympy import *
from dtumathtools import *
import pytest

init_printing()

# remove sympy variable named "test"
test = 0
del test


def test_week1():
    # Store dag
    x, y = symbols("x y")
    f = x * y**2 + x

    res = f.diff(x), f.diff(y)
    assert res == (y**2 + 1, 2 * x * y)

    res = f.diff(x, 2), f.diff(y, 2), f.diff(x, y), f.diff(y, x)
    assert res == (0, 2 * x, 2 * y, 2 * y)

    res = f.diff(x).subs({x: -2, y: 3})
    assert res == 10

    res = f.diff(x, y).subs({x: 5, y: -13})
    assert res == -26

    f = 4 - x**2 - y**2
    p = dtuplot.plot3d(f, (x, -3, 3), (y, -3, 3), show=False)
    p = dtuplot.plot3d(
        f, (x, -3, 3), (y, -3, 3), camera={"elev": 25, "azim": 45}, show=False
    )
    p = dtuplot.plot3d(
        f,
        (x, -3, 3),
        (y, -3, 3),
        wireframe=True,
        rendering_kw={"color": "red", "alpha": 0.5},
        show=False,
    )
    p = dtuplot.plot3d(f, (x, -3, 3), (y, -3, 3), use_cm=True, legend=True, show=False)

    dtuplot.plot_contour(f, (x, -3, 3), (y, -3, 3), is_filled=False, show=False)

    zvals = [-2, -1, 0, 1]
    dtuplot.plot_contour(
        f,
        (x, -3, 3),
        (y, -3, 3),
        rendering_kw={"levels": zvals, "alpha": 0.5},
        is_filled=False,
        show=False,
    )

    p = dtuplot.plot3d(f, (x, -3, 3), (y, -3, 3), use_cm=True, legend=True, show=False)

    f = cos(x) + sin(y)
    p = dtuplot.plot3d(
        f,
        (x, -pi / 2, 3 / 2 * pi),
        (y, 0, 2 * pi),
        use_cm=True,
        camera={"elev": 45, "azim": -65},
        legend=True,
        show=False,
    )
    nf = Matrix([f.diff(x), f.diff(y)])

    dtuplot.plot_vector(
        nf, (x, -pi / 2, 3 / 2 * pi), (y, 0, 2 * pi), scalar=False, show=False
    )

    dtuplot.plot_vector(
        nf,
        (x, -pi / 2, 3 / 2 * pi),
        (y, 0, 2 * pi),
        quiver_kw={"color": "black"},
        contour_kw={"cmap": "Blues_r", "levels": 20},
        grid=False,
        xlabel="x",
        ylabel="y",
        n=15,
        show=False,
    )

    p = dtuplot.plot3d(
        f,
        (x, -pi / 2, 3 / 2 * pi),
        (y, 0, 2 * pi),
        use_cm=True,
        camera={"elev": 45, "azim": -65},
        legend=True,
        show=False,
    )

    f = 1 - x**2 / 2 - y**2 / 2
    x0 = Matrix([1, -1])
    e = Matrix([-1, -2]).normalized()

    p1 = dtuplot.scatter(
        x0,
        rendering_kw={"markersize": 10, "color": "r"},
        xlim=[-2, 2],
        ylim=[-2, 2],
        show=False,
    )
    p1.extend(dtuplot.quiver(x0, e, show=False))

    Nabla = Matrix([diff(f, x), diff(f, y)]).subs({x: x0[0], y: x0[1]})
    a = e.dot(Nabla)
    u, t = symbols("u t", real=True)
    r = Matrix([u * cos(u), u * sin(u)])
    rd = diff(r, u)
    u0 = 3 * pi / 2
    rdu0 = rd.subs(u, u0)
    ru0 = r.subs(u, u0)
    T = ru0 + t * rdu0

    p = dtuplot.plot_parametric(
        r[0],
        r[1],
        (u, 0, 4 * pi),
        rendering_kw={"color": "red"},
        use_cm=False,
        show=False,
    )
    p.extend(
        dtuplot.plot_parametric(
            T[0],
            T[1],
            (t, -1.5, 1.5),
            rendering_kw={"color": "royalblue"},
            use_cm=False,
            show=False,
        )
    )
    p.extend(
        dtuplot.scatter(
            ru0, rendering_kw={"markersize": 10, "color": "black"}, show=False
        )
    )
    p.extend(dtuplot.quiver(ru0, rdu0, rendering_kw={"color": "black"}, show=False))

    # Lille dag
    x, y = symbols("x y")
    g = y**2 - x**2
    res = solveset(Eq(g, 0), y)
    assert res == {-x, x}

    plot_implicit(Eq(g, 0), show=False)

    res = (
        g.subs({x: 1, y: 0}),
        g.subs({x: 0, y: 1}),
        g.subs({x: -1, y: 0}),
        g.subs({x: 0, y: -1}),
    )
    assert res == (-1, 1, -1, 1)

    plot_implicit(g > 0, show=False)

    f = 4 - x**2 - y**2
    dtuplot.plot3d(f, (x, -2, 2), (y, -2, 2), use_cm=True, legend=True, show=False)

    a = {x: 1, y: -1}
    P1 = f.subs(a) + f.diff(x).subs(a) * (x - 1) + f.diff(y).subs(a) * (y + 1)
    assert P1 == -2 * x + 2 * y + 6

    def poly_approx(f, var, expand_from, degree):
        for i, x in enumerate(var):
            f = f.series(x, expand_from[i], degree + 1).removeO()
        return f

    res = poly_approx(f, (x, y), (1, -1), 1)
    assert res == -2 * x + 2 * y + 6

    N = Matrix([2, -2, 1])
    a0 = Matrix([1, -1, f.subs(a)])
    p = dtuplot.plot3d(
        f,
        (x, -2, 2),
        (y, -2, 2),
        rendering_kw={"alpha": 0.3, "cmap": "Blues"},
        xlim=(-2, 3),
        ylim=(-3, 2),
        zlim=(-1, 4),
        camera={"elev": 10, "azim": -110},
        show=False,
    )
    p.extend(
        dtuplot.plot3d(
            P1,
            (x, 0, 2),
            (y, -2, 0),
            rendering_kw={"color": "green", "alpha": 0.5},
            show=False,
        )
    )
    p.extend(
        dtuplot.scatter(
            a0, rendering_kw={"alpha": 1, "s": 100, "color": "black"}, show=False
        )
    )
    p.extend(dtuplot.quiver(a0, N, {"color": "red"}, show=False))

    x, y, u = symbols("x y u")
    f = x**2 / 10 + y**2 / 10 + 10
    r = Matrix([u * cos(u), u * sin(u)])
    h = f.subs({x: r[0], y: r[1]})
    p = dtuplot.plot3d(
        f,
        (x, -10, 10),
        (y, -10, 10),
        use_cm=True,
        camera={"elev": 20, "azim": -125},
        rendering_kw={"alpha": 0.4},
        show=False,
    )
    p.extend(
        dtuplot.plot3d_parametric_line(
            r[0],
            r[1],
            0,
            (u, 0, 4 * pi),
            use_cm=False,
            rendering_kw={"color": "red"},
            show=False,
        )
    )
    r1 = r.subs(u, 3 * pi)
    p.extend(
        dtuplot.scatter(
            r1[0], r1[1], 0, rendering_kw={"color": "black", "s": 100}, show=False
        )
    )
    p.extend(
        dtuplot.quiver(
            r1[0],
            r1[1],
            0,
            0,
            0,
            f.subs({x: r1[0], y: r1[1]}),
            rendering_kw={"color": "orange"},
            show=False,
        )
    )
    r2 = r.subs(u, 3 * pi / 2)
    p.extend(
        dtuplot.scatter(
            r2[0], r2[1], 0, rendering_kw={"color": "black", "s": 100}, show=False
        )
    )
    p.extend(
        dtuplot.quiver(
            r2[0],
            r2[1],
            0,
            0,
            0,
            f.subs({x: r2[0], y: r2[1]}),
            rendering_kw={"color": "orange"},
            show=False,
        )
    )

    dh = h.diff(u)
    dh.subs(u, 3 * pi / 2), dh.subs(u, 3 * pi)
    x, y, z = symbols("x y z")
    f = 1 - x**2 / 2 - y**2 / 2

    p0 = Matrix([1, -1, 0])
    p_parab = dtuplot.plot3d(
        f,
        (x, -2, 2),
        (y, -2, 2),
        use_cm=True,
        camera={"elev": 20, "azim": -80},
        rendering_kw={"alpha": 0.4},
        show=False,
    )
    p_point = dtuplot.scatter(p0, rendering_kw={"color": "black", "s": 100}, show=False)
    res = p_parab + p_point

    dfx = f.diff(x)
    t = symbols("t")
    xtan = p0 + Matrix([1, 0, dfx.subs({x: p0[0], y: p0[1]})]) * t
    n0 = Matrix([0, 1, 0])
    p_xplane = dtuplot.plot_geometry(
        Plane(p0, n0),
        (x, -2, 2),
        (y, -2, 2),
        (z, -3, 1),
        rendering_kw={"alpha": 0.3, "color": "blue"},
        show=False,
    )
    p_xtan = dtuplot.plot3d_parametric_line(
        xtan[0],
        xtan[1],
        xtan[2],
        (t, -1, 1),
        use_cm=False,
        rendering_kw={"color": "red"},
        show=False,
    )
    res = p_parab + p_point + p_xplane + p_xtan

    dfx.subs({x: p0[0], y: p0[1]})
    p_parab2 = dtuplot.plot3d(
        f,
        (x, -2, 2),
        (y, -2, 2),
        use_cm=True,
        camera={"elev": 15, "azim": -60},
        rendering_kw={"alpha": 0.4},
        show=False,
    )
    dfy = f.diff(y)
    ytan = p0 + Matrix([0, 1, dfy.subs({x: p0[0], y: p0[1]})]) * t
    n1 = Matrix([1, 0, 0])
    p_yplane = dtuplot.plot_geometry(
        Plane(p0, n1),
        (x, -2, 2),
        (y, -2, 2),
        (z, -3, 1),
        rendering_kw={"alpha": 0.3, "color": "green"},
        show=False,
    )
    p_ytan = dtuplot.plot3d_parametric_line(
        ytan[0],
        ytan[1],
        ytan[2],
        (t, -1, 1),
        use_cm=False,
        rendering_kw={"color": "red"},
        show=False,
    )
    res = p_parab2 + p_point + p_yplane + p_ytan

    assert dfy.subs({x: p0[0], y: p0[1]}) == 1

    n2 = Matrix([1, 0, dfx]).cross(Matrix([0, 1, dfy]))
    n3 = n2.subs({x: p0[0], y: p0[1]})

    p_xyplane = dtuplot.plot_geometry(
        Plane(p0, n3),
        (x, -2, 2),
        (y, -2, 2),
        (z, -3, 1),
        rendering_kw={"alpha": 0.5, "color": "grey"},
        show=False,
    )
    res = p_parab + p_point + p_xtan + p_ytan + p_xyplane

    e = Matrix([-S(1) / sqrt(5), -S(2) / sqrt(5)])
    p_2dline = dtuplot.plot(
        2 * x - 3,
        (x, -2, 2),
        xlim=(-2, 2),
        ylim=(-2, 2),
        rendering_kw={"color": "grey"},
        show=False,
    )
    p_2darrow = dtuplot.quiver((1, -1), e, rendering_kw={"color": "red"}, show=False)
    p_2dpoint = dtuplot.scatter(
        1, -1, rendering_kw={"color": "black", "s": 10}, show=False
    )
    res = p_2dline + p_2darrow + p_2dpoint

    n4 = Matrix([2, -1, 0])  # normal vektoren tilsvarende y=2x-3
    p_vertical_plane = dtuplot.plot_geometry(
        Plane(p0, n4),
        (x, -2, 2),
        (y, -2, 2),
        (z, -3, 1),
        rendering_kw={"alpha": 0.35, "color": "blue"},
        show=False,
    )
    p_normalvector = dtuplot.quiver(p0, n4, rendering_kw={"color": "red"}, show=False)
    p_arrow_along_plane = dtuplot.quiver(
        p0,
        [e[0], e[1], f.subs({x: 1, y: -1})],
        rendering_kw={"color": "orange"},
        show=False,
    )
    res = p_parab + p_point + p_vertical_plane + p_normalvector + p_arrow_along_plane

    assert Matrix([dfx, dfy]).subs({x: 1, y: -1}) == Matrix([-1, 1])

    a = e.dot(Nabla)
    assert a == -sqrt(5) / 5

    r = Matrix([e[0], e[1], a])
    tangent = p0 + r * t
    p_linetan = dtuplot.plot3d_parametric_line(
        tangent[0],
        tangent[1],
        tangent[2],
        (t, -2, 2),
        use_cm=False,
        rendering_kw={"color": "red"},
        show=False,
    )
    res = p_parab + p_point + p_vertical_plane + p_linetan

    res = (
        p_parab
        + p_point
        + p_linetan
        + p_xyplane
        + p_vertical_plane
        + p_normalvector
        + p_arrow_along_plane
    )


def test_week2():
    # Store dag
    x, y = symbols("x y")
    f = sin(x**2 + y**2)
    dtuplot.plot3d(
        f, (x, -1.5, 1.5), (y, -1.5, 1.5), rendering_kw={"color": "blue"}, show=False
    )
    P1 = dtutools.taylor(f, [x, 0, y, 0], degree=2)
    assert P1 == 0
    p = dtuplot.plot3d(
        P1,
        (x, -1.5, 1.5),
        (y, -1.5, 1.5),
        show=False,
        rendering_kw={"alpha": 0.5},
        camera={"azim": -81, "elev": 18},
    )
    p.extend(dtuplot.plot3d(f, (x, -1.5, 1.5), (y, -1.5, 1.5), show=False))
    P2 = dtutools.taylor(f, [x, 0, y, 0], 3)
    assert P2 == x**2 + y**2
    dtuplot.plot3d(f, P2, (x, -1.5, 1.5), (y, -1.5, 1.5), show=False)
    P6 = dtutools.taylor(f, [x, 0, y, 0], 7)
    p = dtuplot.plot3d(f, (x, -1.5, 1.5), (y, -1.5, 1.5), show=False)
    p.legend = True
    f_p1 = f.subs([(x, 1 / 5), (y, 1 / 5)])
    P1_p1 = P1.subs([(x, 1 / 5), (y, 1 / 5)])
    P2_p1 = P2.subs([(x, 1 / 5), (y, 1 / 5)])
    P6_p1 = P6.subs([(x, 1 / 5), (y, 1 / 5)])
    res = f_p1 - P1_p1, f_p1 - P2_p1, f_p1 - P6_p1
    f_p2 = f.subs([(x, 1 / 2), (y, 1 / 2)])
    P1_p2 = P1.subs([(x, 1 / 2), (y, 1 / 2)])
    P2_p2 = P2.subs([(x, 1 / 2), (y, 1 / 2)])
    P6_p2 = P6.subs([(x, 1 / 2), (y, 1 / 2)])
    res = f_p2 - P1_p2, f_p2 - P2_p2, f_p2 - P6_p2
    z = symbols("z")
    f = 7 * x**2 - 4 * x * y + 6 * y**2 - 4 * y * z + 5 * z**2 - 2 * x + 20 * y - 10 * z
    H = dtutools.hessian(f)
    var_vec = Matrix([x, y, z])
    A = S(1) / 2 * H
    k = (var_vec.T * A * var_vec)[0].expand()
    assert k == 7 * x**2 - 4 * x * y + 6 * y**2 - 4 * y * z + 5 * z**2
    f_matrix = k + (Matrix([-2, 20, -10]).T * var_vec)[0]

    # Lille dag
    x, y = symbols("x y")
    var_vec = Matrix([x, y])
    lignM = Eq(11 * x**2 - 24 * x * y + 4 * y**2 - 20 * x + 40 * y - 60, 0)
    H = dtutools.hessian(lignM.lhs)
    A = S(1) / 2 * H
    k = (var_vec.T * S(1) / 2 * H * var_vec)[0].expand()
    l = (Matrix([-20, 40]).T * var_vec)[0].expand()
    assert k == 11 * x**2 - 24 * x * y + 4 * y**2
    assert l == -20 * x + 40 * y
    A.eigenvects()
    q1 = Matrix([S(3) / 4, 1])
    q2 = Matrix([-S(4) / 3, 1])
    q1 = q1.normalized()  # Eller q1 = q1 / sqrt((q1.T * q1)[0])
    q2 = q2.normalized()  # q2 = q2 / sqrt((q2.T * q2)[0])
    assert q1 == Matrix([S(3) / 5, S(4) / 5])
    assert q2 == Matrix([-S(4) / 5, S(3) / 5])
    Q = Matrix.hstack(q1, q2)
    assert Q.det() == 1
    Lambda = Matrix([[-5, 0], [0, 20]])
    assert Eq(Lambda, Q.T * A * Q) == True
    x1, y1 = symbols("x1 y1")
    var_vec_1 = Matrix([x1, y1])
    lignM_1 = (
        (var_vec_1.T * Q.T * A * Q * var_vec_1)[0]
        + (Matrix([-20, 40]).T * Q * var_vec_1)[0]
        - 60
    )
    Eq(lignM_1, 0)
    -5 * (x1 - 2) ** 2, expand(-5 * (x1 - 2) ** 2), 20 * (y1 + 1) ** 2, expand(
        20 * (y1 + 1) ** 2
    )
    lign = Eq((-5 * (x1 - 2) ** 2 + 20 * (y1 + 1) ** 2 - 60), 0)
    lign
    lign = Eq((lign.lhs + 60) / 60, (lign.rhs + 60) / 60)
    lign
    assert Q * Matrix([2, -1]) == Matrix([2, 1])
    ((Q * Matrix([S(1) / 2, 1])).T * var_vec)[0], (
        (Q * Matrix([-S(1) / 2, 1])).T * var_vec
    )[0] + 2
    t = symbols("t")
    M = dtuplot.plot_implicit(
        lignM, (x, -4, 8), (y, -6, 6), show=False, aspect="equal", size=(6, 6)
    )
    sym1 = dtuplot.plot_parametric(
        2 + q1[0] * t, 1 + q1[1] * t, (t, -20, 20), show=False
    )
    sym2 = dtuplot.plot_parametric(
        2 + q2[0] * t, 1 + q2[1] * t, (t, -20, 20), show=False
    )
    asymp1 = dtuplot.plot_implicit(
        Eq(-x / S(2) + y, 0), (x, -4, 8), (y, -6, 6), show=False
    )
    asymp2 = dtuplot.plot_implicit(
        Eq(-S(11) * x / 10 + y / S(5) + 2, 0), (x, -4, 8), (y, -6, 6), show=False
    )
    q1p = dtuplot.quiver(
        Matrix([2, 1]), q1 * 2, rendering_kw={"color": "black"}, show=False
    )
    q2p = dtuplot.quiver(
        Matrix([2, 1]), q2 * 2, rendering_kw={"color": "black"}, show=False
    )
    M.extend(sym1)
    M.extend(sym2)
    M.extend(asymp1)
    M.extend(asymp2)
    M.extend(q1p)
    M.extend(q2p)
    M.legend = False


def test_week3():
    x, y = symbols("x y")
    f = x**3 - 3 * x**2 + y**3 - 3 * y**2
    lign1 = Eq(f.diff(x), 0)
    lign2 = Eq(f.diff(y), 0)
    assert f.diff(x) == 3 * x**2 - 6 * x
    assert f.diff(y) == 3 * y**2 - 6 * y
    sols = nonlinsolve([lign1, lign2], [x, y])
    assert (0, 0) in sols
    assert (0, 2) in sols
    assert (2, 0) in sols
    assert (2, 2) in sols
    H = dtutools.hessian(f)
    fxx = f.diff(x, 2)
    fxy = f.diff(x, y)
    fyy = f.diff(y, 2)
    H = Matrix([[fxx, fxy], [fxy, fyy]])
    assert H == Matrix([[(6 * (x - 1)).factor(), 0], [0, (6 * (y - 1)).factor()]])
    [H.subs([(x, x0), (y, y0)]) for (x0, y0) in sols]
    assert dtutools.taylor(f, [x, 0, y, 0], 3) == -3 * x**2 - 3 * y**2
    assert (
        dtutools.taylor(f, [x, 2, y, 2], 3) == 3 * (x - 2) ** 2 + 3 * (y - 2) ** 2 - 8
    )
    pf = dtuplot.plot3d(
        f,
        (x, -0.8, 2.8),
        (y, -0.8, 2.8),
        use_cm=True,
        colorbar=False,
        show=False,
        wireframe=True,
        rendering_kw={"alpha": 0.6},
    )
    # Following command changed, as the scatter function changed.
    # Each point is now given in a list, so '*' is removed.
    points = dtuplot.scatter(
        [Matrix([x0, y0, f.subs([(x, x0), (y, y0)])]) for (x0, y0) in sols],
        show=False,
        rendering_kw={"s": 100, "color": "red"},
    )
    pf.camera = {"azim": -50, "elev": 30}
    pf.extend(points)
    f = x**4 + 4 * x**2 * y**2 + y**4 - 4 * x**3 - 4 * y**3 + 2
    lign1 = Eq(f.diff(x), 0)
    lign2 = Eq(f.diff(y), 0)
    lign1, lign2, f
    sols = nonlinsolve([lign1, lign2], [x, y])
    assert (0, 0) in sols
    assert (0, 3) in sols
    assert (1, 1) in sols
    assert (3, 0) in sols
    [(N(xsol), N(ysol)) for (xsol, ysol) in sols]
    stat_punkter = list(sols)[:-2]
    H = dtutools.hessian(f)
    assert (H[1, 0]).factor() == 16 * x * y
    Hesse_matricer = [H.subs([(x, x0), (y, y0)]) for x0, y0 in stat_punkter]
    Eig_Hesse_matricer = [h.eigenvals() for h in Hesse_matricer]
    list(zip(Hesse_matricer, Eig_Hesse_matricer))
    dtuplot.plot(f.subs(y, x), 2, (x, -0.5, 1.2), axis_center="auto", show=False)
    tmp = f.subs(y, x) - f.subs([(x, 0), (y, 0)])
    assert tmp == 6 * x**4 - 8 * x**3
    assert dtutools.taylor(f, [x, 0, y, 0], 3) == 2
    pf = dtuplot.plot3d(
        f,
        (x, -2, 5),
        (y, -2, 5),
        xlim=(-2, 5),
        ylim=(-2, 5),
        zlim=(-30, 15),
        show=False,
        rendering_kw={"alpha": 0.5},
    )
    pf.camera = {"azim": -161, "elev": 5}
    # Following command changed, as the scatter function changed.
    # Each point is now given in a list, so '*' is removed.
    points = dtuplot.scatter(
        [Matrix([x0, y0, f.subs([(x, x0), (y, y0)])]) for x0, y0 in stat_punkter],
        show=False,
        rendering_kw={"color": "red", "s": 30},
    )
    pf.camera = {"azim": -161, "elev": -5}
    res = pf + points
    with pytest.warns(
        match="The provided expression contains Boolean functions. In order to plot the expression, the algorithm automatically switched to an adaptive sampling."
    ):
        M = dtuplot.plot_implicit(
            Eq(x, 0),
            Eq(y, 1 - x),
            Eq(y, -1),
            (1 - x >= y) & (y >= -1) & (x >= 0),
            (x, -0.1, 2.1),
            (y, -1.1, 1.1),
            show=False,
        )
    M.legend = False
    f = 3 + x - x**2 - y**2
    niveau = dtuplot.plot_contour(f, (x, -0.1, 2.1), (y, -1.1, 1.1), show=False)
    niveau.extend(
        dtuplot.plot_implicit(
            Eq(x, 0),
            Eq(y, 1 - x),
            Eq(y, -1),
            (x, -0.1, 2.1),
            (y, -1.1, 1.1),
            show=False,
        )
    )
    lign1 = Eq(f.diff(x), 0)
    lign2 = Eq(f.diff(y), 0)
    sols = nonlinsolve([lign1, lign2], [x, y])
    assert (S(1) / 2, 0) in sols
    dtuplot.plot(f.subs(y, -1), (x, 0, 2), title="Randlinjen f(x, -1)", show=False)
    dtuplot.plot(f.subs(y, 1 - x), (x, 0, 2), title="Randlinjen f(x, 1-x)", show=False)
    dtuplot.plot(
        f.subs(x, 0),
        (y, -1, 1),
        ylim=(0, 3),
        aspect="equal",
        title="Randlinjen f(0, y)",
        show=False,
    )
    stat_punkter = set(sols)

    lodret = solve(f.subs(x, 0).diff(y))
    vandret = solve(f.subs(y, -1).diff(x))
    skrå = solve(f.subs(y, 1 - x).diff(x))

    stat_punkter.update(set([(0, y0) for y0 in lodret]))
    stat_punkter.update(set([(x0, -1) for x0 in vandret]))
    stat_punkter.update(set([(x0, 1 - x0) for x0 in skrå]))
    undersøgelses_punkter = list(stat_punkter) + [(0, 1), (0, -1), (2, -1)]
    f_værdier = [f.subs([(x, x0), (y, y0)]) for x0, y0 in undersøgelses_punkter]

    minimum = min(f_værdier)
    maximum = max(f_værdier)
    assert 3 in f_værdier
    assert S(9) / 4 in f_værdier
    assert S(25) / 8 in f_værdier
    assert S(13) / 4 in f_værdier
    assert 2 in f_værdier
    assert 0 in f_værdier
    u = symbols("u")
    pf = dtuplot.plot3d(
        f, (x, 0, 2), (y, -1, 1), show=False, rendering_kw={"alpha": 0.7}
    )
    # Following command changed, as the scatter function changed.
    # Each point is now given in a list, so '[]' is added.
    punkter = dtuplot.scatter(
        [Matrix([2, -1, 0]), Matrix([1 / 2, 0, 13 / 4])],
        show=False,
        rendering_kw={"color": "red", "s": 20},
    )
    l1 = dtuplot.plot3d_parametric_line(
        u,
        -1,
        f.subs({x: u, y: -1}),
        (u, 0, 2),
        use_cm=False,
        show=False,
        rendering_kw={"color": "red", "linewidth": 2},
    )
    l2 = dtuplot.plot3d_parametric_line(
        0,
        u,
        f.subs({x: 0, y: u}),
        (u, -1, 1),
        use_cm=False,
        show=False,
        rendering_kw={"color": "red", "linewidth": 2},
    )
    l3 = dtuplot.plot3d_parametric_line(
        u,
        1 - u,
        f.subs({x: u, y: 1 - u}),
        (u, 0, 2),
        use_cm=False,
        show=False,
        rendering_kw={"color": "red", "linewidth": 2},
    )
    combined = pf + punkter + l1 + l2 + l3
    combined.camera = {"azim": 118, "elev": 61}
    combined.legend = False


def test_week4():
    u, x, y, a, b = symbols("u x y a b")
    f = exp(u) * sin(u)
    p = dtuplot.plot(f, (u, -pi, pi), {"color": "red"}, axis_center="auto", show=False)
    area = 0
    for i in range(10):
        xval = i * pi / 5 - pi
        yval = f.subs(u, xval)

        # Hjørner af firkant
        c1 = Point(xval, 0)
        c2 = Point(xval + pi / 5, 0)
        c3 = Point(xval + pi / 5, yval)
        c4 = Point(xval, yval)

        poly = Polygon(c1, c2, c3, c4)
        p.extend(
            dtuplot.plot_geometry(poly, {"color": "green", "alpha": 0.5}, show=False)
        )

        # Kan ikke finde areal af en linje
        if yval != 0:
            area += poly.area

    p.legend = False
    assert abs(area.evalf() - 10.799) < 1e-3
    F = integrate(f, u)
    assert F == E**u * sin(u) / 2 - E**u * cos(u) / 2
    assert abs(integrate(f, (u, -pi, pi)).evalf() - 11.5487) < 1e-3
    r = Matrix([sin(u), sin(u) * cos(u)])
    p_kurve = dtuplot.plot_parametric(
        r[0],
        r[1],
        (u, 0, 2 * pi),
        use_cm=False,
        label="r(u)",
        axis_center="auto",
        show=False,
    )
    dr = r.diff(u)
    t = symbols("t")
    r_tan = r.subs(u, pi / 3) + t * dr.subs(u, pi / 3)
    p_point = dtuplot.scatter(r.subs(u, pi / 3), show=False)
    p_tan = dtuplot.plot_parametric(
        r_tan[0], r_tan[1], (t, -1, 1), use_cm=False, label="r '(pi/3)", show=False
    )
    res = p_kurve + p_point + p_tan
    jacobi = sqrt(dr.dot(dr))
    assert simplify(jacobi) == sqrt(cos(u) ** 2 + cos(2 * u) ** 2)
    assert abs(integrate(jacobi, (u, 0, 2 * pi)).evalf() - 6.09722) < 1e-3
    x, y, z = symbols("x y z")
    f = sqrt(x**2 + y**2 + z**2)
    r = Matrix([u * cos(u), u * sin(u), u])
    p_rumkurve = dtuplot.plot3d_parametric_line(
        r[0],
        r[1],
        r[2],
        (u, 0, 2 * pi),
        use_cm=False,
        label="r(u)",
        aspect="equal",
        show=False,
    )
    dr = r.diff(u)
    jacobi = sqrt(dr.dot(dr))
    assert simplify(jacobi) == sqrt(u**2 + 2)
    assert (
        abs(
            integrate(f.subs({x: r[0], y: r[1], z: r[2]}) * jacobi, (u, 0, 5)).evalf()
            - 64.802889
        )
        < 1e-3
    )
    assert abs(integrate(jacobi, (u, 0, 5)).evalf() - 14.9658) < 1e-3


def test_week5():
    # Store dag
    u, v = symbols("u v")
    dtuplot.plot_parametric(
        3 + v, 2 + 2 * v, (v, -1, 1), xlim=(0, 5), ylim=(0, 5), show=False
    )
    x, y = symbols("x y")
    with pytest.warns(
        UserWarning,
        match="The provided expression contains Boolean functions. In order to plot the expression, the algorithm automatically switched to an adaptive sampling.",
    ):
        område = dtuplot.plot_implicit(
            Eq(x, 2),
            Eq(y, 2 * x + 1),
            Eq(y, 1 - x),
            (x <= 2) & (y <= 2 * x + 1) & (y >= 1 - x),
            (x, -0.1, 5),
            (y, -1.1, 5.1),
            aspect="equal",
            size=(8, 8),
            show=False,
        )
    AB = dtuplot.quiver(
        Matrix([1, 0]), Matrix([0, 3]), show=False, rendering_kw={"color": "black"}
    )
    område.extend(AB)
    dtuplot.plot3d_parametric_surface(
        u,
        1 - u + 3 * u * v,
        0,
        (u, 0, 2),
        (v, 0, 1),
        camera={"elev": 90, "azim": -90},
        show=False,
    )
    cirkel = dtuplot.plot_implicit(
        Eq((x - 2) ** 2 + (y - 1) ** 2, 1),
        ((x - 2) ** 2 + (y - 1) ** 2 <= 1),
        (x, 0, 3),
        (y, 0, 3),
        show=False,
    )
    AB = dtuplot.quiver(
        Matrix([2, 1]),
        Matrix([cos(pi / 4), sin(pi / 4)]),
        rendering_kw={"color": "black"},
        show=False,
    )
    cirkel.extend(AB)
    dtuplot.plot3d_parametric_surface(
        2 + v * cos(u),
        1 + v * sin(u),
        0,
        (u, 0, 2 * pi),
        (v, 0, 1),
        camera={"elev": 90, "azim": -90},
        show=False,
    )
    with pytest.warns(
        UserWarning,
        match="The provided expression contains Boolean functions. In order to plot the expression, the algorithm automatically switched to an adaptive sampling.",
    ):
        dtuplot.plot_implicit(
            Eq(y, 1),
            Eq(x, 1),
            Eq(y, x + 1),
            ((x <= 1) & (y >= 1) & (y <= 1 + x)),
            (x, 0, 2),
            (y, 0, 2),
            title="Integrationsområde B",
            show=False,
        )
    r = Matrix([u, 1 + u * v])
    f = 2 * x * y
    JacobiM = Matrix.hstack(r.diff(u), r.diff(v))
    Jacobi = abs(JacobiM.det())
    assert (
        integrate(f.subs([(x, u), (y, 1 + u * v)]) * Jacobi, (u, 0, 1), (v, 0, 1))
        == S(11) / 12
    )
    f = (x - 1) ** 2 * (y + 1) ** 2
    r = Matrix([u * cos(v), u * sin(v) / 2])
    dtuplot.plot3d_parametric_surface(
        u,
        v,
        0,
        (u, 1, 2),
        (v, -pi, pi),
        camera={"elev": 90, "azim": -90},
        xlim=(0, 3),
        ylim=(-3.5, 3.5),
        show=False,
    )
    område = dtuplot.plot3d_parametric_surface(
        r[0],
        r[1],
        0,
        (u, 1, 2),
        (v, -pi, pi),
        camera={"elev": 90, "azim": -90},
        xlim=(-2, 2),
        ylim=(-2, 2),
        show=False,
    )
    JacobiM = Matrix.hstack(r.diff(u), r.diff(v))
    Jacobi = abs(JacobiM.det())
    assert Jacobi.simplify() == abs(u) / 2
    integrand = f.subs([(x, r[0]), (y, r[1])]) * Jacobi
    M = integrate(integrand, (u, 1, 2), (v, -pi, pi))
    assert M == S(267) * pi / 64
    Mmidtpunkt = (
        Matrix(
            [
                integrate(r[0] * integrand, (u, 1, 2), (v, -pi, pi)),
                integrate(r[1] * integrand, (u, 1, 2), (v, -pi, pi)),
            ]
        )
        / M
    )
    assert Mmidtpunkt == Matrix([-S(94) / 89, S(34) / 89])
    punkt = dtuplot.scatter(
        Matrix([Mmidtpunkt[0], Mmidtpunkt[1], 0]),
        show=False,
        rendering_kw={"color": "black"},
        xlim=(-2, 2),
        ylim=(-2, 2),
    )
    område.extend(punkt)
    z = symbols("z")
    f = 8 * z
    r = Matrix([u * cos(u), u * sin(u), u * v])
    dtuplot.plot3d_parametric_surface(*r, (u, 0, pi / 2), (v, 0, 1), show=False)
    kryds = r.diff(u).cross(r.diff(v))
    Jacobi = sqrt((kryds.T * kryds)[0]).simplify()
    assert Jacobi == sqrt(u**4 + u**2)
    integrand = f.subs(z, r[2]) * Jacobi
    assert (
        abs(integrate(integrand, (u, 0, pi / 2), (v, 0, 1)).evalf() - 8.062867) < 1e-3
    )

    # Lille dag
    x, y, z, u, v = symbols("x y z u v", real=True)
    # sympy kan ofte lave bedre simplificeringer af udtryk, når den ved, at variablerne er reelle,
    # så når vi kan er det en god ide at gøre. Ellers kan nogle integraler tage ret lang tid.
    h = x**2 - y**2 + 5
    r = Matrix([x, y, h])
    flade = dtuplot.plot3d_parametric_surface(
        *r,
        (x, -2, 2),
        (y, -2, 2),
        use_cm=True,
        camera={"elev": 30, "azim": -130},
        show=False,
    )
    kvadrat = dtuplot.plot3d_parametric_surface(
        x, y, 0, (x, -2, 2), (y, -2, 2), rendering_kw={"color": "black"}, show=False
    )
    res = flade + kvadrat
    r = Matrix([u * cos(v), u * sin(v), h.subs({x: u * cos(v), y: u * sin(v)})])
    flade = dtuplot.plot3d_parametric_surface(
        *r, (u, 1, 2), (v, 0, 2 * pi), show=False, camera={"azim": -75, "elev": 40}
    )
    skive = dtuplot.plot3d_parametric_surface(
        r[0], r[1], 0, (u, 1, 2), (v, 0, 2 * pi), show=False
    )
    res = flade + skive
    dtuplot.plot_parametric(
        u**2 + 1, u, (u, -1, 1), use_cm=False, aspect="equal", show=False
    )
    profil = Matrix([u**2 + 1, 0, u])
    profil_plot = dtuplot.plot3d_parametric_line(
        *profil, (u, -1, 1), show=False, camera={"azim": -65, "elev": 12}, use_cm=False
    )
    r = Matrix([(u**2 + 1) * cos(v), (u**2 + 1) * sin(v), u])
    r = Matrix([[cos(v), -sin(v), 0], [sin(v), cos(v), 0], [0, 0, 1]]) * profil
    flade = dtuplot.plot3d_parametric_surface(
        *r,
        (u, -1, 1),
        (v, 0, 2 * pi),
        camera={"azim": -90, "elev": 15},
        title="Omdrejningsfladen",
        show=False,
    )
    dtuplot.plot(
        (x - 1) ** 3 + 1, (x, 0, 2), axis_center="auto", ylabel="z", show=False
    )
    profil = Matrix([u, 0, (u - 1) ** 3 + 1])
    r = Matrix([[cos(v), sin(v), 0], [sin(v), cos(v), 0], [0, 0, 1]]) * profil
    flade = dtuplot.plot3d_parametric_surface(
        *r,
        (u, 0, 2),
        (v, 0, 2 * pi),
        camera={"azim": -65, "elev": 25},
        use_cm=True,
        legend=False,
        show=False,
    )
    profil = Matrix([2 + sin(u), 0, u])
    dtuplot.plot3d_parametric_line(
        *profil,
        (u, 0, 8 * pi),
        use_cm=False,
        camera={"azim": -28, "elev": 13},
        show=False,
    )
    r = Matrix([(2 + sin(u)) * cos(v), (2 + sin(u)) * sin(v), u])
    flade = dtuplot.plot3d_parametric_surface(
        *r,
        (u, 0, 8 * pi),
        (v, 0, 2 * pi),
        camera={"azim": -62, "elev": 15},
        use_cm=True,
        legend=False,
        show=False,
    )
    lede = Matrix([2 * cos(u), sin(u), 0])
    dtuplot.plot3d_parametric_line(
        *lede, (u, 0, 2 * pi), use_cm=False, ylim=(-2, 2), xlim=(-2, 2), show=False
    )
    r = Matrix([lede[0], lede[1], v])
    flade = dtuplot.plot3d_parametric_surface(
        *r,
        (u, 0, 2 * pi),
        (v, 0, 1),
        ylim=(-2, 2),
        xlim=(-2, 2),
        zlim=(0, 2),
        use_cm=True,
        legend=False,
        show=False,
    )
    r = Matrix([2 * cos(u), sin(u), v * (2 * cos(u) + sin(u) ** 2)])
    dtuplot.plot3d_parametric_surface(
        *r,
        (u, 0, 2 * pi),
        (v, 0, 1),
        camera={"azim": -120, "elev": 20},
        use_cm=True,
        legend=False,
        show=False,
    )
    h = x**2 / 2 + y + 2
    with pytest.warns(
        UserWarning,
        match="The provided expression contains Boolean functions. In order to plot the expression, the algorithm automatically switched to an adaptive sampling.",
    ):
        dtuplot.plot_implicit(
            (x >= 0) & (x <= 2) & (y >= -2 * x) & (y <= 0),
            (x, 0, 2),
            (y, -4, 0),
            aspect="equal",
            show=False,
        )
    trekant = Matrix([u, v * (-2 * u)])
    u_range = (u, 0, 2)
    v_range = (v, 0, 1)
    r = Matrix([trekant[0], trekant[1], h.subs({x: trekant[0], y: trekant[1]})])
    flade = dtuplot.plot3d_parametric_surface(
        *r,
        u_range,
        v_range,
        show=False,
        rendering_kw={"color": "blue"},
        camera={"azim": -155, "elev": 15},
    )
    grundflade = dtuplot.plot3d_parametric_surface(
        r[0], r[1], 0, u_range, v_range, show=False, rendering_kw={"alpha": 0.6}
    )
    res = flade + grundflade
    kryds = r.diff(u).cross(r.diff(v))
    Jacobi = kryds.norm()
    assert Jacobi.simplify() == 2 * sqrt(u**2 + 2) * abs(u)
    assert abs(integrate(Jacobi, u_range, v_range).evalf() - 7.91234) < 1e-3
    profil = Matrix([3 + cos(u), 0, sin(u)])
    u_range = (u, 0, 2 * pi)
    h = z**2
    dtuplot.plot_parametric(
        profil[0],
        profil[2],
        u_range,
        xlim=(0, 4),
        ylim=(-1, 1),
        ylabel="z",
        use_cm=False,
        aspect="equal",
        show=False,
    )
    r = Matrix([[cos(v), -sin(v), 0], [sin(v), cos(v), 0], [0, 0, 1]]) * profil
    v_range = (v, 0, 2 * pi)
    flade = dtuplot.plot3d_parametric_surface(
        *r, u_range, v_range, zlim=(-4, 4), use_cm=True, legend=False, show=False
    )
    Jacobi = r.diff(u).cross(r.diff(v)).norm().simplify()
    assert Jacobi == abs(cos(u) + 3)
    integrand = h.subs({x: r[0], y: r[1], z: r[2]}) * Jacobi
    assert integrate(integrand, u_range, v_range) == 6 * pi**2
    integrand = Jacobi
    assert integrate(integrand, u_range, v_range) == 12 * pi**2


def test_week6():
    ## Tænk ikke for meget over dette

    x, y, z, u, v, w = symbols("x y z u v w", real=True)
    ur = (u, 0, 1)
    l1 = dtuplot.plot3d_parametric_line(
        u, 0, 0, ur, show=False, use_cm=False, rendering_kw={"color": "red"}
    )
    l2 = dtuplot.plot3d_parametric_line(
        0, u, 0, ur, show=False, use_cm=False, rendering_kw={"color": "red"}
    )
    l3 = dtuplot.plot3d_parametric_line(
        0, 0, u, ur, show=False, use_cm=False, rendering_kw={"color": "red"}
    )
    l4 = dtuplot.plot3d_parametric_line(
        1 - u, u, 0, ur, show=False, use_cm=False, rendering_kw={"color": "red"}
    )
    l5 = dtuplot.plot3d_parametric_line(
        u, 0, 1 - u, ur, show=False, use_cm=False, rendering_kw={"color": "red"}
    )
    l6 = dtuplot.plot3d_parametric_line(
        0, u, 1 - u, ur, show=False, use_cm=False, rendering_kw={"color": "red"}
    )
    grundflade = dtuplot.plot3d_parametric_surface(
        u * (1 - v),
        v,
        0,
        ur,
        (v, 0, 1),
        show=False,
        rendering_kw={"color": "blue", "alpha": 0.75},
    )
    dash1 = dtuplot.plot3d_parametric_line(
        0.3,
        0.7 * u,
        0,
        ur,
        show=False,
        use_cm=False,
        rendering_kw={"color": "grey", "linestyle": "dashed"},
    )
    dash2 = dtuplot.plot3d_parametric_line(
        0.3,
        0.7 - 0.7 * u,
        0.7 * u,
        ur,
        show=False,
        use_cm=False,
        rendering_kw={"color": "grey", "linestyle": "dashed"},
    )
    dash3 = dtuplot.plot3d_parametric_line(
        0.3,
        0,
        0.7 * u,
        ur,
        show=False,
        use_cm=False,
        rendering_kw={"color": "grey", "linestyle": "dashed"},
    )
    pil3d = dtuplot.quiver(
        Matrix([0.3, 0.375, 0]),
        Matrix([0, 0, 0.375]),
        show=False,
        rendering_kw={"color": "black"},
    )

    with pytest.warns(
        UserWarning,
        match="The provided expression contains Boolean functions. In order to plot the expression, the algorithm automatically switched to an adaptive sampling.",
    ):
        bund = dtuplot.plot_implicit(
            (x >= 0) & (x <= 1) & (y >= 0) & (y <= 1 - x),
            (x, 0, 1),
            (y, 0, 1),
            show=False,
        )
    pil2d = dtuplot.quiver(
        Matrix([0.2, 0]),
        Matrix([0, 0.8]),
        show=False,
        rendering_kw={"color": "black", "width": 0.025},
    )

    skelet = l1 + l2 + l3 + l4 + l5 + l6 + dash1 + dash2 + dash3 + pil3d
    tetra = grundflade + skelet
    tetra.legend = False
    tetra.camera = {"azim": 25, "elev": 25}
    tetra.size = (6, 6)
    trekant = bund + pil2d
    trekant.legend = False
    trekant.grid = False

    d = dtuplot.plotgrid(tetra, trekant, nr=1, nc=2, size=(6, 6), show=False)
    f = (1 - x) ** 2
    h = 1 - x - y
    bund_punkt = Matrix([u, v * (1 - u), 0])
    top_punkt = Matrix([u, v * (1 - u), h.subs({x: u, y: v * (1 - u)})])
    r = bund_punkt + w * (top_punkt - bund_punkt)
    _ = Matrix.hstack(*[r.diff(v) for v in [u, v, w]])
    determinanten = _.det()  # underscore holder værdien fra seneste output
    Jacobi = determinanten
    # vi ved at determinanten er positiv i det betragtede område, så det er ikke nødvendigt at tage absolut værdien
    # Jacobi.simplify()
    assert Jacobi.factor() == -((u - 1) ** 2 * (v - 1)).factor()
    M = integrate(
        f.subs({x: r[0], y: r[1], z: r[2]}) * Jacobi, (u, 0, 1), (v, 0, 1), (w, 0, 1)
    )
    assert M == S(1) / 10
    xi = (
        Matrix(
            [
                integrate(
                    coord * f.subs({x: r[0], y: r[1], z: r[2]}) * Jacobi,
                    (u, 0, 1),
                    (v, 0, 1),
                    (w, 0, 1),
                )
                for coord in r
            ]
        )
        / M
    )
    assert xi == Matrix([S(1) / 6, S(5) / 18, S(5) / 18])
    with pytest.warns(
        UserWarning,
        match="The provided expression contains Boolean functions. In order to plot the expression, the algorithm automatically switched to an adaptive sampling.",
    ):
        dtuplot.plot_implicit(
            (x >= 1 / 2) & (x <= 2) & (y <= 1 / x) & (y >= 0),
            (x, 0, 2),
            (y, 0, 2),
            show=False,
        )
    profil = Matrix([u, 0, v / u])
    legeme = Matrix([[cos(w), -sin(w), 0], [sin(w), cos(w), 0], [0, 0, 1]]) * profil
    determinanten = Matrix.hstack(*[legeme.diff(v) for v in [u, v, w]]).det()
    Jacobi = abs(determinanten.simplify())
    assert Jacobi == 1
    assert integrate(Jacobi, (u, S(1) / 2, 2), (v, 0, 1), (w, 0, 2 * pi)) == 3 * pi
    l1 = Eq(y, cos(x))
    l2 = Eq(y, cos(x) + 1)
    x_range = (x, 0, 2 * pi)

    dtuplot.plot_implicit(l1, l2, x_range, (y, -1, 2), aspect="equal", show=False)
    mur = Matrix([u, cos(u) + v, w * u / 2])
    determinanten = Matrix.hstack(*[mur.diff(v) for v in [u, v, w]]).det()
    ## antag at variablerne er positive
    Jacobi = abs(posify(determinanten)[0])
    assert determinanten == u / 2
    f = 1 / x
    integrand = (f.subs({x: mur[0], y: mur[1], z: mur[2]}) * Jacobi).simplify()
    integrand = S(1) / 2
    assert integrate(integrand, (u, 0, 2 * pi), (v, 0, 1), (w, 0, 1)) == pi


def test_week7():
    # Store dag
    assert True
    x, y, z, u = symbols("x y z u", real=True)
    r1 = Matrix([cos(u), sin(u), u / 2])
    r2 = Matrix([1, 0, u / 2])
    V = Matrix([-y, x, 2 * z])
    u_range = (u, 0, 4 * pi)

    K1 = dtuplot.plot3d_parametric_line(
        *r1, u_range, show=False, rendering_kw={"color": "red"}
    )
    K2 = dtuplot.plot3d_parametric_line(
        *r2, u_range, show=False, rendering_kw={"color": "blue"}
    )
    felt = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, 0, 6),
        show=False,
        quiver_kw={"alpha": 0.5, "length": 0.1, "color": "black"},
        n=5,
    )

    combined = K1 + K2 + felt
    combined.legend = False
    r1d = r1.diff(u)
    r2d = r2.diff(u)
    integrand1 = V.subs({x: r1[0], y: r1[1], z: r1[2]}).dot(r1d)
    integrand2 = V.subs({x: r2[0], y: r2[1], z: r2[2]}).dot(r2d)
    integrand1.simplify(), integrand2.simplify()
    assert integrate(integrand1, (u, 0, 4 * pi)) == 4 * pi + 4 * pi**2
    assert integrate(integrand2, (u, 0, 4 * pi)) == 4 * pi**2

    u_range = (u, 0, 1)
    r1 = dtuplot.plot3d_parametric_line(
        u, 0, 0, u_range, show=False, rendering_kw={"color": "red"}
    )
    r2 = dtuplot.plot3d_parametric_line(
        1, u, 0, u_range, show=False, rendering_kw={"color": "red"}
    )
    r3 = dtuplot.plot3d_parametric_line(
        1, 1, u, u_range, show=False, rendering_kw={"color": "red"}
    )
    xyz = dtuplot.scatter(
        Matrix([1, 1, 1]), show=False, rendering_kw={"color": "black"}
    )
    combined = r1 + r2 + r3 + xyz
    combined.legend = False
    combined.camera = {"azim": 37, "elev": 16}

    r1 = Matrix([u, 0, 0])
    r2 = Matrix([x, u, 0])
    r3 = Matrix([x, y, u])
    r1d = r1.diff(u)
    r2d = r2.diff(u)
    r3d = r3.diff(u)
    r1d, r2d, r3d

    V = Matrix([y**2 + z, 2 * y * z**2 + 2 * y * x, 2 * y**2 * z + x])
    integrand1 = V[0].subs({x: u, y: 0, z: 0})
    integrand2 = V[1].subs({y: u, z: 0})
    integrand3 = V[2].subs({z: u})
    assert integrand1 == 0
    assert integrand2 == 2 * u * x
    assert integrand3 == 2 * u * y**2 + x
    F = (
        integrate(integrand1, (u, 0, x))
        + integrate(integrand2, (u, 0, y))
        + integrate(integrand3, (u, 0, z))
    )
    V_F = dtutools.gradient(F)
    assert Eq(V_F, V) == True
    t = symbols("t")
    knude = (
        Matrix(
            [
                -10 * cos(t) - 2 * cos(5 * t) + 15 * sin(2 * t),
                -15 * cos(2 * t) + 10 * sin(t) - 2 * sin(5 * t),
                10 * cos(3 * t),
            ]
        )
        * S(1)
        / 10
    )
    dtuplot.plot3d_parametric_line(
        *knude, (t, -pi, pi), rendering_kw={"color": "blue"}, legend=False, show=False
    )
    assert (
        integrate(
            V.subs({x: knude[0], y: knude[1], z: knude[2]}).dot(knude.diff(t)),
            (t, -pi, pi),
        )
        == 0
    )

    # Lille dag
    x, y, z = symbols("x y z")
    f = x**2 * sin(y) * z
    df = dtutools.gradient(f)
    dtutools.gradient(f, [x, z])
    df0 = df.subs([(x, 1), (y, 2), (z, 3)])
    assert abs(N(df0)[0] - 5.45578) < 1e-4
    assert abs(N(df0)[1] + 1.2484) < 1e-4
    assert abs(N(df0)[2] - 0.909297) < 1e-4
    V = Matrix([x * y * sin(z), x * ln(y), -x * y * z**3])
    divV = dtutools.div(V, var=[x, y, z])
    assert divV == -3 * x * y * z**2 + x / y + y * sin(z)
    u, v, w = symbols("u v w")
    # v optræder ikke i vektorfeltet
    V2 = Matrix([u, w**2, u * sin(w)])
    assert dtutools.div(V2, var=[u, v, w]) == u * cos(w) + 1
    divV0 = divV.subs([(x, 1), (y, 2), (z, 3)])
    N(divV0)
    rotV = dtutools.rot(V, var=[x, y, z])
    assert rotV == Matrix([-x * z**3, x * y * cos(z) + y * z**3, -x * sin(z) + log(y)])
    assert dtutools.rot(V2, var=[u, v, w]) == Matrix([-2 * w, -sin(w), 0])
    rotV0 = rotV.subs([(x, 1), (y, 2), (z, 3)])
    N(rotV0)


def test_week8():
    x, y, z = symbols("x y z")
    V = Matrix([x, y, 2])
    u, v = symbols("u v")
    r = Matrix([u * cos(v), u * sin(v), u**2])
    p_parab = dtuplot.plot3d_parametric_surface(
        *r,
        (u, 0, 1),
        (v, -pi, pi),
        use_cm=False,
        camera={"elev": 25, "azim": -55},
        show=False,
    )
    p_felt = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, 0, 1.2),
        n=4,
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.1, "color": "red"},
        show=False,
    )
    res = p_parab + p_felt
    # Kommer vektorer fra alle hjørner. Der kommer for mange
    # vektorer hvis "p_parab" bruges, så her sættes n ned
    dummy_surface = dtuplot.plot3d_parametric_surface(
        *r, (u, 0, 1), (v, -pi, pi), n=8, show=False
    )
    p_felt2 = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, 0, 1),
        slice=dummy_surface[0],
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.1, "color": "red"},
        show=False,
    )
    # bedre kamera vinkel til at se vektorerne her
    p_parab.camera = {"elev": 60, "azim": -50}
    res = p_parab + p_felt2
    N_parab = r.diff(u).cross(r.diff(v))
    simplify(N_parab)
    N_parab = -simplify(N_parab)
    N_parab.norm().simplify()
    integrand = N_parab.dot(V.subs({x: r[0], y: r[1], z: r[2]}))
    assert simplify(integrand) == 2 * u * (u**2 - 1)
    assert integrate(integrand, (u, 0, 1), (v, -pi, pi)) == -pi
    r2 = Matrix([u * cos(v), u * sin(v), 1])
    n2 = r2.diff(u).cross(r2.diff(v))
    assert simplify(n2) == Matrix([0, 0, u])
    integrand2 = n2.dot(V.subs({x: r2[0], y: r2[1], z: r2[2]}))
    assert integrate(integrand2, (u, 0, 1), (v, -pi, pi)) == 2 * pi
    p_låg = dtuplot.plot3d_parametric_surface(
        *r2,
        (u, 0, 1),
        (v, -pi, pi),
        use_cm=False,
        n1=4,
        n2=16,
        camera={"elev": 25, "azim": -55},
        show=False,
    )
    p_feltlåg = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, 0, 1),
        slice=p_låg[0],
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.1, "color": "red"},
        show=False,
    )
    p_parab.camera = {"elev": 15, "azim": -60}
    res = p_parab + p_felt2 + p_låg + p_feltlåg
    V = Matrix([-x + cos(z), -y * x, 3 * z + exp(y)])
    a = symbols("a")
    # Da man ikke kan plotte et 3D volumen (nemt), plotter vi overfladerne,
    p = dtuplot.plot3d_parametric_surface(
        x,
        y,
        y**2,
        (x, 0, 3),
        (y, 0, 2),
        {"color": "royalblue"},
        use_cm=False,
        aspect="equal",
        show=False,
    )
    p.extend(
        dtuplot.plot3d_parametric_surface(
            0,
            y,
            a * y**2,
            (a, 0, 1),
            (y, 0, 2),
            {"color": "royalblue", "alpha": 0.5},
            use_cm=False,
            aspect="equal",
            show=False,
        )
    )
    p.extend(
        dtuplot.plot3d_parametric_surface(
            3,
            y,
            a * y**2,
            (a, 0, 1),
            (y, 0, 2),
            {"color": "royalblue", "alpha": 0.5},
            use_cm=False,
            aspect="equal",
            show=False,
        )
    )
    p.extend(
        dtuplot.plot3d_parametric_surface(
            x,
            2,
            a * 4,
            (x, 0, 3),
            (a, 0, 1),
            {"color": "royalblue", "alpha": 0.5},
            use_cm=False,
            aspect="equal",
            show=False,
        )
    )
    p.extend(
        dtuplot.plot3d_parametric_surface(
            x,
            y,
            0,
            (x, 0, 3),
            (y, 0, 2),
            {"color": "royalblue", "alpha": 0.5},
            use_cm=False,
            aspect="equal",
            show=False,
        )
    )
    p_felt = dtuplot.plot_vector(
        V,
        (x, 0, 3),
        (y, 0, 2),
        (z, 0, 4),
        n=4,
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.05, "color": "red"},
        show=False,
    )
    res = p + p_felt
    u, v, w = symbols("u v w")
    r = Matrix([u, v, w * v**2])
    M = Matrix.hstack(r.diff(u), r.diff(v), r.diff(w))
    jacobi = M.det()
    assert jacobi == v**2
    divV = dtutools.div(V, var=[x, y, z])
    assert divV == 2 - x
    divV_r = divV.subs({x: r[0], y: r[1], z: r[2]})
    assert divV_r == 2 - u
    assert integrate(divV_r * jacobi, (u, 0, 3), (v, 0, 2), (w, 0, 1)) == 4
    x, y, z = symbols("x y z")
    V = Matrix([-y + x, x, z])
    u, v = symbols("u v")
    radius = 2
    r = radius * Matrix([sin(u) * cos(v), sin(u) * sin(v), cos(u)])
    p_surface = dtuplot.plot3d_spherical(
        radius,
        (u, pi / 6, pi / 2),
        (v, 0, pi),
        aspect="equal",
        camera={"elev": 25, "azim": 55},
        show=False,
    )
    dummy_surface = dtuplot.plot3d_spherical(
        radius, (u, pi / 6, pi / 2), (v, 0, pi), show=False, n=8
    )
    p_felt = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, 0, 1),
        slice=dummy_surface[0],
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.2, "color": "red"},
        show=False,
    )
    res = p_surface + p_felt
    N = r.diff(u).cross(r.diff(v))
    integrand = N.dot(V.subs({x: r[0], y: r[1], z: r[2]}))
    assert (
        integrate(integrand, (u, pi / 6, pi / 2), (v, 0, pi)) == S(5) * sqrt(3) * pi / 2
    )
    V = Matrix([8 * x, 8, 4 * z**3])
    r = u * Matrix([sin(v) * cos(w), sin(v) * sin(w), cos(v)])
    M = Matrix.hstack(r.diff(u), r.diff(v), r.diff(w))
    # determinanten er positiv. Eneste led der ikke er
    # kvadreret er sin(v), som er positiv indenfor v's grænser
    jacobi = M.det()
    divV = dtutools.div(V, [x, y, z])
    divV_r = divV.subs({x: r[0], y: r[1], z: r[2]})
    assert (
        integrate(divV_r * jacobi, (u, 0, a), (v, 0, pi / 2), (w, -pi, pi))
        == S(8) * pi * a**5 / 5 + S(16) * pi * a**3 / 3
    )
    # Første flade tilsvarer at fastsætte u til radius
    r1 = r.subs(u, a)
    n1 = r1.diff(v).cross(r1.diff(w))  # har tjekket at den pejer udad
    integrand1 = n1.dot(V.subs({x: r1[0], y: r1[1], z: r1[2]}))
    flux1 = integrate(integrand1, (v, 0, pi / 2), (w, -pi, pi))
    # Anden flade tilsvarer at fastsætte v til pi/2
    # Tilbageværende bliver skiven med radius a
    r2 = r.subs(v, pi / 2)
    n2 = -r2.diff(u).cross(r2.diff(w))  # skal være negativ før at den pejer udad
    integrand2 = n2.dot(V.subs({x: r2[0], y: r2[1], z: r2[2]}))
    flux2 = integrate(integrand2, (u, 0, a), (w, -pi, pi))
    assert flux1 + flux2 == S(8) * pi * a**5 / 5 + S(16) * pi * a**3 / 3


def test_week9():
    x, y, z = symbols("x y z")
    V = Matrix([3 * z, 5 * x, -2 * y])
    u = symbols("u")
    s = Matrix([cos(u), sin(u), sin(u)])
    p_kurve = dtuplot.plot3d_parametric_line(
        *s,
        (u, 0, 2 * pi),
        {"color": "orange", "linewidth": 5},
        zlim=(-1.1, 1.1),
        use_cm=False,
        aspect="equal",
        show=False,
    )
    p_felt = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, -1, 1),
        n=4,
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.05, "color": "red"},
        show=False,
    )
    res = p_kurve + p_felt
    ds = s.diff(u)
    integrand = ds.dot(V.subs({x: s[0], y: s[1], z: s[2]}))
    assert integrate(integrand, (u, 0, 2 * pi)) == 2 * pi
    u, v = symbols("u v")
    r = Matrix([u * cos(v), u * sin(v), u * sin(v)])
    assert dtutools.rot(V, var=[x, y, z]) == Matrix([-2, 3, 5])
    p_flade = dtuplot.plot3d_parametric_surface(
        *r, (u, 0, 1), (v, 0, 2 * pi), use_cm=False, show=False
    )
    p_felt_rot = dtuplot.plot_vector(
        dtutools.rot(V, var=[x, y, z]),
        (x, -1, 1),
        (y, -1, 1),
        (z, -1, 1),
        n=4,
        use_cm=False,
        quiver_kw={"alpha": 0.5, "length": 0.05, "color": "red"},
        show=False,
    )
    res = p_kurve + p_flade + p_felt_rot
    N = r.diff(u).cross(r.diff(v))
    assert simplify(N) == Matrix([0, -u, u])
    p_normalvektor = dtuplot.quiver(s.subs(u, 0), N.subs({u: 1, v: 0}), show=False)
    p_omloebs = dtuplot.quiver(s.subs(u, 0), ds.subs(u, 0), show=False)
    p_kurve.camera = {"elev": 5, "azim": -35}
    res = p_kurve + p_flade + p_normalvektor + p_omloebs
    integrand = N.dot(dtutools.rot(V, var=[x, y, z]))
    assert simplify(integrand) == 2 * u
    assert integrate(integrand, (v, 0, 2 * pi), (u, 0, 1)) == 2 * pi
    x, y, z, u, v = symbols("x y z u v")
    V = Matrix([y * x, y * z, x * z])
    r = Matrix([cos(v) * (1 + u**2), sin(v) * (1 + u**2), sin(u)])
    p_flade = dtuplot.plot3d_parametric_surface(
        *r,
        (u, -pi / 2, pi / 2),
        (v, -pi, pi / 2),
        use_cm=False,
        aspect="equal",
        camera={"elev": 30, "azim": -80},
        show=False,
    )
    dummy_surface = dtuplot.plot3d_parametric_surface(
        *r, (u, -pi / 2, pi / 2), (v, -pi, pi / 2), n=10, show=False
    )
    p_felt_flade = dtuplot.plot_vector(
        V,
        (x, -1, 1),
        (y, -1, 1),
        (z, -1, 1),
        slice=dummy_surface[0],
        quiver_kw={"alpha": 0.5, "length": 0.2, "color": "red"},
        use_cm=False,
        show=False,
    )
    # Vi vil gerne kende retningen af normalvektoren, så vi
    # sikrer os at vi gennemløber randen i den rigtige retning
    N = r.diff(u).cross(r.diff(v))
    # vektor dobbelt så lang, så den kan ses fra denne vinkel
    p_normalvektor = dtuplot.quiver(
        r.subs({u: 0, v: -pi / 4}),
        2 * N.subs({u: 0, v: -pi / 4}),
        {"color": "black"},
        show=False,
    )
    combined_flade = p_flade + p_felt_flade + p_normalvektor
    combined_flade.title = "Fladen og feltet"
    s1 = r.subs(u, -pi / 2)
    s2 = r.subs(u, pi / 2)
    s3 = r.subs(v, -pi)
    s4 = r.subs(v, pi / 2)
    ds1 = s1.diff(v)
    ds2 = s2.diff(v)
    ds3 = s3.diff(u)
    ds4 = s4.diff(u)
    p_rand = dtuplot.plot3d_parametric_line(
        *s1,
        (v, -pi, pi / 2),
        {"color": "orange", "linewidth": 5},
        use_cm=False,
        aspect="equal",
        camera={"elev": 30, "azim": -80},
        show=False,
    )
    p_rand.extend(
        dtuplot.plot3d_parametric_line(
            *s2,
            (v, -pi, pi / 2),
            {"color": "orange", "linewidth": 5},
            use_cm=False,
            show=False,
        )
    )
    p_rand.extend(
        dtuplot.plot3d_parametric_line(
            *s3,
            (u, -pi / 2, pi / 2),
            {"color": "orange", "linewidth": 5},
            use_cm=False,
            show=False,
        )
    )
    p_rand.extend(
        dtuplot.plot3d_parametric_line(
            *s4,
            (u, -pi / 2, pi / 2),
            {"color": "orange", "linewidth": 5},
            use_cm=False,
            show=False,
        )
    )
    p_flade_mesh = dtuplot.plot3d_parametric_surface(
        *r,
        (u, -pi / 2, pi / 2),
        (v, -pi, pi / 2),
        rendering_kw={"alpha": 0},
        wf_rendering_kw={"alpha": 0.4},
        wireframe=True,
        show=False,
    )
    p_felt = dtuplot.plot_vector(
        V,
        (x, -3, 3),
        (y, -3, 3),
        (z, -1, 1),
        quiver_kw={"alpha": 0.5, "length": 0.2, "color": "red"},
        n1=5,
        n2=5,
        n3=2,
        show=False,
    )
    # for hver af de 4 felter vil vi også gerne have retningen af deres afledte
    # dette skal bruges til at bestemme hvilken retning vi skal omløbe linjerne i
    p_omloebs = dtuplot.quiver(
        s1.subs({u: -pi / 2, v: -pi}),
        ds1.subs({u: -pi / 2, v: -pi}),
        {"color": "red"},
        show=False,
    )
    p_omloebs.extend(
        dtuplot.quiver(
            s2.subs({u: -pi / 2, v: -pi}),
            ds2.subs({u: -pi / 2, v: -pi}),
            {"color": "green"},
            show=False,
        )
    )
    p_omloebs.extend(
        dtuplot.quiver(
            s3.subs({u: -pi / 2, v: -pi}),
            ds3.subs({u: -pi / 2, v: -pi}),
            {"color": "blue"},
            show=False,
        )
    )
    p_omloebs.extend(
        dtuplot.quiver(
            s4.subs({u: -pi / 2, v: -pi}),
            ds4.subs({u: -pi / 2, v: -pi}),
            {"color": "purple"},
            show=False,
        )
    )
    combined_rand = p_rand + p_flade_mesh + p_felt + p_omloebs
    combined_rand.legend = False
    combined_rand.title = "Feltet på randen af fladen"
    dtuplot.plotgrid(combined_rand, combined_flade, nr=1, nc=2, show=False)
    i1 = ds1.dot(V.subs({x: s1[0], y: s1[1], z: s1[2]}))
    i2 = ds2.dot(V.subs({x: s2[0], y: s2[1], z: s2[2]}))
    i3 = ds3.dot(V.subs({x: s3[0], y: s3[1], z: s3[2]}))
    i4 = ds4.dot(V.subs({x: s4[0], y: s4[1], z: s4[2]}))
    assert (
        simplify(
            -integrate(i1, (v, -pi, pi / 2))
            + integrate(i2, (v, -pi, pi / 2))
            + integrate(i3, (u, -pi / 2, pi / 2))
            - integrate(i4, (u, -pi / 2, pi / 2))
        )
        == -S(5) * pi**2 / 2 + pi**4 / 16 + 21
    )
    integrand = N.dot(dtutools.rot(V, var=[x, y, z]).subs({x: r[0], y: r[1], z: r[2]}))
    simplify(integrand)
    assert (
        integrate(integrand, (u, -pi / 2, pi / 2), (v, -pi, pi / 2))
        == -S(5) * pi**2 / 2 + pi**4 / 16 + 21
    )
