# Licensed under MIT License - see LICENSE
"""
A tree class and a makeTree function.
"""

import numpy as np
from .latticeND import latticeND

__all__ = ["clusterTree", "makeTree"]

class clusterTree():
    """
    A tree class. 
    
    Note:
        `clusterTree` can be either the tree itself or the branch of a tree.
    """

    def __init__(self, label, mask, isleaf=True):
        """
        Args:
            label (int): Label of this tree/branch. 
            mask (`numpy.ndarray` of bool): The area ocupied by this 
                tree/branch.
            isleaf (bool, default to True): Whether this is a leaf branch 
                (or "leaf" for short) or not.
        """

        self._label = label
        self._mask = mask.copy()
        self._isleaf = isleaf

        self._branches = dict()
        self._children = dict()
        self._parent = dict()

    @property
    def label(self):
        """int: Label of this tree/branch."""
        return self._label

    @property
    def mask(self):
        """`numpy.ndarray` of bool: Area ocupied by
            this tree/branch."""
        return self._mask

    @mask.setter
    def mask(self, mask):
        self._mask = mask.copy()

    @property
    def isleaf(self):
        """bool: Whether this is a leaf or not."""
        return self._isleaf

    @property
    def branches(self):
        """dict of int: All branches of the tree. 
            Empty if this is a branch."""
        return self._branches
    
    @property
    def children(self):
        """dict of int: Children of this branch/tree. 
            Empty if this is a leaf."""
        return self._children
    
    @property
    def parent(self):
        """dict of int: Parent of this branch. 
            Empty if this is a tree."""
        return self._parent
    
    def create_leaf(self, label, mask):
        """
        Create a new leaf to the tree.

        Note:
            This method does *not* connect the new leaf to any of the 
            presenting branch!

        Args:
            label (int): Label of the new leaf. 
            mask (`numpy.ndarray` of bool): The area ocupied by the new 
                leaf.
        """

        self._branches[label] = clusterTree(label, mask)

    def merge_branch(self, label, mask, branch):
        """
        Merge many old branches to a new branch. 

        Note:
            Here, "merge" means setting the new branch to be the parent of
            old branches, *not* removing them!

        Args:
            label (int): Label of the new branch. 
            mask (`numpy.ndarray` of bool): The area ocupied by the new 
                branch.
            branch (set or list of int): Labels of branches to be merged.
        """

        self.branches[label] = clusterTree(label, mask, False)
        for i in branch: 
            self._branches[label]._children[i] = self._branches[i]
            self._branches[i]._parent[label] = self._branches[label]

    def merge_final(self, branch):        
        """
        Merge final branches to the tree. 

        Note:
            Even if there is only one final branch, we still need to merge
            (or, more properly, "link") it to the tree. Mind the difference 
            between "tree" and "branch".

        Args:
            branch (set or list of int): Labels of branches to be merged.
        """

        self._isleaf = False
        for i in branch: 
            self._children[i] = self._branches[i]
            self._branches[i]._parent[-1] = self
            self._mask = self._mask | self._branches[i]._mask

    def topology(self, print_text=True):        
        """
        Print topology of the tree in pure text. 

        Note:
            Applying this method to large (with more than 100 branches)
            or deep (with more than 100 levels) trees is not recommend.

        Args:
            print_text (bool): Whether to print to screen or not.

        Returns:
            str: Visualized topology of this tree.
        """

        stack = [self]
        stage = [0]
        string = ""

        while len(stack) > 0:
            b = stack.pop() # pop a branch
            s = stage.pop() # pop a stage

            string += " "*s*4 + "|__(%d)\n"%(b._label)
            for i in list(b._children)[::-1]:
                stack.append(b._children[i])
                stage.append(s+1)

        if print_text:
            print(string)

        return string


def makeTree(data, min_value, min_delta=0, min_npix=1, num_level=100,
    print_progress=True):
    """
    Make dendrogram tree from N-dimensional data.

    Note:
        Applying this method to large (with more than 100 branches)
        or deep (with more than 100 levels) trees is not recommend.

    Args:
        data (`numpy.ndarray` of scalar): Data to make dendrogram tree.
        min_value (scalar): Minimum value to consider.
        min_delta (scalar, default to 0): Lag to be ignored. 
        min_npix (int, default to 1): Minimum number of pixels to form a 
            cluster.
        num_level (int, default to 100): Number of levels.
        print_progress (bool, default to True): Whether to print progress 
            or not.

    Returns:
        `clusterTree`: Tree for the dendrogram.

    Examples:
        Consider a simple two-dimensional bimodal data, let's generate the 
        tree with `min_value=0`:

        >>> data = np.array([[2,1], [1,2]])
        >>> tree = makeTree(data, min_value=0)
        Level 1/100
        ...
        Level 100/100

        To check the result, we can print the topology of tree:

        >>> tp = tree.topology()
        |__(-1)
            |__(2)
                |__(0)
                |__(1)

        As expected, two branches 0 and 1 illustrates the bimodality.
        Similarly, the script below generates dendrogram for a three-peak
        distribution:

        >>> data = np.array([[3,1,1],[1,1,1],[2,1,3]])
        >>> tree = makeTree(data, min_value=0, print_progress=False)
        >>> tp = tree.topology()
        |__(-1)
            |__(3)
                |__(0)
                |__(1)
                |__(2)
    """

    max_value = np.nanmax(data)
    level_list = np.linspace(max_value, min_value, num_level)
    tree = clusterTree(-1, np.zeros(data.shape, dtype=bool))
    new_label = 0
    current_label = -1 * np.ones(data.shape, dtype=int)

    for i, level in enumerate(level_list):
        if print_progress:
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
                tree.branches[min(smallset)].mask = mask 

            # create leaf if there is no overlaping clusters
            elif len(smallset) == 0:
                if (np.max(data[mask]) > level+min_delta and 
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
