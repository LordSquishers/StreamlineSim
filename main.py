import numpy as np
import matplotlib.pyplot as plt
from source import Source, Vortex, Doublet

wx = [-3, 3]
wy = [-2, 2]

DEFAULT_STRENGTH_SOURCE = 1
STAGNATION_POINT_TOLERANCE = 0.25

Y, X = np.mgrid[wy[0]:wy[1]:100j, wx[0]:wx[1]:100j]

# sources = [Source(0, 0, 0), Vortex(0, 0, 0), Doublet(0, 0, 0)]
sources = [Source(1, -0.5, 0), Source(-1, 0.5, 0)]


def calculate_fluid():
    # vector fields
    u = 1  # streamline of strength 1 in x+ direction
    v = 0

    for src in sources:
        su, sv = src.evaluate(X, Y)
        u = u + su
        v = v + sv

    stagnation_points = [[], []]

    X_step = (wx[1] - wx[0]) / 100.0
    current_x = wx[0]
    i = 0
    j = 0

    for u0 in u:
        for ux in u0:
            if abs(ux) < STAGNATION_POINT_TOLERANCE and abs(v[i, j]) < STAGNATION_POINT_TOLERANCE:
                # print(current_x, Y[i, j])
                stagnation_points[0].append(current_x)
                stagnation_points[1].append(Y[i, j])
            current_x = current_x + X_step
            j = j + 1
        current_x = wx[0]
        j = 0
        i = i + 1

    # Varying color along a streamline
    fig = plt.figure(figsize=(12, 7))

    plt.xlim(wx)
    plt.ylim(wy)

    strm = plt.streamplot(X, Y, u, v, color=u, linewidth=1.5, cmap='plasma')
    fig.colorbar(strm.lines)

    for src in sources:
        if src.strength == 0:
            continue
        plt.scatter(src.x0, src.y0)

    plt.xlabel('x')
    plt.ylabel('y')

    plt.title('Incompressible Fluid Simulation')
    plt.text(-1.25, wy[0] - 0.5, '[Source | Sink | AC Vortex | C Vortex | Doublet | Clear]')
    plt.scatter(wx[0] + 0.1, wy[1] - 0.1, color='red')
    plt.scatter(stagnation_points[0], stagnation_points[1], color='red', marker='x')

    plt.show(block=False)


calculate_fluid()


while True:
    clicks = plt.ginput(6, 0, False)

    state = 0
    for nx, ny in clicks:
        if abs(nx - wx[0]) < 0.1 and abs(ny - wy[1]) < 0.1:
            state = state + 1
            continue
        else:
            if state == 5:
                sources = [Source(0, 0, 0)]

        if state == 4:
            value = DEFAULT_STRENGTH_SOURCE
            sources.append(Doublet(value, nx, ny))
        if state == 2 or state == 3:
            value = DEFAULT_STRENGTH_SOURCE * (1 if state == 2 else -1)
            sources.append(Vortex(value, nx, ny))
        if state == 0 or state == 1:
            value = DEFAULT_STRENGTH_SOURCE * (1 if state == 0 else -1)
            sources.append(Source(value, nx, ny))

        state = state + 1
    plt.close()
    calculate_fluid()
