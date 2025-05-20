# Template 1 for using library
## What is Turing Tumble?
Turing Tumble is a mechanical puzzle game that simulates computational logic through the interaction of falling marbles (balls) and configurable parts (blocks) placed on a board.
On a game board, falling balls are guided by plug-in building blocks. Individual blocks (bits) can switch between two states (0, 1), thereby changing the path for subsequent balls. Only one ball is in motion at any time. Balls are released from one of two launchers located at the top: blue balls from the left launcher, red balls from the right launcher. 
Each launcher is controlled by a lever at the bottom edge of the game board. The left lever releases a ball from the left launcher, and the right lever from the right launcher. Initially, one lever is manually activated. The currently configured path then directs the falling ball toward one of the two levers, which automatically triggers the next ball from the corresponding launcher.

The game has a predetermined number of marbles to complete challenges and the objective of the game may be to produce a predefined pattern of blue and red balls in the collection trough at the bottom, or to reach specific configurations of blocks that change their position. These blocks with two positions can be interpreted as bits, thus acting as memory or counters.

Parts:

Ball guides:

-Ramps (ItemType.RAMP_LEFT or ItemType.RAMP_RIGHT): Direct the ball left or right. These are placed on the board in the initial state to the left and can be flipped.

-Crossovers (ItemType.CROSSOVER ): Allow balls coming from the left to go right, and vice versa.

Bits (ItemType.BIT_LEFT or ItemType.BIT_RIGHT):

-Have two distinct states (flipped to the left or flipped to the right).

-Direct balls left or right depending on their current state. A bit flipped to the left will direct the ball to the right, while a bit flipped to the right will direct the ball to the left.

-Switches states each time a ball passes through. These are placed on the board in the initial state to the left and can be flipped.

Gear bits (ItemType.GEAR_BIT_LEFT or ItemType.GEAR_BIT_RIGHT) and gears (ItemType.GEAR):

-Gear bits are similar to bits, but they can be connected by gears and function as a group where every gear bit has the same state.

-When a ball passes through a gear bit, the whole group of gear bits switches states.

Capture block (ItemType.INTERCEPTOR):

-Captures balls and stops the sequence.

The function in the library is used to place the named Part on the actual board. The position is a tuple of two integers, representing the x and y coordinates on the board.
Empty spaces are where you can place bits, ramps, interceptor, crossover and gear bits.
Gray spaces are where you can place gears. The list of functions is later executed by a parser.

| Component Type              | Symbol |
| --------------------------- | ------ |
| `ComponentType.EMPTY`       | `.`    |
| `ComponentType.GEAR`        | `G`    |
| `ComponentType.BIT_LEFT`    | `L`    |
| `ComponentType.BIT_RIGHT`   | `R`    |
| `ComponentType.RAMP_LEFT`   | `\`    |
| `ComponentType.RAMP_RIGHT`  | `/`    |
| `ComponentType.CROSSOVER`   | `X`    |
| `ComponentType.INTERCEPTOR` | `I`    |
| `ComponentType.LAUNCHER`    | `S`    |
| `ComponentType.LEVER_BLUE`  | `B`    |
| `ComponentType.LEVER_RED`   | `r`    |
| `ComponentType.GRAY_SPACE`  | `#`    |


## Library
Solve the challenge using the following function:
```{python}   
 def add_component(self, type: ComponentType, x: int, y: int) -> None:
    
    """Adds a component of the specified type to the board at position (x, y),
    
    if the position is within the bounds of the board."""
   
    if 0 <= x < self.width and 0 <= y < self.height:
    
        self.components[y][x] = Component(type, x, y)
```        
The available component types are defined and named previously ItemType, and the board dimensions are `self.width`(15) × `self.height`(17).

## Challenge
The challenge you need to solve using the library is: ${question}

## Output
The Output should be a collection of the functions from the library to be executed in the order they are needed to solve the challenge. The output should be just the newly added parts, and not a reconstruction of the whole board.
The output should be a list of function call strings, each using the following format:
"add_component(type=ItemType.COMPONENT_NAME, x=INT, y=INT)".

Output example: [
"add_component(type=ItemType.RAMP_LEFT, x=4, y=0)",
"add_component(type=ItemType.BIT_LEFT, x=5, y=1)",
"add_component(type=ItemType.INTERCEPTOR, x=6, y=9)"
]
