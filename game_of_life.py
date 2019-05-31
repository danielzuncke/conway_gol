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

    Vars:
        width:    width of matrix
        height:   height of matrix
        scaleMatrix:  initiated as None, when the matrix needs to be scaled
                      to make image it will be sized to be the multiplier in
                      the matrix multiplication
        Arena:    randomly generated first generation
        progress: list containing all generations

    Functions:
        iterate:   calculates next generation
        caught:    returns True if game is caught in loop
        setScaleMatrix:  can be called to set scaleMatrix
        scaleUp:   scales a given matrix up for better presentation
        toPNG:     saves given matrix to png file
        toCMD:     prints a given matrix to command line
        loop:      plays the game
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.scaleMatrix = None
        self.Arena = np.random.randint(2, size=(height, width), dtype=np.int)
        self.progress = [self.Arena]

    # TODO: implement faster algorithm (that can make use of multithreading)
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
        print(f'def iterate in ms: {milli() - t1}')

    def caught(self, depth=2):
        """
        Checks if game is stuck by looking for duplicates in progress list

        Args:
            depth:    defines how many previous generations
                      0: won't check any
                      1: returns True if playing field doesn't change at all
                      2: returns True also if alternating structures exist
                         (recommended)
                      to detect more complex loops depth can be set higher,
                      usually not necessary, high numbers will impact
                      performance

        Returns:
            True:    when caught in a loop
            False:   when not caught in a loop
        """
        t1 = milli()
        if len(self.progress) == 1:
            return False
        if depth > len(self.progress):
            depth = len(self.progress)
        for A in self.progress[len(self.progress) - 1 - depth:
                               len(self.progress) - 1]:
            if np.array_equal(self.progress[-1], A):
                print(f'def iterate in ms: {milli() - t1}')  # why def iterate?
                return True
        print(f'def caught in ms: {milli() - t1}')
        return False

    def setScaleMatrix(self, scale=1):
        """
        Function to set self.scaleMatrix

        Args:
            scale:  factor by which the matrix is supposed to be bigger
        """
        t1 = milli()
        self.scaleMatrix = np.zeros((self.height, self.width * scale),
                                    dtype=np.int)
        for a in range(self.height):
            for b in range(scale):
                self.scaleMatrix[a, a * scale + b] = 1
        print(f'def setScaleMatrix in ms: {milli() - t1}')

    def scaleUp(self, A, scale=1):
        """
        Scale up matrix size by a factor: [2, 3] * 3 = [6, 9]

        Args:
            A:       matrix to be scaled
            scale:   factor to be applied

        Returns:
            temp:    scaled matrix A
        """
        if self.scaleMatrix is None:
            self.setScaleMatrix(scale)
        return ((A@self.scaleMatrix).transpose()@self.scaleMatrix).transpose()

    # TODO: multithread
    def toPNG(self, A, x, scale=1):
        """
        Creates ordered PNGs

        Args:
            A:      matrix that will be printed to png
            x:      current generation (to view progress in command line)
            scale:  scales the size that one matrix value will
                    take in pixels
        """
        t1 = milli()
        t2 = milli()
        A = self.scaleUp(A, scale)
        print(f'def scaleUp in ms: {milli() - t2}')
        cv2.imwrite('output_' + str(x) + '.png', A * 255)  # pylint: disable=E1101
        print(f'gen: {x}')
        print(f'def toPNG in ms: {milli() - t1}')

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

    # TODO: fix docstring last, will need a lot of changing otherwise
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
                self.toPNG(self.progress[-1], i + 1, multiPNGscale)
                # TODO: move files to directory, %path% doens't work
                # os.rename('%Projekte%\\Python\\conway_gol\\output_' +
                #          str(i + 1) + '.png',
                #          '%Projekte%\\Python\\conway_gol\\output\\output_'
                #          + str(i + 1) + '.png')
            self.iterate(self.progress[-1])
            if self.caught():
                print()
                self.toPNG(self.progress[-1], multiPNGscale, i + 1)
                print('caught in loop')
                break
            print(f'length of progress[]: {len(self.progress)}')
            print()
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
