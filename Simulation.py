import numpy as np


class Ising:

    board_setups = [
        'random',
        'magnetised',
        'checkerboard',
        'stripes',
        'two sides'
    ]

    def __init__(self, N):
        """

        """
        self.N = N
        self.spins_board = self.set_spins_board(N)
        self.T_crit = 2/np.log(1 + 2**0.5)
        self.T = self.T_crit
        self.outM = 0
        self.step_count = 0
        self.energy = self._energy()
        self.magnetization = self._magnetization()

    def set_spins_board(self, N, board_setup='random'):
        if board_setup == self.board_setups[0]:
            return np.random.randint(0, 2, (N, N), int)*2 - 1
        elif board_setup == self.board_setups[1]:
            return np.ones((N, N), int) * -1
        elif board_setup == self.board_setups[2]:
            board = np.ones((N, N), int)
            board[::2] *= -1
            board[:, ::2] *= -1
            return board
        elif board_setup == self.board_setups[3]:
            board = np.ones((N, N), int)
            board[::2] *= -1
            return board
        elif board_setup == self.board_setups[4]:
            board = np.ones((N, N), int)
            board[N//2:] *= -1
            return board
        else:
            raise ValueError

    def _energy(self):
        return self.H_board.sum() / 2

    @property
    def average_energy(self):
        return self.energy / self.N**2

    def _magnetization(self):
        return self.spins_board.sum()

    @property
    def average_magnetization(self):
        return self.magnetization / self.N ** 2

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
        delta_energy, acceptance = self._random_acceptance(x, y)
        if acceptance:
            self.spins_board[x, y] *= -1
            self.magnetization += 2 * self.spins_board[x, y]
            self.energy += delta_energy

    def _random_acceptance(self, i, j):
        delta_energy = - self._H(i, j) * 2
        acceptance_probability = np.exp(-delta_energy/self.T)
        random_num = np.random.random()
        return delta_energy, random_num < acceptance_probability
