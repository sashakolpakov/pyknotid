from setuptools import setup, find_packages, Extension

from os.path import join, sep, dirname
from os import walk, environ
import glob
import re


package_data = {}

def recursively_include(results, directory, patterns):
    for root, subfolders, files in walk(directory):
        for fn in files:
            if not any([glob.fnmatch.fnmatch(fn, pattern) for pattern in patterns]):
                continue
            filename = join(root, fn)
            directory = 'pyknotid'
            if directory not in results:
                results[directory] = []
            results[directory].append(join(*filename.split(sep)[1:]))

recursively_include(package_data, 'pyknotid',
                    ['*.tmpl', '*.pov', '*.pyx', '*.pxd', '*.py',
                     ])

# Switched to Numba for most performance-critical code
# Still keeping chelpers and coctree in Cython (too complex to convert easily)
try:
    from Cython.Build import cythonize
    import numpy
except ImportError:
    print('Cython or numpy could not be imported. Some optional Cython extensions '
          '(chelpers, coctree) will not be built. pyknotid will use Python/Numba '
          'routines instead.')
    ext_modules = []
    include_dirs = []
else:
    ext_modules = [
            Extension("pyknotid.spacecurves.chelpers", ["pyknotid/spacecurves/chelpers.pyx"],
                    libraries=["m"]),
            Extension("pyknotid.simplify.coctree", ["pyknotid/simplify/coctree.pyx"],
                    libraries=["m"]),
            ]
    ext_modules = cythonize(ext_modules)
    include_dirs = [numpy.get_include()]

pyknotid_init_filen = join(dirname(__file__), 'pyknotid', '__init__.py')
version = None
try:
    with open(pyknotid_init_filen) as fileh:
        lines = fileh.readlines()
except IOError:
    pass
else:
    for line in lines:
        line = line.strip()
        if line.startswith('__version__ = '):
            matches = re.findall(r'["\'].+["\']', line)
            if matches:
                version = matches[0].strip("'").strip('"')
                break
if version is None:
    raise RuntimeError(f'Error: version could not be loaded from {pyknotid_init_filen}')

if 'READTHEDOCS' in environ and environ['READTHEDOCS'] == 'True':
    print('Installing for doc only')
    install_requires=['numpy', 'peewee', 'vispy', 'sympy', 'numba']
else:
    install_requires=['numpy', 'networkx', 'planarity',
                      'peewee', 'vispy', 'sympy', 'appdirs',
                      'requests', 'tqdm', 'numba']

long_description = '''
Pyknotid
========

Python modules for detecting and measuring knotting and linking.
pyknotid uses Numba for high-performance numerical computations.
pyknotid can analyse space-curves, i.e. sets of points in
three-dimensions, or can parse standard topological
representations of knot diagrams.

A graphical interface to some of these tools is available online at
`Knot ID <http://inclem.net/knotidentifier>`__.

pyknotid was developed as part of the Leverhulme Trust Research
Programme Grant RP2013-K-009: Scientific Properties of Complex Knots
(SPOCK), a collaboration between the University of Bristol and Durham
University in the UK. For more information, see the `SPOCK homepage
<http://www.maths.dur.ac.uk/spock/index.html/>`__.

If you use pyknotid in your research, please `cite us
<http://pyknotid.readthedocs.io/en/latest/sources/about.html#cite-us>`__.

Questions or comments are welcome, please email alexander.taylor@bristol.ac.uk.

Documentation
-------------

pyknotid is documented online at `readthedocs
<http://pyknotid.readthedocs.io/en/latest/sources/overview.html>`__.
'''

setup(
    name='pyknotid',
    version=version,
    description=('Tools for identifying and analysing knots, in space-curves '
                 'or standard topological representations'),
    long_description=long_description,
    author='Alexander Taylor',
    author_email='alexander.taylor@bristol.ac.uk',
    python_requires='>=3.8',
    install_requires=install_requires,
    ext_modules=ext_modules,
    include_dirs=include_dirs,
    packages=find_packages(),
    package_data=package_data,
    entry_points={
        'console_scripts': [
            'analyse-knot-file = pyknotid.cli.analyse_knot_file:main',
            'plot-knot = pyknotid.cli.plot_knot:main']
        }
)
