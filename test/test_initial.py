import numpy as np
import Simulation


def test_magnetised():
    ising = Simulation.Ising(32, initial_board='magnetised')
    assert np.abs(ising.magnetization) == 32**2
    assert np.isclose(ising.average_energy, -2)


def test_checkerboard():
    ising = Simulation.Ising(32, initial_board='checkerboard')
    assert np.abs(ising.magnetization) == 0
    assert np.isclose(ising.average_energy, 2)


def test_twosides():
    small_ising = Simulation.Ising(32, initial_board='two sides')
    big_ising = Simulation.Ising(64, initial_board='two sides')
    assert np.abs(small_ising.magnetization) == np.abs(big_ising.magnetization) == 0
    # assert
