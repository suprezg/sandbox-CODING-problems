# Optimal Solution

## Idea

The problem requires calculating the total square feet of wrapping paper needed to wrap $N$ rectangular presents. For each present, we parse its dimensions given in the format `lxwxh` to extract the integer values for length ($l$), width ($w$), and height ($h$).

To process each present:

1. Compute the three side areas: $A_1 = l \times w$, $A_2 = w \times h$, and $A_3 = h \times l$.
2. Determine the slack paper needed, which is the area of the smallest side given by $\min(A_1, A_2, A_3)$.
3. Compute the surface area plus slack as $2A_1 + 2A_2 + 2A_3 + \min(A_1, A_2, A_3)$.
4. Accumulate this value into a global running total `totalSquareFeet`.

After iterating through all $N$ presents, the algorithm returns `totalSquareFeet`.

## Pseudocode

### Solver

```
FUNCTION solve(presentsList):
    totalSquareFeet = 0

    snapshots = []

    FOR EACH present IN presentsList DO
        length, width, height = parseDimensions(present)

        area1 = length * width
        area2 = width * height
        area3 = height * length

        smallestSide = findMinimum(area1, area2, area3)

        presentPaper = (2 * area1) + (2 * area2) + (2 * area3) + smallestSide

        snapshot = (present, length, width, height, area1, area2, area3, smallestSide, presentPaper)
        APPEND snapshot to snapshots

        totalSquareFeet = totalSquareFeet + presentPaper
    END FOR

    RETURN (answer = totalSquareFeet, proof=snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(presentsList, answer, proof)
    claimedAnswer = answer
    expectedProofLength = LENGTH(presentsList)

    IF expectedProofLength != LENGTH(PROOF):
        RETURN FALSE

    computedAnswer = 0

    FOR index FROM 0 TO LENGTH(presentsList) - 1:
        snapshot = proof[index]

        present = presentsList[index]
        
        IF snapshot.present != present:
            RETURN FALSE
            
        IF snapshot.area1 != (snapshot.length * snapshot.width)  OR
           snapshot.area2 != (snapshot.width * snapshot.height)   OR
           snapshot.area3 != (snapshot.height * snapshot.length):
            RETURN FALSE
            
        IF snapshot.smallestSide > snapshot.area1 OR 
           snapshot.smallestSide > snapshot.area2 OR 
           snapshot.smallestSide > snapshot.area3:
            RETURN FALSE

        IF snapshot.smallestSide != snapshot.area1 AND 
           snapshot.smallestSide != snapshot.area2 AND 
           snapshot.smallestSide != snapshot.area3:
            RETURN FALSE
            
        computedPresentPaper = (2 * snapshot.area1) + (2 * snapshot.area2) + (2 * snapshot.area3) + snapshot.smallestSide
        IF snapshot.presentPaper != computedPresentPaper:
            RETURN FALSE
            
        computedAnswer = computedAnswer + snapshot.presentPaper

    IF computedAnswer == claimedAnswer:
        RETURN TRUE
    ELSE:
        RETURN FALSE
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    In the worst-case scenario, the algorithm must process each of the $N$ presents in the input list sequentially. Parsing each string and performing fixed arithmetic operations takes constant time per present.

    The exact total number of operations performed across all input presents is defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N)$$

2. Best Case Analysis

    In the best-case scenario, every present string still requires complete parsing and evaluation to compute its required surface area and slack. No computation can be bypassed regardless of the dimension values.

    The exact total number of operations remains constant per element, defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the lower bound on time complexity yields:

    $$\Omega(N)$$

### Space Complexity

To store the input list of $N$ dimension strings, the system uses memory directly proportional to $N$. Furthermore, processing each string requires a constant amount of auxiliary variables for calculations (`totalSquareFeet`, `l`, `w`, `h`, `area1`, `area2`, `area3`, and `smallestSide`).

The memory performance function is $S(N) = N + 1$. Using Asymptotic Approximation, approximating $S(N)$ yields a space complexity of:

$$\mathcal{O}(N)$$

## Pros and Cons

### Pros

- **Optimal Time Complexity**: Evaluates each present in constant time $\mathcal{O}(1)$, leading to a linear overall runtime of $\mathcal{O}(N)$.
- **Simple Implementation**: Directly translates the mathematical formula provided in the problem statement into scalar arithmetic steps.
- **Accuracy**: Ensures correct calculation of slack paper by using the minimum of the three calculated side areas.

### Cons

- **String Parsing Overhead**: Relying on string splitting or parsing for every present introduces slight string processing overhead compared to raw numerical inputs.
- **Memory Usage for Input**: Storing all $N$ input strings in memory requires linear space $\mathcal{O}(N)$ prior to processing.