import numpy as np
import cursor
import os
import shutil
import cv2


class GameOfLife:
    """
    Recreates Conway's game of life and can be printed to cmd or to PNG series

    Args:
        width:    width of matrix
        height:   height of matrix

    Vars:
        width:    width of matrix
        height:   height of matrix
        src_path: script path
        dst_path: path to which generated files are moved
        progress: list containing all generations

    Functions:
        countNeighbors:  returns how many living cells surround target cell
        iterate:  calculates next generation
        caught: checks if game is caught in a loop
        toPNG:  saves given matrix or list of matrices to png file
                pixel size is scalable
        toCMD:  prints a given matrix to command line
        loop:   plays the game
    """

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.src_path = os.path.abspath('.') + ('\\')
        self.dst_path = os.path.abspath('.') + ('\\output\\')
        self.progress = [np.random.randint(2, size=(height, width),
                                           dtype=np.int)]
        self.temp = np.zeros((self.height, self.width), dtype=np.int)

    def countNeighbors(self, A, x, y):
        """
        Counts alive neighbors of a given cell in matrix and returns next gen
        cell status

        Args:
            A:    matrix that contains the cell of interest
            x:    position of cell
            y:    position of cell

        Returns:
            None
        """
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

    def iterate(self, A):
        """
        Calculates next generation and appends it to progress list

        Args:
            A:    matrix to evaluate
        """
        for x in range(self.height):
            for y in range(self.width):
                self.countNeighbors(A, x, y)
        self.progress.append(self.temp.copy())

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

    def toPNG(self, scale=5, singlePNG=None):
        """
        Creates ordered PNGs; cell-size adjustable, standard 5 by 5 pixels

        Args:
            scale:    scales the size that one matrix value will
                      take in pixels
            singlePNG:  only saves last Matrix in list
        """
        if singlePNG is None:
            for x, A in enumerate(self.progress):
                cv2.imwrite(  # pylint: disable=E1101
                    'output_' + str(x) + '.png',
                    np.kron(A, np.ones((scale, scale), dtype=np.int) * 255))
                shutil.move(self.src_path + 'output_' + str(x) + '.png',
                            self.dst_path + 'output_' + str(x) + '.png')
        else:
            cv2.imwrite('single_output.png',  # pylint: disable=E1101
                        np.kron(self.progress[-1],
                                np.ones((scale, scale), dtype=np.int) * 255))
            shutil.move(self.src_path + 'single_output.png',
                        self.dst_path + 'single_output.png')

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
                    output += '█'  # good chars: █, ▄, ▓, ░, ■
            output += '\n'
        print(output)
        print(f'gen: {x}')

    def loop(self, generations=1, toCMD=None, singlePNG=None, singlePNGscale=1,
             multiPNG=None, multiPNGscale=1, loopLen=5, depth=2):
        """
        Plays the game of life, can print to cmd or save as png's

        Args:
            generations:  number of iterations
            toCMD:    if True the game will be printed to the
                      command line
            singlePNG:  if True the final outcome will be saved as PNG
            singlePNGscale:  scales the size that one matrix value will
                             take in pixels
            multiPNG: if True the playthrough will be saved as PNG
            multiPNGscale:  scales the size that one matrix value will
                            take in pixels
            loopLen:  number of matrizes that are recorded going back
                      from most recent
            depth:    how deep list checks for duplicates
        """
        if toCMD:
            cursor.hide()
        for i in range(generations + 1):
            if toCMD:
                self.toCMD(self.progress[-1], i)
            if self.caught(depth):
                print('caught in loop')
                break
            if i != generations:
                self.iterate(self.progress[-1])
        if multiPNG:
            self.toPNG(multiPNGscale)
        if singlePNG:
            self.toPNG(singlePNGscale, self.progress[-1])
        if toCMD:
            cursor.show()


if __name__ == "__main__":
    example = GameOfLife(int(input('width: ')), int(input('height: ')))
    example.loop(generations=(int(input('generations: '))),
                 multiPNG=True, multiPNGscale=5)
