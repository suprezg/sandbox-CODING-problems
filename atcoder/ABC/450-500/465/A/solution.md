# Optimal Solution

## Idea

The problem asks whether an integer $A$ represents a strict supermajority over an integer $B$ under a two-thirds majority rule:
$$A > B \times \frac{2}{3}$$

Direct evaluation using floating-point division ($B \times \frac{2}{3}$ or $\frac{2B}{3}$) can introduce precision issues due to binary floating-point representation. To guarantee exact algebraic comparison, we clear the denominator by multiplying both sides of the inequality by $3$:
$$3 \times A > 2 \times B$$

Since $A$ and $B$ are positive integers ($1 \le A, B \le 1000$), multiplying both sides by the positive constant $3$ preserves the inequality without altering its direction. We compute $3 \times A$ and $2 \times B$ using standard integer arithmetic, compare the two values, and output `"Yes"` if $3 \times A > 2 \times B$, or `"No"` otherwise.

## Pseudocode

### Solver

```
FUNCTION solve(a, b):
    scaled_a = 3 * a
    scaled_b = 2 * b

    is_supermajority = FALSE
    IF scaled_a > scaled_b THEN
        is_supermajority = TRUE
        result = "Yes"
    ELSE
        result = "No"
    END IF

    snapshot = (a, b, scaled_a, scaled_b, is_supermajority, result)
    snapshots = [snapshot]

    RETURN (answer = result, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(a, b, answer, proof):
    IF LENGTH(proof) != 1 THEN
        RETURN FALSE
    END IF

    snapshot = proof[0]
    expected_scaled_a = 3 * a
    expected_scaled_b = 2 * b

    IF snapshot.a != a OR snapshot.b != b OR
       snapshot.scaled_a != expected_scaled_a OR
       snapshot.scaled_b != expected_scaled_b THEN
        RETURN FALSE
    END IF

    expected_supermajority = (expected_scaled_a > expected_scaled_b)
    IF snapshot.is_supermajority != expected_supermajority THEN
        RETURN FALSE
    END IF

    IF expected_supermajority THEN
        expected_result = "Yes"
    ELSE
        expected_result = "No"
    END IF

    IF snapshot.result != expected_result THEN
        RETURN FALSE
    END IF

    IF expected_result == answer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    The algorithm performs two scalar integer multiplications ($3 \times A$ and $2 \times B$) and a single integer comparison ($scaled\_a > scaled\_b$). Under the given constraints ($1 \le A, B \le 1000$), all arithmetic operations execute in a fixed number of CPU cycles.

    The exact performance function is:

    $$T(A, B) = 1$$

    Using Asymptotic Approximation to establish the upper bound yields:

    $$\mathcal{O}(1)$$

2. Best Case Analysis

    Regardless of the input values of $A$ and $B$, the two products and the comparison must always be computed. No operations can be bypassed.

    The performance function remains:

    $$T(A, B) = 1$$

    Using Asymptotic Approximation to establish the lower bound yields:

    $$\Omega(1)$$

### Space Complexity

The algorithm requires only a constant number of scalar auxiliary variables (`scaled_a`, `scaled_b`, `is_supermajority`, `result`).

The memory performance function is $S(A, B) = 1$. Using Asymptotic Approximation, approximating $S(A, B)$ yields an auxiliary space complexity of:

$$\mathcal{O}(1)$$

## Pros and Cons

### Pros

- **Exact Arithmetic**: Clearing fractions eliminates floating-point rounding errors and precision loss.
- **Optimal Time Complexity**: Evaluates the condition in $\mathcal{O}(1)$ constant time.
- **Minimal Space Usage**: Uses $\mathcal{O}(1)$ auxiliary memory without allocating dynamic structures.
- **Overflow-Safe**: For $A, B \le 1000$, the maximum intermediate value is $3 \times 1000 = 3000$, well within standard 32-bit and 64-bit signed integer limits.

### Cons

- **Strict Inequality Sensitivity**: Because the problem requires strict supermajority, boundary cases where $3A = 2B$ (such as $A = 666, B = 999$) result in `"No"`, requiring strict inequality handling rather than non-strict ($\ge$).
