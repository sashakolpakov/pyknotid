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
                    ['*.tmpl', '*.pov', '*.py',
                     ])

# All performance-critical code uses Numba
ext_modules = []
include_dirs = []

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
    install_requires=['numpy', 'peewee', 'vispy', 'sympy']
else:
    install_requires=['numpy', 'networkx', 'planarity',
                      'peewee', 'vispy', 'sympy', 'appdirs',
                      'requests', 'tqdm']

# Read the README for long description
readme_path = join(dirname(__file__), 'README.md')
try:
    with open(readme_path, 'r', encoding='utf-8') as f:
        long_description = f.read()
    long_description_content_type = 'text/markdown'
except FileNotFoundError:
    long_description = (
        'Python modules for detecting and measuring knotting and linking. '
        'See https://github.com/SPOCKnots/pyknotid for more information.'
    )
    long_description_content_type = 'text/plain'

setup(
    name='pyknotid',
    version=version,
    description=('Tools for identifying and analysing knots, in space-curves '
                 'or standard topological representations'),
    long_description=long_description,
    long_description_content_type=long_description_content_type,
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
