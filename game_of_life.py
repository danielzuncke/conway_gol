import numpy as np
import cursor
import os
import sys
import cv2
import time
from concurrent.futures import ThreadPoolExecutor

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

    def __init__(self, width, height, max_workers=4):
        self.width = width
        self.height = height
        self.max_workers = max_workers
        self.progress = [np.random.randint(2, size=(height, width),
                                           dtype=np.int)]
        self.temp = np.zeros((self.height, self.width), dtype=np.int)

    def countNeighbors(self, A, x, y):
        neighbors = 0
        for i in range(3):
            if (x - 1 + i) < 0 or (x - 1 + i) == self.height:
                continue
            for j in range(3):
                if (y - 1 + j) < 0 or (y - 1 + j) == self.width:
                    continue
                if j == 1 and i == 1:
                    continue
                if A[x - 1 + i, y - 1 + j] == 1:
                    neighbors += 1
        if neighbors == 3:
            self.temp[x, y] = 1
            return
        elif neighbors == 2 and A[x, y] == 1:
            self.temp[x, y] = 1
            return
        self.temp[x, y] = 0
        return

    # TODO: implement multiprocessing additionally (divide matrix in similar
    #       pieces and calculate them independently)
    # TODO: search for parts that don't change
    def iterate(self, A):
        """
        Creates next generation and appends it to progress list

        Args:
            A:    matrix to evaluate
        """
        with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
            for x in range(self.height):
                for y in range(self.width):
                    executor.submit(self.countNeighbors(A, x, y))
        self.progress.append(self.temp.copy())

    # TODO: implement multithreading
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
        if len(self.progress) == 1:
            return False
        if depth > len(self.progress):
            depth = len(self.progress)
        for A in self.progress[len(self.progress) - 1 - depth:
                               len(self.progress) - 1]:
            if np.array_equal(self.progress[-1], A):
                return True
        return False

    def toPNG(self, scale, singlePNG=None):
        """
        Creates ordered PNGs

        Args:
            A:      matrix that will be printed to png
            x:      current generation (to view progress in command line)
            scale:  scales the size that one matrix value will
                    take in pixels
        """
        if singlePNG is None:
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                for x, A in enumerate(self.progress):
                    executor.submit(cv2.imwrite('output_' + str(x) + '.png',  # pylint: disable=E1101
                                                np.kron(A, np.ones((scale, scale),
                                                                   dtype=np.int) * 255)))
        else:
            cv2.imwrite('single_output.png', np.kron(A,  # pylint: disable=E1101
                                                     np.ones((scale, scale), dtype=np.int) * 255))

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
             multiPNG=None, multiPNGscale=1, loopLen=5, depth=2):
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
        if toCMD:
            cursor.hide()
        for i in range(generations + 1):
            t = milli()
            if toCMD:
                self.toCMD(self.progress[-1], i)
            if self.caught(depth):
                print('caught in loop')
                break
            if i != generations:
                self.iterate(self.progress[-1])
            print(f'finished {i} in {(milli() - t)/1000}s')
        if multiPNG:
            self.toPNG(multiPNGscale)
        if singlePNG:
            self.toPNG(singlePNGscale, self.progress[-1])
        if toCMD:
            cursor.show()


if __name__ == "__main__":
    test = GameOfLife(int(input('width: ')), int(input('height: ')))
    test.loop(generations=(int(input('generations: '))),
              toCMD=False, multiPNG=True, multiPNGscale=5)
