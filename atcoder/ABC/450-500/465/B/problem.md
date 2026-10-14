# B - Parking 2

## Statement
There is a parking lot with a tiered pricing system. The hourly parking fees are structured as follows:
* During the peak period from exactly $L$ o'clock to exactly $R$ o'clock, a fee of $X$ is charged for each hour parked.
* During any period not covered by the peak period above, a fee of $Y$ is charged for each hour parked.

If a car is parked in this lot continuously from exactly $A$ o'clock to exactly $B$ o'clock on the same day (without crossing midnight), what is the total parking fee?

## Constraints
* $1 \le X, Y \le 1000$
* $1 \le L < R \le 23$
* $1 \le A < B \le 23$
* All input values are integers.

## Input and Output Format

### Input

The input is given from Standard Input in the following format:

```
X Y L R A B
```

### Ouput

Output the answer.

## Input and Output Instances

### Instance 1
**Input:**
```
700 300 9 17 7 21
```

**Output:**
```
7400
```

**Explanation:**
The car is parked from $7$ o'clock to $21$ o'clock. The total fee is calculated as follows:
* For the $2$ hours from $7$ o'clock to $9$ o'clock (off-peak), a fee of $300 \times 2 = 600$ is charged.
* For the $8$ hours from $9$ o'clock to $17$ o'clock (peak), a fee of $700 \times 8 = 5600$ is charged.
* For the $4$ hours from $17$ o'clock to $21$ o'clock (off-peak), a fee of $300 \times 4 = 1200$ is charged.

The total fee is $600 + 5600 + 1200 = 7400$.

---

### Instance 2
**Input:**
```
600 500 9 17 17 20
```

**Output:**
```
1500
```

**Explanation:**
The car is parked from $17$ o'clock to $20$ o'clock. 
Since the peak period is from $9$ o'clock to $17$ o'clock, none of the parking duration falls within the peak period.
Thus, all $3$ hours are charged at the off-peak rate of $500$ per hour.
The total fee is $500 \times 3 = 1500$.

---

### Instance 3
**Input:**
```
900 200 12 14 11 13
```

**Output:**
```
1100
```

**Explanation:**
The car is parked from $11$ o'clock to $13$ o'clock.
* The $1$ hour from $11$ o'clock to $12$ o'clock is charged at the off-peak rate of $200$.
* The $1$ hour from $12$ o'clock to $13$ o'clock is charged at the peak rate of $900$.

The total fee is $200 \times 1 + 900 \times 1 = 1100$.

---

### Instance 4
**Input:**
```
100 50 1 10 2 8
```

**Output:**
```
600
```

**Explanation:**
The car is parked from $2$ o'clock to $8$ o'clock. 
Since the peak period is from $1$ o'clock to $10$ o'clock, the entire parking duration of $6$ hours falls within the peak period.
Thus, all $6$ hours are charged at the peak rate of $100$ per hour.
The total fee is $100 \times 6 = 600$.