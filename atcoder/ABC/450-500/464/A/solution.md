# Optimal Solution

## Idea

The problem asks us to determine whether the Eastern Army (`E`) or the Western Army (`W`) has strictly more soldiers in a recorded battle string $S$. The length of $S$ is guaranteed to be an odd integer, which ensures that one army will always hold a strict majority and ties are mathematically impossible.

To achieve a clean, streamlined implementation without convoluted branching inside the loop:

1. **Modular Army Counter (`updateSoldierCount`)**:
   A dedicated helper function `updateSoldierCount(soldier_char, east_count, west_count)` takes a character (`'E'` or `'W'`) and references to the two army counters, incrementing the appropriate tally directly.

2. **Inward Pointer Traversal**:
   - Initialize `left_pointer = 0` and `right_pointer = |S| - 1`.
   - Initialize `east_soldiers_count = 0` and `west_soldiers_count = 0`.
   - The total number of iterations is `total_iterations = FLOOR(|S| / 2)`.
   - The loop runs with `iteration_index` from $0$ to `total_iterations`.

3. **Loop Invariant with Early Break on Final Iteration**:
   - At the beginning of each iteration, check if it is the **last iteration** (`iteration_index == total_iterations`). If so, immediately `BREAK` out of the loop.
   - For all non-last iterations, evaluate both pointers using `updateSoldierCount` on `input_string[left_pointer]` and `input_string[right_pointer]`.
   - Then, always advance both pointers inward (`left_pointer` incremented by $1$, `right_pointer` decremented by $1$).
   - Because $|S|$ is odd, in the second-to-last iteration both pointers move inward to point at the exact central character of the string ($left\_pointer == right\_pointer = \lfloor |S| / 2 \rfloor$).

4. **Midpoint Evaluation Outside the Loop**:
   - Upon breaking out of the loop at the final iteration, both pointers are resting at the midpoint.
   - Outside the loop, evaluate **only** `left_pointer` using `updateSoldierCount`, cleanly accounting for the central soldier without any duplicate counting.

5. **Decision**:
   - Compare the final tallies: return `"East"` if `east_soldiers_count > west_soldiers_count`, otherwise return `"West"`.

## Pseudocode

### Helper Functions

```
FUNCTION updateSoldierCount(soldier_char, east_count, west_count):
    IF soldier_char == 'E' THEN
        east_count = east_count + 1
    ELSE IF soldier_char == 'W' THEN
        west_count = west_count + 1
    END IF
END FUNCTION
```

### Solver

