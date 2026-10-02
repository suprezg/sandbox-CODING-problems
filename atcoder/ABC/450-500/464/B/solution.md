# Optimal Solution

## Idea

The problem requires cropping an image represented as an $H \times W$ grid of pixels (`.` for white, `#` for black) by removing all outer border rows and columns that consist entirely of white pixels. At least one black pixel `#` is guaranteed to exist in the grid.

To optimize the cropping process and eliminate memory churn from repeated subgrid reallocations, we maintain **two tracker lists simultaneously**:
- `empty_rows`: stores the indices of outer rows that contain exclusively white pixels.
- `empty_columns`: stores the indices of outer columns that contain exclusively white pixels.

Whenever checking any cell $(r, c)$ across all four scanning phases or during final grid reconstruction, the algorithm **simultaneously evaluates both trackers**. A pixel is evaluated if and only if it belongs to the active subgrid:
$$r \notin \text{empty\_rows} \quad \text{AND} \quad c \notin \text{empty\_columns}$$

The four borders are analyzed sequentially:

1. **Top Border Scan**:
   Iterate $r$ from $0$ to $H - 1$ (skipping any $r \in \text{empty\_rows}$). Across active columns ($c \notin \text{empty\_columns}$):
   - If any cell `grid[r][c]` is `#`, break immediately.
   - If all active cells in row $r$ are `.`, append $r$ to `empty_rows`.

2. **Bottom Border Scan**:
   Iterate $r$ from $H - 1$ down to $0$ (skipping any $r \in \text{empty\_rows}$). Across active columns ($c \notin \text{empty\_columns}$):
   - If any active cell `grid[r][c]` is `#`, break immediately.
   - If all active cells in row $r$ are `.`, append $r$ to `empty_rows`.

3. **Left Border Scan**:
   Iterate column index $c$ from $0$ to $W - 1$ (skipping any $c \in \text{empty\_columns}$). Across active rows ($r \notin \text{empty\_rows}$):
   - If any active cell `grid[r][c]` is `#`, break immediately.
   - If all active cells in column $c$ are `.`, append $c$ to `empty_columns`.

4. **Right Border Scan**:
   Iterate column index $c$ from $W - 1$ down to $0$ (skipping any $c \in \text{empty\_columns}$). Across active rows ($r \notin \text{empty\_rows}$):
   - If any active cell `grid[r][c]` is `#`, break immediately.
   - If all active cells in column $c$ are `.`, append $c$ to `empty_columns`.

5. **Final Output Construction**:
   Iterate through rows $r \in [0, H - 1]$ and columns $c \in [0, W - 1]$:
   - Filter rows using `NOT CONTAINS(empty_rows, r)`.
   - Filter columns using `NOT CONTAINS(empty_columns, c)`.
   - Concatenate the remaining characters to form the cropped lines and return the final image.

## Pseudocode

### Solver

