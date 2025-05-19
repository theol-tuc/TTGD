# Template 1 for using Matrix
## What is Turing Tumble?
Turing Tumble is a mechanical puzzle game that simulates computational logic through the interaction of falling marbles (balls) and configurable parts (blocks) placed on a board. It visually and physically demonstrates basic computational principles and binary logic.
On a game board, falling balls are guided by plug-in building blocks. Individual blocks (bits) can switch between two positions (1, 2), thereby changing the path for subsequent balls. Only one ball is in motion at any time. Balls are released from one of two reservoirs located at the top: blue balls from the left reservoir, red balls from the right reservoir.
Each reservoir is controlled by a lever at the bottom edge of the game board. The left lever releases a ball from the left reservoir, and the right lever from the right reservoir. Initially, one lever is manually activated. The currently configured path then directs the falling ball toward one of the two levers, which automatically triggers the next ball from the corresponding reservoir.
The process stops when either the reservoir supposed to supply the next ball is empty, or when a ball lands in a capture block and thus cannot trigger a new ball.

The objective of the game may be to produce a predefined pattern of blue and red balls in the collection trough at the bottom, or to reach specific configurations of blocks that change their position. These blocks with two positions can be interpreted as bits, thus acting as memory or counters.

This is how the Parts are displayed in the encoded Board:
```{python} 
ComponentType.EMPTY: row.append(".")
ComponentType.GEAR: row.append("G")
ComponentType.BIT_LEFT: row.append("L")
ComponentType.BIT_RIGHT: row.append("R")
ComponentType.RAMP_LEFT: row.append("\\")
ComponentType.RAMP_RIGHT: row.append("/")
ComponentType.CROSSOVER: row.append("X")
ComponentType.INTERCEPTOR: row.append("I")
ComponentType.LAUNCHER: row.append("S")
ComponentType.LEVER_BLUE: row.append("B")
ComponentType.LEVER_RED: row.append("r")
ComponentType.GRAY_SPACE: row.append("#")
else:
row.append(" ")
```

The functions in the library are used to place the named Part on the actual board, which is then executed by a parser. The position is a tuple of two integers, representing the x and y coordinates on the board.

## Library
Solve the challenge by building the board as a Matrix with all of the parts defined in: ${matrixParts}

## Challenge
The challenge you need to solve is: ${question}

## Output
The Output should be a Matrix of lists, with every space of the board filled with the symbol corresponding to the part in that space.