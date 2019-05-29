import numpy as np
import cursor
import os
import sys
from time import sleep

class GameOfLife:
    """
    Recreates Conway's game of life and can be printed to commandline

    Args:
        width:       width of matrix
        height:      height of matrix

    Functions:
        toString:    returns a generation in form of a string
        draw:        plays the game out and prints evolution process
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.Arena = np.random.randint(2, size=(self.height, self.width))
        self.progress = []
        self.progress.append(self.Arena)

    def iterate(self):
        """
        Creates next generation and append to progress list
        """
        temp = np.zeros((self.height, self.width))
        # cell who's neighbors are counted A[x, y]
        for x in range(self.height):
            for y in range(self.width):
                # counting neighbors and spawning, killing cells in accordance
                neighbors = 0
                for i in range(3):
                    if (x - 1 + i) < 0 or (x - 1 + i) == self.height:
                        continue
                    for j in range(3):
                        if (y - 1 + j) < 0 or (y - 1 + j) == self.width:
                            continue
                        if j == 1 and i == 1:
                            continue
                        if self.progress[-1][x - 1 + i, y - 1 + j] == 1:
                            neighbors += 1
                if neighbors == 3:
                    temp[x, y] = 1
                elif neighbors == 2 and self.progress[-1][x, y] == 1:
                    temp[x, y] = 1
        self.progress.append(temp)

        # break loop if it doesnt change anymore
        # partly implement: checks last element vs 2 and 3 generations before
        if len(self.progress) >= 4:
            if (np.all(self.progress[-1] == self.progress[-3]) or
                    np.all(self.progress[-1] == self.progress[-4])):
                sys.exit('stuck in recurrent loop')

    def toString(self, x=-1):
        """
        Args:
            x:  generation to evaluate, by standard the last generation

        Returns:
            string representing the playing field with dead and alive cells
        """
        output = '\n'
        for i in range(self.height):
            for j in range(self.width):
                if self.progress[x][i, j] == 0:
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
            print(self.toString())
            self.iterate()
            if i != (generations - 1):
                sleep(t / 1000)
            print('gen:', i)
        cursor.show()


if __name__ == "__main__":
    test = GameOfLife(int(input('width: ')), int(input('height: ')))
    test.draw(generations=(int(input('generations: '))) + 1)
