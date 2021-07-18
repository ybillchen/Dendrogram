# Licensed under MIT License - see LICENSE

import numpy as np
from .percolationND import latticeND

__all__ = ["clusterTree", "makeTree"]

class clusterTree():
    def __init__(self, label, mask, isleaf=True):
        self._label = label
        self._branches = dict()
        self._children = dict()
        self._parent = dict()
        self._mask = mask.copy()
        self._isleaf = isleaf

    @property
    def label(self):
        return self._label

    @property
    def branches(self):
        return self._branches
    
    @property
    def children(self):
        return self._children
    
    @property
    def parent(self):
        return self._parent
    
    @property
    def mask(self):
        return self._mask

    @property
    def isleaf(self):
        return self._isleaf
    
    def create_leaf(self, label, mask):
        self._branches[label] = clusterTree(label, mask)

    def update_mask(self, mask):
        self._mask = mask.copy()

    def merge_branch(self, label, mask, branch):
        self.branches[label] = clusterTree(label, mask, False)
        for i in branch: 
            self._branches[label]._children[i] = self._branches[i]
            self._branches[i]._parent[label] = self._branches[label]

    def merge_final(self, branch):
        self._isleaf = False
        for i in branch: 
            self._children[i] = self._branches[i]
            self._branches[i]._parent[-1] = self
            self._mask = self._mask | self._branches[i]._mask

def makeTree(data, min_value, min_delta=0, min_npix=1, num_level=100):
    max_level = np.nanmax(data)
    level_list = np.linspace(max_level, min_value, num_level)
    tree = clusterTree(-1, np.zeros(data.shape, dtype=bool))
    new_label = 0
    current_label = -1 * np.ones(data.shape, dtype=int)

    for i, level in enumerate(level_list):
        print("Level %d/%d"%(i+1,num_level))

        temp_lattice = latticeND(data, level)
        temp_lattice.identify_cluster()
        labelset = set(temp_lattice.label.flatten())
        labelset.discard(-1)

        # loop over clusters
        for label in labelset:
            mask = temp_lattice.label == label
            smallset = set(current_label[mask])
            smallset.discard(-1)

            # update branch if there is only one overlaping cluster
            if len(smallset) == 1: 

                # update current labels
                current_label[mask] = (min(smallset) * 
                    np.ones(data[mask].shape, dtype=int))
                tree.branches[min(smallset)].update_mask(mask) 

            # create leaf if there is no overlaping clusters
            elif len(smallset) == 0:
                if (np.max(data[mask]>level+min_delta) and 
                    len(data[mask]) >= min_npix):

                    # update current labels
                    current_label[mask] = (new_label * 
                        np.ones(data[mask].shape, dtype=int))
                    tree.create_leaf(new_label, mask) 
                    new_label += 1

            # merge leaves if there are many overlaping clusters
            elif len(smallset) > 1: 
                tree.merge_branch(new_label, mask, smallset) 

                # update current labels
                current_label[mask] = (new_label * 
                    np.ones(data[mask].shape, dtype=int))
                new_label += 1

    currentset = set(current_label.flatten())
    currentset.discard(-1)

    tree.merge_final(currentset)

    return tree
