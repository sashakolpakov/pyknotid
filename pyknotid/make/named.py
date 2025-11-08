'''Named knots and links
=====================

Functions for making certain knots. The knots available are an
arbitrary selection based on known analytic forms.

Each of these functions returns a
:class:`~pyknotid.spacecurves.knot.Knot` or other appropriate pyknotid
space curve class.

API documentation
-----------------

'''

import numpy as np

from pyknotid.spacecurves.knot import Knot

__all__ = [
    'unknot', 'k3_1', 'trefoil', 'k4_1', 'figure_eight',
    'lissajous', 'k5_2', 'k6_1', 'k3_1_composite_3_1', 'k8_21'
]

def unknot(num_points=100):
    '''Returns a simple circle.'''
    data = np.zeros((num_points, 3), dtype=np.float64)
    ts = np.linspace(0, 2*np.pi, num_points)
    data[:, 0] = 3*np.sin(ts)
    data[:, 1] = 3*np.cos(ts)
    data[:, 2] = np.sin(3*ts)
    return Knot(data)

def k3_1(num_points=100):
    '''Returns a particular trefoil knot conformation.'''
    data = np.zeros((num_points, 3), dtype=np.float64)
    ts = np.linspace(0, 2*np.pi, num_points)
    data[:, 0] = (2+np.cos(3*ts))*np.cos(2*ts)
    data[:, 1] = (2+np.cos(3*ts))*np.sin(2*ts)
    data[:, 2] = np.sin(3*ts)
    return Knot(data)
trefoil = k3_1


def k4_1(num_points=100):
    '''Returns a particular figure eight knot conformation.'''
    data = np.zeros((num_points, 3), dtype=np.float64)
    ts = np.linspace(0, 2*np.pi, num_points)
    data[:, 0] = (2+np.cos(2*ts))*np.cos(3*ts)
    data[:, 1] = (2+np.cos(2*ts))*np.sin(3*ts)
    data[:, 2] = np.sin(4*ts)
    return Knot(data)
figure_eight = k4_1

def lissajous(nx=3, ny=2, nz=7, px=0.7, py=0.2, pz=0., num_points=100):
    '''Returns a `Lissajous knot
    <https://en.wikipedia.org/wiki/Lissajous_knot>`__ with the given
    parameters.'''
    data = np.zeros((num_points, 3), dtype=np.float64)
    ts = np.linspace(0, 2*np.pi, num_points)
    data[:, 0] = np.cos(nx*ts+px)
    data[:, 1] = np.cos(ny*ts+py)
    data[:, 2] = np.cos(nz*ts+pz)
    return Knot(data)


def k5_2(num_points=100):
    '''Returns a Lissajous conformation of the knot 5_2.'''
    return lissajous(3, 2, 7, 0.7, 0.2, 0., num_points)
three_twist = k5_2

def k6_1(num_points=100):
    '''Returns a Lissajous conformation of the knot 6_1.'''
    return lissajous(3, 2, 5, 1.5, 0.2, 0., num_points)
stevedore = k6_1

def k3_1_composite_3_1(num_points=100):
    '''Returns a Lissajous conformation of the composite double trefoil 3_1
    # 3_1.
    '''
    return lissajous(3, 5, 7, 0.7, 1., 0., num_points)
square = k3_1_composite_3_1

def k8_21(num_points=100):
    '''Returns a Lissajous conformation of the knot 8_21.'''
    return lissajous(3, 4, 7, 0.1, 0.7, 0., num_points)
