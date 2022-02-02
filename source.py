import numpy as np


class Source:

    def __init__(self, strength, x0, y0):
        self.strength = strength
        self.x0 = x0
        self.y0 = y0

    def evaluate(self, x_map, y_map):
        i = (self.strength / (2 * np.pi)) * (x_map - self.x0) / ((x_map - self.x0) ** 2 + (y_map - self.y0) ** 2)
        j = (self.strength / (2 * np.pi)) * (y_map - self.y0) / ((x_map - self.x0) ** 2 + (y_map - self.y0) ** 2)
        return i, j


class Vortex:

    def __init__(self, strength, x0, y0):
        self.strength = strength
        self.x0 = x0
        self.y0 = y0

    def evaluate(self, x_map, y_map):  # not working?
        u = -(self.strength / (2 * np.pi)) * (y_map - self.y0) / ((x_map - self.x0) ** 2 + (y_map - self.y0) ** 2)
        v = (self.strength / (2 * np.pi)) * (x_map - self.x0) / ((x_map - self.x0) ** 2 + (y_map - self.y0) ** 2)
        return u, v


class Doublet:

    def __init__(self, strength, x0, y0):
        self.strength = strength
        self.x0 = x0
        self.y0 = y0

    def evaluate(self, x_map, y_map):  # not working?
        w = -(self.strength / (2 * np.pi)) * ((x_map - self.x0) ** 2 - (y_map - self.y0) ** 2) / ((x_map - self.x0) ** 2 + (y_map - self.y0) ** 2)**2
        z = -(self.strength / (2 * np.pi)) * 2 * (x_map - self.x0) * (y_map - self.y0) / ((x_map - self.x0) ** 2 + (y_map - self.y0) ** 2) ** 2
        return w, z

