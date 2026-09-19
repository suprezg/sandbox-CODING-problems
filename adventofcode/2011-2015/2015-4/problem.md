# Day 4: The Ideal Stocking Stuffer

## Statement
Santa Claus needs your help to mine some **AdventCoins** (an economically forward-thinking cryptocurrency similar to Bitcoins) to use as Christmas stocking stuffers for all the well-behaved, tech-savvy children around the world.

To successfully mine an AdventCoin, you must find an MD5 hash that, when represented in hexadecimal, starts with at least **five zeroes** (i.e., `00000...`). 

The input to the MD5 hash function is a secret key (which is your puzzle input) concatenated directly with a decimal number $N$ (with no leading zeroes, starting from $1, 2, 3, \dots$). Your task is to find the **lowest positive integer $N$** such that the MD5 hash of the combined string `secret_key + N` begins with at least five hexadecimal zeroes.

For instance:
- If the secret key is `abcdef`, you need to find the smallest positive integer $N$ such that MD5(`abcdef` + $N$) starts with `00000`. In this case, the smallest such integer is $609043$, because MD5(`abcdef609043`) yields a hexadecimal hash starting with `000001dbbfa...`.
- If the secret key is `pqrstuv`, the smallest integer $N$ is $1048970$, because MD5(`pqrstuv1048970`) yields a hexadecimal hash starting with `000006136ef...`.

## Constraints
- The secret key is a non-empty string consisting only of lowercase English letters (`a`-`z`).
- The length of the secret key, $L$, is typically small ($1 \le L \le 32$).
- The target number $N$ must be a positive integer ($N \ge 1$) represented in standard decimal notation without any leading zeroes.
- The hexadecimal representation of the MD5 hash uses lowercase letters (`a`-`f`) and digits (`0`-`9`), spanning 32 characters in total.
- You must find the *absolute minimum* $N$ satisfying the criteria.

## Input and Output Format

### Input
The input consists of a single line containing a string representing the secret key.

### Output
Print a single integer, which is the lowest positive integer $N$ such that the MD5 hash of the concatenation of the secret key and $N$ starts with at least five zeroes in its hexadecimal representation.

## Input and Output Instances

### Instance 1
**Input:**
```
abcdef
```

**Output:**
```
609043
```

**Explanation:**
We search for the smallest integer $N \ge 1$ starting from $1$.
- For $N = 1$, MD5(`abcdef1`) = `e80b5017098950fc58aad83c8c14978e` (does not start with `00000`).
- For $N = 2$, MD5(`abcdef2`) = `f151b72a690e87900b734892c9431bf3` (does not start with `00000`).
...
- For $N = 609043$, MD5(`abcdef609043`) = `000001dbbfa3a5c83a2d506429c7b00e`, which successfully starts with five zeroes (`00000`). This is the smallest positive integer to achieve this.

### Instance 2
**Input:**
```
pqrstuv
```

**Output:**
```
1048970
```

**Explanation:**
By testing sequential integers starting from $1$ appended to the key `pqrstuv`:
- MD5(`pqrstuv1`) = `7c4b7808298db51f287ee3b8cae0dc41`
- ...
- MD5(`pqrstuv1048970`) = `000006136ef2ff3b291c411134018e1d`
The hash starts with `00000`, and $1048970$ is the lowest integer that produces this result.

### Instance 3
**Input:**
```
iwrupvqb
```

**Output:**
```
346386
```

**Explanation:**
Iterating through positive integers starting from $1$ combined with the secret key `iwrupvqb`, we find that the integer $346386$ is the first one to yield an MD5 hash starting with five zeroes:
- MD5(`iwrupvqb346386`) = `000004514302f232b7fed3e1ef6d34b4`, which begins with `00000`.