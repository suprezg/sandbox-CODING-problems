# A - Decisive Battle

## Statement

A colossal war is taking place in a certain capital city between two rival factions: the **Eastern Army** and the **Western Army**. 

To keep track of the battle's progress and the distribution of forces, Takahashi recorded the details of the active fighting forces into a single string $S$.
The string $S$ consists solely of the uppercase characters `E` and `W`, where:
* Each occurrence of the character `E` represents a single soldier belonging to the **Eastern Army**.
* Each occurrence of the character `W` represents a single soldier belonging to the **Western Army**.

Your task is to analyze the recorded string $S$ and determine which army has the upper hand. Specifically, you must count the number of soldiers in each army and:
* Output `East` if the Eastern Army has strictly more soldiers than the Western Army.
* Output `West` if the Western Army has strictly more soldiers than the Eastern Army.

The length of the string $S$ is guaranteed to be an **odd integer**. Because the total number of soldiers is odd, it is mathematically guaranteed that one army will always have strictly more soldiers than the other (i.e., a tie is impossible).

---

## Constraints

* $S$ is a string consisting only of the characters `E` and `W`.
* The length of $S$, denoted as $|S|$, satisfies $1 \le |S| \le 99$.
* $|S|$ is guaranteed to be an **odd** number.

---

## Input and Output Format

### Input

The input is provided from Standard Input in the following format:

$$S$$

### Output

Print a single line containing either `East` or `West` (case-sensitive) depending on which army has the majority of the soldiers.

---

## Input and Output Instances

### Instance 1
**Input:**
```
EEWEW
```

**Output:**
```
East
```

**Explanation:**
The string $S$ is `EEWEW`. Counting the characters, we find:
* Count of `E` (Eastern Army): 3
* Count of `W` (Western Army): 2

Since $3 > 2$, the Eastern Army has more soldiers than the Western Army. Thus, the output is `East`.

---

### Instance 2
**Input:**
```
WWWWWWW
```

**Output:**
```
West
```

**Explanation:**
The string $S$ is `WWWWWWW`. Counting the characters, we find:
* Count of `E` (Eastern Army): 0
* Count of `W` (Western Army): 7

Since the Western Army has 7 soldiers while the Eastern Army has none ($7 > 0$), the Western Army has the majority. Thus, the output is `West`.

---

### Instance 3 (Generated)
**Input:**
```
E
```

**Output:**
```
East
```

**Explanation:**
The string $S$ consists of a single character `E`, which represents 1 soldier in the Eastern Army and 0 in the Western Army. Since $1 > 0$, the Eastern Army is larger. This is the smallest possible valid input according to the constraints.

---

### Instance 4 (Generated)
**Input:**
```
WWEWW
```

**Output:**
```
West
```

**Explanation:**
The string $S$ is `WWEWW`.
* Count of `E` (Eastern Army): 1
* Count of `W` (Western Army): 4

Since $4 > 1$, the Western Army strictly outnumbers the Eastern Army. Thus, the output is `West`.