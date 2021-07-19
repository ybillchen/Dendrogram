# Licensed under MIT License - see LICENSE
"""
An N-dimensional lattice class with an identify_cluster method.
"""

import numpy as np

__all__ = ["latticeND"]

class latticeND():
    """
    An N-dimensional lattice class.
    """

    def __init__(self, data, level):
        """
        Args:
            data (`numpy.ndarray` of scalar): Data to make dendrogram tree.
            level (scalar): level of this lattice.
        """

        self._shape = data.shape
        self._dim = len(self._shape)
        self._len = np.prod(self._shape)
        self._lattice = data > level

        self._label = None

    @property
    def shape(self):
        """`numpy.ndarray` of int: Shape of the lattice."""
        return self._shape
    
    @property
    def dim(self):
        """int: Dimension of the lattice."""
        return self._dim

    @property
    def len(self):
        """int: Total number of elements in the lattice."""
        return self._len
    
    @property
    def lattice(self):
        """`numpy.ndarray` of int: Area ocupied by the lattice."""
        return self._lattice

    @property
    def label(self):
        """`numpy.ndarray` of int: Label of clusters."""
        return self._label
    
    def identify_cluster(self):
        """
        Identify clusters in the lattice.

        A cluster is a group of connected (neighboring) elements. 

        Returns:
            `numpy.ndarray` of int: Label of clusters.
        """

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
            
            len_j = self._len
            neighbors = -1 * np.ones(2*self._dim, dtype=int)
            # find neighbors in each dimension
            for j in range(self._dim):
                # length of the j-th dimension
                len_j = len_j // self._shape[j]

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


