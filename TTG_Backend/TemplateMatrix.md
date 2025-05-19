# Template 1 for using Matrix
## What is Turing Tumble?
Turing Tumble is a mechanical puzzle game that simulates computational logic through the interaction of falling marbles (balls) and configurable parts (blocks) placed on a board. It visually and physically demonstrates basic computational principles and binary logic.
On a game board, falling balls are guided by plug-in building blocks. Individual blocks (bits) can switch between two positions (1, 2), thereby changing the path for subsequent balls. Only one ball is in motion at any time. Balls are released from one of two reservoirs located at the top: blue balls from the left reservoir, red balls from the right reservoir.
Each reservoir is controlled by a lever at the bottom edge of the game board. The left lever releases a ball from the left reservoir, and the right lever from the right reservoir. Initially, one lever is manually activated. The currently configured path then directs the falling ball toward one of the two levers, which automatically triggers the next ball from the corresponding reservoir.
The process stops when either the reservoir supposed to supply the next ball is empty, or when a ball lands in a capture block and thus cannot trigger a new ball.

The objective of the game may be to produce a predefined pattern of blue and red balls in the collection trough at the bottom, or to reach specific configurations of blocks that change their position. These blocks with two positions can be interpreted as bits, thus acting as memory or counters.

Parts:

Ball guides:

-Ramps (ItemType.RAMP_LEFT or ItemType.RAMP_RIGHT) : Direct the ball left or right.

-Crossovers(ItemType.CROSSOVER): Allow balls coming from the left to go right, and vice versa.

Bits (ItemType.BIT_LEFT or ItemType.BIT_RIGHT):

-Have two distinct states (flipped to the left or flipped to the right).

-Direct balls left or right depending on their current state. A bit flipped to the left will direct the ball to the right, while a bit flipped to the right will direct the ball to the left.

-Switch states each time a ball passes through.

Gear bits (ItemType.GEAR_BIT_LEFT or ItemType.GEAR_BIT_RIGHT) and gears (ItemType.GEAR):

-Gear bits are similar to bits, but they can be connected by gears and function as a group where every gear bit has the same state.

-When a ball passes through a gear bit, the whole group of gear bits switches states.

Capture block (ItemType.INTERCEPTOR):

-Captures balls and stops the sequence.

The functions in the library are used to place the named Part on the actual board, which is then executed by a parser. The position is a tuple of two integers, representing the x and y coordinates on the board.

## Library
Solve the challenge by building the board as a Matrix with all of the parts defined in: ${matrixParts}

## Challenge
The challenge you need to solve using the library is: ${question}

## Output
The Output should be collection of the functions from the library to be executed in the order they are needed to solve the challenge. The output should be in the form of a list of functions, with each function being represented as a string.