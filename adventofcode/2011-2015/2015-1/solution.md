# Optimal Solution

## Idea

The problem requires calculating Santa's final floor level starting from floor $0$ by evaluating a sequence of instructions represented by parentheses in a string $S$ of length $N$. Each opening parenthesis `(` increments the floor level by $+1$, while each closing parenthesis `)` decrements it by $-1$.

To process the string efficiently, a two-pointer technique is utilized:

1. Initialize a variable `counter` to $0$ to keep track of the cumulative floor level.
2. Initialize two pointers: `left` at index $0$ (the start of the string) and `right` at index $N - 1$ (the end of the string).
3. Calculate the required number of loop iterations as $\lceil N / 2 \rceil$. This guarantees that both pointers meet at the center without missing any characters.
4. During each iteration:
    - Check the character at index `left`. If it is `(`, increment `counter` by $1$; if `)`, decrement `counter` by $1$.
    - Check whether `left` and `right` point to distinct indices (`left` $\ne$ `right`). If they are distinct, evaluate the character at index `right` in the same manner.
    - If `left` and `right` point to the exact same index (`left` $=$ `right`), which occurs on the final iteration of an odd-length string, skip evaluating `right` to avoid duplicate processing.
    - Increment `left` by $1$ and decrement `right` by $1$.
5. Return `counter` as the final floor number after all iterations complete.

## Pseudocode

### Solver

```
FUNCTION solve(S):
    stringLength = LENGTH(S)
    floorLevel = 0
    leftPointer = 0
    rightPointer = N - 1
    totalIterations = CEIL(stringLength / 2)

    snapshots = []

    FOR index FROM 1 TO totalIterations:

        oldFloorLevel=floorLevel

        IF S[leftPointer] == '(':
            floorLevel = floorLevel + 1
        ELSE IF S[leftPointer] == ')':
            floorLevel = floorLevel - 1
        
        IF S[rightPointer] == '(':
		        floorLevel = floorLevel + 1
        ELSE IF S[rightPointer] == ')':
		        floorLevel = floorLevel - 1

        IF leftPointer == rightPointer:
            IF S[rightPointer] == '(':
                floorLevel = floorLevel + 1
            ELSE IF S[rightPointer] == ')':
                floorLevel = floorLevel - 1

        changeInFloor = oldFloorLevel - FloorLevel
        snapshot = (index, leftPointer, rightPointer, changeInFloor)
        APPEND snapshot TO snapshots

        leftPointer = leftPointer + 1
        rightPointer = rightPointer - 1

    RETURN (answer=floorLevel, proof=snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(S, answer, proof):
    stringLength = LENGTH(S)
    expectedProofLength = CEIL(stringLength / 2)
    
    IF LENGTH(proof) != expectedProofLength:
        RETURN FALSE
    
    claimedAnswer = answer
    computedAnswer = 0

    FOR index FROM 0 TO expectedProofLength - 1:

        snapshot = proof[index]
        claimedLeftPointer  = snapshot.leftPointer
        claimedRightPointer = snapshot.rightPointer
        claimedChangeInFloor = snapshot.changeInFloor
        
        IF claimedLeftPointer != index OR claimedRightPointer != (N - 1 - index):
            RETURN FALSE

        computedChangeInFloor = 0
        
        IF S[claimedLeftPointer] == '(':
            computedChangeInFloor = computedChangeInFloor + 1
        ELSE IF S[claimedLeftPointer] == ')':
            computedChangeInFloor = computedChangeInFloor - 1

        IF S[claimedRightPointer] == '(':
            computedChangeInFloor = computedChangeInFloor + 1
        ELSE IF S[claimedRightPointer] == ')':
            computedChangeInFloor = computedChangeInFloor - 1
            
        IF claimedLeftPointer == claimedRightPointer:
            IF S[claimedLeftPointer] == '(':
                computedChangeInFloor = computedChangeInFloor + 1
            ELSE IF S[claimedRightPointer] == ')':
                computedChangeInFloor = computedChangeInFloor - 1

        IF claimedChangeInFloor != computedChangeInFloor:
            RETURN FALSE
            
        computedAnswer = computedAnswer + computedChangeInFloor

    IF computedAnswer == claimedAnswer:
        RETURN TRUE
    ELSE:
        RETURN FALSE
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis
    
    In the worst-case scenario, the algorithm must evaluate every character in string $S$ because every instruction directly impacts Santa's final floor level.
    
    The exact total number of character evaluation operations performed across all iterations is given by the Performance Function:
    
    $$T(N) = N$$
    
    We state that we are using Asymptotic Approximation to determine the upper bound on time complexity as the input size $N$ grows. Approximating the performance function $T(N)$ yields Big O notation:
    
    $$\mathcal{O}(N)$$
    
2. Best Case Analysis
    
    In the best-case scenario, regardless of the order or composition of `(` and `)` characters, no instruction can be skipped because every single character dictates a floor change.
    
    The exact total number of operations remains unchanged, defined by the Performance Function:
    
    $$T(N) = N$$
    
    We state that we are using Asymptotic Approximation to establish the lower bound on time complexity. Approximating the performance function $T(N)$ yields Big Omega notation:
    
    $$\Omega(N)$$
    

### Space Complexity

The algorithm only uses a constant number of scalar auxiliary variables (`counter`, `left`, `right`, `N`, and iteration counters) regardless of input length $N$.

The memory performance function is $S(N) = 1$. Stating that we are using Asymptotic Approximation, approximating $S(N)$ yields an auxiliary space complexity of:

$$\mathcal{O}(1)$$

## Pros and Cons

### Pros

- **Optimal Time Complexity**: Processes all $N$ characters in exactly $N$ operations, easily passing within the $1.0$-second time limit for $N \le 10^5$.
- **Minimal Space Usage**: Operates in $\mathcal{O}(1)$ auxiliary space without requiring extra arrays or data structures.
- **Symmetric Traversal**: Demonstrates two-pointer logic that processes elements from both ends simultaneously.
- **Edge Case Safety**: Explicitly handles odd-length strings by preventing double-counting when pointers meet at the middle character.

### Cons

- **Branch Overhead**: Contains additional pointer comparison logic (`left != right`) inside the main loop to handle midpoints, introducing slight instruction branching overhead compared to a standard linear scan.
- **No Early Termination**: Must process the entire string $S$ under all conditions, as every character contributes to the final answer.