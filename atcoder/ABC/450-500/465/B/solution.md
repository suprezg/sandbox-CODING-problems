# Optimal Solution

## Idea

The problem requires calculating the total parking fee for a continuous parking duration from hour $A$ to hour $B$ ($1 \le A < B \le 23$). The hourly fee is tiered:
- Hours spent within the peak interval $[L, R]$ ($1 \le L < R \le 23$) are charged at the peak rate $X$ per hour.
- All remaining hours outside $[L, R]$ are charged at the normal rate $Y$ per hour.

Rather than simulating each 1-hour time slice iteratively, we determine the overlapping duration between the parking interval $[A, B]$ and the peak interval $[L, R]$ using 1D **Interval Intersection**:

1. The total duration of parking is:
   $$\text{total\_hours} = B - A$$

2. The intersection of the two intervals $[A, B]$ and $[L, R]$ has boundaries:
   $$\text{intersect\_start} = \max(A, L)$$
   $$\text{intersect\_end} = \min(B, R)$$

3. The duration spent during peak hours is:
   $$\text{peak\_hours} = \max(0, \text{intersect\_end} - \text{intersect\_start})$$
   *(If the intervals do not overlap, $\text{intersect\_end} \le \text{intersect\_start}$, and taking $\max(0, \dots)$ safely yields $0$.)*

4. The remaining duration spent during off-peak hours is:
   $$\text{normal\_hours} = \text{total\_hours} - \text{peak\_hours}$$

5. The total parking fee is computed directly as:
   $$\text{total\_fee} = (\text{peak\_hours} \times X) + (\text{normal\_hours} \times Y)$$

## Pseudocode

### Solver

```
FUNCTION solve(x, y, l, r, a, b):
    total_hours = b - a

    intersect_start = MAX(a, l)
    intersect_end = MIN(b, r)

    peak_hours = MAX(0, intersect_end - intersect_start)
    normal_hours = total_hours - peak_hours

    total_fee = (peak_hours * x) + (normal_hours * y)

    snapshot = (x, y, l, r, a, b, total_hours, peak_hours, normal_hours, total_fee)
    snapshots = [snapshot]

    RETURN (answer = total_fee, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(x, y, l, r, a, b, answer, proof):
    IF LENGTH(proof) != 1 THEN
        RETURN FALSE
    END IF

    snapshot = proof[0]

    IF snapshot.x != x OR snapshot.y != y OR
       snapshot.l != l OR snapshot.r != r OR
       snapshot.a != a OR snapshot.b != b THEN
        RETURN FALSE
    END IF

    expected_total_hours = b - a
    expected_intersect_start = MAX(a, l)
    expected_intersect_end = MIN(b, r)
    expected_peak_hours = MAX(0, expected_intersect_end - expected_intersect_start)
    expected_normal_hours = expected_total_hours - expected_peak_hours
    expected_total_fee = (expected_peak_hours * x) + (expected_normal_hours * y)

    IF snapshot.total_hours != expected_total_hours OR
       snapshot.peak_hours != expected_peak_hours OR
       snapshot.normal_hours != expected_normal_hours OR
       snapshot.total_fee != expected_total_fee THEN
        RETURN FALSE
    END IF

    IF expected_total_fee == answer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    The algorithm performs a constant number of scalar arithmetic operations: two subtraction operations, one `MAX`, one `MIN`, two multiplications, and one addition. All operations execute in $\mathcal{O}(1)$ time regardless of the values of $A$, $B$, $L$, and $R$.

    The Performance Function is defined as:

    $$T = 1$$

    Using Asymptotic Approximation to establish the upper bound on time complexity yields:

    $$\mathcal{O}(1)$$

2. Best Case Analysis

    Regardless of whether the parking duration overlaps with peak hours or lies entirely outside them, the same constant number of arithmetic evaluations are performed.

    The Performance Function remains:

    $$T = 1$$

    Using Asymptotic Approximation to establish the lower bound on time complexity yields:

    $$\Omega(1)$$

### Space Complexity

The algorithm requires only a constant number of scalar auxiliary variables (`total_hours`, `intersect_start`, `intersect_end`, `peak_hours`, `normal_hours`, `total_fee`). No dynamic collections or memory buffers are allocated.

The auxiliary memory performance function is $S = 1$. Using Asymptotic Approximation, approximating $S$ yields an auxiliary space complexity of:

$$\mathcal{O}(1)$$

## Pros and Cons

### Pros

- **Direct Interval Intersection**: Computes the overlapping duration analytically in $\mathcal{O}(1)$ time, eliminating the need for hour-by-hour iteration loops.
- **Minimal Auxiliary Space**: Operates in $\mathcal{O}(1)$ memory with zero allocations.
- **Robust Disjoint Handling**: Taking $\max(0, \text{intersect\_end} - \text{intersect\_start})$ inherently handles non-overlapping intervals without additional conditional branching.
- **Overflow-Free Arithmetic**: Under the problem constraints ($X, Y \le 1000$ and duration $\le 22$ hours), the maximum fee is $22,000$, well within standard 32-bit integer limits.

### Cons

- **Single Peak Period Assumption**: The direct closed-form formula assumes exactly one contiguous peak interval $[L, R]$; multi-interval or recurring peak schedules would require multiple interval intersections or segment sweeps.
