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
Solve the challenge by building the board as a Matrix with the following function:
```{python}
"""    
    def initialize_board(self) -> None:
        \"\"\"Initialize the board with empty components\"\"\"
        self.components = [[Component(ComponentType.EMPTY, x, y)
                            for x in range(self.width)]
                           for y in range(self.height)]

        # Set up borders and invalid spaces
        self.setup_board_structure()

    def setup_board_structure(self) -> None:
        \"\"\"Set up the board structure with borders and invalid spaces\"\"\"

        #Set up the diamond pattern
        self.setup_diamond_pattern()

        # Set vertical borders
        for y in range(self.height):
            self.components[y][0].type = ComponentType.BORDER_VERTICAL
            self.components[y][14].type = ComponentType.BORDER_VERTICAL

        # Set horizontal border (last row)
        for x in range(self.width):
            self.components[16][x].type = ComponentType.BORDER_HORIZONTAL

        # Add levers at the bottom
        self.components[14][6].type = ComponentType.LEVER_BLUE
        self.components[14][5].type = ComponentType.LEVER_BLUE
        self.components[14][3].type = ComponentType.LEVER_BLUE
        self.components[14][8].type = ComponentType.LEVER_RED
        self.components[14][9].type = ComponentType.LEVER_RED
        self.components[14][11].type = ComponentType.LEVER_RED

        # Add corners
        self.components[16][0].type = ComponentType.CORNER_LEFT
        self.components[16][14].type = ComponentType.CORNER_RIGHT

        # Add launchers at the top
        self.components[2][5].type = ComponentType.LAUNCHER  # Left launcher
        self.components[2][9].type = ComponentType.LAUNCHER  # Right launcher

        for y in range (1, self.width-1):
            self.components[13][y].type = ComponentType.INVALID

        self.components[13][7].type = ComponentType.EMPTY
        self.components[14][7].type = ComponentType.INVALID
        self.components[15][7].type = ComponentType.INVALID

    def setup_diamond_pattern(self) -> None:
        \"\"\"Set up the diamond pattern of invalid spaces\"\"\"
        # Row 1 (index 0)
        for x in range(1, self.width - 1):
            if x == 1 or (3 <= x <= 11) or x == 13:
                self.components[0][x].type = ComponentType.INVALID
            elif x == 2:
                self.components[0][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 12:
                self.components[0][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 2 (index 1)
        for x in range(1, self.width - 1):
            if x in [1, 2] or (4 <= x <= 10) or x in [12, 13]:
                self.components[1][x].type = ComponentType.INVALID
            elif x == 3:
                self.components[1][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 11:
                self.components[1][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 3 (index 2)
        for x in range(1, self.width - 1):
            if x in [1, 2, 3] or (5 <= x <= 9) or x in [11, 12, 13]:
                self.components[2][x].type = ComponentType.INVALID
            elif x == 4:
                self.components[2][x].type = ComponentType.BORDER_DIAGONAL_LEFT
            elif x == 10:
                self.components[2][x].type = ComponentType.BORDER_DIAGONAL_RIGHT

        # Row 4 (index 3)
        for x in range(1, self.width - 1):
            if x in [1,2,3,7,11,12,13]:
                self.components[3][x].type = ComponentType.INVALID
            elif x % 2 == 0:
                self.components[3][x].type = ComponentType.GRAY_SPACE
            else:
                self.components[3][x].type = ComponentType.EMPTY

        # Row 5 (index 4)
        for x in range(1, self.width):
            if x in [1,2,12,13]:
                self.components[4][x].type = ComponentType.INVALID
            elif x % 2 == 1:
                self.components[4][x].type = ComponentType.GRAY_SPACE
            else:
                self.components[4][x].type = ComponentType.EMPTY



        # Middle rows
        for y in range(5, 13):
            for x in range(2,14):
                if (x + y) % 2 == 1:
                    self.components[y][x].type = ComponentType.GRAY_SPACE
                else:
                    self.components[y][x].type = ComponentType.EMPTY
            self.components[y][1].type = ComponentType.INVALID
            self.components[y][13].type = ComponentType.INVALID

        # Bottom rows
        for y in range(self.height - 3, self.height - 1):
            for x in range(1, self.width - 1):
                if (x <= 6) or (x >= 8):
                    self.components[y][x].type = ComponentType.INVALID

        self.components[14][6].type = ComponentType.LEVER_BLUE
        self.components[14][5].type = ComponentType.LEVER_BLUE
        self.components[14][3].type = ComponentType.LEVER_BLUE
        self.components[14][8].type = ComponentType.LEVER_RED
        self.components[14][9].type = ComponentType.LEVER_RED
        self.components[14][11].type = ComponentType.LEVER_RED"""
```
## Challenge
The challenge you need to solve is: ${question}

## Output
The Output should be a Matrix of lists, with every space of the board filled with the symbol corresponding to the part in that space.