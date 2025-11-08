import numpy as np


def get_rotation_angles(number):
    '''
    Returns a list of theta, phi values, approximately evenly
    distributed on the sphere.

    Uses the generalised spiral points algorithm explained in
    E B Saff and
    A B J Kuijlaars, Distributing many points on a sphere, The
    Mathematical Intelligencer 19(1) 1997.
    '''

    angles = np.zeros((number, 2))
    angles[0] = np.array([np.arccos(-1), 0])

    for k in range(2, number+1):
        h_k = -1. + (2. * (k - 1)) / (number - 1)
        theta = np.arccos(h_k)
        phi = (angles[k-2, 1] + 3.6/np.sqrt(number) *
               1. / np.sqrt(1 - h_k**2)) % (2*np.pi)
        angles[k-1, 0] = theta
        angles[k-1, 1] = phi
    angles[-1, 1] = 0.  # Last phi will be inf otherwise

    return angles

def rotate_vector_to_top(vector):
    '''Returns a rotation matrix that will rotate the given vector to
    point upwards.

    Parameters
    ----------
    vector : ndarray
        The (3D) vector to rotate.
    '''

    theta = np.arccos(vector[2] / np.linalg.norm(vector))
    phi = np.arctan2(vector[1], vector[0])
    return rotate_to_top(theta, phi)

def rotate_to_top(theta, phi):

    '''
    Returns a rotation matrix that will rotate a sphere such that
    the given positions are at the top.

    Parameters
    ----------
    theta : float
        The latitudinal variable.
    phi : float
        The longitudinal variable.
    '''

    chi = -1 * phi
    alpha = theta

    cc = np.cos(chi)
    sc = np.sin(chi)
    ca = np.cos(alpha)
    sa = np.sin(alpha)
    first_rotation = np.array([[cc, -sc, 0],
                              [sc, cc, 0],
                              [0, 0, 1]])
    second_rotation = np.array([[ca, 0, -sa],
                               [0, 1, 0],
                               [sa, 0, ca]])

    return second_rotation.dot(first_rotation)

def rotate_axis_angle(axis, angle):
    axis = np.array(axis) / np.linalg.norm(axis)
    ux, uy, uz = axis

    ct = np.cos(angle)
    st = np.sin(angle)
    
    arr = np.array(
        [[ct + ux**2*(1-ct), ux*uy*(1-ct) - uz*st, ux*uz*(1-ct) + uy*st],
         [uy*ux*(1-ct) + uz*st, ct + uy**2*(1-ct), uy*ux*(1-ct) - ux*st],
         [uz*ux*(1-ct) - uy*st, uz*uy*(1-ct) + ux*st, ct + uz**2*(1-ct)]])

    return arr
    
