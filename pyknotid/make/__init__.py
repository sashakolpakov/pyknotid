'''
This module provides functions for creating knotted or linked space
curves, for inspection or use as examples.

All knot creating functions are available in the pyknotid.make
namespace, although they are distributed amongst other modules as below.

'''
# from pyknotid.make import knot
# from pyknotid.make import randomwalks

# from pyknotid.make.ideal import available_ideal_knots, ideal_knot
from pyknotid.make.torus import torus_knot, torus_link
from pyknotid.make.named import (
    unknot, k3_1, trefoil, k4_1, figure_eight,
    lissajous, k5_2, k6_1, k3_1_composite_3_1, k8_21
)

__all__ = [
    'torus_knot', 'torus_link',
    'unknot', 'k3_1', 'trefoil', 'k4_1', 'figure_eight',
    'lissajous', 'k5_2', 'k6_1', 'k3_1_composite_3_1', 'k8_21'
]
