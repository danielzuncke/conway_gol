import numpy as np
import cursor
import os
from time import sleep

class GameOfLife:
    """ Recreates Conway's game of life and can be printed to commandline """

    def __init__(self, length, bordertype, fps=500, generations=1):
        """
        length       length of dimensions\n
        bordertype   define bordertype: void, wrap or mirror\n
        fps          redraw-rate in ms\n
        generations  number of generations simulated
        """
        self.l = length
        self.A = np.random.randint(2, size=(self.l, self.l))
        self.b = bordertype
        self.fps = fps
        self.generations = generations
        ...

    def iterate(self):
        temp = np.zeros((self.l, self.l))
        ...
    ...

    def arenaString(self):
        """ draws playing field for each generation """
        output = '\n'
        for i in range(self.l):
            for j in range(self.l):
                output += self.A[i, j].astype('str') + ' '
            output += '\n'
        return output

    def draw(self):
        for i in range(self.generations):
            os.system('cls')  # on windows
            # os.system('clear')  #on linux / os x
            print(self.arenaString())
            self.iterate()
            sleep(.5)
        ...


test = GameOfLife(5, 'void')
test.draw()
