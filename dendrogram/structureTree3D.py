import numpy as np
from percolation3D import lattice3D

class clusterTree3D():
    def __init__(self, label, mask):
        self.label = label
        self.branches = dict()
        self.children = dict()
        self.parent = dict()
        self.mask = mask.copy()

    def create_leaf(self, label, mask):
        self.branches[label] = clusterTree3D(label, mask)
        self.branches[label].isleaf = True

    def update_branch(self, label, mask):
        self.branches[label].mask = mask.copy()

    def merge_branch(self, label, mask, branch):
        self.branches[label] = clusterTree3D(label, mask)
        self.branches[label].isleaf = False
        for i in list(branch): 
            self.branches[label].children[i] = self.branches[i]
            self.branches[i].parent[label] = self.branches[label]

def makeTree3D(data, min_value, min_delta=0, min_npix=1, num_level=100):
    max_level = np.nanmax(data)
    level_list = np.linspace(min_value, max_level, num_level)[::-1]
    myTree = clusterTree3D(-1, np.zeros(data.shape, dtype=int))
    newlabel = 0
    currentlattice = lattice3D(data, max_level)
    currentlattice.label = np.ones(data.shape, dtype=int) * (-1)
    for level in level_list:
        print level
        templattice = lattice3D(data, level)
        templattice.identify_cluster()
        labelset = set(templattice.label.reshape(data.shape[0]*data.shape[1]*data.shape[2]))
        labelset.discard(-1)
        for label in labelset:
            mask = (templattice.label == label)
            smallset = set(currentlattice.label[mask])
            smallset.discard(-1)
            if len(smallset) == 1: 
                currentlattice.label[mask] = np.ones(data[mask].shape, dtype=int) * min(smallset)
                myTree.update_branch(min(smallset), mask) 
            elif len(smallset) == 0:
                #if len(data[mask][data[mask]>(level+min_delta)]) >= min_npix: 
                if np.max(data[mask]>level+min_delta) and len(data[mask]) >= min_npix: 
                    #newmask = (mask & (data>(level+min_delta)))
                    newmask = mask.copy()
                    currentlattice.label[newmask] = np.ones(data[newmask].shape, dtype=int) * newlabel
                    myTree.create_leaf(newlabel, newmask) 
                    newlabel = newlabel + 1
            elif len(smallset) > 1: 
                myTree.merge_branch(newlabel, mask, smallset) 
                currentlattice.label[mask] = np.ones(data[mask].shape, dtype=int) * newlabel
                newlabel = newlabel + 1
    currentset = set(currentlattice.label.reshape(data.shape[0]*data.shape[1]*data.shape[2]))
    currentset.discard(-1)
    for i in list(currentset):
        myTree.children[i] = myTree.branches[i]
        myTree.branches[i].parent[-1] = myTree
        myTree.mask = ((myTree.mask) | (myTree.branches[i].mask))
    return myTree

