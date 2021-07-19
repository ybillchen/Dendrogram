# Licensed under MIT License - see LICENSE

from . import lattice, structureTree
from .lattice import *
from .structureTree import *

__all__ = lattice.__all__ + structureTree.__all__
__version__ = "0.2.dev"
__name__ = "dendrogram"
__author__ = ["Xi Meng", "Bill Chen"]
