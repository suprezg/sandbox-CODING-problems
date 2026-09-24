# Optimal Solution

## Idea

The problem requires tracking the on/off states of $1,000,000$ lights arranged in a $1000 \times 1000$ grid (with coordinates $(X, Y) \in [0, 999]^2$) across a sequence of $N$ instructions. All lights start in the **off** state. Each instruction specifies an operation (`turn on`, `turn off`, or `toggle`) over an inclusive rectangular coordinate range $[X_1, X_2] \times [Y_1, Y_2]$.

This can be modeled mathematically using **Set Theory**, where the set of lit lights is represented as a dynamic set `mainSet` of unique coordinate identifiers:
1. **Coordinate Hashing (Cantor Pairing Function)**:
   To represent 2D coordinates $(X, Y)$ as unique scalar IDs with zero collisions, we employ Cantor's pairing function bijection $\pi: \mathbb{N}_0 \times \mathbb{N}_0 \to \mathbb{N}_0$:
   $$\text{ID}(X, Y) = \frac{(X + Y)(X + Y + 1)}{2} + Y$$
   For a grid with coordinates up to $999$, the maximum ID generated is $\frac{(999 + 999)(999 + 999 + 1)}{2} + 999 = 1,998,000$, which comfortably fits into standard integer types.

2. **Instruction Mapping via Set-Theoretic Operations**:
   For each instruction, a temporary set `tempSet` is populated with the Cantor IDs of all coordinates in the rectangular region $[X_1, X_2] \times [Y_1, Y_2]$. We then update `mainSet` using algebraic set operations:
   - **`turn on` $\implies$ Union ($A \cup B$)**:
     $$\text{MainSet} \gets \text{MainSet} \cup \text{TempSet}$$
     Adds all lights in the rectangle to the lit set.
   - **`turn off` $\implies$ Set Difference ($A \setminus B$)**:
     $$\text{MainSet} \gets \text{MainSet} \setminus \text{TempSet}$$
     Removes all lights in the rectangle from the lit set.
   - **`toggle` $\implies$ Symmetric Difference ($A \Delta B$)**:
     $$\text{MainSet} \gets (\text{MainSet} \cup \text{TempSet}) \setminus (\text{MainSet} \cap \text{TempSet})$$
     Inverts the state of every light in the rectangle: lights currently ON turn OFF, and lights currently OFF turn ON.

3. **Counting Lit Lights**:
   After evaluating all $N$ instructions sequentially, the total number of lit lights is simply the cardinality of the final set, $|\text{mainSet}|$.

## Pseudocode

### Helper Functions

```
FUNCTION cantorPairing(x, y):
    RETURN (((x + y) * (x + y + 1)) / 2) + y
END FUNCTION

FUNCTION generateGridSet(x1, y1, x2, y2):
    gridSet = SET()
    FOR x FROM x1 TO x2 DO
        FOR y FROM y1 TO y2 DO
            coordId = cantorPairing(x, y)
            ADD coordId TO gridSet
        END FOR
    END FOR
    RETURN gridSet
END FUNCTION

FUNCTION decodeInstruction(instructionString):
    // Parse instructionString into action and bounding coordinates
    IF STARTS_WITH(instructionString, "turn on") THEN
        action = "TURN_ON"
        parts = EXTRACT_COORDINATES(instructionString) // returns x1, y1, x2, y2
    ELSE IF STARTS_WITH(instructionString, "turn off") THEN
        action = "TURN_OFF"
        parts = EXTRACT_COORDINATES(instructionString)
    ELSE IF STARTS_WITH(instructionString, "toggle") THEN
        action = "TOGGLE"
        parts = EXTRACT_COORDINATES(instructionString)
    END IF
    RETURN (action, parts.x1, parts.y1, parts.x2, parts.y2)
END FUNCTION

FUNCTION setUnion(setA, setB):
    result = COPY(setA)
    FOR EACH element IN setB DO
        ADD element TO result
    END FOR
    RETURN result
END FUNCTION

FUNCTION setIntersection(setA, setB):
    result = SET()
    FOR EACH element IN setA DO
        IF CONTAINS(setB, element) THEN
            ADD element TO result
        END IF
    END FOR
    RETURN result
END FUNCTION

FUNCTION setDifference(setA, setB):
    result = SET()
    FOR EACH element IN setA DO
        IF NOT CONTAINS(setB, element) THEN
            ADD element TO result
        END IF
    END FOR
    RETURN result
END FUNCTION

FUNCTION setSymmetricDifference(setA, setB):
    unionSet = setUnion(setA, setB)
    intersectionSet = setIntersection(setA, setB)
    result = setDifference(unionSet, intersectionSet)
    RETURN result
END FUNCTION
```

### Solver

