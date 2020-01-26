from setuptools import setup

setup(
    name='SimpleIsingApp',
    version='1.0',
    packages=['SimpleIsingApp'],
    url='https://github.com/MarikinPaulina/IsingApp',
    license='MIT',
    author='Paulina Marikin, Jacob Głuch',
    description='Small app in Python with simulation of Ising model on square lattice made for university project.',
    install_requires=['numpy', 'matplotlib'],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'SimpleIsingApp=SimpleIsingApp.Graphs:main_entrypoint',
        ],
    },

)
