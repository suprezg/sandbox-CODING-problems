# Optimal Solution

## Idea

The problem requires calculating the number of unique houses that receive at least one present from Santa as he moves across an infinite two-dimensional Cartesian grid. Santa starts at coordinate $(0, 0)$ and delivers a present, then follows a sequence of $N$ directional movement instructions represented by characters in a string $S$ of length $N$:
* `^` instructs Santa to move North ($(x, y) \to (x, y + 1)$)
* `v` instructs Santa to move South ($(x, y) \to (x, y - 1)$)
* `>` instructs Santa to move East ($(x, y) \to (x + 1, y)$)
* `<` instructs Santa to move West ($(x, y) \to (x - 1, y)$)

Rather than relying on a standard Set data structure, the solution tracks visited houses using a `Map` where key-value pairs represent `(hashCode, visitCount)`. To map signed infinite grid coordinates $(x, y) \in \mathbb{Z}^2$ to unique non-negative integer hash codes, the algorithm uses two mathematical transformations:

1. **Sign Mapping (`negativeToPositive`)**: 
   Transforms signed integers $z \in \mathbb{Z}$ into non-negative integers $z' \in \mathbb{N}_0$ using Zigzag encoding:
   * If $z \ge 0$: $z' = 2z$
   * If $z < 0$: $z' = -2z - 1$
   This function takes $x$ and $y$ as references, processes each coordinate with an `if-else` check, appends the transformed values to a tuple, and returns `(nonNegativeX, nonNegativeY)`.

2. **Spatial Hashing (`hashIt`)**:
   Maps a pair of non-negative integers $(X, Y) \in \mathbb{N}_0^2$ to a unique 1D scalar integer using Szudzik's pairing function:
   * If $X < Y$: $\text{hashCode} = Y^2 + X$
   * If $X \ge Y$: $\text{hashCode} = X^2 + X + Y$

3. **Journey Simulation & Visit Counting**:
   * Initialize `uniqHouse = 0`, $x = 0$, $y = 0$, and an empty `visitedMap`.
   * Iterate through each position of Santa's journey (starting at index $0$ for $(0, 0)$ prior to processing each movement instruction in $S$):
     - **Task 1 (Map Lookup & House Counting)**: Deconstruct `(nonNegativeX, nonNegativeY) = negativeToPositive(x, y)` and compute `hashCode = hashIt(nonNegativeX, nonNegativeY)`. Peek into `visitedMap` at key `hashCode`:
       * If `hashCode` is not present: assign `visitedMap[hashCode] = 1` and increment `uniqHouse` by $1$.
       * If `hashCode` is already present: increment `visitedMap[hashCode]` by $1$ without incrementing `uniqHouse`.
     - **Task 2 (Instruction Evaluation)**: Read character $S[\text{index}]$ and update $(x, y)$ accordingly:
       * `^` $\implies y \gets y + 1$
       * `v` $\implies y \gets y - 1$
       * `>` $\implies x \gets x + 1$
       * `<` $\implies x \gets x - 1$
   * Return `uniqHouse` after all instructions in string $S$ are processed.

## Pseudocode

### Helper Functions

```
FUNCTION negativeToPositive(x, y):
    tuple = []

    IF x >= 0 THEN
        APPEND (x * 2) TO tuple
    ELSE
        APPEND ((-2 * x) - 1) TO tuple
    END IF

    IF y >= 0 THEN
        APPEND (y * 2) TO tuple
    ELSE
        APPEND ((-2 * y) - 1) TO tuple
    END IF

    RETURN tuple
END FUNCTION

FUNCTION hashIt(x, y):
    IF x < y THEN
        RETURN (y * y) + x
    ELSE
        RETURN (x * x) + x + y
    END IF
END FUNCTION
```

### Solver

