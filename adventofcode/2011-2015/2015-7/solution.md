# Optimal Solution

## Idea

The problem requires simulating an assembly of digital logic gates and wires forming a Directed Acyclic Graph (DAG) and calculating the final 16-bit unsigned integer signal on wire `a`. Each instruction specifies an input expression connected to a destination wire in the format `<input_expression> -> <destination_wire>`.

To model the physical wire assembly faithfully and deterministically:

1. **State Representation**:
   We maintain a dictionary named `wires` where each key is a wire identifier string (e.g., `"x"`, `"a"`) and each value is an unsigned 16-bit integer in the range $[0, 65535]$.

2. **Expression Decoding**:
   A dedicated decoding function `decodeExpression` parses the left-hand side of each instruction into:
   - An operation descriptor: `"assignment"`, `"unary-Not"`, `"binary-AND"`, `"binary-OR"`, `"binary-LSHIFT"`, or `"binary-RSHIFT"`.
   - A list `operands` containing the wire identifiers or numerical constant values supplied in the expression.

3. **Sequential Execution & 16-Bit Casting**:
   For each instruction in dependency order:
   - The left-hand side is decoded, and the returned operation and operand list are stored in temporary variables (`tempOperation`, `tempOperands`).
   - The destination wire identifier on the right-hand side is extracted as `key`.
   - A `SWITCH` construct evaluates the operation by resolving each operand (either retrieving its integer value directly or looking up its signal from `wires`).
   - The evaluated result is bitmasked using `65535` (`& 0xFFFF`), casting the result into an exact 16-bit unsigned integer.
   - The cast value is assigned into `wires[key]`.

4. **Result Retrieval**:
   Once all instructions are evaluated, the signal on wire `a` is retrieved from `wires["a"]` as the final answer.

## Pseudocode

### Helper Functions

```
FUNCTION isInteger(token):
    RETURN (token MATCHES "^[0-9]+$")
END FUNCTION

FUNCTION resolveValue(operand, wires):
    IF isInteger(operand) THEN
        RETURN TO_INT(operand)
    ELSE
        RETURN wires[operand]
    END IF
END FUNCTION

FUNCTION decodeExpression(inputExpression):
    tokens = SPLIT(TRIM(inputExpression), " ")
    tokenCount = LENGTH(tokens)

    IF tokenCount == 1 THEN
        operands = [tokens[0]]
        RETURN ("assignment", operands)
    ELSE IF tokenCount == 2 THEN
        // Unary NOT operation: "NOT x"
        operands = [tokens[1]]
        RETURN ("unary-Not", operands)
    ELSE
        // Binary operations: "x OP y"
        leftOperand = tokens[0]
        operator = tokens[1]
        rightOperand = tokens[2]
        operands = [leftOperand, rightOperand]

        IF operator == "AND" THEN
            RETURN ("binary-AND", operands)
        ELSE IF operator == "OR" THEN
            RETURN ("binary-OR", operands)
        ELSE IF operator == "LSHIFT" THEN
            RETURN ("binary-LSHIFT", operands)
        ELSE IF operator == "RSHIFT" THEN
            RETURN ("binary-RSHIFT", operands)
        END IF
    END IF
END FUNCTION
```

### Solver

```
FUNCTION solve(instructionsList):
    wires = MAP()
    snapshots = []
    instructionCount = LENGTH(instructionsList)

    FOR index FROM 0 TO instructionCount - 1 DO
        currentInstruction = instructionsList[index]
        parts = SPLIT(currentInstruction, " -> ")
        leftSide = TRIM(parts[0])
        rightSide = TRIM(parts[1])
        key = rightSide

        (operation, operands) = decodeExpression(leftSide)
        tempOperation = operation
        tempOperands = operands

        evaluatedValue = 0

        SWITCH tempOperation DO
            CASE "assignment":
                rawVal = resolveValue(tempOperands[0], wires)
                evaluatedValue = rawVal

            CASE "unary-Not":
                rawVal = resolveValue(tempOperands[0], wires)
                evaluatedValue = BITWISE_NOT(rawVal)

            CASE "binary-AND":
                val1 = resolveValue(tempOperands[0], wires)
                val2 = resolveValue(tempOperands[1], wires)
                evaluatedValue = BITWISE_AND(val1, val2)

            CASE "binary-OR":
                val1 = resolveValue(tempOperands[0], wires)
                val2 = resolveValue(tempOperands[1], wires)
                evaluatedValue = BITWISE_OR(val1, val2)

            CASE "binary-LSHIFT":
                val1 = resolveValue(tempOperands[0], wires)
                shiftAmount = resolveValue(tempOperands[1], wires)
                evaluatedValue = BITWISE_LSHIFT(val1, shiftAmount)

            CASE "binary-RSHIFT":
                val1 = resolveValue(tempOperands[0], wires)
                shiftAmount = resolveValue(tempOperands[1], wires)
                evaluatedValue = BITWISE_RSHIFT(val1, shiftAmount)
        END SWITCH

        // Cast evaluated value into 16-bit unsigned integer
        castValue = BITWISE_AND(evaluatedValue, 65535)
        wires[key] = castValue

        snapshot = (index, currentInstruction, leftSide, key, tempOperation, tempOperands, castValue)
        APPEND snapshot TO snapshots
    END FOR

    answer = wires["a"]
    RETURN (answer = answer, proof = snapshots)
END FUNCTION
```

### Verifier

