# Optimal Solution

## Idea

The problem requires classifying a list of $N$ strings as either **nice** or **naughty** and returning the total count of **nice** strings. A string is classified as **nice** if and only if it satisfies three specific criteria simultaneously:
1. **Condition 1 (Vowel Count)**: Contains at least three vowels from the set $\{ \text{`a'}, \text{`e'}, \text{`i'}, \text{`o'}, \text{`u'} \}$.
2. **Condition 2 (Double Letter)**: Contains at least one letter that appears twice in a row (e.g., `xx`, `dd`).
3. **Condition 3 (Forbidden Substrings)**: Does **not** contain any of the two-character substrings: `ab`, `cd`, `pq`, or `xy`.

To process each string efficiently with minimal operations, the algorithm iterates through each string in chunked steps of size 2 (reducing loop iterations to $\lceil |S| / 2 \rceil$ per string) while maintaining a reference to the previous character `prevCharacter` to bridge adjacent characters across consecutive chunks:

1. Initialize two counters: `nice = 0` and `naughty = 0`.
2. For each string `currentString` in the input list:
   - Initialize tracking variables: `conditionOne = 0` (integer count of vowels), `conditionTwo = FALSE` (boolean flag for duplicate consecutive characters), `conditionThree = FALSE` (boolean flag indicating if a forbidden substring is detected), and `prevCharacter = ""`.
   - Compute `totalSteps = CEIL(stringLength / 2)` and iterate with step index `stepIndex` from $0$ to `totalSteps - 1`:
     - Extract `firstChar = currentString[2 * stepIndex]`.
     - Extract `secondChar = currentString[2 * stepIndex + 1]` if within string bounds, else `""`.
     - **Main Condition 1 (Vowel Tracking)**: If `conditionOne < 3`, inspect `firstChar` and `secondChar`. Increment `conditionOne` by $1$ for each character that is a vowel.
     - **Main Condition 2 (Double Letter Tracking)**: If `conditionTwo == FALSE`, check if `firstChar == secondChar` (within the current pair) or if `prevCharacter == firstChar` (across the chunk boundary). If either condition holds, set `conditionTwo = TRUE`.
     - **Main Condition 3 (Forbidden Substrings Tracking & Early Exit)**: If `conditionThree == FALSE`, check if `firstChar + secondChar` or `prevCharacter + firstChar` matches any forbidden substring (`ab`, `cd`, `pq`, `xy`). If a match occurs, set `conditionThree = TRUE` and immediately **break** the inner loop, as the presence of any forbidden substring definitively classifies the string as naughty without needing further character evaluations.
     - Update `prevCharacter` to `secondChar` (or `firstChar` if `secondChar` is empty) for the next iteration.
   - After completing or breaking out of the string traversal, evaluate the final state:
     - If `conditionOne >= 3`, `conditionTwo == TRUE`, and `conditionThree == FALSE`, classify the string as **nice** and increment `nice` by $1$.
     - Otherwise, classify the string as **naughty** and increment `naughty` by $1$.
3. Return `nice` as the final count of valid strings.

## Pseudocode

### Helper Functions

```
FUNCTION isVowel(ch):
    RETURN (ch == 'a' OR ch == 'e' OR ch == 'i' OR ch == 'o' OR ch == 'u')
END FUNCTION

FUNCTION isForbidden(pair):
    RETURN (pair == "ab" OR pair == "cd" OR pair == "pq" OR pair == "xy")
END FUNCTION
```

### Solver

```
FUNCTION solve(stringsList):
    nice = 0
    naughty = 0
    snapshots = []

    FOR EACH currentString IN stringsList DO
        stringLength = LENGTH(currentString)
        conditionOne = 0
        conditionTwo = FALSE
        conditionThree = FALSE
        prevCharacter = ""

        totalSteps = CEIL(stringLength / 2)

        FOR stepIndex FROM 0 TO totalSteps - 1 DO
            firstIndex = 2 * stepIndex
            firstChar = currentString[firstIndex]

            secondChar = ""
            IF firstIndex + 1 < stringLength THEN
                secondChar = currentString[firstIndex + 1]
            END IF

            // Main Condition 1: Vowel count check
            IF conditionOne < 3 THEN
                IF isVowel(firstChar) THEN
                    conditionOne = conditionOne + 1
                END IF
                IF secondChar != "" AND isVowel(secondChar) THEN
                    conditionOne = conditionOne + 1
                END IF
            END IF

            // Main Condition 2: Consecutive duplicate letter check
            IF conditionTwo == FALSE THEN
                IF secondChar != "" AND firstChar == secondChar THEN
                    conditionTwo = TRUE
                ELSE IF prevCharacter != "" AND prevCharacter == firstChar THEN
                    conditionTwo = TRUE
                END IF
            END IF

            // Main Condition 3: Forbidden substring check with early break
            IF conditionThree == FALSE THEN
                IF secondChar != "" AND isForbidden(firstChar + secondChar) THEN
                    conditionThree = TRUE
                    BREAK
                ELSE IF prevCharacter != "" AND isForbidden(prevCharacter + firstChar) THEN
                    conditionThree = TRUE
                    BREAK
                END IF
            END IF

            // Update boundary character for next chunk
            IF secondChar != "" THEN
                prevCharacter = secondChar
            ELSE
                prevCharacter = firstChar
            END IF
        END FOR

        isNice = FALSE
        IF conditionOne >= 3 AND conditionTwo == TRUE AND conditionThree == FALSE THEN
            nice = nice + 1
            isNice = TRUE
        ELSE
            naughty = naughty + 1
        END IF

        snapshot = (currentString, conditionOne, conditionTwo, conditionThree, isNice, nice, naughty)
        APPEND snapshot TO snapshots
    END FOR

    RETURN (answer = nice, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(stringsList, answer, proof):
    claimedAnswer = answer
    expectedProofLength = LENGTH(stringsList)

    IF LENGTH(proof) != expectedProofLength THEN
        RETURN FALSE
    END IF

    computedNice = 0
    computedNaughty = 0

    FOR index FROM 0 TO expectedProofLength - 1 DO
        snapshot = proof[index]
        currentString = stringsList[index]
        stringLength = LENGTH(currentString)

        IF snapshot.currentString != currentString THEN
            RETURN FALSE
        END IF

        expectedConditionOne = 0
        expectedConditionTwo = FALSE
        expectedConditionThree = FALSE
        prevChar = ""

        totalSteps = CEIL(stringLength / 2)

        FOR stepIndex FROM 0 TO totalSteps - 1 DO
            firstIndex = 2 * stepIndex
            firstChar = currentString[firstIndex]

            secondChar = ""
            IF firstIndex + 1 < stringLength THEN
                secondChar = currentString[firstIndex + 1]
            END IF

            IF expectedConditionOne < 3 THEN
                IF isVowel(firstChar) THEN
                    expectedConditionOne = expectedConditionOne + 1
                END IF
                IF secondChar != "" AND isVowel(secondChar) THEN
                    expectedConditionOne = expectedConditionOne + 1
                END IF
            END IF

            IF expectedConditionTwo == FALSE THEN
                IF secondChar != "" AND firstChar == secondChar THEN
                    expectedConditionTwo = TRUE
                ELSE IF prevChar != "" AND prevChar == firstChar THEN
                    expectedConditionTwo = TRUE
                END IF
            END IF

            IF expectedConditionThree == FALSE THEN
                IF secondChar != "" AND isForbidden(firstChar + secondChar) THEN
                    expectedConditionThree = TRUE
                    BREAK
                ELSE IF prevChar != "" AND isForbidden(prevChar + firstChar) THEN
                    expectedConditionThree = TRUE
                    BREAK
                END IF
            END IF

            IF secondChar != "" THEN
                prevChar = secondChar
            ELSE
                prevChar = firstChar
            END IF
        END FOR

        IF snapshot.conditionOne != expectedConditionOne OR
           snapshot.conditionTwo != expectedConditionTwo OR
           snapshot.conditionThree != expectedConditionThree THEN
            RETURN FALSE
        END IF

        expectedIsNice = (expectedConditionOne >= 3 AND expectedConditionTwo == TRUE AND expectedConditionThree == FALSE)
        IF snapshot.isNice != expectedIsNice THEN
            RETURN FALSE
        END IF

        IF expectedIsNice THEN
            computedNice = computedNice + 1
        ELSE
            computedNaughty = computedNaughty + 1
        END IF

        IF snapshot.nice != computedNice OR snapshot.naughty != computedNaughty THEN
            RETURN FALSE
        END IF
    END FOR

    IF computedNice == claimedAnswer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    In the worst-case scenario, the algorithm must process all characters of every string $S_i$ (e.g. when strings are nice or contain no forbidden substrings, or when a forbidden substring appears in the final chunk). For each string $S_i$ of length $|S_i|$, the algorithm performs at most $\lceil |S_i| / 2 \rceil$ chunk iterations. Within each iteration, fixed character comparisons, vowel lookups, and pair matching take $\mathcal{O}(1)$ constant time.

    The total number of operations performed across all input strings is defined by the Performance Function:

    $$T(N, M) = \sum_{i=1}^{N} \left\lceil \frac{|S_i|}{2} \right\rceil \le N \cdot \left\lceil \frac{M}{2} \right\rceil$$

    where $M = \max_{1 \le i \le N} |S_i|$ is the maximum string length. Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N \cdot M)$$

2. Best Case Analysis

    In the best-case scenario, every input string contains a forbidden substring within its initial character chunk (at `stepIndex = 0`). Because detecting a forbidden substring immediately sets `conditionThree = TRUE` and breaks out of the inner loop, each string requires only $\mathcal{O}(1)$ operations.

    The total number of operations across all $N$ strings in the best-case scenario is defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the lower bound on time complexity yields:

    $$\Omega(N)$$

### Space Complexity

Processing each string requires only a constant number of scalar tracking variables (`conditionOne`, `conditionTwo`, `conditionThree`, `firstChar`, `secondChar`, `prevCharacter`, `nice`, and `naughty`). Storing the input list requires memory proportional to the total character count $\sum_{i=1}^N |S_i|$.

The auxiliary memory performance function is $S(N, M) = 1$. Using Asymptotic Approximation, approximating $S(N, M)$ yields an auxiliary space complexity of:

$$\mathcal{O}(1)$$

## Pros and Cons

### Pros

- **Early Termination on Forbidden Substrings**: Immediately halts the inner loop (`BREAK`) upon detecting a forbidden substring, skipping all subsequent character evaluations for naughty strings and optimizing runtime.
- **Reduced Loop Overhead**: Processing 2 characters per iteration halves the maximum number of loop cycles to $\lceil |S| / 2 \rceil$ while fully inspecting all characters.
- **Complete Boundary Coverage**: Tracking `prevCharacter` guarantees that transitions across 2-character chunk boundaries (`prevCharacter + firstChar`) are evaluated without missing adjacent duplicates or forbidden substrings.
- **Early-Condition Shielding**: Outer guards (`conditionOne < 3`, `conditionTwo == FALSE`, `conditionThree == FALSE`) skip redundant boolean checks once a condition is already satisfied or flagged.
- **Minimal Auxiliary Space**: Requires only $\mathcal{O}(1)$ auxiliary memory without allocating additional data structures or dynamic collections.

### Cons

- **Conditional Branch Complexity**: Utilizing nested conditionals for pairs within chunks and across chunk boundaries introduces branch evaluation overhead inside the inner loop.
- **Sequential String Parsing**: Evaluates strings one after another without concurrent multi-threading or SIMD vectorization.
