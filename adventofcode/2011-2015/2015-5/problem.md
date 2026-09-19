# Day 5: Doesn't He Have Intern-Elves For This?

## Statement

Santa needs your help to clean up his text file containing a large list of strings. He wants to categorize each string as either **nice** or **naughty** based on a set of specific rules. 

A string is classified as **nice** if and only if it satisfies all three of the following properties simultaneously:
1. **At least three vowels**: The string must contain at least three vowels (specifically, from the set `aeiou` only). These vowels do not need to be distinct. For instance, the string `aaa` contains three vowels (all of them are `a`) and thus satisfies this condition.
2. **Consecutive duplicate letters**: The string must contain at least one letter that appears twice in a row. For example, `xx`, `abcdde` (due to `dd`), or `aabbccdd` (due to `aa`, `bb`, `cc`, or `dd`) all satisfy this condition.
3. **No forbidden substrings**: The string must **not** contain any of the following two-character substrings: `ab`, `cd`, `pq`, or `xy`. This rule is absolute; even if a string meets the first two conditions, the presence of any forbidden substring immediately makes it **naughty**.

Any string that fails to meet one or more of these three conditions is classified as **naughty**.

Your task is to analyze the given list of strings and determine the total number of **nice** strings.

## Constraints

- The input consists of $N$ lines, where each line contains a single string.
- $1 \le N \le 1000$ (The number of strings to classify).
- The length of each string $S$, denoted by $|S|$, satisfies $1 \le |S| \le 100$.
- Each string consists solely of lowercase English letters (`a`-`z`).

## Input and Output Format

### Input
The input consists of multiple lines. Each line contains a single non-empty string of lowercase English letters. The input is terminated by the end-of-file (EOF).

### Output
Print a single integer representing the total count of **nice** strings.

## Input and Output Instances

### Instance 1

#### Input
```text
ugknbfddgicrmopn
aaa
jchzalrnumimnmhp
haegwjzuvuyypxyu
dvszwmarrgswjxmb
```

#### Output
```text
2
```

#### Explanation
- `ugknbfddgicrmopn` is **nice** because it contains at least three vowels (`u`, `i`, `o`), a double letter (`dd`), and none of the forbidden substrings.
- `aaa` is **nice** because it contains three vowels (`a`, `a`, `a`), a double letter (`aa`), and no forbidden substrings. Note that the letters used to satisfy different rules are allowed to overlap.
- `jchzalrnumimnmhp` is **naughty** because it does not contain any double letters.
- `haegwjzuvuyypxyu` is **naughty** because it contains the forbidden substring `xy`.
- `dvszwmarrgswjxmb` is **naughty** because it contains only one vowel (`a`).
Thus, there are exactly 2 nice strings.

### Instance 2

#### Input
```text
aeiouxx
abxx
ccddeea
```

#### Output
```text
2
```

#### Explanation
- `aeiouxx` is **nice** because it has 5 vowels (`a`, `e`, `i`, `o`, `u`), a double letter (`xx`), and no forbidden substrings.
- `abxx` is **naughty** because it contains the forbidden substring `ab`, despite having a double letter `xx`.
- `ccddeea` is **nice** because it contains 3 vowels (`e`, `e`, `a`), multiple double letters (`cc`, `dd`, `ee`), and no forbidden substrings.
Thus, there are exactly 2 nice strings.

### Instance 3

#### Input
```text
qwerasdfzxcv
apqee
urxx
```

#### Output
```text
0
```

#### Explanation
- `qwerasdfzxcv` is **naughty** because it only has 2 vowels (`e`, `a`) and contains no consecutive duplicate letters.
- `apqee` is **naughty** because it contains the forbidden substring `pq`.
- `urxx` is **naughty** because it contains only 1 vowel (`u`).
Thus, there are 0 nice strings.