```
FUNCTION solve(input_string):
    string_length = LENGTH(input_string)
    east_soldiers_count = 0
    west_soldiers_count = 0

    left_pointer = 0
    right_pointer = string_length - 1
    total_iterations = FLOOR(string_length / 2)

    snapshots = []

    FOR iteration_index FROM 0 TO total_iterations DO
        // On the final iteration, break out of the loop
        IF iteration_index == total_iterations THEN
            BREAK
        END IF

        // Evaluate both pointers for the current pair
        updateSoldierCount(input_string[left_pointer], east_soldiers_count, west_soldiers_count)
        updateSoldierCount(input_string[right_pointer], east_soldiers_count, west_soldiers_count)

        // Record snapshot before pointer advancement
        snapshot = (iteration_index, left_pointer, right_pointer, east_soldiers_count, west_soldiers_count, "PAIRED")
        APPEND snapshot TO snapshots

        // Advance both pointers toward the center
        left_pointer = left_pointer + 1
        right_pointer = right_pointer - 1
    END FOR

    // Outside the loop: evaluate only the left pointer (the central midpoint)
    updateSoldierCount(input_string[left_pointer], east_soldiers_count, west_soldiers_count)

    midpoint_snapshot = (total_iterations, left_pointer, right_pointer, east_soldiers_count, west_soldiers_count, "MIDPOINT")
    APPEND midpoint_snapshot TO snapshots

    IF east_soldiers_count > west_soldiers_count THEN
        winner = "East"
    ELSE
        winner = "West"
    END IF

    RETURN (answer = winner, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(input_string, answer, proof):
    string_length = LENGTH(input_string)
    total_iterations = FLOOR(string_length / 2)
    expected_proof_length = total_iterations

    IF LENGTH(proof) != expected_proof_length THEN
        RETURN FALSE
    END IF

    claimed_answer = answer
    computed_east_count = 0
    computed_west_count = 0
    computed_left_pointer = 0
    computed_right_pointer = string_length - 1

    FOR iteration_index FROM 0 TO total_iterations DO
        IF iteration_index == total_iterations THEN
            BREAK
        END IF

        snapshot = proof[iteration_index]

        updateSoldierCount(input_string[computed_left_pointer], computed_east_count, computed_west_count)
        updateSoldierCount(input_string[computed_right_pointer], computed_east_count, computed_west_count)

        IF snapshot.iteration_index != iteration_index OR
           snapshot.left_pointer != computed_left_pointer OR
           snapshot.right_pointer != computed_right_pointer OR
           snapshot.east_soldiers_count != computed_east_count OR
           snapshot.west_soldiers_count != computed_west_count OR
           snapshot.stage != "PAIRED" THEN
            RETURN FALSE
        END IF

        computed_left_pointer = computed_left_pointer + 1
        computed_right_pointer = computed_right_pointer - 1
    END FOR

    // Verify midpoint evaluation outside the loop
    updateSoldierCount(input_string[computed_left_pointer], computed_east_count, computed_west_count)

    final_snapshot = proof[total_iterations]
    IF final_snapshot.iteration_index != total_iterations OR
       final_snapshot.left_pointer != computed_left_pointer OR
       final_snapshot.right_pointer != computed_right_pointer OR
       final_snapshot.east_soldiers_count != computed_east_count OR
       final_snapshot.west_soldiers_count != computed_west_count OR
       final_snapshot.stage != "MIDPOINT" THEN
        RETURN FALSE
    END IF

    IF computed_east_count > computed_west_count THEN
        computed_winner = "East"
    ELSE
        computed_winner = "West"
    END IF

    IF computed_winner == claimed_answer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    In the worst-case scenario, every soldier in string $S$ must be tallied because the overall distribution of `'E'` and `'W'` determines the outcome.

    Let $N = |S|$ (an odd integer). The algorithm defines $K = \lceil N / 2 \rceil$ total iterations.
    - Inside the loop, exactly $K - 1$ iterations execute before the break condition triggers. In each iteration, $2$ characters are evaluated via `updateSoldierCount` ($\mathcal{O}(1)$) and both pointers are shifted ($\mathcal{O}(1)$), resulting in $2(K - 1) = 2 \cdot \frac{N - 1}{2} = N - 1$ character inspections.
    - Outside the loop, exactly $1$ final character (the central midpoint at `left_pointer`) is evaluated via `updateSoldierCount` ($\mathcal{O}(1)$).

    The exact total number of character inspections across the entire algorithm is:

    $$(N - 1) + 1 = N$$

    The Performance Function is defined as:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N)$$

2. Best Case Analysis

    In the best-case scenario, even if all characters belong to the same army, the algorithm evaluates every character to compute the complete tally.

    The total number of operations remains constant, defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to establish the lower bound on time complexity yields:

    $$\Omega(N)$$

### Space Complexity

The algorithm maintains a constant number of scalar auxiliary variables (`left_pointer`, `right_pointer`, `east_soldiers_count`, `west_soldiers_count`, `string_length`, `total_iterations`, `iteration_index`). No dynamic memory, auxiliary buffers, or heap structures are allocated.

The auxiliary memory performance function is $S(N) = 1$. Using Asymptotic Approximation, approximating $S(N)$ yields a space complexity of:

$$\mathcal{O}(1)$$

## Pros and Cons

### Pros

- **Clean and Branchless Loop Body**: Eliminates nested conditionals within the loop body. The loop maintains a uniform pattern: check break on the last iteration, evaluate paired characters, and advance both pointers.
- **Dedicated Helper Function**: Modularizes character comparison and counter mutation cleanly via `updateSoldierCount`.
- **Zero Midpoint Duplication**: Handling the midpoint strictly outside the loop ensures the central character is evaluated once without complex mid-loop conditional pointer skipping.
- **Optimal Linear Time & Minimal Space**: Performs exactly $N$ evaluations in $\mathcal{O}(N)$ time and operates in $\mathcal{O}(1)$ auxiliary space.

### Cons

- **Outside-of-Loop Finalization**: Requires a post-loop step to evaluate the final central element rather than resolving all characters entirely within the loop body.
- **No Early Termination**: Does not terminate early when one army has secured an unassailable majority before all characters are inspected.
