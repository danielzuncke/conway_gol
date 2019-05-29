import numpy as np
import cursor
import os
from time import sleep

class GameOfLife:
    """Recreates Conway's game of life and can be printed to commandline

    Args:
        length:      length of dimensions
        bordertype:  define bordertype: void, wrap
    """

    def __init__(self, length, bordertype):
        self.l = length
        self.A = np.random.randint(2, size=(self.l, self.l))
        self.b = bordertype
        ...

    def iterate(self):
        temp = np.zeros((self.l, self.l))
        ...

    def arenaString(self):
        """
        Returns:
            string representing the playing field with dead (0)
            and alive (1) cells
        """
        output = '\n'
        for i in range(self.l):
            for j in range(self.l):
                output += self.A[i, j].astype('str') + ' '
            output += '\n'
        return output

    def draw(self, generations=1, t=500):
        """
        Prints playing field

        Args:
            generations: how many evolutions will be simulated
            t:           redraw frequenzy in ms
        """
        for i in range(generations):
            os.system('cls')  # on windows
            # os.system('clear')  #on linux / os x
            print(self.arenaString())
            self.iterate()
            if i != (generations - 1):
                sleep(t / 1000)
        ...


test = GameOfLife(5, 'void')
test.draw()
