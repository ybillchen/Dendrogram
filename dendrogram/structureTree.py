import numpy as np
from .percolationND import latticeND

class clusterTree():
    def __init__(self, label, mask):
        self.label = label
        self.branches = dict()
        self.children = dict()
        self.parent = dict()
        self.mask = mask.copy()

    def create_leaf(self, label, mask):
        self.branches[label] = clusterTree(label, mask)
        self.branches[label].isleaf = True

    def update_branch(self, label, mask):
        self.branches[label].mask = mask.copy()

    def merge_branch(self, label, mask, branch):
        self.branches[label] = clusterTree(label, mask)
        self.branches[label].isleaf = False
        for i in list(branch): 
            self.branches[label].children[i] = self.branches[i]
            self.branches[i].parent[label] = self.branches[label]

def makeTree3D(data, min_value, min_delta=0, min_npix=1, num_level=100):
    max_level = np.nanmax(data)
    level_list = np.linspace(max_level, min_value, num_level)
    myTree = clusterTree(-1, np.zeros(data.shape, dtype=int))
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
                myTree.update_branch(min(smallset), mask) 

            # create leaf if there is only no overlaping clusters
            elif len(smallset) == 0:
                if (np.max(data[mask]>level+min_delta) and 
                    len(data[mask]) >= min_npix):

                    # update current labels
                    current_label[mask] = (new_label * 
                        np.ones(data[mask].shape, dtype=int))
                    myTree.create_leaf(new_label, mask) 
                    new_label += 1

            # merge leaves if there are many overlaping clusters
            elif len(smallset) > 1: 
                myTree.merge_branch(new_label, mask, smallset) 

                # update current labels
                current_label[mask] = (new_label * 
                    np.ones(data[mask].shape, dtype=int))
                new_label += 1

    currentset = set(ccurrent_label.flatten())
    currentset.discard(-1)

    for i in list(currentset):
        myTree.children[i] = myTree.branches[i]
        myTree.branches[i].parent[-1] = myTree
        myTree.mask = ((myTree.mask) | (myTree.branches[i].mask))

    return myTree