```
FUNCTION solve(instructionsList):
    mainSet = SET()
    snapshots = []

    FOR index FROM 0 TO LENGTH(instructionsList) - 1 DO
        instructionString = instructionsList[index]
        (action, x1, y1, x2, y2) = decodeInstruction(instructionString)
        tempSet = generateGridSet(x1, y1, x2, y2)

        oldMainSetSize = LENGTH(mainSet)

        IF action == "TURN_ON" THEN
            mainSet = setUnion(mainSet, tempSet)
        ELSE IF action == "TURN_OFF" THEN
            mainSet = setDifference(mainSet, tempSet)
        ELSE IF action == "TOGGLE" THEN
            mainSet = setSymmetricDifference(mainSet, tempSet)
        END IF

        newMainSetSize = LENGTH(mainSet)
        snapshot = (index, instructionString, action, x1, y1, x2, y2, LENGTH(tempSet), oldMainSetSize, newMainSetSize)
        APPEND snapshot TO snapshots
    END FOR

    RETURN (answer = LENGTH(mainSet), proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(instructionsList, answer, proof):
    claimedAnswer = answer
    expectedProofLength = LENGTH(instructionsList)

    IF LENGTH(proof) != expectedProofLength THEN
        RETURN FALSE
    END IF

    verifierMainSet = SET()

    FOR index FROM 0 TO expectedProofLength - 1 DO
        snapshot = proof[index]
        instructionString = instructionsList[index]

        IF snapshot.instructionString != instructionString THEN
            RETURN FALSE
        END IF

        (expectedAction, expectedX1, expectedY1, expectedX2, expectedY2) = decodeInstruction(instructionString)
        IF snapshot.action != expectedAction OR 
           snapshot.x1 != expectedX1 OR snapshot.y1 != expectedY1 OR 
           snapshot.x2 != expectedX2 OR snapshot.y2 != expectedY2 THEN
            RETURN FALSE
        END IF

        expectedTempSet = generateGridSet(expectedX1, expectedY1, expectedX2, expectedY2)
        IF snapshot.tempSetSize != LENGTH(expectedTempSet) THEN
            RETURN FALSE
        END IF

        IF snapshot.oldMainSetSize != LENGTH(verifierMainSet) THEN
            RETURN FALSE
        END IF

        IF expectedAction == "TURN_ON" THEN
            verifierMainSet = setUnion(verifierMainSet, expectedTempSet)
        ELSE IF expectedAction == "TURN_OFF" THEN
            verifierMainSet = setDifference(verifierMainSet, expectedTempSet)
        ELSE IF expectedAction == "TOGGLE" THEN
            verifierMainSet = setSymmetricDifference(verifierMainSet, expectedTempSet)
        END IF

        IF snapshot.newMainSetSize != LENGTH(verifierMainSet) THEN
            RETURN FALSE
        END IF
    END FOR

    IF LENGTH(verifierMainSet) == claimedAnswer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    Let $N$ denote the total number of instructions, and let $K = 1,000,000$ denote the total number of lights in the $1000 \times 1000$ grid. For instruction $i$ targeting a subgrid of dimensions $W_i \times H_i$ (where $W_i = X_2 - X_1 + 1$ and $H_i = Y_2 - Y_1 + 1$), generating `tempSet` requires $R_i = W_i \cdot H_i$ Cantor hash computations and set insertions ($\mathcal{O}(R_i)$).

    Performing the set operations (`setUnion`, `setDifference`, `setIntersection`, `setSymmetricDifference`) processes elements in $\mathcal{O}(|\text{mainSet}| + |\text{tempSet}|) \le \mathcal{O}(K)$ operations per instruction.

    The total number of operations across all $N$ instructions is defined by the Performance Function:

    $$T(N, K) = \sum_{i=1}^{N} \mathcal{O}(R_i + K) \le N \cdot \mathcal{O}(K)$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N \cdot K)$$

2. Best Case Analysis

    In the best-case scenario, the instructions target minimal $1 \times 1$ regions ($R_i = 1$) and `mainSet` remains near empty ($\emptyset$). However, every instruction must still be decoded, its grid set generated, and set operations evaluated.

    The total number of operations performed across all $N$ instructions is defined by the Performance Function:

    $$T(N) = \sum_{i=1}^{N} R_i$$

    Using Asymptotic Approximation to determine the lower bound on time complexity yields:

    $$\Omega(N)$$

### Space Complexity

The algorithm stores `mainSet`, which contains at most $K = 1,000,000$ unique Cantor coordinate IDs representing lit lights. In each iteration, `tempSet` stores at most $K$ IDs for the target rectangular area. Temporary intermediate sets for union and intersection also scale with at most $K$ elements.

The memory performance function is $S(K) = \mathcal{O}(K)$. Using Asymptotic Approximation, approximating $S(K)$ yields a space complexity of:

$$\mathcal{O}(K)$$

where $K = 1,000,000$ for a $1000 \times 1000$ grid.

## Pros and Cons

### Pros

- **Mathematical Rigor**: Formulates the problem cleanly using foundational set theory (union, difference, symmetric difference) and bijection theory (Cantor pairing function).
- **Collision-Free Coordinate IDs**: Cantor's pairing function maps every 2D coordinate $(X, Y) \in \mathbb{N}_0^2$ to a unique 1D scalar integer without hash collisions.
- **Explicit Set State**: At any instruction boundary, `mainSet` directly contains exactly the unique IDs of all currently lit lights.
- **High Modularity**: Breaks down complex range toggling and state flipping into reusable, independent algebraic set utilities.

### Cons

- **Dynamic Set Allocation Overhead**: Constructing dynamic hash sets and allocating intermediate sets for union and symmetric difference operations introduces heap allocation and hashing overhead per instruction compared to direct in-place 2D array indexing or 1D bit manipulation.
- **Intermediate Set Copies**: Evaluating $(A \cup B) \setminus (A \cap B)$ creates multiple intermediate sets per toggle command, increasing transient memory churn.