```
FUNCTION solve(S):
    stringLength = LENGTH(S)
    uniqHouse = 0
    x = 0
    y = 0

    visitedMap = MAP()
    snapshots = []

    FOR index FROM 0 TO stringLength DO
        (nonNegativeX, nonNegativeY) = negativeToPositive(x, y)
        hashCode = hashIt(nonNegativeX, nonNegativeY)

        isNewHouse = FALSE
        IF NOT CONTAINS_KEY(visitedMap, hashCode) THEN
            visitedMap[hashCode] = 1
            uniqHouse = uniqHouse + 1
            isNewHouse = TRUE
        ELSE
            visitedMap[hashCode] = visitedMap[hashCode] + 1
        END IF

        snapshot = (index, x, y, nonNegativeX, nonNegativeY, hashCode, visitedMap[hashCode], isNewHouse, uniqHouse)
        APPEND snapshot TO snapshots

        IF index < stringLength THEN
            direction = S[index]
            IF direction == '^' THEN
                y = y + 1
            ELSE IF direction == 'v' THEN
                y = y - 1
            ELSE IF direction == '>' THEN
                x = x + 1
            ELSE IF direction == '<' THEN
                x = x - 1
            END IF
        END IF
    END FOR

    RETURN (answer = uniqHouse, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(S, answer, proof):
    stringLength = LENGTH(S)
    expectedProofLength = stringLength + 1

    IF LENGTH(proof) != expectedProofLength THEN
        RETURN FALSE
    END IF

    claimedAnswer = answer
    computedUniqHouse = 0
    verifierMap = MAP()
    computedX = 0
    computedY = 0

    FOR index FROM 0 TO expectedProofLength - 1 DO
        snapshot = proof[index]

        IF snapshot.x != computedX OR snapshot.y != computedY THEN
            RETURN FALSE
        END IF

        (expectedNonNegX, expectedNonNegY) = negativeToPositive(computedX, computedY)
        IF snapshot.nonNegativeX != expectedNonNegX OR snapshot.nonNegativeY != expectedNonNegY THEN
            RETURN FALSE
        END IF

        expectedHashCode = hashIt(expectedNonNegX, expectedNonNegY)
        IF snapshot.hashCode != expectedHashCode THEN
            RETURN FALSE
        END IF

        IF NOT CONTAINS_KEY(verifierMap, expectedHashCode) THEN
            verifierMap[expectedHashCode] = 1
            computedUniqHouse = computedUniqHouse + 1
            IF snapshot.isNewHouse != TRUE THEN
                RETURN FALSE
            END IF
        ELSE
            verifierMap[expectedHashCode] = verifierMap[expectedHashCode] + 1
            IF snapshot.isNewHouse != FALSE THEN
                RETURN FALSE
            END IF
        END IF

        IF snapshot.visitedCount != verifierMap[expectedHashCode] OR snapshot.uniqHouse != computedUniqHouse THEN
            RETURN FALSE
        END IF

        IF index < stringLength THEN
            direction = S[index]
            IF direction == '^' THEN
                computedY = computedY + 1
            ELSE IF direction == 'v' THEN
                computedY = computedY - 1
            ELSE IF direction == '>' THEN
                computedX = computedX + 1
            ELSE IF direction == '<' THEN
                computedX = computedX - 1
            END IF
        END IF
    END FOR

    IF computedUniqHouse == claimedAnswer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    In the worst-case scenario, Santa evaluates $N + 1$ grid locations across $N$ movement instructions. Evaluating each location involves mapping signed coordinates to non-negative coordinates via Zigzag encoding, computing the unique Szudzik hash, and looking up or updating key-value pairs in the map, all of which execute in $\mathcal{O}(1)$ average time.

    The total number of operations performed across Santa's journey is defined by the Performance Function:

    $$T(N) = N + 1$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N)$$

2. Best Case Analysis

    In the best-case scenario, even if Santa repeatedly revisits previously explored houses (e.g. moving back and forth between two houses), every movement instruction in string $S$ must still be read, hashed, and looked up in the map. No movement instruction can be bypassed.

    The total number of operations remains unchanged, defined by the Performance Function:

    $$T(N) = N + 1$$

    Using Asymptotic Approximation to determine the lower bound on time complexity yields:

    $$\Omega(N)$$

### Space Complexity

The map stores an entry for every unique house visited. In the worst case where every move leads to a new unvisited location, the map contains $N + 1$ unique key-value pairs. Storing auxiliary scalar variables (`uniqHouse`, `x`, `y`, `nonNegativeX`, `nonNegativeY`, `hashCode`) requires constant space.

The memory performance function is $S(N) = N + 1$. Using Asymptotic Approximation, approximating $S(N)$ yields a space complexity of:

$$\mathcal{O}(N)$$

## Pros and Cons

### Pros

- **Collision-Free Custom Hash**: Combining Zigzag encoding with Szudzik's pairing function maps any 2D integer grid coordinate $(x, y) \in \mathbb{Z}^2$ to a unique 1D non-negative scalar integer without relying on string serialization or set data structures.
- **Optimal Linear Time**: Processes all $N$ instructions in $\mathcal{O}(N)$ overall time, easily completing within performance limits for $|S| \le 10^5$.
- **Explicit Visit Frequency Tracking**: Uses a map of `(hashCode, visitCount)` rather than a simple set, allowing full tracking of how many presents each house receives.
- **Exact Grid Simulation**: Accurately handles Santa's initial present drop at $(0, 0)$ alongside subsequent move updates.

### Cons

- **Map Hash Overhead**: Relies on hash map lookups which carry constant factor overhead compared to direct array access.
- **Memory Consumption**: Storing entries for up to $N + 1$ unique coordinates requires linear auxiliary space $\mathcal{O}(N)$.
- **Scalar Integer Growth**: Hashing extreme coordinates on very long paths leads to quadratic growth of the hash value ($Y^2 + X$ or $X^2 + X + Y$), requiring integer types capable of holding large values.
