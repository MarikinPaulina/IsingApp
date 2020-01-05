import numpy as np


class Ising:

    def __init__(self, N, T=0, outM=0):
        """

        """
        self.N = N
        self.spins_board = np.random.randint(0, 2, (N, N), int) - 1
        self.T = T
        self.outM = outM
        self.step_count = 0

    @property
    def energy(self):
        return self.H_board.sum() / 2

    @property
    def average_energy(self):
        return self.energy / self.N**2

    @property
    def magnetism(self):
        return self.spins_board.sum()

    @property
    def average_magnetism(self):
        return self.magnetism / self.N**2

    @property
    def H_board(self):
        neighbours = np.roll(self.spins_board, 1, 0) + np.roll(self.spins_board, -1, 0) + \
            np.roll(self.spins_board, 1, 1) + np.roll(self.spins_board, -1, 1)
        h = -self.spins_board * neighbours
        return h

    def _H(self, i, j):
        neighbours = self.spins_board[(i+1) % self.N, j] + self.spins_board[(i-1) % self.N, j] + \
                     self.spins_board[i, (j+1) % self.N] + self.spins_board[i, (j-1) % self.N]
        h = -self.spins_board[i, j] * neighbours
        return h

    def reset(self):
        self.spins_board = np.random.randint(0, 2, (self.N, self.N), int) - 1

    def step(self):
        self.step_count += 1
        x, y = np.random.randint(0, self.N, 2)
        if self._random_acceptance(x, y):
            self.spins_board[x, y] *= -1

    def _random_acceptance(self, i, j):
        delta_energy = - self._H(i, j) * 2
        acceptance_probability = np.exp(-delta_energy/self.T)
        random_num = np.random.random()
        return random_num < acceptance_probability
