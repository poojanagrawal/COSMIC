#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (C) Katie Breivik (2017-2020)
#
# This file is part of the cosmic python package.
#
# cosmic is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# cosmic is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with cosmic.  If not, see <http://www.gnu.org/licenses/>.

"""Setup the cosmic package
"""

from __future__ import print_function

import glob
import os.path
import versioneer
import sys

from setuptools import find_packages
from distutils.command.sdist import sdist

try:
    from numpy.distutils.core import setup, Extension
    from numpy.distutils.ccompiler import CCompiler_object_filenames
except ImportError:
    raise ImportError("Building fortran extensions requires numpy.")

# set basic metadata
PACKAGENAME = "cosmic"
DISTNAME = "cosmic-popsynth"
AUTHOR = "Katie Breivik"
AUTHOR_EMAIL = "katie.breivik@gmail.com"
LICENSE = "GPLv3"

cmdclass = {}

# -- versioning ---------------------------------------------------------------

__version__ = versioneer.get_version()
cmdclass.update(versioneer.get_cmdclass())

# -- documentation ------------------------------------------------------------

# import sphinx commands
try:
    from sphinx.setup_command import BuildDoc
except ImportError:
    pass
else:
    cmdclass["build_sphinx"] = BuildDoc

cmdclass["sdist"] = sdist

# read description
with open("README.md", "rb") as f:
    long_description = f.read().decode().strip()

# -- dependencies -------------------------------------------------------------

setup_requires = [
    "numpy",
]

if 'test' in sys.argv:
    setup_requires.extend([
        'setuptools',
        'pytest-runner',
    ])

install_requires = [
    'numpy >= 1.16, <=1.18.4 ; python_version == \'3.6\'',
    'numpy >= 1.16 ; python_version > \'3.6\'',
    'scipy >= 0.12.1',
    'astropy >= 1.1.1',
    'configparser',
    'tqdm >= 4.0',
    'pandas >= 0.24',
    'tables > 3.5.0',
    'h5py >= 1.3',
    'schwimmbad >= 0.3.1',
    'matplotlib >= 2.0.0'
]
tests_require = [
    'pytest'
]
extras_require = {
    "doc": [
        "sphinx >= 1.6.1",
        "numpydoc >= 0.8.0",
        "sphinx-bootstrap-theme >= 0.6",
        "sphinxcontrib-programoutput",
        "sphinx-automodapi",
        "ipython",
        "sphinx_rtd_theme",
    ],
}

# fortran compile
wrapper = Extension(
    "cosmic._evolvebin",
    sources=[
        "cosmic/src/METISSE/src/track_support.f90",
        "cosmic/src/METISSE/src/z_support.f90",
        "cosmic/src/METISSE/src/zcnsts_METISSE.f90",
        "cosmic/src/comenv.f",
        "cosmic/src/corerd.f",
        "cosmic/src/deltat.f",
        "cosmic/src/dgcore.f",
        "cosmic/src/evolv2.f",
        "cosmic/src/gntage.f",
        "cosmic/src/hrdiag.f",
        "cosmic/src/instar.f",
        "cosmic/src/kick.f",
        "cosmic/src/mix.f",
        "cosmic/src/mlwind.f",
        "cosmic/src/mrenv.f",
        "cosmic/src/ran3.f",
        "cosmic/src/rl.f",
        "cosmic/src/star.f",
        "cosmic/src/zcnsts.f",
        "cosmic/src/zfuncs.f",
        "cosmic/src/concatkstars.f",
        "cosmic/src/comprad.f",
        "cosmic/src/bpp_array.f",
        "cosmic/src/checkstate.f",
    ],
# ,module_dirs=["cosmic/src/mod/"]
# ,extra_compile_args = ["-g","-O0"],
    extra_f77_compile_args=["-O0","-fimplicit-none", "-g", "-fbacktrace",  "-fcheck=all", "-Wall"],
    extra_f90_compile_args=["-O0", "-fimplicit-none", "-g", "-fbacktrace",  "-fcheck=all", "-Wall"]
)

# -- run setup ----------------------------------------------------------------

packagenames = find_packages()
scripts = glob.glob(os.path.join("bin", "*"))

setup(name=DISTNAME,
      provides=[PACKAGENAME],
      version=__version__,
      description="Compact Object Synthesis and Monte Carlo Investigation Code",
      long_description=long_description,
      long_description_content_type='text/markdown',
      ext_modules=[wrapper],
      author=AUTHOR,
      author_email=AUTHOR_EMAIL,
      license=LICENSE,
      packages=packagenames,
      include_package_data=True,
      cmdclass=cmdclass,
      url='https://github.com/COSMIC-PopSynth/COSMIC',
      scripts=scripts,
      setup_requires=setup_requires,
      install_requires=install_requires,
      tests_require=tests_require,
      extras_require=extras_require,
      python_requires='>3.5, <4',
      use_2to3=False,
      classifiers=[
          'Development Status :: 4 - Beta',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Intended Audience :: Science/Research',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Science/Research',
          'Natural Language :: English',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: Astronomy',
          'Topic :: Scientific/Engineering :: Physics',
          'Operating System :: POSIX',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                  ],
      )
