import numpy as np
import threading
import cv2

class game:
    def __init__(self):
        self.height = 5
        self.width = 5
        self.progress = [np.ones((5, 5), dtype=np.int)]
        for i in range(5):
            for j in range(5):
                if i == 1 or i == 3:
                    self.progress[0][i, j] = 0
        print(f'initiated Matrix:\n{self.progress[0]}\n')
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

    def iterate(self, A, status=False):
        threads = []
        for x in range(self.height):
            for y in range(self.width):
                t = threading.Thread(
                    target=(lambda A, x, y: self.countNeighbors(A, x, y)),
                    args=(A, x, y,))
                threads.append(t)
                t.start()
                t.join()
        # [t.start() for t in threads]
        # [t.join() for t in threads]
        print(f'temp:\n{self.temp}\n')
        self.progress.append(self.temp)
        print(f'temp added:\n{self.progress[-1]}\n')

    def toPNG(self, scale):
        # threads = []
        for x, A in enumerate(self.progress):
                # t = threading.Thread(target=(lambda x: cv2.imwrite(  # pylint: disable=E1101
                #    'output_' + str(x) + '.png',
                #    np.kron(A, np.ones((scale, scale),
                #                       dtype=np.int) * 255))), args=(x,))
                # threads.append(t)
            cv2.imwrite('test_' + str(x) + '.png', np.kron(A,
                                                           np.ones((scale, scale), dtype=np.int) * 255))
            print(f'list progress {x}:\n{A}\n')
        # [t.start() for t in threads]
        # [t.join() for t in threads]

    def loop(self, generations=5, scale=5):
        for x in range(generations):
            self.iterate(self.progress[-1])
        self.toPNG(scale)


test = game()
test.loop()
