# B - Crop

## Statement

We are given a grid representation of a black-and-white image. The image has a height of $H$ pixels and a width of $W$ pixels.
Each pixel at the intersection of the $i$-th row from the top and the $j$-th column from the left is characterized by:
- `.` representing a white pixel.
- `#` representing a black pixel.

Your objective is to perform a cropping operation on this image. This cropping process involves trimming away any outer borders that consist entirely of white pixels. Specifically, the following operations are executed in sequence:
1. **Trim Top:** While the topmost row of the current grid consists solely of white pixels (`.`), remove this row from the grid.
2. **Trim Bottom:** While the bottommost row of the current grid consists solely of white pixels (`.`), remove this row from the grid.
3. **Trim Left:** While the leftmost column of the current grid consists solely of white pixels (`.`), remove this column from the grid.
4. **Trim Right:** While the rightmost column of the current grid consists solely of white pixels (`.`), remove this column from the grid.

Alternatively, this process is mathematically equivalent to finding the smallest bounding box that contains all the black pixels (`#`) in the image. Since the problem guarantees that there is at least one black pixel present, this bounding box is always well-defined. 
Specifically, if we find:
- The minimum row index containing a `#` as $r_{\min}$ and the maximum row index as $r_{\max}$ ($1 \le r_{\min} \le r_{\max} \le H$).
- The minimum column index containing a `#` as $c_{\min}$ and the maximum column index as $c_{\max}$ ($1 \le c_{\min} \le c_{\max} \le W$).

The cropped image will be the rectangular subgrid of the original grid spanning from row $r_{\min}$ to $r_{\max}$ and from column $c_{\min}$ to $c_{\max}$.

You are required to output the resulting cropped grid.

## Constraints

- $1 \le H, W \le 50$
- $H$ and $W$ are integers.
- Each character $C_{i,j}$ in the grid is either `.` (white) or `#` (black).
- At least one black pixel (`#`) exists in the given input grid.

## Input and Output Format

### Input

The input is given from Standard Input in the following format:

$$\begin{array}{l}
H \quad W \\
C_{1,1}C_{1,2}\ldots C_{1,W} \\
C_{2,1}C_{2,2}\ldots C_{2,W} \\
\vdots \\
C_{H,1}C_{H,2}\ldots C_{H,W}
\end{array}$$

### Output

Output the image after performing the cropping process. 
If the cropped image has height $h$ and width $w$, print it as $h$ lines, each containing $w$ characters, representing the cropped grid:

$$\begin{array}{l}
c_{1,1}c_{1,2}\ldots c_{1,w} \\
c_{2,1}c_{2,2}\ldots c_{2,w} \\
\vdots \\
c_{h,1}c_{h,2}\ldots c_{h,w}
\end{array}$$

where $c_{i,j}$ is either `.` or `#`.

## Input and Output Instances

### Instance 1

#### Input
```
4 5
.....
..#..
.###.
.....
```

#### Output
```
.#.
###
```

#### Explanation
- The first row contains only white pixels (`.....`), so it is removed.
- The fourth row contains only white pixels (`.....`), so it is removed.
- In the remaining $2 \times 5$ grid, the first column contains only white pixels, so it is removed.
- In the remaining $2 \times 4$ grid, the last column contains only white pixels, so it is removed.
- The resulting $2 \times 3$ grid is printed.

---

### Instance 2

#### Input
```
3 4
#...
....
...#
```

#### Output
```
#...
....
...#
```

#### Explanation
- The topmost row contains a black pixel (at column 1).
- The bottommost row contains a black pixel (at column 4).
- The leftmost column contains a black pixel (at row 1).
- The rightmost column contains a black pixel (at row 3).
- No rows or columns consist entirely of white pixels at their respective outer edges, so the image is left unchanged.

---

### Instance 3

#### Input
```
5 6
......
......
...#..
......
......
```

#### Output
```
#
```

#### Explanation
The only black pixel is located at row 3, column 4. Everything else is white. Thus, cropping removes all other rows and columns, leaving only a $1 \times 1$ grid containing `#`.

---

### Instance 4

#### Input
```
2 2
.#
..
```

#### Output
```
#
```

#### Explanation
- The second row is entirely white, so it is removed.
- The first column of the remaining row is white, so it is removed.
- The resulting grid is a $1 \times 1$ grid containing only `#`.

---

### Instance 5

#### Input
```
1 1
#
```

#### Output
```
#
```

#### Explanation
The grid is already $1 \times 1$ and contains a black pixel. No cropping can be performed.