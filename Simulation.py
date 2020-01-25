import numpy as np

board_setups = [
        'random',
        'magnetised',
        'checkerboard',
        'stripes',
        'two sides'
    ]


class Ising:
    board_setups = board_setups

    def __init__(self,
                 N: int,
                 T: float=1,
                 M: float=0,
                 initial_board: board_setups = 'random'):
        """
        Implements Metropolis-Hasting algorithm that simulates Ising model.
        Algorithm runs over 2D square lattice with periodic boundary conditions.

        :param N: int, size of side of lattice - whole lattice has N^2 spins
        :param T: float, temperature in units critical temperature for infinite lattice
        :param M: float, outside magnetic field
        :param initial_board: str, one of options for initial state of lattice
        """
        self.spins_board = self.set_spins_board(N, board_setups[1])
        self.T_crit = 2/np.log(1 + 2**0.5)
        self.T = self.T_crit*T
        self.outM = M
        self.step_count = 0
        self.energy = self._energy()
        self.magnetization = self._magnetization()

    def set_spins_board(self,
                        N: int,
                        board_setup: board_setups = 'random') -> np.array:
        """
        Creates square lattices of given size with spines {1,-1}.
        State is chosen based on board_setup parameter
        :param N: int, size of side of lattice - whole lattice has N^2 spins
        :param board_setup:
        :return: np.array, square array of spines in given state
        """
        if board_setup == self.board_setups[0]:
            return np.random.randint(0, 2, (N, N), int)*2 - 1
        elif board_setup == self.board_setups[1]:
            board = np.ones((N, N), int) * -1
            board[0, 0] *= -1
            return board
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
        return self.energy / self.spins_board.size

    def _magnetization(self):
        return self.spins_board.sum()

    @property
    def average_magnetization(self):
        return self.magnetization / self.spins_board.size

    @property
    def H_board(self):
        neighbours = np.roll(self.spins_board, 1, 0) + np.roll(self.spins_board, -1, 0) + \
            np.roll(self.spins_board, 1, 1) + np.roll(self.spins_board, -1, 1)
        h = -self.spins_board * neighbours
        return h

    def _H(self, i: int, j: int):
        N = self.spins_board.shape[0]
        neighbours = self.spins_board[(i+1) % N, j] + self.spins_board[(i-1) % N, j] + \
                     self.spins_board[i, (j+1) % N] + self.spins_board[i, (j-1) % N]
        h = -self.spins_board[i, j] * neighbours
        return h

    def step(self):
        self.step_count += 1
        x, y = np.random.randint(0, self.spins_board.shape[0], 2)
        delta_energy, acceptance = self._random_acceptance(x, y)
        if acceptance:
            self.spins_board[x, y] *= -1
            self.magnetization += 2 * self.spins_board[x, y]
            self.energy += delta_energy

    def _random_acceptance(self, i:int, j:int):
        delta_energy = - self._H(i, j) * 2
        acceptance_probability = np.exp(-delta_energy/self.T)
        random_num = np.random.random()
        return delta_energy, random_num < acceptance_probability
