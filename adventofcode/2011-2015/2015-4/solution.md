# Optimal Solution

## Idea

The problem requires finding the lowest positive integer $N$ ($N \ge 1$) such that when $N$ is appended in standard decimal notation to a given secret key string $K$ (e.g., `abcdef`), the MD5 hash of the combined string $K + N$, represented as a 32-character lowercase hexadecimal string, begins with at least **five zeroes** (`00000`).

Due to the cryptographic properties of the MD5 hash function—specifically pre-image resistance and the avalanche effect—the output hash values are pseudo-randomly distributed, making it impossible to invert the hash function analytically. Therefore, the optimal deterministic strategy to find the *absolute minimum* integer $N$ is an exhaustive sequential search:

1. Initialize a counter variable `currentNumber` to $1$.
2. In each iteration of an indefinite loop:
   - Form the concatenated string `combinedString` by appending the decimal representation of `currentNumber` directly to `secretKey`.
   - Compute the 128-bit MD5 hash of `combinedString` and represent it as a 32-character hexadecimal string `hashString`.
   - Extract the 5-character prefix of `hashString`.
   - Check if this prefix is equal to `"00000"`.
   - If the prefix matches `"00000"`, terminate the loop and return `currentNumber` as the answer.
   - Otherwise, increment `currentNumber` by $1$ and continue the search.

## Pseudocode

### Solver

```
FUNCTION solve(secretKey):
    currentNumber = 1
    snapshots = []

    WHILE TRUE DO
        combinedString = CONCAT(secretKey, STRING(currentNumber))
        hashString = MD5_HEX(combinedString)
        prefix = SUBSTRING(hashString, 0, 5)

        hasFiveZeroes = FALSE
        IF prefix == "00000" THEN
            hasFiveZeroes = TRUE
        END IF

        snapshot = (currentNumber, combinedString, hashString, prefix, hasFiveZeroes)
        APPEND snapshot TO snapshots

        IF hasFiveZeroes THEN
            RETURN (answer = currentNumber, proof = snapshots)
        END IF

        currentNumber = currentNumber + 1
    END WHILE
END FUNCTION
```

### Verifier

```
FUNCTION verify(secretKey, answer, proof):
    claimedAnswer = answer
    expectedProofLength = claimedAnswer

    IF LENGTH(proof) != expectedProofLength THEN
        RETURN FALSE
    END IF

    FOR index FROM 0 TO expectedProofLength - 1 DO
        snapshot = proof[index]
        expectedNumber = index + 1

        IF snapshot.currentNumber != expectedNumber THEN
            RETURN FALSE
        END IF

        expectedCombinedString = CONCAT(secretKey, STRING(expectedNumber))
        IF snapshot.combinedString != expectedCombinedString THEN
            RETURN FALSE
        END IF

        computedHash = MD5_HEX(expectedCombinedString)
        IF snapshot.hashString != computedHash THEN
            RETURN FALSE
        END IF

        computedPrefix = SUBSTRING(computedHash, 0, 5)
        IF snapshot.prefix != computedPrefix THEN
            RETURN FALSE
        END IF

        IF index < expectedProofLength - 1 THEN
            IF snapshot.hasFiveZeroes != FALSE OR computedPrefix == "00000" THEN
                RETURN FALSE
            END IF
        ELSE
            IF snapshot.hasFiveZeroes != TRUE OR computedPrefix != "00000" THEN
                RETURN FALSE
            END IF
        END IF
    END FOR

    IF snapshot.currentNumber == claimedAnswer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    In the worst-case scenario, the algorithm tests sequential candidate integers from $1$ up to the target answer $N$. For each candidate $i$ ($1 \le i \le N$), the algorithm performs string concatenation of length $L + \lfloor \log_{10} i \rfloor + 1$ (where $L$ is the length of `secretKey`) and computes the MD5 digest. Because $L \le 32$ and $\lfloor \log_{10} N \rfloor + 1 \le 10$, the total input string length is well within a single 512-bit (64-byte) cryptographic message block, requiring $\mathcal{O}(1)$ operations per hash computation.

    The exact total number of hash evaluation operations performed is defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N)$$

    *(Note: Since each hexadecimal digit has 16 possible values, the probability of any candidate hash beginning with five zeroes is $16^{-5} = \frac{1}{1,048,576}$. The expected number of iterations is $\mathbb{E}[N] \approx 1.05 \times 10^6$, executing within a fraction of a second in compiled languages).*

2. Best Case Analysis

    In the best-case scenario, the very first integer evaluated ($N = 1$) produces an MD5 hash that begins with at least five zeroes (`00000`). The search terminates immediately on the initial iteration.

    The total number of hash evaluation operations in this case is defined by the Performance Function:

    $$T(N) = 1$$

    Using Asymptotic Approximation to determine the lower bound on time complexity yields:

    $$\Omega(1)$$

### Space Complexity

The algorithm only maintains scalar tracking variables (`currentNumber`, `hasFiveZeroes`) and temporary string buffers for concatenation and hash generation, all bounded by the small length of the combined input string ($L + \mathcal{O}(\log_{10} N)$).

The auxiliary memory performance function is $S(N) = 1$. Using Asymptotic Approximation, approximating $S(N)$ yields an auxiliary space complexity of:

$$\mathcal{O}(1)$$

## Pros and Cons

### Pros

- **Guaranteed Minimality**: Testing positive integers in strictly ascending order ($1, 2, 3, \dots$) guarantees discovering the absolute lowest integer $N$ that satisfies the condition.
- **Minimal Space Usage**: Operates using $\mathcal{O}(1)$ auxiliary space without retaining previously computed hashes or requiring large auxiliary data structures.
- **Single-Block Digest Efficiency**: The concatenated string length ($L + |N| < 64$ bytes) fits within a single MD5 chunk, maximizing hashing throughput.
- **Immediate Early Termination**: Halts immediately upon finding the first valid hash prefix match without redundant computations.

### Cons

- **Sequential Compute Overhead**: Because cryptographic hash functions cannot be inverted algebraically, finding the target requires brute-force iteration through an average of $\approx 10^6$ hashes.
- **CPU Bound in Single Thread**: Linear sequential evaluation does not exploit multi-core parallelism or hardware-accelerated SIMD instructions unless explicitly parallelized.
- **String Conversion Cost**: Formatting integer strings and hexadecimal digests in each cycle introduces small string conversion overhead per iteration.
