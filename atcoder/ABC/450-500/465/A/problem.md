# A - Supermajority

## Statement

You are given two positive integers, $A$ and $B$.

Your task is to determine whether $A$ represents a strict supermajority relative to $B$ under a two-thirds majority rule. Specifically, you need to check if the value of $A$ is strictly greater than two-thirds of $B$.

Mathematically, you need to evaluate the following inequality:
$$A > B \times \frac{2}{3}$$

To avoid floating-point inaccuracies, this inequality can also be equivalently evaluated using integer arithmetic as:
$$3 \times A > 2 \times B$$

If the inequality holds true, output `Yes`. Otherwise, output `No`.

## Constraints

- $1 \le A, B \le 1000$
- $A$ and $B$ are integers.

## Input and Output Format

### Input

The input is given from Standard Input in the following format:

```
A B
```
### Output

Output the answer.

## Input and Output Instances

### Input Instance 1
```
316 465
```

### Output Instance 1
```
Yes
```

**Explanation:**  
We check if $3 \times A > 2 \times B$.  
Here, $3 \times 316 = 948$ and $2 \times 465 = 930$.  
Since $948 > 930$ is true (which means $316 > 465 \times \frac{2}{3} = 310$), we output `Yes`.

---

### Input Instance 2
```
101 248
```

### Output Instance 2
```
No
```

**Explanation:**  
We check if $3 \times A > 2 \times B$.  
Here, $3 \times 101 = 303$ and $2 \times 248 = 496$.  
Since $303 > 496$ is false (which means $101 > 248 \times \frac{2}{3} \approx 165.33$ is false), we output `No`.

---

### Input Instance 3
```
666 999
```

### Output Instance 3
```
No
```

**Explanation:**  
We check if $3 \times A > 2 \times B$.  
Here, $3 \times 666 = 1998$ and $2 \times 999 = 1998$.  
Since $1998 > 1998$ is false (we require a strict inequality), we output `No`.

---

### Input Instance 4
```
2 3
```

### Output Instance 4
```
No
```

**Explanation:**  
Here, $A = 2$ and $B = 3$.  
Checking the inequality: $3 \times 2 > 2 \times 3 \Rightarrow 6 > 6$, which is false. Thus, we output `No`.

---

### Input Instance 5
```
3 4
```

### Output Instance 5
```
Yes
```

**Explanation:**  
Here, $A = 3$ and $B = 4$.  
Checking the inequality: $3 \times 3 > 2 \times 4 \Rightarrow 9 > 8$, which is true. Thus, we output `Yes`.