"""
Numba implementation of invariants (replacing cinvariants.pyx).
"""
import numpy as np

try:
    import numba
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False


if NUMBA_AVAILABLE:
    @numba.jit(nopython=True)
    def _crude_modulus(val, modulo):
        """Helper function for modulus operation."""
        if val < 0:
            return val + modulo
        return val

    @numba.jit(nopython=True)
    def _vassiliev_degree_3_inner(arrows):
        """
        Inner computation for vassiliev_degree_3 (JIT compiled).

        Note: Uses a simple array-based approach instead of Python sets
        to track used index combinations in nopython mode.
        """
        num_arrows = len(arrows)
        num_crossings = len(arrows) * 2

        representations_sum_1 = 0
        representations_sum_2 = 0

        # Track used combinations with a fixed-size array
        # We use a simple approach: mark combinations by a unique index
        # Max possible combinations is num_arrows^3, but we only track what we've seen
        max_combinations = num_arrows * num_arrows * num_arrows
        used_combinations = np.zeros(max_combinations, dtype=np.int8)

        for i1 in range(num_arrows):
            arrow1 = arrows[i1]
            a1s = arrow1[0]
            a1e = arrow1[1]
            sign1 = arrow1[2]

            a1e = _crude_modulus(a1e - a1s, num_crossings)

            for i2 in range(num_arrows):
                arrow2 = arrows[i2]
                a2s = arrow2[0]
                a2e = arrow2[1]
                sign2 = arrow2[2]

                a2s = _crude_modulus(a2s - a1s, num_crossings)
                a2e = _crude_modulus(a2e - a1s, num_crossings)

                for i3 in range(num_arrows):
                    arrow3 = arrows[i3]
                    a3s = arrow3[0]
                    a3e = arrow3[1]
                    sign3 = arrow3[2]

                    a3s = _crude_modulus(a3s - a1s, num_crossings)
                    a3e = _crude_modulus(a3e - a1s, num_crossings)

                    # Create ordered indices (sorted tuple equivalent)
                    indices = np.array([i1, i2, i3], dtype=np.int64)
                    indices.sort()

                    # Map to unique index for tracking
                    combo_index = indices[0] * num_arrows * num_arrows + indices[1] * num_arrows + indices[2]

                    if used_combinations[combo_index]:
                        continue

                    if (a2s < a1e and a3e < a1e and a3e > a2s and
                        a3s > a1e and a2e > a3s):
                        representations_sum_1 += sign1 * sign2 * sign3
                        used_combinations[combo_index] = 1
                    if (a2e < a1e and a3s < a1e and a3s > a2e and
                        a2s > a1e and a3e > a2s):
                        representations_sum_2 += sign1 * sign2 * sign3
                        used_combinations[combo_index] = 1

        return representations_sum_1 / 2. + representations_sum_2


def vassiliev_degree_3(arrows):
    """
    Calculate the Vassiliev invariant of degree 3.

    Now uses Numba for performance instead of Cython.

    Parameters
    ----------
    arrows : ndarray
        Array of arrow data with shape (n, 3) where each row is [start, end, sign]

    Returns
    -------
    float
        The Vassiliev degree 3 invariant value
    """
    if not NUMBA_AVAILABLE:
        raise ImportError("numba is required for this function. Install with: pip install numba")

    return _vassiliev_degree_3_inner(arrows)