```
FUNCTION verify(instructionsList, answer, proof):
    claimedAnswer = answer
    expectedProofLength = LENGTH(instructionsList)

    IF LENGTH(proof) != expectedProofLength THEN
        RETURN FALSE
    END IF

    verifierWires = MAP()

    FOR index FROM 0 TO expectedProofLength - 1 DO
        snapshot = proof[index]
        currentInstruction = instructionsList[index]

        parts = SPLIT(currentInstruction, " -> ")
        expectedLeftSide = TRIM(parts[0])
        expectedKey = TRIM(parts[1])

        IF snapshot.currentInstruction != currentInstruction OR
           snapshot.leftSide != expectedLeftSide OR
           snapshot.key != expectedKey THEN
            RETURN FALSE
        END IF

        (expectedOperation, expectedOperands) = decodeExpression(expectedLeftSide)
        IF snapshot.tempOperation != expectedOperation OR
           snapshot.tempOperands != expectedOperands THEN
            RETURN FALSE
        END IF

        computedRaw = 0
        SWITCH expectedOperation DO
            CASE "assignment":
                computedRaw = resolveValue(expectedOperands[0], verifierWires)

            CASE "unary-Not":
                computedRaw = BITWISE_NOT(resolveValue(expectedOperands[0], verifierWires))

            CASE "binary-AND":
                val1 = resolveValue(expectedOperands[0], verifierWires)
                val2 = resolveValue(expectedOperands[1], verifierWires)
                computedRaw = BITWISE_AND(val1, val2)

            CASE "binary-OR":
                val1 = resolveValue(expectedOperands[0], verifierWires)
                val2 = resolveValue(expectedOperands[1], verifierWires)
                computedRaw = BITWISE_OR(val1, val2)

            CASE "binary-LSHIFT":
                val1 = resolveValue(expectedOperands[0], verifierWires)
                shiftAmount = resolveValue(expectedOperands[1], verifierWires)
                computedRaw = BITWISE_LSHIFT(val1, shiftAmount)

            CASE "binary-RSHIFT":
                val1 = resolveValue(expectedOperands[0], verifierWires)
                shiftAmount = resolveValue(expectedOperands[1], verifierWires)
                computedRaw = BITWISE_RSHIFT(val1, shiftAmount)
        END SWITCH

        expectedCastValue = BITWISE_AND(computedRaw, 65535)
        IF snapshot.castValue != expectedCastValue THEN
            RETURN FALSE
        END IF

        verifierWires[expectedKey] = expectedCastValue
    END FOR

    IF verifierWires["a"] == claimedAnswer THEN
        RETURN TRUE
    ELSE
        RETURN FALSE
    END IF
END FUNCTION
```

## Analysis

### Time Complexity

1. Worst Case Analysis

    Let $N$ denote the total number of instructions in the circuit. For each instruction, string parsing and token splitting evaluate a constant-length expression ($\le 3$ tokens), executing in $\mathcal{O}(1)$ time.

    The decoding function `decodeExpression` inspects the token count and returns the corresponding operation descriptor in $\mathcal{O}(1)$ operations. The switch construct resolves up to two operands via dictionary lookup or numerical conversion, executes a single bitwise logic operation (`AND`, `OR`, `NOT`, `LSHIFT`, or `RSHIFT`), and performs bitmask truncation (`& 65535`), all of which take $\mathcal{O}(1)$ constant time.

    The exact total number of instruction evaluation operations performed across the entire circuit is defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the upper bound on time complexity yields:

    $$\mathcal{O}(N)$$

2. Best Case Analysis

    In the best-case scenario, the circuit instructions are processed in topological order without any missing prerequisites. Every instruction still requires string parsing, expression decoding, operand resolution, bitwise calculation, 16-bit casting, and dictionary assignment.

    The total number of evaluation operations remains unchanged, defined by the Performance Function:

    $$T(N) = N$$

    Using Asymptotic Approximation to determine the lower bound on time complexity yields:

    $$\Omega(N)$$

### Space Complexity

The algorithm stores the signal state of each resolved wire within the dictionary `wires`. Since each instruction assigns a signal to exactly one distinct destination wire in the DAG, `wires` stores at most $N$ unique key-value pairs where each key is a wire identifier string and each value is an unsigned 16-bit integer. The auxiliary variables `tempOperation`, `tempOperands`, and intermediate scalars require $\mathcal{O}(1)$ space per iteration.

The memory performance function is $S(N) = N$. Using Asymptotic Approximation, approximating $S(N)$ yields a space complexity of:

$$\mathcal{O}(N)$$

## Pros and Cons

### Pros

- **Hardware-Accurate 16-Bit Semantics**: Enforces strict unsigned 16-bit bounds using bitmasking (`& 65535`) across all bitwise operations, correctly simulating bitwise complements and overflows.
- **Modular Expression Decoding**: Decouples lexical analysis of expressions in `decodeExpression` from circuit execution logic in `solve`, facilitating clear maintenance and validation.
- **Explicit Signal Tracing**: The `wires` dictionary records wire signals directly, allowing state inspection at every step and enabling comprehensive snapshot verification.
- **Linear Execution Time**: Evaluates the circuit in $\mathcal{O}(N)$ time and space, efficiently handling up to $N = 10^5$ instructions.

### Cons

- **Sequential Topological Dependency**: Sequential evaluation requires that input instructions are organized in topological dependency order; out-of-order execution without prior dependency sorting would encounter unresolved wire references.
- **Dictionary Lookup Overhead**: Managing wire signals in a hash map incurs small hashing and reference overhead compared to contiguous indexed array storage.
