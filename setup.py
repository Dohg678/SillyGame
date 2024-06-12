from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("./scripts/scriptscython/buttons.pyx")
)