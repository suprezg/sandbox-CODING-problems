# Day 2: I Was Told There Would Be No Math

## Statement

The elves at the North Pole are running low on wrapping paper and need to submit an order for more. They have a detailed list containing the dimensions (length $l$, width $w$, and height $h$) of each present they need to wrap. Because they want to be as efficient and cost-effective as possible, they want to order exactly the amount of wrapping paper they need.

Fortunately, every present is a perfect right rectangular prism (a box), which simplifies the calculation. The surface area of a box with dimensions $l \times w \times h$ is given by:
$$\text{Surface Area} = 2lw + 2wh + 2hl$$

However, wrapping presents perfectly is a difficult task, so the elves also require a little extra paper for each present as slack. The amount of extra paper needed is equal to the **area of the smallest side** of the box. 

Thus, the total wrapping paper required for a single present is calculated as:
$$\text{Total Paper} = (2 \times l \times w) + (2 \times w \times h) + (2 \times h \times l) + \min(l \times w, w \times h, h \times l)$$

Given a list of present dimensions, your task is to compute the total square feet of wrapping paper the elves need to order.

## Constraints

- The number of presents, $N$, satisfies $1 \le N \le 1000$.
- Each dimension of a present (length $l$, width $w$, and height $h$) is a positive integer.
- The dimensions satisfy $1 \le l, w, h \le 100$.
- All dimensions in the input are measured in feet.

## Input and Output Format

### Input

The input consists of $N$ lines. Each line contains the dimensions of a single present in the format `lxwxh`, where $l$, $w$, and $h$ are positive integers representing the length, width, and height of the present, respectively.

### Output

Print a single integer representing the total number of square feet of wrapping paper the elves should order for all the listed presents.

## Input and Output Instances

### Instance 1

#### Input
```text
2x3x4
```

#### Output
```text
58
```

#### Explanation
For a present with dimensions `2x3x4` (length = 2, width = 3, height = 4):
- The area of the sides are $2 \times 3 = 6$, $3 \times 4 = 12$, and $4 \times 2 = 8$.
- The total surface area is $2 \times 6 + 2 \times 12 + 2 \times 8 = 12 + 24 + 16 = 52$ square feet.
- The smallest side area is $6$ square feet.
- The total wrapping paper required is $52 + 6 = 58$ square feet.

---

### Instance 2

#### Input
```text
1x1x10
```

#### Output
```text
43
```

#### Explanation
For a present with dimensions `1x1x10` (length = 1, width = 1, height = 10):
- The area of the sides are $1 \times 1 = 1$, $1 \times 10 = 10$, and $10 \times 1 = 10$.
- The total surface area is $2 \times 1 + 2 \times 10 + 2 \times 10 = 2 + 20 + 20 = 42$ square feet.
- The smallest side area is $1$ square foot.
- The total wrapping paper required is $42 + 1 = 43$ square feet.

---

### Instance 3

#### Input
```text
2x3x4
1x1x10
```

#### Output
```text
101
```

#### Explanation
There are two presents in this list:
- The first present (`2x3x4`) requires $58$ square feet (as shown in Instance 1).
- The second present (`1x1x10`) requires $43$ square feet (as shown in Instance 2).
- The grand total of wrapping paper needed is $58 + 43 = 101$ square feet.

---

### Instance 4

#### Input
```text
5x5x5
```

#### Output
```text
175
```

#### Explanation
For a cube present with dimensions `5x5x5` (length = 5, width = 5, height = 5):
- The area of all sides is $5 \times 5 = 25$ square feet.
- The total surface area is $6 \times 25 = 150$ square feet.
- The smallest side area is $25$ square feet.
- The total wrapping paper required is $150 + 25 = 175$ square feet.