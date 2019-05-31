import numpy as np
import cursor
import os
import sys
import cv2
import time

def milli(): return int(round(time.time() * 1000))

class GameOfLife:
    """
    Recreates Conway's game of life and can be printed to commandline

    Args:
        width:     width of matrix
        height:    height of matrix

    Functions:
        iterate:   calculates next generation
        caught:    returns True if game is caught in loop
        scaleUp:   scales matrix up
        toPNG:     saves matrix to png file
        toCMD:     prints matrix to command line
        loop:      plays the game
    """

    def __init__(self, width, height):
        self.Arena = np.random.randint(2, size=(height, width))
        self.progress = []  # stores only last 4 generations
        self.progress.append(self.Arena)

    def iterate(self, A):
        """
        Creates next generation and appends it to progress list

        Args:
            A:    matrix to evaluate
        """
        t1 = milli()
        temp = np.zeros((A.shape[0], A.shape[1]))
        # cell who's neighbors are counted A[x, y]
        for x in range(A.shape[0]):
            for y in range(A.shape[1]):
                # counting neighbors and spawning, killing cells in accordance
                neighbors = 0
                for i in range(3):
                    if (x - 1 + i) < 0 or (x - 1 + i) == A.shape[0]:
                        continue
                    for j in range(3):
                        if (y - 1 + j) < 0 or (y - 1 + j) == A.shape[1]:
                            continue
                        if j == 1 and i == 1:
                            continue
                        if A[x - 1 + i, y - 1 + j] == 1:
                            neighbors += 1
                if neighbors == 3:
                    temp[x, y] = 1
                elif neighbors == 2 and A[x, y] == 1:
                    temp[x, y] = 1
        self.progress.append(temp)
        t2 = milli()
        print(f'def iterate in ms: {t2 - t1}')

    # TODO: define depth that will be controlled
    def caught(self):
        """
        Checks if game is stuck by looking for for duplicates in progress list

        Returns:
            True:    when caught in a loop
            False:   when not caught in a loop
        """
        t1 = milli()
        for A in self.progress[:-1]:
            if np.array_equal(self.progress[-1], A):
                t2 = milli()
                print(f'def iterate in ms: {t2 - t1}')
                return True
        t2 = milli()
        print(f'def caught in ms: {t2 - t1}')
        return False

    def scaleUp(self, A, scale):
        """
        Scale up matrix size by a factor: [2, 2] * 3 = [6, 6]

        Args:
            A:       matrix to be scaled
            scale:   factor to be applied

        Returns:
            temp:    scaled matrix A
        """
        t1 = milli()
        temp = np.zeros(dtype=int, shape=(
            scale * A.shape[0], scale * A.shape[1]))
        for i in range(A.shape[0]):
            for a in range(scale):
                for j in range(A.shape[1]):
                    for b in range(scale):
                        temp[scale * i + a, scale * j + b] = A[i, j]
        t2 = milli()
        print(f'def scaleUp in ms: {t2 - t1}')
        return temp

    def toPNG(self, A, scale, x):
        """
        Creates ordered PNGs

        Args:
            A:      matrix that will be printed to png
            scale:  scales the size that one matrix value will
                    take in pixels
            x:      current generation (to view progress in command line)
        """
        t1 = milli()
        A = self.scaleUp(A, scale)
        cv2.imwrite('output_' + str(x) + '.png', A * 255)  # pylint: disable=E1101
        print(f'gen: {x}')
        t2 = milli()
        print(f'def toPNG in ms: {t2 - t1}')

    def toCMD(self, A, x=0):
        """
        Prints playing field to CMD

        Args:
            A:    matrix to be printed
            x:    generation
        """
        os.system('cls')  # on windows
        output = '\n'
        for i in range(A.shape[0]):
            for j in range(A.shape[1]):
                if A[i, j] == 0:
                    output += ' '
                else:
                    output += '█'  # probable bests: █, ▄, ▓, ░, ■
            output += '\n'
        print(output)
        print(f'gen: {x}')

    def loop(self, generations=1, toCMD=None, singlePNG=None, singlePNGscale=1,
             multiPNG=None, multiPNGscale=1, loopLen=5):
        """
        Plays the game of life and prints either to CMD or to PNGs

        Args:
            generations:     number of iterations
            toCMD:           if True the game will be printed to the
                             command line
            singlePNG:       if True the final outcome will be saved as PNG
            singlePNGscale:  scales the size that one matrix value will
                             take in pixels
            multiPNG:        if True the playthrough will be saved as PNG
            multiPNGscale:   scales the size that one matrix value will
                             take in pixels
            loopLen:         number of matrizes that are recorded going back
                             from most recent
        """
        cursor.hide()
        for i in range(generations):
            if toCMD:
                self.toCMD(self.progress[-1], i + 1)
            if multiPNG:
                self.toPNG(self.progress[-1], multiPNGscale, i + 1)
                # TODO: move files to directory, %path% doens't work
                # os.rename('%Projekte%\\Python\\conway_gol\\output_' +
                #          str(i + 1) + '.png',
                #          '%Projekte%\\Python\\conway_gol\\output\\output_'
                #          + str(i + 1) + '.png')
            self.iterate(self.progress[-1])
            if len(self.progress) > loopLen:
                self.progress.pop(0)
                if self.caught():
                    print()
                    self.toPNG(self.progress[-1], multiPNGscale, i + 1)
                    print('caught in loop')
                    break
        print()
        if singlePNG:
            self.toPNG(self.progress[-1], singlePNGscale, generations)
            # TODO: move files to directory, %path% doesn't work
            # os.rename('%Projekte%\\Python\\conway_gol\\output_' +
            #          str(i + 1) + '.png',
            #          '%Projekte%\\Python\\conway_gol\\output\\output_'
            #          + str(i + 1) + '.png')
        cursor.show()


if __name__ == "__main__":
    test = GameOfLife(int(input('width: ')), int(input('height: ')))
    test.loop(generations=(int(input('generations: '))),
              toCMD=False, multiPNG=True, multiPNGscale=5)
