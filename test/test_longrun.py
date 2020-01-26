from tqdm import tqdm
import numpy as np
from SimpleIsingApp import Simulation


def test_magnetised_hot():
    np.random.seed(789)
    ising = Simulation.Ising(32, T=900, initial_board='magnetised')
    E_start = ising.energy
    for _ in tqdm(range(int(1e5))):
        ising.step()
    assert ising.energy > E_start
    assert np.abs(ising.average_magnetization) < (2 * ising.spins_board.std())


def test_checker_hot():
    np.random.seed(789)
    ising = Simulation.Ising(32, T=900, initial_board='checkerboard')
    E_start = ising.energy
    for _ in tqdm(range(int(1e5))):
        ising.step()
    assert ising.energy < E_start
    assert np.abs(ising.average_magnetization) < (2 * ising.spins_board.std())


def test_magnetised_cold():
    np.random.seed(789)
    ising = Simulation.Ising(32, T=1e-5, initial_board='magnetised')
    E_avg_start = ising.average_energy
    for _ in tqdm(range(int(1e5))):
        ising.step()
    assert np.isclose(ising.average_energy, E_avg_start)
    assert np.abs(ising.average_magnetization) - 1 <= (2 * ising.spins_board.std())


def test_random_cold():
    np.random.seed(789)
    ising = Simulation.Ising(16, T=1e-5, initial_board='random')
    for _ in tqdm(range(int(1e5))):
        ising.step()
    assert np.isclose(ising.average_energy, -2)
    assert np.abs(ising.average_magnetization) - 1 <= (2 * ising.spins_board.std())