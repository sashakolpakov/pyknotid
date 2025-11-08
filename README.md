# Pyknotid

[![PyPI version](https://img.shields.io/pypi/v/pyknotid.svg)](https://pypi.org/project/pyknotid/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Python modules for detecting and measuring knotting and linking. pyknotid can analyse space-curves (sets of points in three dimensions) or parse standard topological representations of knot diagrams.

<p align="center">
  <img src="doc/k10_92_ideal_small.png" alt="The knot 10_92, visualised by pyknotid" width="300"/>
</p>

## Features

- **Knot identification** from space curves or topological representations
- **Polynomial invariants** (Alexander, Jones, HOMFLY-PT, Kauffman)
- **Vassiliev invariants** computation
- **Knot simplification** using octree algorithms
- **Visualization** of knots in 3D
- **Database** of known knots for identification
- **High performance** with optional Numba JIT compilation (2-3x faster)

## Installation

pyknotid requires Python 3.8 or later. Install it with:

```bash
pip install pyknotid
```

**For best performance**, install with Numba support:

```bash
pip install pyknotid[performance]
```

This enables JIT-compiled high-performance numerical computations (2-3x faster). Without Numba, pyknotid will work but use slower pure Python fallbacks.

### Development Installation

To try the latest development version, clone this repository and run:

```bash
git clone https://github.com/SPOCKnots/pyknotid.git
cd pyknotid
pip install -e .
```

For development with all optional dependencies:

```bash
pip install -e ".[dev]"
```

## Quick Start

```python
import pyknotid.spacecurves as sp
import pyknotid.make as mk

# Create a figure-eight knot
k = sp.Knot(mk.figure_eight(num_points=100))

# Visualize it
k.plot()

# Calculate the Alexander polynomial at t=-1
k.alexander_polynomial(-1)
# Output: 6.9999999999999991

# Calculate the symbolic Alexander polynomial
import sympy as sym
t = sym.var('t')
k.alexander_polynomial(t)
# Output: 2/t - 3/t**2 + 2/t**3

# Simplify the knot representation
k.octree_simplify(5)
# Run 0 of 5, 100 points remain
# Run 1 of 5, 98 points remain
# ...
# Reduced to 77 points

k.plot()
```

## Documentation

Full documentation is available at [pyknotid.readthedocs.io](http://pyknotid.readthedocs.io).

## Requirements

The following dependencies are automatically installed:

- numpy >= 1.19
- networkx >= 2.5
- planarity >= 0.4
- peewee >= 3.14
- vispy >= 0.6
- sympy >= 1.8
- appdirs >= 1.4
- requests >= 2.25
- tqdm >= 4.60

### Optional Dependencies

- **numba >= 0.55** (recommended for performance): Install with `pip install pyknotid[performance]`
- **pytest, pytest-cov, black, flake8, mypy** (for development): Install with `pip install pyknotid[dev]`
- **sphinx, sphinx-rtd-theme** (for documentation): Install with `pip install pyknotid[docs]`

## About

pyknotid was originally developed as part of the Leverhulme Trust Research Programme Grant RP2013-K-009: Scientific Properties of Complex Knots (SPOCK), a collaboration between the University of Bristol and Durham University in the UK.

For more information, see the [SPOCK homepage](http://www.maths.dur.ac.uk/spock/index.html/).

### Related Tools

A graphical interface to some of these tools is available online at [Knot ID](http://inclem.net/knotidentifier).

## Citation

If you use pyknotid in your research, please cite it. See [CITATION.cff](CITATION.cff) for citation information, or use:

```bibtex
@Misc{pyknotid,
  author = {Alexander J Taylor and other SPOCK contributors},
  title = {pyknotid knot identification toolkit},
  howpublished = {\url{https://github.com/SPOCKnots/pyknotid}},
  year = 2017,
}
```

For more details, see our [citation guidelines](http://pyknotid.readthedocs.io/en/latest/sources/about.html#cite-us).

## License

pyknotid is released under the [MIT License](LICENSE.txt).

## Contributing

Contributions are welcome! Please feel free to:

- Report bugs or request features via [GitHub Issues](https://github.com/SPOCKnots/pyknotid/issues)
- Submit pull requests
- Improve documentation

## Contact

Questions or comments are welcome. Please email alexander.taylor@bristol.ac.uk or open an issue on GitHub.

## Links

- **Homepage**: https://github.com/SPOCKnots/pyknotid
- **Documentation**: http://pyknotid.readthedocs.io
- **PyPI**: https://pypi.org/project/pyknotid/
- **Bug Tracker**: https://github.com/SPOCKnots/pyknotid/issues
