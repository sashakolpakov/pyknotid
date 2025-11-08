'''
Random polygons from the quaternionic viewpoint [1]
===================================================

[1] These polygons are generated following the algorithms of (Cantarella, Deguchi and Shonkwiler. "Probability Theory of Random Polygons from the Quaternionic Viewpoint". Communications on Pure and Applied Mathematics 67 (2014).)
'''

import numpy as np

def get_closed_loop(length, seed=0, normalisation=7.5):
    '''
    Returns the points of a closed Cantarella walk with the given
    number of points.

    Parameters
    ----------
    length : int
        The number of segments in the walk.
    seed : int
        The random seed to use. Defaults to 0, which causes a new
        seed to be chosen randomly.
    normalisation : float
        The average segment length to normalise to. Defaults to 7.5,
        purely to work well with plotting defaults (tube radius 1).

    '''
    edges = closed_loop_segments(length, seed)
    return edges_to_path(edges) * normalisation * length / 2.

def get_open_line(length, seed=0, normalisation=7.5):
    '''
    Returns the points of an open Cantarella walk with the given
    number of points.

    Parameters
    ----------
    length : int
        The number of segments in the walk.
    seed : int
        The random seed to use. Defaults to 0, which causes a new
        seed to be chosen randomly.
    normalisation : float
        The average segment length to normalise to. Defaults to 7.5,
        purely to work well with plotting defaults (tube radius 1).
    '''
    edges = open_line_segments(length, seed)
    return edges_to_path(edges) * normalisation * length / 2.

def get_open_by_distance_line(length, distance=0., seed=0, normalisation=7.5):
    edges = open_by_distance_segments(length, distance, seed)
    return edges_to_path(edges) * normalisation * length / 2.

def open_line_segments(num, seed=0):
    if seed == 0:
        seed = np.random.randint(1000000)
        
    generator = np.random.RandomState()
    generator.seed(seed)
    
    # wjs is a vector uniformly distributed on the (4*num)-sphere
    # Such a vector is given by (4*num) normally distributed numbers in a
    # normalised vector
    wjs = generator.normal(size=4 * num)
    normfac = 1./np.sqrt(np.sum(wjs*wjs))
    wjs *= normfac
    
    # Redistribute wjs as sets of 4-points
    points = wjs.reshape((num, 4))
    
    edges = np.zeros((num, 3))
    
    # Create each edge as a transformation of the 4-points
    edges[:, 0] = (points[:, 0]**2 + points[:, 1]**2 - points[:, 2]**2 -
                   points[:, 3]**2)
    edges[:, 1] = 2 * (points[:, 1] * points[:, 2] - points[:, 0] *
                       points[:, 3])
    edges[:, 2] = 2 * (points[:, 0] * points[:, 2] - points[:, 1] *
                       points[:, 3])
    return edges


def closed_loop_segments(num, seed=0):
    if seed == 0:
        seed = np.random.randint(1000000)
        
    generator = np.random.RandomState()
    generator.seed(seed)
    
    uu = generator.normal(size=num) + 1j*generator.normal(size=num)
    vv = generator.normal(size=num) + 1j*generator.normal(size=num)
    
    u = uu / np.sqrt(uu.dot(uu.conj()))
    uconj = u.conj()
    vc = vv - u.conj().dot(vv)*u
    v = vc / np.sqrt(vc.dot(vc.conj()))
    vconj = v.conj()

    edges = np.zeros((num, 3),dtype=float)
    
    edges[:, 0] = (u * uconj - v * vconj).real
    edges[:, 1] = (-1j * (u * vconj - v * uconj)).real
    edges[:, 2] = (u * vconj + v * uconj).real
    
    return edges
    

def open_by_distance_segments(num, distance=0., seed=0):
    '''Get a list of line vectors whose sum fails to close by the given distance fraction.

    Parameters
    ----------
    num : int
        The number of segments
    distance : float
        The distance fraction (0 <= distance <= 1) by which their sum doesn't close.
    seed : int
        The random seed.
    '''
    if seed == 0:
        seed = np.random.randint(1000000)

    if distance > 1. or distance < 0.:
        raise ValueError('distance must be between 0 and 1')

    distance *= 2.

    generator = np.random.RandomState()
    generator.seed(seed)
    
    uu = generator.normal(size=num) + 1j*generator.normal(size=num)
    vv = generator.normal(size=num) + 1j*generator.normal(size=num)
    
    u = uu / np.sqrt(uu.dot(uu.conj()))
    uconj = u.conj()
    vc = vv - u.conj().dot(vv)*u
    v = vc / np.sqrt(vc.dot(vc.conj()))
    vconj = v.conj()

    # modu = np.sqrt(np.sum(u**2 + uconj**2))
    # print 'modu is', modu
    # u /= modu
    # uconj /= modu
    u *= np.sqrt(1 + distance / 2.)
    uconj *= np.sqrt(1 + distance / 2.)

    # modv = np.sqrt(np.sum(v**2 + vconj**2))
    # print 'modv is', modv
    # v /= modv
    # vconj /= modv
    v *= np.sqrt(1 - distance / 2.)
    vconj *= np.sqrt(1 - distance / 2.)

    # print 'mod u', np.sqrt(np.sum(u**2 + uconj**2)), np.sqrt(1 + distance/2.)
    # print 'mod v', np.sqrt(np.sum(v**2 + vconj**2)), np.sqrt(1 - distance/2.)

    edges = np.zeros((num, 3),dtype=float)
    
    edges[:, 0] = (u * uconj - v * vconj).real
    edges[:, 1] = (-1j * (u * vconj - v * uconj)).real
    edges[:, 2] = (u * vconj + v * uconj).real
    
    return edges

def edges_to_path(edges):
    num = len(edges)
    path = np.zeros((num + 1, 3))
    for i in range(num):
        path[i+1] = path[i] + edges[i]
    return path
