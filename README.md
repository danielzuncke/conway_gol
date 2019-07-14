# Conway's game of life
built in python 3.7.3\
\
**version on master branch might not be in working condition, select latest working_state branch instead**

## packages

* cursor
* numpy
* opencv-python

## TODO's

* def iterate: implement multiprocessing
* clean up code from tests
* multithread cmd outputs
* update documentation
* pause on keyhit, enter menu
* menu with ability to:
  * save and load matrix
  * import matrix from png
  * continue simulation (for n iterations)

## rules for the game

* playing field is initiated at random with dead and alive cells
* a dead cell gets revived when it has exactly three living neighbors
* a living cell with two or three living neighbors stays alive, otherwise it dies
[Wikipedia](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life "Wikipedia: Conway's game of life")

## Example gif from PNGs
![](gol.gif)
