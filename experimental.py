import os
import cursor
from time import sleep

cursor.hide()
for i in range(10):
    os.system('cls')
    print(i + 1)
    sleep(0.5)
