import numpy as np
import cursor
import os
import sys
import cv2
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
        self.progress = []  # stores only last 4 generations
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
        if len(self.progress) == 5:
            if (np.all(self.progress[-1] == self.progress[-3]) or
                    np.all(self.progress[-1] == self.progress[-4])):
                cursor.show()
                sys.exit('stuck in recurrent loop')
            self.progress.pop(0)

    def toString(self, x=-1):
        """
        Returns matrix formatted for console output

        Args:
            x:  generation to return; standard: last generation, 4 are stored

        Returns:
            string representing the playing field with dead and alive cells
        """
        output = '\n'
        for i in range(self.height):
            for j in range(self.width):
                if self.progress[x][i, j] == 0:
                    output += ' '
                else:
                    output += '█'  # probable bests: █, ▄, ▓, ░, ■
            output += '\n'
        return output

    def toPNG(self, i):
        """
        Creates ordered PNGs to animate the game of life
        """
        cv2.imwrite('output_' + str(i) + '.png', self.progress[-1] * 255)  # pylint: disable=E1101
        print(f'generation: {i}')

    def toCMD(self, i):
        """
        Prints playing field to CMD
        """
        os.system('cls')  # on windows
        print(self.toString())
        print('gen:', i)

    def loop(self, generations=1, toCMD=None, toPNG=None):
        """
        Plays the game of life and prints either to CMD or to PNGs

        Args:
            generations:  number of iterations
            toCMD:        if True the game will be printed to the command line
            toCMD:        if True the game will be saved as PNGs
        """
        cursor.hide()
        for i in range(generations):
            if toCMD:
                self.toCMD(i)
            if toPNG:
                self.toPNG(i)
            self.iterate()
        cursor.show()


if __name__ == "__main__":
    test = GameOfLife(int(input('width: ')), int(input('height: ')))
    test.loop(generations=(int(input('generations: '))) + 1, toPNG=True)
