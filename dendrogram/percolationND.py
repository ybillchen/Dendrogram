# Licensed under MIT License - see LICENSE
"""
An N-dimensional lattice class with an identify_cluster method.
"""

import numpy as np

__all__ = ["latticeND"]

class latticeND():
    def __init__(self, data, level):
        self._shape = data.shape
        self._dim = len(self._shape)
        self._len = np.prod(self._shape) # total number of elements
        self._lattice = data > level
        self._label = None
        self._percolate = None

    @property
    def label(self):
        return self._label

    @property
    def percolate(self):
        return self._percolate
    
    def identify_cluster(self):
        # for simplicity, use flattened labels
        label_flat = -1 * np.ones(self._len, dtype=int)
        lattice_flat = self._lattice.flatten()

        # define proper labels, which change over time
        max_label = self._len / 2 + 1
        proper_label = np.arange(max_label)
        new_label = 0

        for i in range(self._len):
            if not lattice_flat[i]:
                continue

            neighbors = -1 * np.ones(2*self._dim, dtype=int)
            # find neighbors in each dimension
            for j in range(self._dim):
                # length of the j-th dimension
                len_j = self._len // self._shape[j]

                idx = i // len_j # index in block
                off = i % len_j # offset in block

                # 2 neighbors
                if idx > 0:
                    neighbors[2*j] = label_flat[i-len_j]
                if idx < self._shape[j]-1:
                    neighbors[2*j+1] = label_flat[i+len_j]

            # set label to the first identified cluster
            if np.max(neighbors) < 0:
                label_flat[i] = new_label
                new_label += 1
            else:
                nonzero = np.unique(proper_label[neighbors[neighbors>-1]])
                label_flat[i] = np.min(nonzero)

                # set connecting clusters to the same lable
                same_label = np.min(nonzero)
                if nonzero.shape[0] > 1:
                    for non in nonzero:
                        replace = np.where(proper_label==non)[0]
                        proper_label[replace] = (same_label * 
                            np.ones(replace.shape[0], dtype=int))

        # update labels (only those with lable > -1)
        label_flat[lattice_flat] = proper_label[label_flat[lattice_flat]]

        self._label = label_flat.reshape(self._shape)
        return self._label

    def percolating(self):
        top = set(self._label[0].reshape(self._len // self._shape[0]))
        bottom = set(self._label[-1].reshape(self._len // self._shape[0]))
        top.discard(-1)
        bottom.discard(-1)

        self._percolate = (top & bottom != set())
        return self._percolate


