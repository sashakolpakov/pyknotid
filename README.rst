Pyknotid
========

.. image:: https://github.com/sashakolpakov/pyknotid/workflows/Tests/badge.svg
    :target: https://github.com/sashakolpakov/pyknotid/actions?query=workflow%3ATests
    :alt: Test Status

.. image:: https://github.com/sashakolpakov/pyknotid/workflows/Documentation/badge.svg
    :target: https://github.com/sashakolpakov/pyknotid/actions?query=workflow%3ADocumentation
    :alt: Documentation Status

.. image:: https://img.shields.io/pypi/v/pyknotid.svg
    :target: https://pypi.org/project/pyknotid/
    :alt: PyPI version

Python modules for detecting and measuring knotting and linking.
pyknotid can analyse space-curves, i.e. sets of points in
three-dimensions, or can parse standard topological
representations of knot diagrams.

pyknotid was originally developed as part of the Leverhulme Trust
Research Programme Grant RP2013-K-009: Scientific Properties of
Complex Knots (SPOCK), a collaboration between the University of
Bristol and Durham University in the UK. For more information, see the
`SPOCK homepage <http://www.maths.dur.ac.uk/spock/index.html/>`__.

.. image:: doc/k10_92_ideal_small.png
   :align: center
   :scale: 25%
   :alt: The knot 10_92, visualised by pyknotid.

Documentation
-------------

pyknotid is documented online at `readthedocs
<http://pyknotid.readthedocs.io/en/latest/sources/overview.html>`__.

Installation
------------

pyknotid requires Python 3.8 or later. Install it with::

  $ pip install pyknotid

**For best performance**, install with Numba support::

  $ pip install pyknotid[performance]

This enables JIT-compiled high-performance numerical computations
(2-3x faster). Without Numba, pyknotid will work but use slower
pure Python fallbacks.

To try the latest development version, clone this repository and run::

  $ pip install -e .

Requirements
~~~~~~~~~~~~

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

Optional dependencies:

- cython (for improved performance, automatically built if available)

For development, install additional dependencies with::

  $ pip install -e ".[dev]"


Example usage
-------------

.. code:: python

    In [1]: import pyknotid.spacecurves as sp

    In [2]: import pyknotid.make as mk

    In [3]: k = sp.Knot(mk.three_twist(num_points=100))

    In [4]: k.plot()

    In [5]: k.alexander_polynomial(-1)
    Finding crossings
    i = 0 / 97
    7 crossings found

    Simplifying: initially 14 crossings
    -> 10 crossings after 2 runs
    Out[5]: 6.9999999999999991

    In [6]: import sympy as sym

    In [7]: t = sym.var('t')

    In [8]: k.alexander_polynomial(t)
    Simplifying: initially 10 crossings
    -> 10 crossings after 1 runs
    Out[8]: 2/t - 3/t**2 + 2/t**3

    In [9]: k.octree_simplify(5)
    Run 0 of 5, 100 points remain
    Run 1 of 5, 98 points remain
    Run 2 of 5, 104 points remain
    Run 3 of 5, 92 points remain
    Run 4 of 5, 77 points remain

    Reduced to 77 points

    In [10]: k.plot()
