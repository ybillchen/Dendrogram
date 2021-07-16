import numpy as np

class lattice3D():
    def __init__(self, data, p):
        rand = data.copy()
        self.shape = data.shape
        self.level = p
        self.mask = (rand>p)
        self.lattice = self.mask * 1
    
    def identify_cluster(self):
        self.label = np.ones(self.shape, dtype=int)*-1
        self.max_labels = self.shape[0] * self.shape[1] * self.shape[2] / 2 + 1
        self.proper_label = np.arange(self.max_labels)
        self.new_label = 0
        for i in range(self.lattice.shape[0]):
            for j in range(self.lattice.shape[1]):
                for k in range(self.lattice.shape[2]):
                    if self.lattice[i][j][k]:
                        left = -1
                        right = -1
                        up = -1
                        down = -1
                        front = -1
                        back = -1
                        if j != 0: 
                            left = self.label[i][j-1][k]
                        if j != self.lattice.shape[1]-1:
                            right = self.label[i][j+1][k]
                        if i != 0:
                            up = self.label[i-1][j][k]
                        if i != self.lattice.shape[0]-1:
                            down = self.label[i+1][j][k]
                        if k != 0:
                            front = self.label[i][j][k-1]
                        if k != self.lattice.shape[2]-1:
                            back = self.label[i][j][k+1]
                        if left==-1 and right==-1 and up==-1 and down==-1 and front==-1 and back==-1: 
                            self.label[i][j][k] = self.new_label
                            self.new_label = self.new_label + 1
                        else: 
                            nonzero = np.array([left, right, up, down, front, back], dtype=int)
                            nonzero = self.proper_label[nonzero[nonzero!=-1]]
                            self.label[i][j][k] = np.min(nonzero)
                            if len(set(nonzero)) > 1:
                                for non in nonzero:
                                    self.proper_label[self.proper_label==non] = \
                                    np.array([np.min(nonzero)]*len(self.proper_label[self.proper_label==non]))
        for i in range(self.label.shape[0]):
            for j in range(self.label.shape[1]):
                for k in range(self.label.shape[2]):
                    if self.label[i][j][k] > 0:
                        self.label[i][j][k] = self.proper_label[(self.label[i][j][k])]
    
    def percolating(self):
        top = set(self.label[0].reshape(self.shape[1]*self.shape[2]))
        bottom = set(self.label[-1].reshape(self.shape[1]*self.shape[2]))
        top.discard(-1)
        bottom.discard(-1)
        if top & bottom != set():
            self.percolate = 1
            return 1
        else:
            self.percolate = 0
            return 0


