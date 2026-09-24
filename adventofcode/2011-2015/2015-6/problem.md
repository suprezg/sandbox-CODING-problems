# Probably a Fire Hazard

## Statement
Because your neighbors keep defeating you in the holiday house decorating contest year after year, you have decided to deploy one million lights in a $1000 \times 1000$ grid. 

To help you win, Santa has mailed you instructions on how to display the ideal lighting configuration. 

The lights in your grid are numbered from $0$ to $999$ in each direction; the lights at each corner are located at coordinates $(0,0)$, $(0,999)$, $(999,999)$, and $(999,0)$. 

The instructions consist of sequential commands to `turn on`, `turn off`, or `toggle` various inclusive coordinate ranges. Each coordinate range represents opposite corners of a rectangle, inclusive. For example, a coordinate range like `0,0 through 2,2` refers to a $3 \times 3$ square containing $9$ lights. 

All lights in the grid start in the **off** state. To defeat your neighbors, you must execute all of Santa's instructions in the exact order they are listed.

Your goal is to determine: **after following all instructions, how many lights are lit?**

## Constraints
* The grid is strictly of size $1000 \times 1000$ (containing exactly $1,000,000$ lights).
* Coordinates $X$ and $Y$ are integers such that $0 \le X, Y \le 999$.
* In any range $X_1,Y_1 \text{ through } X_2,Y_2$, it is guaranteed that $0 \le X_1 \le X_2 \le 999$ and $0 \le Y_1 \le Y_2 \le 999$.
* All lights are initially turned off.

## Input and Output Format

### Input
The input consists of multiple lines, where each line contains a single instruction. Each instruction will be in one of the following formats:
* `turn on X1,Y1 through X2,Y2`
* `turn off X1,Y1 through X2,Y2`
* `toggle X1,Y1 through X2,Y2`

### Output
Print a single integer representing the total number of lights that are turned on (lit) after executing all instructions in order.

## Input and Output Instances

### Instance 1
**Input:**
```
turn on 0,0 through 999,999
```

**Output:**
```
1000000
```

**Explanation:**
The grid is of size $1000 \times 1000$. The instruction `turn on 0,0 through 999,999` targets the entire grid and turns every single light on. Thus, all $1,000,000$ lights are lit.

---

### Instance 2
**Input:**
```
turn on 0,0 through 999,999
toggle 0,0 through 999,0
turn off 499,499 through 500,500
```

**Output:**
```
998996
```

**Explanation:**
1. `turn on 0,0 through 999,999` turns on all $1,000,000$ lights.
2. `toggle 0,0 through 999,0` toggles the first row of $1000$ lights. Since they were all on, they all turn off. The count of lit lights becomes $1,000,000 - 1000 = 999,000$.
3. `turn off 499,499 through 500,500` turns off the middle $2 \times 2 = 4$ lights. These lights were previously on, so turning them off reduces the lit count by $4$.
The final count is $999,000 - 4 = 998,996$.

---

### Instance 3
**Input:**
```
turn on 10,10 through 20,20
toggle 15,15 through 25,25
turn off 20,20 through 30,30
```

**Output:**
```
135
```

**Explanation:**
1. `turn on 10,10 through 20,20` turns on an $11 \times 11$ area of $121$ lights.
2. `toggle 15,15 through 25,25` toggles an $11 \times 11$ area. The overlapping $6 \times 6 = 36$ lights (from coordinate $(15,15)$ to $(20,20)$) that were ON are turned OFF. The remaining $121 - 36 = 85$ lights in the toggled area that were OFF are turned ON. This results in $85 \text{ (from first action)} + 85 \text{ (from second action)} = 170$ lit lights.
3. `turn off 20,20 through 30,30` turns off any lit lights in this $11 \times 11$ area. Of the currently lit lights, $35$ of them fall into this region (the range $[20..25] \times [20..25]$ excluding $(20,20)$). Turning them off leaves $170 - 35 = 135$ lights lit.