```
FUNCTION solve(grid):
    h = LENGTH(grid)
    w = LENGTH(grid[0])

    empty_rows = []
    empty_columns = []
    snapshots = []

    // 1. Top border scan (evaluating only active columns not in empty_columns)
    FOR r FROM 0 TO h - 1 DO
        IF CONTAINS(empty_rows, r) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR c FROM 0 TO w - 1 DO
            IF NOT CONTAINS(empty_columns, c) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND r TO empty_rows
        END IF
    END FOR

    // 2. Bottom border scan (evaluating only active columns not in empty_columns)
    FOR r FROM h - 1 DOWNTO 0 DO
        IF CONTAINS(empty_rows, r) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR c FROM 0 TO w - 1 DO
            IF NOT CONTAINS(empty_columns, c) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND r TO empty_rows
        END IF
    END FOR

    // 3. Left border scan (evaluating only active rows not in empty_rows)
    FOR c FROM 0 TO w - 1 DO
        IF CONTAINS(empty_columns, c) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR r FROM 0 TO h - 1 DO
            IF NOT CONTAINS(empty_rows, r) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND c TO empty_columns
        END IF
    END FOR

    // 4. Right border scan (evaluating only active rows not in empty_rows)
    FOR c FROM w - 1 DOWNTO 0 DO
        IF CONTAINS(empty_columns, c) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR r FROM 0 TO h - 1 DO
            IF NOT CONTAINS(empty_rows, r) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND c TO empty_columns
        END IF
    END FOR

    snapshot = (empty_rows, empty_columns)
    APPEND snapshot TO snapshots

    // 5. Build cropped grid considering both empty_rows and empty_columns simultaneously
    result_grid = []
    FOR r FROM 0 TO h - 1 DO
        IF NOT CONTAINS(empty_rows, r) THEN
            current_row = ""
            FOR c FROM 0 TO w - 1 DO
                IF NOT CONTAINS(empty_columns, c) THEN
                    current_row = current_row + grid[r][c]
                END IF
            END FOR
            APPEND current_row TO result_grid
        END IF
    END FOR

    RETURN (answer = result_grid, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(grid, answer, proof):
    IF LENGTH(proof) != 1 THEN
        RETURN FALSE
    END IF

    snapshot = proof[0]
    claimed_empty_rows = snapshot.empty_rows
    claimed_empty_columns = snapshot.empty_columns

    h = LENGTH(grid)
    w = LENGTH(grid[0])

    computed_empty_rows = []
    computed_empty_columns = []

    // Verify top border scan
    FOR r FROM 0 TO h - 1 DO
        IF CONTAINS(computed_empty_rows, r) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR c FROM 0 TO w - 1 DO
            IF NOT CONTAINS(computed_empty_columns, c) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND r TO computed_empty_rows
        END IF
    END FOR

    // Verify bottom border scan
    FOR r FROM h - 1 DOWNTO 0 DO
        IF CONTAINS(computed_empty_rows, r) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR c FROM 0 TO w - 1 DO
            IF NOT CONTAINS(computed_empty_columns, c) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND r TO computed_empty_rows
        END IF
    END FOR

    // Verify left border scan
    FOR c FROM 0 TO w - 1 DO
        IF CONTAINS(computed_empty_columns, c) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR r FROM 0 TO h - 1 DO
            IF NOT CONTAINS(computed_empty_rows, r) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND c TO computed_empty_columns
        END IF
    END FOR

    // Verify right border scan
    FOR c FROM w - 1 DOWNTO 0 DO
        IF CONTAINS(computed_empty_columns, c) THEN
            CONTINUE
        END IF

        has_black_pixel = FALSE
        FOR r FROM 0 TO h - 1 DO
            IF NOT CONTAINS(computed_empty_rows, r) THEN
                IF grid[r][c] == '#' THEN
                    has_black_pixel = TRUE
                    BREAK
                END IF
            END IF
        END FOR

        IF has_black_pixel THEN
            BREAK
        ELSE
            APPEND c TO computed_empty_columns
        END IF
    END FOR

    IF claimed_empty_rows != computed_empty_rows OR
       claimed_empty_columns != computed_empty_columns THEN
        RETURN FALSE
    END IF

    // Reconstruct cropped grid and compare with claimed answer
    computed_result = []
    FOR r FROM 0 TO h - 1 DO
        IF NOT CONTAINS(computed_empty_rows, r) THEN
            row_str = ""
            FOR c FROM 0 TO w - 1 DO
                IF NOT CONTAINS(computed_empty_columns, c) THEN
                    row_str = row_str + grid[r][c]
                END IF
            END FOR
            APPEND row_str TO computed_result
        END IF
    END FOR

    IF computed_result == answer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    Let $H$ and $W$ denote the height and width of the input grid ($1 \le H, W \le 50$).
    - During each of the four scans, any cell check $(r, c)$ simultaneously evaluates whether $r \in \text{empty\_rows}$ and $c \in \text{empty\_columns}$. Cells outside the active subgrid are skipped immediately.
    - Across all four scans, each active row and column is evaluated at most once until the first `#` is reached, leading to at most $4 \cdot (H \cdot W)$ total cell checks.
    - The final rendering phase traverses only the remaining active subgrid of dimensions $(H - |\text{empty\_rows}|) \times (W - |\text{empty\_columns}|) \le H \times W$.
    - The overall algorithm runs strictly in linear time relative to the number of grid pixels:

    $$T(H, W) = \mathcal{O}(H \cdot W)$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(H \cdot W)$$

2. Best Case Analysis

    In the best-case scenario, the outer border edges already contain `#` pixels on the top, bottom, leftmost, and rightmost boundaries. Each of the four scans terminates immediately on its very first row or column, performing at most $H + W$ operations:

    $$T(H, W) = H + W$$

    Using Asymptotic Approximation to establish the lower bound on time complexity yields:

    $$\Omega(H + W)$$

### Space Complexity

The algorithm stores only the tracker lists `empty_rows` (at most $H - 1$ entries) and `empty_columns` (at most $W - 1$ entries), along with scalar iteration indices. The original grid is inspected directly without intermediate subgrid copies.

The auxiliary memory performance function is $S(H, W) = H + W$. Using Asymptotic Approximation, approximating $S(H, W)$ yields an auxiliary space complexity of:

$$\mathcal{O}(H + W)$$

## Pros and Cons

### Pros

- **Simultaneous 2D Constraint Enforcement**: Evaluates both `empty_rows` and `empty_columns` concurrently in every phase, ensuring that operations always target the precise active subgrid.
- **Zero Memory Allocation Churn**: Preserves the original grid in-place without creating intermediate subgrids or performing repetitive string slicing.
- **Strict Linear Complexity**: Operates in $\mathcal{O}(H \cdot W)$ time and $\mathcal{O}(H + W)$ auxiliary space.
- **Early-Break Optimization**: Each row and column scan halts immediately upon encountering the first `#`, bypassing redundant inner cells.

### Cons

- **Sequential Scan Ordering**: Analyzes top, bottom, left, and right borders sequentially rather than computing coordinate bounding limits in a single matrix pass.
- **Membership Lookup Overhead**: Checking list membership (`CONTAINS(empty_rows, r)` and `CONTAINS(empty_columns, c)`) introduces minor linear scan overhead per step unless implemented using boolean direct-address lookup tables.
