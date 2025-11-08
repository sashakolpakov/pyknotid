"""
Numba implementation of space curve helper functions (replacing chelpers.pyx).

This module requires numba for performance. If numba is not available,
import will fail and the pure Python 'helpers' module will be used instead.
"""
import numpy as np

try:
    import numba
    from numba.typed import List
except ImportError:
    raise ImportError("numba is required for nhelpers. Install with: pip install numba")


@numba.jit(nopython=True)
def cross_product(px, py, qx, qy):
    """Simple 2D cross product."""
    return px * qy - py * qx

@numba.jit(nopython=True)
def sign(a):
    """Return sign of a number."""
    if a > 0.:
        return 1.
    elif a < 0.:
        return -1.
    return 0.

@numba.jit(nopython=True)
def mag_difference(a, b):
    """The magnitude of the vector joining a and b."""
    return np.sqrt((b[0] - a[0])**2 + (b[1] - a[1])**2)

@numba.jit(nopython=True)
def _do_vectors_intersect(px, py, dpx, dpy, qx, qy, dqx, dqy):
    """
    Takes four vectors p, dp and q, dq, then tests whether they cross in
    the dp/dq region. Returns this boolean, and the (fractional) point where
    the crossing actually occurs.
    """
    cross_prod = cross_product(dpx, dpy, dqx, dqy)
    if abs(cross_prod) < 0.000001:
        return (0, 0., 0.)

    t = cross_product(qx - px, qy - py, dqx, dqy) / cross_prod
    if t < 1.0 and t > 0.0:
        u = cross_product(qx - px, qy - py, dpx, dpy) / cross_prod
        if u < 1.0 and u > 0.0:
            return (1, t, u)
    return (0, -1., -1.)

@numba.jit(nopython=True)
def _find_crossings_inner(v, dv, points, segment_lengths,
                         current_index, comparison_index,
                         max_segment_length, jump_mode):
        """
        Inner function for finding crossings (JIT compiled).

        Returns crossings as a 2D array instead of list of lists.
        """
        vx = v[0]
        vy = v[1]
        vz = v[2]
        dvx = dv[0]
        dvy = dv[1]
        dvz = dv[2]

        twice_max_segment_length = 2 * max_segment_length

        # Use a pre-allocated array to store crossings (max possible)
        # Each crossing creates 2 entries, max is len(points) crossings
        max_crossings = len(points) * 2
        crossings_data = np.zeros((max_crossings, 4), dtype=np.float64)
        crossing_count = 0

        i = 0
        already_jumped = 0

        while i < len(points) - 1:
            point = points[i]
            distance = np.sqrt((vx - point[0])**2 + (vy - point[1])**2)

            if distance < twice_max_segment_length or already_jumped:
                already_jumped = 0
                next_point = points[i + 1]
                jump_x = next_point[0] - point[0]
                jump_y = next_point[1] - point[1]
                jump_z = next_point[2] - point[2]

                intersect, intersect_i, intersect_j = _do_vectors_intersect(
                    vx, vy, dvx, dvy, point[0], point[1],
                    jump_x, jump_y)

                if intersect:
                    pz = point[2]
                    dpz = jump_z

                    crossing_sign = sign((vz + intersect_i * dvz) -
                                        (pz + intersect_j * dpz))

                    crossing_direction = sign(cross_product(
                        dvx, dvy, jump_x, jump_y))

                    # Add first crossing
                    crossings_data[crossing_count, 0] = current_index + intersect_i
                    crossings_data[crossing_count, 1] = comparison_index + intersect_j + i
                    crossings_data[crossing_count, 2] = crossing_sign
                    crossings_data[crossing_count, 3] = crossing_sign * crossing_direction
                    crossing_count += 1

                    # Add second crossing (reverse)
                    crossings_data[crossing_count, 0] = comparison_index + intersect_j + i
                    crossings_data[crossing_count, 1] = current_index + intersect_i
                    crossings_data[crossing_count, 2] = -1. * crossing_sign
                    crossings_data[crossing_count, 3] = crossing_sign * crossing_direction
                    crossing_count += 1

                i += 1

            elif jump_mode == 3:
                i += 1  # naive mode - check everything
                already_jumped = 1
            elif jump_mode == 2:
                num_jumps = int(np.floor(distance / max_segment_length)) - 1
                if num_jumps < 1:
                    num_jumps = 1
                i += num_jumps
                already_jumped = 1
            else:  # Catch all other jump modes
                distance_travelled = 0.
                jumps = 0
                while (distance_travelled < (distance - max_segment_length) and
                       i < len(points)):
                    jumps += 1
                    distance_travelled += segment_lengths[i]
                    i += 1
                if jumps > 1:
                    i -= 2
                already_jumped = 1

        # Return only the filled part of the array
        return crossings_data[:crossing_count]


def find_crossings(v, dv, points, segment_lengths, current_index,
                  comparison_index, max_segment_length, jump_mode=1):
    """
    Searches for crossings between the given vector and any other
    vector in the list of points, returning all of them as a list.

    Now uses Numba for performance instead of Cython.

    Parameters
    ----------
    v0 : ndarray
        The current point, a 1D vector.
    dv : ndarray
        The vector connecting the current point to the next one
    points : ndarray
        The array or (x, y) values of all the other points
    segment_lengths : ndarray
        The length of each segment joining a point to the
        next one.
    current_index : long
        The index of the point currently being tested.
    comparison_index : long
        The index of the first comparison point
    jump_mode : int
        1 to check every jump distance, 2 to jump based on
        the maximum one, 3 to never jump and check the length
        of every step.

    Returns
    -------
    list
        List of crossing data, each entry is [index1, index2, sign, direction]
    """
    # Get crossings as array
    crossings_array = _find_crossings_inner(
        v, dv, points, segment_lengths,
        current_index, comparison_index,
        max_segment_length, jump_mode
    )

    # Convert to list of lists for backward compatibility
    return [list(row) for row in crossings_array]
