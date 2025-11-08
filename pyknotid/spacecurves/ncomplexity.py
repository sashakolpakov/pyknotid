"""
Numba implementation of complexity functions (replacing ccomplexity.pyx).

This module requires numba for performance. If numba is not available,
import will fail and pure Python fallbacks will be used.
"""
import sys
import numpy as np

try:
    import numba
except ImportError:
    raise ImportError("numba is required for ncomplexity. Install with: pip install numba")


@numba.jit(nopython=True)
def _higher_order_writhe_inner(points, contributions, order):
    """Inner loop for higher_order_writhe (JIT compiled)."""
    indices = np.zeros(4, dtype=np.int64)
    writhe = 0.0
    n = len(points)

    for i1 in range(n - 3):
        indices[0] = i1
        for i2 in range(i1 + 1, n - 1):
            indices[1] = i2
            for i3 in range(i2 + 1, n - 1):
                indices[2] = i3
                for i4 in range(i3 + 1, n - 1):
                    indices[3] = i4
                    writhe += (contributions[indices[order[0]], indices[order[1]]] *
                              contributions[indices[order[2]], indices[order[3]]])
    return writhe

@numba.jit(nopython=True)
def _second_order_writhes_inner(points, contributions):
    """Inner loop for second_order_writhes (JIT compiled)."""
    writhe_1 = 0.0
    writhe_2 = 0.0
    writhe_3 = 0.0
    n = len(points)

    for i1 in range(n - 3):
        for i2 in range(i1 + 1, n - 1):
            for i3 in range(i2 + 1, n - 1):
                for i4 in range(i3 + 1, n - 1):
                    writhe_1 += contributions[i1, i2] * contributions[i3, i4]
                    writhe_2 += contributions[i1, i3] * contributions[i2, i4]
                    writhe_3 += contributions[i1, i4] * contributions[i2, i3]

    pi2_squared = (2 * np.pi) ** 2
    return (writhe_1 / pi2_squared,
            writhe_2 / pi2_squared,
            writhe_3 / pi2_squared)

@numba.jit(nopython=True)
def _second_order_writhes_no_basepoint_inner(points, contributions):
    """Inner loop for second_order_writhes_no_basepoint (JIT compiled)."""
    writhe_1 = 0.0
    writhe_2 = 0.0
    writhe_3 = 0.0
    n = len(points)

    for i1 in range(n - 1):
        # Build possible_i2s: list(range(i1 + 1, n - 1)) + list(range(i1))
        for i2_pass in range(2):
            if i2_pass == 0:
                i2_start, i2_end = i1 + 1, n - 1
            else:
                i2_start, i2_end = 0, i1

            for i2 in range(i2_start, i2_end):
                # Build possible_i3s based on i2
                if i2 > i1:
                    # list(range(i2 + 1, n - 1)) + list(range(i1))
                    for i3_pass in range(2):
                        if i3_pass == 0:
                            i3_start, i3_end = i2 + 1, n - 1
                        else:
                            i3_start, i3_end = 0, i1

                        for i3 in range(i3_start, i3_end):
                            # Build possible_i4s based on i3
                            if i3 > i1:
                                # list(range(i3 + 1, n - 1)) + list(range(i1))
                                for i4_pass in range(2):
                                    if i4_pass == 0:
                                        i4_start, i4_end = i3 + 1, n - 1
                                    else:
                                        i4_start, i4_end = 0, i1

                                    for i4 in range(i4_start, i4_end):
                                        writhe_1 += contributions[i1, i2] * contributions[i3, i4]
                                        writhe_2 += contributions[i1, i3] * contributions[i2, i4]
                                        writhe_3 += contributions[i1, i4] * contributions[i2, i3]
                            else:
                                # list(range(i3 + 1, i1))
                                for i4 in range(i3 + 1, i1):
                                    writhe_1 += contributions[i1, i2] * contributions[i3, i4]
                                    writhe_2 += contributions[i1, i3] * contributions[i2, i4]
                                    writhe_3 += contributions[i1, i4] * contributions[i2, i3]
                else:
                    # list(range(i2 + 1, i1))
                    for i3 in range(i2 + 1, i1):
                        # i3 is in range(i2 + 1, i1), so i3 < i1
                        # possible_i4s = list(range(i3 + 1, i1))
                        for i4 in range(i3 + 1, i1):
                            writhe_1 += contributions[i1, i2] * contributions[i3, i4]
                            writhe_2 += contributions[i1, i3] * contributions[i2, i4]
                            writhe_3 += contributions[i1, i4] * contributions[i2, i3]

    pi2_squared = (2 * np.pi) ** 2
    return (writhe_1 / pi2_squared,
            writhe_2 / pi2_squared,
            writhe_3 / pi2_squared)


def higher_order_writhe(points, contributions, order):
    """
    Calculate higher order writhe.

    Uses Numba for performance.
    """
    # Print progress (can't do this inside numba nopython mode)
    for i1 in range(len(points) - 3):
        print('\rcython i1', i1, len(points) - 4, end='')
        sys.stdout.flush()

    result = _higher_order_writhe_inner(points, contributions, order)
    print()
    return result


def second_order_writhes(points, contributions):
    """
    Calculate second order writhes.

    Uses Numba for performance.
    """
    # Print progress
    for i1 in range(len(points) - 3):
        if i1 % 5 == 0:
            print('\rcython i1', i1, len(points) - 4, end='')
        sys.stdout.flush()

    result = _second_order_writhes_inner(points, contributions)
    print()
    return result


def second_order_writhes_no_basepoint(points, contributions):
    """
    Calculate second order writhes without basepoint.

    Uses Numba for performance.
    """
    # Print progress
    for i1 in range(len(points) - 1):
        if i1 % 5 == 0:
            print('\rnbp cython i1', i1, len(points) - 4, end='')
        sys.stdout.flush()

    result = _second_order_writhes_no_basepoint_inner(points, contributions)
    print()
    return result
