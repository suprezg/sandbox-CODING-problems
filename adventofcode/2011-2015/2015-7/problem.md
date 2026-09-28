# Day 7: Some Assembly Required

## Statement

Santa has brought a set of wires and bitwise logic gates for Bobby Tables! Since Bobby is a bit young to assemble the circuit on his own, he needs your help to simulate the circuit and determine the final signal on a specific wire.

The circuit consists of a set of named **wires** and **bitwise logic gates**. 
- Each wire is identified by a unique label consisting of one or more lowercase English letters (e.g., `x`, `y`, `a`, `mw`).
- Each wire can carry a **16-bit unsigned integer signal** (a value from `0` to `65535`).
- A signal is provided to each wire by exactly one source: either a constant value, another wire, or the output of a logic gate.
- Although a wire has only one source, its signal can be routed to multiple destinations.
- A gate or wire cannot propagate a signal until all of its inputs have been fully resolved.

The instructions booklet describes how to connect the components. The connection instructions are of the following types (where `x` and `y` can be wire identifiers or 16-bit integers, and `z` is the destination wire):

1. **Direct Assignment / Connection**: 
   - `x -> z`
   - The signal of `x` is directly provided to wire `z`.
2. **AND Gate**: 
   - `x AND y -> z`
   - The bitwise AND of `x` and `y` is provided to wire `z`.
3. **OR Gate**: 
   - `x OR y -> z`
   - The bitwise OR of `x` and `y` is provided to wire `z`.
4. **LSHIFT (Left Shift)**: 
   - `x LSHIFT n -> z`
   - The signal of `x` is shifted left by `n` bits, and the result is provided to wire `z`.
5. **RSHIFT (Right Shift)**: 
   - `x RSHIFT n -> z`
   - The signal of `x` is shifted right by `n` bits (logical shift), and the result is provided to wire `z`.
6. **NOT (Bitwise Complement)**: 
   - `NOT x -> z`
   - The 16-bit bitwise complement of `x` is provided to wire `z`.

All bitwise operations are performed on **16-bit unsigned integers**. This means that any results must be kept within the range $[0, 65535]$. For instance, the `NOT` operation on a value $v$ produces $65535 - v$.

Your task is to determine the final signal value that is ultimately provided to **wire `a`**.

---

## Constraints

- The number of instructions $N$ is between $1$ and $10^5$.
- Wire identifiers consist of 1 to 4 lowercase English letters (e.g., `a`, `b`, `aa`, `xyz`).
- Numerical constants in the input are integers in the range $[0, 65535]$.
- Shift amounts $n$ in `LSHIFT` and `RSHIFT` instructions are integers in the range $[0, 15]$.
- The circuit is guaranteed to be a **Directed Acyclic Graph (DAG)**. There are no feedback loops or circular dependencies, meaning every wire's signal can be uniquely resolved to a single static value.
- There is exactly one instruction per destination wire.

---

## Input and Output Format

### Input

The input consists of multiple lines, each containing a single instruction. Each instruction describes a connection or gate operation in the format:
`<input_expression> -> <destination_wire>`

The `<input_expression>` can be:
- A single integer or wire identifier: `x`
- A unary operation: `NOT x`
- A binary operation: `x AND y`, `x OR y`, `x LSHIFT n`, `x RSHIFT n`

### Output

Print a single integer representing the 16-bit signal value on wire `a` after the entire circuit has been evaluated.

---

## Input and Output Instances

### Instance 1

#### Input
```text
123 -> x
456 -> y
x AND y -> a
```

#### Output
```text
72
```

#### Explanation
- Wire `x` is assigned the value `123`.
- Wire `y` is assigned the value `456`.
- Wire `a` receives the bitwise AND of `x` and `y`.
- `123 AND 456` in binary is `01111011 AND 111001000 = 001001000`, which is `72` in decimal.

---

### Instance 2

#### Input
```text
123 -> x
NOT x -> a
```

#### Output
```text
65412
```

#### Explanation
- Wire `x` is assigned the value `123`.
- Wire `a` receives the bitwise NOT of `x`.
- In 16-bit unsigned representation, `NOT 123` is equivalent to `65535 - 123`, which equals `65412`.

---

### Instance 3

#### Input
```text
123 -> x
x LSHIFT 2 -> y
y RSHIFT 1 -> a
```

#### Output
```text
246
```

#### Explanation
- Wire `x` is assigned the value `123`.
- Wire `y` receives `x LSHIFT 2`, which is `123 * 4 = 492`.
- Wire `a` receives `y RSHIFT 1`, which is `492 / 2 = 246`.