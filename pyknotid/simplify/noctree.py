"""
Numba implementation of octree functions (replacing coctree.pyx).
"""
import numpy as np

try:
    import numba
    NUMBA_AVAILABLE = True
except ImportError:
    NUMBA_AVAILABLE = False


if NUMBA_AVAILABLE:
    @numba.jit(nopython=True)
    def _diff(dv2, nex, nex2):
        """Calculate difference vector."""
        dv2[0] = nex2[0] - nex[0]
        dv2[1] = nex2[1] - nex[1]
        dv2[2] = nex2[2] - nex[2]

    @numba.jit(nopython=True)
    def _divide(arr, val):
        """Divide array elements by scalar."""
        arr[0] = arr[0] / val
        arr[1] = arr[1] / val
        arr[2] = arr[2] / val

    @numba.jit(nopython=True)
    def _mag(v):
        """Magnitude squared of vector."""
        return v[0]**2 + v[1]**2 + v[2]**2

    @numba.jit(nopython=True)
    def _angle_between(v1, v2):
        """
        Returns angle between v1 and v2, assuming they are normalised to 1.
        Clips value to handle floating point errors.
        """
        value = v1[0] * v2[0] + v1[1] * v2[1] + v1[2] * v2[2]
        if value > 1.:
            value = 1.
        elif value < 0.:
            value = 0.
        return value

    @numba.jit(nopython=True)
    def _angle_exceeds_inner(ps, val, include_closure):
        """
        Inner function for angle_exceeds (JIT compiled).

        Returns True if the sum of angles along ps exceeds val, else False.
        """
        angle = 0.
        nex = ps[0].copy()
        nex2 = ps[1].copy()
        dv2 = np.zeros(3, dtype=np.float64)
        _diff(dv2, nex, nex2)
        mag_val = np.sqrt(_mag(dv2))
        _divide(dv2, mag_val)

        lenps = len(ps)

        if include_closure:
            num_checks = lenps
        else:
            num_checks = lenps - 2

        for i in range(num_checks):
            cur = nex.copy()
            nex = nex2.copy()
            nex2 = ps[(i + 2) % lenps].copy()
            dv = dv2.copy()
            _diff(dv2, nex, nex2)
            mag_val = np.sqrt(_mag(dv2))
            _divide(dv2, mag_val)
            increment = _angle_between(dv, dv2)
            if np.isnan(increment):
                return True
            angle += increment
            if angle > val:
                return True

        if np.isnan(angle):
            # Should match the assert behavior
            return True
        return False

    @numba.jit(nopython=True)
    def _sign(v):
        """Return sign of value."""
        if v > 0:
            return 1.0
        elif v < 0:
            return -1.0
        return 0.0

    @numba.jit(nopython=True)
    def _line_to_segments_inner(line, cut_x, cut_y, cut_z):
        """
        Inner function for line cutting (JIT compiled).

        Returns indices where cuts occur and cut positions.
        We'll do the actual array building in Python.
        """
        n = len(line)
        # Store cut information: (index, cut_type, positions...)
        # cut_type: 0=none, 1=x, 2=y, 3=z, 4=xy, 5=xz, 6=yz, 7=xyz
        max_cuts = n * 3  # Maximum possible cuts
        cut_indices = np.zeros(max_cuts, dtype=np.int64)
        cut_types = np.zeros(max_cuts, dtype=np.int64)
        cut_positions = np.zeros((max_cuts, 3), dtype=np.float64)
        num_cuts = 0

        for i in range(n - 1):
            cur = line[i]
            nex = line[i + 1]

            dx = nex[0] - cur[0]
            dy = nex[1] - cur[1]
            dz = nex[2] - cur[2]

            cross_cut_x = _sign(cur[0] - cut_x) != _sign(nex[0] - cut_x)
            cross_cut_y = _sign(cur[1] - cut_y) != _sign(nex[1] - cut_y)
            cross_cut_z = _sign(cur[2] - cut_z) != _sign(nex[2] - cut_z)

            if not cross_cut_x and not cross_cut_y and not cross_cut_z:
                continue

            cut_indices[num_cuts] = i

            # Determine cut type and calculate positions
            if cross_cut_x and cross_cut_y and cross_cut_z:
                cut_types[num_cuts] = 7
                x_cut_pos = -1 * (cur[0] - cut_x) / dx
                y_cut_pos = -1 * (cur[1] - cut_y) / dy
                z_cut_pos = -1 * (cur[2] - cut_z) / dz
                cut_positions[num_cuts, 0] = x_cut_pos
                cut_positions[num_cuts, 1] = y_cut_pos
                cut_positions[num_cuts, 2] = z_cut_pos
            elif cross_cut_x and cross_cut_y:
                cut_types[num_cuts] = 4
                x_cut_pos = -1 * (cur[0] - cut_x) / dx
                y_cut_pos = -1 * (cur[1] - cut_y) / dy
                cut_positions[num_cuts, 0] = x_cut_pos
                cut_positions[num_cuts, 1] = y_cut_pos
            elif cross_cut_x and cross_cut_z:
                cut_types[num_cuts] = 5
                x_cut_pos = -1 * (cur[0] - cut_x) / dx
                z_cut_pos = -1 * (cur[2] - cut_z) / dz
                cut_positions[num_cuts, 0] = x_cut_pos
                cut_positions[num_cuts, 1] = z_cut_pos
            elif cross_cut_y and cross_cut_z:
                cut_types[num_cuts] = 6
                y_cut_pos = -1 * (cur[1] - cut_y) / dy
                z_cut_pos = -1 * (cur[2] - cut_z) / dz
                cut_positions[num_cuts, 0] = y_cut_pos
                cut_positions[num_cuts, 1] = z_cut_pos
            elif cross_cut_x:
                cut_types[num_cuts] = 1
                cut_positions[num_cuts, 0] = -1 * (cur[0] - cut_x) / dx
            elif cross_cut_y:
                cut_types[num_cuts] = 2
                cut_positions[num_cuts, 0] = -1 * (cur[1] - cut_y) / dy
            elif cross_cut_z:
                cut_types[num_cuts] = 3
                cut_positions[num_cuts, 0] = -1 * (cur[2] - cut_z) / dz

            num_cuts += 1

        return cut_indices[:num_cuts], cut_types[:num_cuts], cut_positions[:num_cuts]


