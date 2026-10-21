# Optimal Solution

## Idea

The problem asks for the minimum number of operations to transform an integer $x = X$ into $Y$ given an integer radix $K \ge 2$. At each step, we can either replace $x$ with $\lfloor x / K \rfloor$ or replace $x$ with any integer $y$ such that $\lfloor y / K \rfloor = x$.

This transition system defines an infinite rooted $K$-ary tree where:
- Every non-negative integer $z$ is a node.
- The parent of any node $z > 0$ is $\lfloor z / K \rfloor$, and the unique root of the tree is $0$ (since $\lfloor 0 / K \rfloor = 0$).
- Replacing $x$ with $\lfloor x / K \rfloor$ corresponds to moving one step up to its parent.
- Replacing $x$ with $y$ where $\lfloor y / K \rfloor = x$ corresponds to moving one step down to one of its $K$ children.

Because the underlying graph is a tree, any transition is an edge traversal. The shortest path between any two nodes $X$ and $Y$ is the unique simple tree path that ascends from both $X$ and $Y$ to their **Lowest Common Ancestor (LCA)**:
$$\text{dist}(X, Y) = \text{dist}(X, \text{LCA}(X, Y)) + \text{dist}(Y, \text{LCA}(X, Y))$$

To find this distance without explicit tree construction:
1. For each test case $(X, Y, K)$, initialize `current_x = X`, `current_y = Y`, and a step counter `total_operations = 0`.
2. Run a `WHILE` loop as long as `current_x != current_y`:
   - Compare `current_x` and `current_y`:
     - If `current_x > current_y`, move `current_x` up to its parent: `current_x = FLOOR(current_x / k)`.
     - Else (since `current_y > current_x`), move `current_y` up to its parent: `current_y = FLOOR(current_y / k)`.
   - At each parent step, increment `total_operations` by $1$.
3. When `current_x == current_y`, both nodes have converged at $\text{LCA}(X, Y)$, and `total_operations` holds the exact minimum number of edges on the path between $X$ and $Y$.
4. Repeat this for all $T$ test cases using a 0-indexed loop from $0$ to $T - 1$ (i.e. over the range $[0, T)$).

## Pseudocode

### Helper Functions

```
FUNCTION solveTestCase(x, y, k):
    current_x = x
    current_y = y
    total_operations = 0
    history = []

    WHILE current_x != current_y DO
        IF current_x > current_y THEN
            current_x = FLOOR(current_x / k)
        ELSE
            current_y = FLOOR(current_y / k)
        END IF

        total_operations = total_operations + 1
        snapshot_step = (current_x, current_y, total_operations)
        APPEND snapshot_step TO history
    END WHILE

    RETURN (operations = total_operations, lca = current_x, history = history)
END FUNCTION
```

### Solver

```
FUNCTION solve(t, test_cases):
    results = []
    snapshots = []

    FOR case_index FROM 0 TO t - 1 DO
        case_data = test_cases[case_index]
        x = case_data.x
        y = case_data.y
        k = case_data.k

        test_result = solveTestCase(x, y, k)
        APPEND test_result.operations TO results

        snapshot = (case_index, x, y, k, test_result.operations, test_result.lca, test_result.history)
        APPEND snapshot TO snapshots
    END FOR

    RETURN (answer = results, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(t, test_cases, answer, proof):
    IF LENGTH(proof) != t OR LENGTH(answer) != t THEN
        RETURN FALSE
    END IF

    FOR case_index FROM 0 TO t - 1 DO
        snapshot = proof[case_index]
        case_data = test_cases[case_index]
        x = case_data.x
        y = case_data.y
        k = case_data.k

        IF snapshot.case_index != case_index OR
           snapshot.x != x OR snapshot.y != y OR snapshot.k != k THEN
            RETURN FALSE
        END IF

        computed_x = x
        computed_y = y
        computed_ops = 0

        WHILE computed_x != computed_y DO
            IF computed_x > computed_y THEN
                computed_x = FLOOR(computed_x / k)
            ELSE
                computed_y = FLOOR(computed_y / k)
            END IF
            computed_ops = computed_ops + 1
        END WHILE

        IF snapshot.operations != computed_ops OR
           snapshot.lca != computed_x OR
           answer[case_index] != computed_ops THEN
            RETURN FALSE
        END IF
    END FOR

    RETURN TRUE
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    In each testcase, moving a node $z$ to its parent $\lfloor z / K \rfloor$ strictly divides its value by $K \ge 2$. The maximum depth of any node $\le 10^{18}$ in the $K$-ary tree is bounded by:
    $$D \le \lfloor \log_K(\max(X, Y)) \rfloor + 1 \le \lfloor \log_2(10^{18}) \rfloor + 1 \approx 60$$

    In the worst case (e.g. when $K = 2$ and the LCA is the root $0$), the while loop performs at most $2 \times 60 = 120$ divisions. Across all $T$ test cases, the Performance Function is:

    $$T_{\text{total}}(T, X, Y, K) = \sum_{i=1}^{T} \mathcal{O}(\log_K(\max(X_i, Y_i))) \le T \cdot \mathcal{O}(\log_K(\max(X, Y)))$$

    Using Asymptotic Approximation to establish the upper bound on time complexity yields:

    $$\mathcal{O}(T \cdot \log_K(\max(X, Y)))$$

    For $T = 2 \times 10^5$, the maximum number of operations is approximately $2 \times 10^5 \times 120 \approx 2.4 \times 10^7$, easily executing within the $2.0$-second time limit.

2. Best Case Analysis

    In the best-case scenario, $X = Y$ for all test cases. The while loop condition `current_x != current_y` evaluates to false immediately on the initial check, performing zero division operations per test case.

    The total number of operations across all $T$ cases is defined by the Performance Function:

    $$T(T) = T$$

    Using Asymptotic Approximation to establish the lower bound yields:

    $$\Omega(T)$$

### Space Complexity

The algorithm requires only scalar auxiliary tracking variables (`current_x`, `current_y`, `total_operations`, `case_index`) for each test case. An array of size $T$ stores the resulting operation counts.

The memory performance function is $S(T) = T$. Using Asymptotic Approximation, approximating $S(T)$ yields a space complexity of:

$$\mathcal{O}(T)$$

## Pros and Cons

### Pros

- **LCA Simplification**: Replaces complex graph searches (such as BFS/Dijkstra) with direct scalar integer division, exploiting the tree property that each node has a unique parent $\lfloor z / K \rfloor$.
- **Logarithmic Convergence**: Because $K \ge 2$, each parent transition reduces the magnitude exponentially, guaranteeing termination in $\le 60$ steps per query.
- **Minimal Auxiliary Memory**: Operates with $\mathcal{O}(1)$ auxiliary memory per testcase without constructing explicit graph nodes or adjacency lists.
- **Exact Integer Arithmetic**: Avoids floating-point logarithms or root approximations, using only standard integer floor division.

### Cons

- **Linear Query Processing**: Test cases are processed sequentially; queries cannot be batched or accelerated via precomputed ancestor tables due to the dynamic radix $K$ varying per query.
