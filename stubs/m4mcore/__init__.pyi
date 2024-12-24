"""
Python bindings for meshes4mic
"""
from __future__ import annotations
import numpy
from . import distances
from . import flux
from . import surfaces
__all__ = ['MarchingCubes', 'distances', 'flux', 'surfaces']
class MarchingCubes:
    @staticmethod
    def _pybind11_conduit_v1_(*args, **kwargs):
        ...
    def __init__(self, mask: numpy.ndarray[numpy.uint8], shape: tuple, calibration: tuple, stride: tuple) -> None:
        ...
    def run(self) -> None:
        ...
