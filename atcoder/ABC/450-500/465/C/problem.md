# C - Reverse Permutation

## Statement

You are given an integer $N$ and a string $S$ of length $N$ consisting of the characters `o` and `x`.

There is an integer sequence $A = (A_1, A_2, \ldots, A_N)$ of length $N$. Initially, $A$ is the identity permutation:
$$A = (1, 2, \ldots, N)$$

We perform $N$ sequential operations on the sequence $A$, indexed by $k = 1, 2, \ldots, N$ in this exact order:
- If $S_k =$ `o` (using 1-based indexing for $S$), we reverse the first $k$ elements of $A$. That is, $A$ is replaced with:
  $$(A_k, A_{k-1}, \ldots, A_1, A_{k+1}, A_{k+2}, \ldots, A_N)$$
- If $S_k =$ `x`, we do nothing.

Your task is to find the final state of the sequence $A$ after all $N$ operations are completed.

---

## Constraints

- $2 \le N \le 5 \times 10^5$
- $N$ is an integer.
- $S$ is a string of length $N$ consisting exclusively of the characters `o` and `x`.

---

## Input and Output Format

### Input

The input is provided from Standard Input in the following format:

```
N
S
```

### Output

Print the elements of the sequence $A$ after all $N$ operations are completed, separated by spaces.

---

## Input and Output Instances

### Instance 1

#### Input
```
5
ooxoo
```

#### Output
```
5 2 1 3 4
```

#### Explanation
The sequence $A$ changes as follows with each step:
- **Initially**: $A = (1, 2, 3, 4, 5)$
- **For $k=1$** ($S_1 =$ `o`): Reverse the first $1$ element. $A$ becomes $(1, 2, 3, 4, 5)$.
- **For $k=2$** ($S_2 =$ `o`): Reverse the first $2$ elements. $A$ becomes $(2, 1, 3, 4, 5)$.
- **For $k=3$** ($S_3 =$ `x`): Do nothing. $A$ remains $(2, 1, 3, 4, 5)$.
- **For $k=4$** ($S_4 =$ `o`): Reverse the first $4$ elements. $A$ becomes $(4, 3, 1, 2, 5)$.
- **For $k=5$** ($S_5 =$ `o`): Reverse the first $5$ elements. $A$ becomes $(5, 2, 1, 3, 4)$.

---

### Instance 2

#### Input
```
7
ooooooo
```

#### Output
```
7 5 3 1 2 4 6
```

#### Explanation
Every operation from $k = 1$ to $7$ reverses the prefix of length $k$. 
- Initially: $(1, 2, 3, 4, 5, 6, 7)$
- $k=1 \implies (1, 2, 3, 4, 5, 6, 7)$
- $k=2 \implies (2, 1, 3, 4, 5, 6, 7)$
- $k=3 \implies (3, 1, 2, 4, 5, 6, 7)$
- $k=4 \implies (4, 2, 1, 3, 5, 6, 7)$
- $k=5 \implies (5, 3, 1, 2, 4, 6, 7)$
- $k=6 \implies (6, 4, 2, 1, 3, 5, 7)$
- $k=7 \implies (7, 5, 3, 1, 2, 4, 6)$

---

### Instance 3

#### Input
```
15
xooxoxoxoxoxxoo
```

#### Output
```
15 11 10 7 6 3 1 2 4 5 8 9 12 13 14
```

#### Explanation
The operations are executed sequentially up to $k=15$. Reversals occur at indices $k \in \{2, 3, 5, 7, 9, 11, 14, 15\}$. Tracing these steps yields the final permutation shown in the output.

---

### Instance 4

#### Input
```
6
oxoxox
```

#### Output
```
5 4 1 2 3 6
```

#### Explanation
- **Initially**: $A = (1, 2, 3, 4, 5, 6)$
- $k=1$ ($S_1 =$ `o`): Reverse prefix of size $1 \implies A = (1, 2, 3, 4, 5, 6)$
- $k=2$ ($S_2 =$ `x`): Do nothing $\implies A = (1, 2, 3, 4, 5, 6)$
- $k=3$ ($S_3 =$ `o`): Reverse prefix of size $3 \implies A = (3, 2, 1, 4, 5, 6)$
- $k=4$ ($S_4 =$ `x`): Do nothing $\implies A = (3, 2, 1, 4, 5, 6)$
- $k=5$ ($S_5 =$ `o`): Reverse prefix of size $5 \implies A = (5, 4, 1, 2, 3, 6)$
- $k=6$ ($S_6 =$ `x`): Do nothing $\implies A = (5, 4, 1, 2, 3, 6)$