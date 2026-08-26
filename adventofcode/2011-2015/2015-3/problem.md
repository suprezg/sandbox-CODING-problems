# Day 3: Perfectly Spherical Houses in a Vacuum

## Statement

Santa Claus is delivering Christmas presents to children living in an infinite two-dimensional Cartesian grid of houses. Each house is represented by a coordinate pair $(x, y)$ where $x$ and $y$ are integers. 

At the start of his journey, Santa begins at the coordinate $(0, 0)$ and immediately delivers a present to the house at this starting location. 

Following this, an elf at the North Pole sends Santa a series of movement directions via radio. The directions are represented as a single continuous string of characters. Each character in the string indicates a move to an adjacent house in one of the four cardinal directions:
*   `^` instructs Santa to move one unit **North** (increasing the y-coordinate: $(x, y) \to (x, y + 1)$).
*   `v` instructs Santa to move one unit **South** (decreasing the y-coordinate: $(x, y) \to (x, y - 1)$).
*   `>` instructs Santa to move one unit **East** (increasing the x-coordinate: $(x, y) \to (x + 1, y)$).
*   `<` instructs Santa to move one unit **West** (decreasing the x-coordinate: $(x, y) \to (x - 1, y)$).

After making each individual move, Santa immediately delivers another present to the house at his new location. 

Because the elf back at the North Pole has had a little too much eggnog, the instructions are highly erratic and often redundant. Consequently, Santa ends up visiting several houses multiple times, delivering more than one present to those locations.

Your task is to determine the total number of unique houses that receive **at least one present** from Santa.

---

## Constraints

*   Let $S$ be the string representing the sequence of moves.
*   The length of the string, $|S|$, satisfies: $1 \le |S| \le 10^5$.
*   The string $S$ consists exclusively of characters from the set { '^', $\text{`v`}, \text{`<`}, \text{`>`}$}.
*   The coordinate grid is theoretically infinite in all four directions. Coordinates $(x, y)$ can range from $[-|S|, |S|]$ in both dimensions, comfortably fitting within standard 32-bit signed integers.

---

## Input and Output Format

### Input
The input consists of a single line containing a non-empty string $S$ representing Santa's movement instructions.

### Output
Print a single integer representing the total number of unique houses that receive at least one present.

---

## Input and Output Instances

### Instance 1
**Input:**
```text
>
```

**Output:**
```text
2
```

**Explanation:**
Santa starts at $(0,0)$ and delivers a present. He then reads the instruction `>` which directs him to move East to $(1,0)$, where he delivers another present. The visited houses are $\{(0,0), (1,0)\}$. The number of unique houses visited is $2$.

---

### Instance 2
**Input:**
```text
^>v<
```

**Output:**
```text
4
```

**Explanation:**
1. Start at $(0,0)$ (Presents delivered: $\{(0,0)\}$)
2. Move North `^` to $(0,1)$ (Presents delivered: $\{(0,0), (0,1)\}$)
3. Move East `>` to $(1,1)$ (Presents delivered: $\{(0,0), (0,1), (1,1)\}$)
4. Move South `v` to $(1,0)$ (Presents delivered: $\{(0,0), (0,1), (1,1), (1,0)\}$)
5. Move West `<` back to $(0,0)$ (Presents delivered: $\{(0,0), (0,1), (1,1), (1,0)\}$)

Even though the house at $(0,0)$ receives two presents, we only count unique houses. The unique set of visited locations is $\{(0,0), (0,1), (1,1), (1,0)\}$, giving a total of $4$ unique houses.

---

### Instance 3
**Input:**
```text
^v^v^v^v^v
```

**Output:**
```text
2
```

**Explanation:**
Santa repeatedly moves back and forth between $(0,0)$ and $(0,1)$. 
*   Starts at $(0,0)$
*   Moves to $(0,1)$, then back to $(0,0)$, then to $(0,1)$, and so on.

The only houses that ever receive presents are $(0,0)$ and $(0,1)$. The total number of unique houses visited is $2$.

---

### Instance 4
**Input:**
```text
^^<<
```

**Output:**
```text
5
```

**Explanation:**
1. Start at $(0,0)$ (Presents delivered: $\{(0,0)\}$)
2. Move North `^` to $(0,1)$ (Presents delivered: $\{(0,0), (0,1)\}$)
3. Move North `^` to $(0,2)$ (Presents delivered: $\{(0,0), (0,1), (0,2)\}$)
4. Move West `<` to $(-1,2)$ (Presents delivered: $\{(0,0), (0,1), (0,2), (-1,2)\}$)
5. Move West `<` to $(-2,2)$ (Presents delivered: $\{(0,0), (0,1), (0,2), (-1,2), (-2,2)\}$)

All 5 locations visited during this journey are unique. Thus, the output is $5$.