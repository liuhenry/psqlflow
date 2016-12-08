import os.path
import subprocess
import sys
from setuptools import setup, Extension
from setuptools.command.build_ext import build_ext


class PSqlParseBuildExt(build_ext):
    """
    Download and build the libpg_query library
    """
    def run(self):
        return_code = subprocess.call(['./build_libpg_query.sh'])
        if return_code:
            sys.stderr.write('''
            An error occurred during extension building.
            Make sure you have bison and flex installed on your system.
            ''')
            sys.exit(return_code)
        build_ext.run(self)


USE_CYTHON = bool(os.environ.get('USE_CYTHON'))

ext = '.pyx' if USE_CYTHON else '.c'

libpg_query = os.path.join('.', 'libpg_query-9.5-latest')

libraries = ['pg_query']

extensions = [
    Extension('psqlflow.parser.parser',
              ['psqlflow/parser/parser' + ext],
              libraries=libraries,
              include_dirs=[libpg_query],
              library_dirs=[libpg_query])
]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(cmdclass={'build_ext': PSqlParseBuildExt},
      ext_modules=extensions)
