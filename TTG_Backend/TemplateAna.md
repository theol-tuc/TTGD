## Game Overview

**Turing Tumble** is a mechanical puzzle game that simulates computational logic by dropping **blue** and **red marbles** from two launchers onto a **15×17 board**, interacting with configurable parts.

* **Marble colors**:

  * **Blue (b)** from the **left launcher**
  * **Red (r)** from the **right launcher**

* **Ball sequencing**:
  One marble falls at a time. After a ball lands on a **lever** (bottom left or right), it automatically releases the next ball from the corresponding launcher.

* **Goal**:
  Solve challenges using a limited set of parts. The objective may be to:

  * Produce a specific output pattern (e.g., a list of marbles reaching the bottom), or
  * Achieve a structural board configuration (if `expectedOutput` is empty).

---

## Board Encoding

Each cell contains a symbol representing a part, space, or border. Coordinates are `(x, y)` with `(0, 0)` in the **top-left**.

### Legend of Board Symbols

| Symbol  | Description         | ItemType Enum                | Placement Rules          |
| ------- | ------------------- | ---------------------------- | ------------------------ |
| `.`     | Empty space         | `ItemType.EMPTY`             | Can place any part       |
| `\`     | Ramp left           | `ItemType.RAMP_LEFT`         | Pre-placed or addable    |
| `/`     | Ramp right          | `ItemType.RAMP_RIGHT`        | Pre-placed or addable    |
| `L`     | Bit left            | `ItemType.BIT_LEFT`          | -                        |
| `R`     | Bit right           | `ItemType.BIT_RIGHT`         | -                        |
| `X`     | Crossover           | `ItemType.CROSSOVER`         | -                        |
| `I`     | Interceptor         | `ItemType.INTERCEPTOR`       | -                        |
| `G`     | Gear                | `ItemType.GEAR`              | Only on gray (`#`) tiles |
| `GL`    | Gear Bit left       | `ItemType.GEAR_BIT_LEFT`     | On non-gray spaces       |
| `GR`    | Gear Bit right      | `ItemType.GEAR_BIT_RIGHT`    | On non-gray spaces       |
| `#`     | Gray space          | `ItemType.GRAY`              | Gears only               |
| `B`     | Blue lever (bottom) | `ItemType.LEVER_BLUE`        | Launches blue balls      |
| `R`     | Red lever (bottom)  | `ItemType.LEVER_RED`         | Launches red balls       |
| `b`     | Blue ball           | `ItemType.BALL_BLUE`         | -                        |
| `r`     | Red ball            | `ItemType.BALL_RED`          | -                        |
| Borders | Frame elements      | `ItemType.BORDER_*`          | -                        |
| `< >`   | Left/Right corners  | `ItemType.CORNER_LEFT/RIGHT` | -                        |
| `i`     | Invalid             | `ItemType.INVALID`           | Do not place parts here  |

---

## Core Mechanic – Part Behavior

| Part            | Behavior                                                                                      |
| --------------- | --------------------------------------------------------------------------------------------- |
| **Ramps**       | Redirect balls left (`\`) or right (`/`). Fixed direction, can be flipped.                    |
| **Bits**        | Flip state each time a ball passes. Direct left or right depending on current state.          |
| **Gear Bits**   | Connected via gears — all flip states **together**. Functionally like Bits, but synchronized. |
| **Crossovers**  | Allow left-right crisscrossing. Path doesn't change.                                          |
| **Interceptor** | Captures a ball and ends the sequence.                                                        |
| **Gears**       | Connect Gear Bits into a group. Must be placed on gray `#` tiles.                             |

---

## Available Function

You can add components like this:

```python
def add_component(self, type: ComponentType, x: int, y: int) -> None:
    """Adds a component to the board at (x, y) if within bounds."""
```

* Valid `x`: 0–14
* Valid `y`: 0–16
* Coordinates are 0-indexed from **top-left** of the board.

---

## 📤 Output Format

You must return a list of **function calls** as strings that add **only** the new parts needed to solve the challenge. Do **not** reconstruct the entire board.

### ✅ Example output:

```python
[
  "add_component(type=ItemType.RAMP_LEFT, x=4, y=0)",
  "add_component(type=ItemType.BIT_LEFT, x=5, y=1)",
  "add_component(type=ItemType.INTERCEPTOR, x=6, y=9)"
]
```

---

## 🎯 CHALLENGE STARTS HERE

**Challenge ID**: 1
**Description**: Make all of the **blue marbles (and only the blue marbles)** reach the end.
**Available Parts**:

* 4× `ItemType.RAMP_LEFT`

**Initial Board Layout**:

```
|i-iiiiiiiii-i|
|ii-iiiiiii-ii|
|iii-SiiiS-iii|
|iii#\#i#.#iii|
|ii#.#/#.#.#ii|
|i#.#\#.#.#.#i|
|i.#.#.#.#.#.i|
|i#.#\#.#.#.#i|
|i.#.#.#.#.#.i|
|i#.#\#.#.#.#i|
|i.#.#.#.#.#.i|
|i#.#\#.#.#.#i|
|i.#.#.#.#.#.i|
|iiiiii.iiiiii|
|iiBiBBiRRiRii|
|iiiiiiiiiiiii|
```

**Marble Counts**:

* Blue Marbles: 8
* Red Marbles: 8

**Expected Output**:

```python
["blue", "blue", "blue", "blue", "blue", "blue", "blue", "blue"]
```

---