def angle_exceeds(ps, val=2*np.pi, include_closure=1):
    """
    Returns True if the sum of angles along ps exceeds val, else False.

    If include_closure, includes the angles with the line closing
    the end and start points.

    Uses Numba for performance.
    """
    if not NUMBA_AVAILABLE:
        raise ImportError("numba is required for this function. Install with: pip install numba")

    ps = np.asarray(ps, dtype=np.float64)
    return _angle_exceeds_inner(ps, val, include_closure)


def line_to_segments(line, cuts=None, join_ends=True):
    """
    Takes a line (set of points), a list of cut planes in
    x, y, z, and a parameter to decide whether the line
    joining the first and last point should also be cut.

    Returns a list of shorter lines resulting from cutting at
    all these cut planes.

    Uses Numba for performance-critical parts.
    """
    if not NUMBA_AVAILABLE:
        raise ImportError("numba is required for this function. Install with: pip install numba")

    line = np.asarray(line, dtype=np.float64)

    if cuts is None:
        xmin, ymin, zmin = np.min(line, axis=0) - 1
        xmax, ymax, zmax = np.max(line, axis=0) + 1
        cut_x = (xmax + xmin) / 2.
        cut_y = (ymax + ymin) / 2.
        cut_z = (zmin + zmax) / 2.
    else:
        cut_x, cut_y, cut_z = cuts

    # Get cut information from numba
    cut_indices, cut_types, cut_positions = _line_to_segments_inner(
        line, cut_x, cut_y, cut_z
    )

    if len(cut_indices) == 0:
        return [line]

    # Build segments from cut information
    segments = []
    cut_i = 0
    line_copy = line.copy()

    for idx, (i, cut_type, positions) in enumerate(zip(cut_indices, cut_types, cut_positions)):
        cur = line_copy[i]
        nex = line_copy[i + 1]
        dv = cur - nex

        if cut_type == 7:  # xyz
            order = np.sort(positions)
            join_point_1 = cur + order[0] * dv
            join_point_2 = cur + order[1] * dv
            join_point_3 = cur + order[2] * dv
            first_seg = np.vstack((line_copy[cut_i:(i+1)], join_point_1))
            second_seg = np.vstack((join_point_1, join_point_2))
            third_seg = np.vstack((join_point_2, join_point_3))
            line_copy[i] = join_point_3
            cut_i = i
            segments.extend([first_seg, second_seg, third_seg])
        elif cut_type == 4:  # xy
            order = np.sort(positions[:2])
            join_point_1 = cur + order[0] * dv
            join_point_2 = cur + order[1] * dv
            first_seg = np.vstack((line_copy[cut_i:(i+1)], join_point_1))
            second_seg = np.vstack((join_point_1, join_point_2))
            line_copy[i] = join_point_2
            cut_i = i
            segments.extend([first_seg, second_seg])
        elif cut_type == 5:  # xz
            order = np.sort(positions[:2])
            join_point_1 = cur + order[0] * dv
            join_point_2 = cur + order[1] * dv
            first_seg = np.vstack((line_copy[cut_i:(i+1)], join_point_1))
            second_seg = np.vstack((join_point_1, join_point_2))
            line_copy[i] = join_point_2
            cut_i = i
            segments.extend([first_seg, second_seg])
        elif cut_type == 6:  # yz
            order = np.sort(positions[:2])
            join_point_1 = cur + order[0] * dv
            join_point_2 = cur + order[1] * dv
            first_seg = np.vstack((line_copy[cut_i:(i+1)], join_point_1))
            second_seg = np.vstack((join_point_1, join_point_2))
            line_copy[i] = join_point_2
            cut_i = i
            segments.extend([first_seg, second_seg])
        elif cut_type in [1, 2, 3]:  # x, y, or z only
            cut_pos = positions[0]
            join_point = cur + cut_pos * dv
            first_seg = np.vstack((line_copy[cut_i:(i+1)], join_point))
            line_copy[i] = join_point
            cut_i = i
            segments.append(first_seg)

    # Handle final segment
    final_seg = line_copy[cut_i:]
    if cut_i > 0:
        if join_ends:
            first_seg = segments.pop(0)
            segments.append(np.vstack((final_seg, first_seg)))
        else:
            segments.append(final_seg)
    else:
        segments.append(final_seg)

    return segments
