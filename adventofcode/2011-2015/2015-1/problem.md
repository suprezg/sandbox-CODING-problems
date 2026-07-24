# Day 1: Not Quite Lisp

## Statement

Santa Claus is preparing to deliver presents in a massive apartment building. However, the directions he received to find the correct floor are quite confusing. 

He begins his journey on the ground floor (floor `0`) and follows a sequence of instructions character by character. The instructions are represented by a string of parentheses:
- An opening parenthesis `(` means Santa should go **up** one floor (+1).
- A closing parenthesis `)` means Santa should go **down** one floor (-1).

The apartment building is infinitely tall, and its basement is infinitely deep. This means Santa will never run out of floors above or below him, and there are no boundaries to stop him from going up or down.

Given a string of parentheses, determine the final floor Santa reaches after processing all the instructions in the sequence.

## Constraints

- The input sequence consists of a single string $S$.
- The length of the string $S$ satisfies $1 \le |S| \le 10^5$.
- The string $S$ contains only the characters `(` and `)`.
- Time Limit: $1.0$ second.
- Memory Limit: $256$ megabytes.

## Input and Output Format

### Input
The input consists of a single line containing the string $S$, representing the sequence of instructions.

### Output
Print a single integer representing the final floor Santa reaches after executing all the instructions.

## Input and Output Instances

### Instance 1
**Input:**
```
(())
```

**Output:**
```
0
```

**Explanation:**
Santa starts on floor `0`. 
1. `(` takes him to floor `1`.
2. `(` takes him to floor `2`.
3. `)` takes him to floor `1`.
4. `)` takes him to floor `0`.
The final floor is `0`.

---

### Instance 2
**Input:**
```
(((
```

**Output:**
```
3
```

**Explanation:**
Santa starts on floor `0`. He encounters three opening parentheses `(((`, each of which instructs him to go up one floor. He ends up on floor `3`.

---

### Instance 3
**Input:**
```
())
```

**Output:**
```
-1
```

**Explanation:**
Santa starts on floor `0`. 
1. `(` takes him to floor `1`.
2. `)` takes him back to floor `0`.
3. `)` takes him down to floor `-1`.
The final floor is `-1` (the first basement level).

---

### Instance 4
**Input:**
```
)())())
```

**Output:**
```
-3
```

**Explanation:**
Santa starts on floor `0`. Following the characters in order:
- `)` -> floor `-1`
- `(` -> floor `0`
- `)` -> floor `-1`
- `)` -> floor `-2`
- `(` -> floor `-1`
- `)` -> floor `-2`
- `)` -> floor `-3`
The final floor is `-3`.