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
        """
        Creates next generation and updates playing field matrix A
        """
        temp = np.zeros((self.l, self.l))
        # cell who's neighbors are counted A[x, y]
        for x in range(self.l):
            for y in range(self.l):
                # counting neighbors and spawning, killing cells in accordance
                neighbors = 0
                for i in range(3):
                    if (x - 1 + i) < 0 or (x - 1 + i) == self.l:
                        continue
                    for j in range(3):
                        if (y - 1 + j) < 0 or (y - 1 + j) == self.l:
                            continue
                        if j == 1 and i == 1:
                            continue
                        if self.A[x - 1 + i, y - 1 + j] == 1:
                            neighbors += 1
                if neighbors == 3:
                    temp[x, y] = 1
                elif neighbors == 2 and self.A[x, y] == 1:
                    temp[x, y] = 1
        self.A = temp

        # TODO: break loop if it doesnt change anymore
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
                if self.A[i, j] == 0:
                    output += ' '
                else:
                    output += '█'  # alternatively: ▄, ▓, ░, ■
            output += '\n'
        return output

    def draw(self, generations=1, t=0):
        """
        Prints playing field

        Args:
            generations: how many evolutions will be simulated
            t:           redraw frequency in ms
        """
        cursor.hide()
        for i in range(generations):
            os.system('cls')  # on windows
            # os.system('clear')  # on linux / os x
            print(self.arenaString())
            self.iterate()
            if i != (generations - 1):
                sleep(t / 1000)
            print('gen:', i)
            print('break with ctrl + c (Windows)')
        cursor.show()


test = GameOfLife(int(input('size: ')), 'void')
test.draw(generations=(int(input('generations: '))) + 1)
