# D - X to Y

## Statement

You are given three integers $X$, $Y$, and $K$ (where $K \ge 2$).

There is a variable $x$, which is initially set to $x = X$. You can perform the following operation on $x$ zero or more times:

- Choose an integer $y$ that satisfies either:
  $$\left\lfloor \frac{x}{K} \right\rfloor = y \quad \text{or} \quad \left\lfloor \frac{y}{K} \right\rfloor = x$$
  and replace the current value of $x$ with $y$.

Here, $\lfloor z \rfloor$ denotes the greatest integer not exceeding $z$ (the floor function).

Find the minimum number of operations required to make $x = Y$. Under the given constraints, it can be proven that there always exists a way to reach $Y$ from $X$ in a finite number of operations.

You are given $T$ test cases; solve each of them.

---

## Constraints

- $1 \le T \le 2 \times 10^5$
- $0 \le X, Y \le 10^{18}$
- $2 \le K \le 10^{18}$
- All input values are integers.

---

## Input and Output Format

### Input

The input is given from Standard Input in the following format:

$$T$$
$$\text{case}_1$$
$$\text{case}_2$$
$$\vdots$$
$$\text{case}_T$$

Each test case is given in the following format:

$$X \quad Y \quad K$$

### Output

Print the answers for the test cases in order, each on a new line.

---

## Input and Output Instances

### Input 1
```text
4
11 9 3
0 0 2
842 180 7
1948706013487601 48019760148910476 89014537
```

### Output 1
```text
2
0
7
5
```

### Explanation 1
* **Test Case 1**: For $X = 11$, $Y = 9$, and $K = 3$, we can transition as follows:
  1. Choose $y = 3$. Since $\lfloor 11 / 3 \rfloor = 3$, the transition $11 \to 3$ is valid.
  2. Choose $y = 9$. Since $\lfloor 9 / 3 \rfloor = 3$, the transition $3 \to 9$ is valid.
  
  This takes $2$ operations, which is the minimum.
  
* **Test Case 2**: $X = 0$ and $Y = 0$. Since they are already equal, $0$ operations are needed.

* **Test Case 3**: The shortest path is $842 \to 120 \to 17 \to 2 \to 0 \to 3 \to 25 \to 180$, requiring $7$ operations.

---

### Input 2
```text
2
5 12 2
100 100 10
```

### Output 2
```text
5
0
```

### Explanation 2
* **Test Case 1**: For $X = 5$, $Y = 12$, and $K = 2$:
  - The ancestors of $5$ dividing by $2$ are: $5 \to 2 \to 1 \to 0$.
  - The ancestors of $12$ dividing by $2$ are: $12 \to 6 \to 3 \to 1 \to 0$.
  - The Lowest Common Ancestor (LCA) is $1$. 
  - The path is $5 \to 2 \to 1 \to 3 \to 6 \to 12$, which takes $5$ operations.

* **Test Case 2**: $X = 100$ and $Y = 100$ are already equal, so $0$ operations are required.