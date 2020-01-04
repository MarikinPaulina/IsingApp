import numpy as np


class Ising:

    def __init__(self, N, T):
        self.N = N
        self.board = np.ones((N, N), int)
        self.T = T

    @property
    def energy(self):
        return self.H_board.sum() / (2*self.N)

    @property
    def magnetism(self):
        return self.board.sum() / self.N

    def H(self):
        h = np.roll(self.board, 1, 0) + np.roll(self.board, -1, 0) + \
            np.roll(self.board, 1, 1) + np.roll(self.board, -1, 1)
        h *= -self.board
        return h

    def reset(self):
        self.board = np.ones((self.N, self.N))
