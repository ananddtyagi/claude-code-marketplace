---
name: math-tools
description: Deterministic mathematical computation using SymPy. Use for ANY math operation requiring exact/verified results - basic arithmetic, algebra (simplify, expand, factor, solve equations), calculus (derivatives, integrals, limits, series), linear algebra (matrices, determinants, eigenvalues), trigonometry, number theory (primes, GCD/LCM, factorization), and statistics. Ensures mathematical accuracy by using symbolic computation rather than LLM estimation.
---

# Math Tools

Deterministic mathematical computation engine using SymPy. All calculations use symbolic math - no LLM estimation.

## When to Use

Use this skill whenever mathematical accuracy matters:
- Arithmetic involving fractions, roots, or large numbers
- Algebraic simplification, expansion, factoring
- Solving equations (polynomial, transcendental, systems)
- Calculus (derivatives, integrals, limits, series)
- Linear algebra (matrices, eigenvalues, determinants)
- Number theory (primes, factorization, GCD/LCM)
- Statistical calculations

## Quick Start

Run the calculator script with operation and arguments:

```bash
python scripts/math_calculator.py <operation> <args...>
```

All results return JSON with `result`, `latex`, and `numeric` fields.

## Core Operations

### Arithmetic
```bash
python scripts/math_calculator.py add 5 3 2          # 10
python scripts/math_calculator.py multiply 2 3 4    # 24
python scripts/math_calculator.py divide 10 4       # 5/2 (exact)
python scripts/math_calculator.py sqrt 8            # 2*sqrt(2)
python scripts/math_calculator.py factorial 10      # 3628800
```

### Algebra
```bash
# Simplify
python scripts/math_calculator.py simplify "(x**2 - 1)/(x - 1)"
# → x + 1

# Expand
python scripts/math_calculator.py expand "(x + 1)**3"
# → x**3 + 3*x**2 + 3*x + 1

# Factor
python scripts/math_calculator.py factor "x**3 - 8"
# → (x - 2)*(x**2 + 2*x + 4)

# Solve equations
python scripts/math_calculator.py solve "x**2 - 5*x + 6" x
# → [2, 3]

python scripts/math_calculator.py solve "2*x + 3 = 7" x
# → [2]
```

### Calculus
```bash
# Derivative
python scripts/math_calculator.py derivative "x**3 + sin(x)" x
# → 3*x**2 + cos(x)

# Second derivative
python scripts/math_calculator.py derivative "x**4" x 2
# → 12*x**2

# Indefinite integral
python scripts/math_calculator.py integrate "x**2" x
# → x**3/3

# Definite integral
python scripts/math_calculator.py integrate "x**2" x 0 1
# → 1/3

# Limit
python scripts/math_calculator.py limit "sin(x)/x" x 0
# → 1

# Limit at infinity
python scripts/math_calculator.py limit "(x**2 + 1)/(x**2 - 1)" x oo
# → 1

# Taylor series
python scripts/math_calculator.py series "exp(x)" x 0 5
# → 1 + x + x**2/2 + x**3/6 + x**4/24 + O(x**5)
```

### Linear Algebra
```bash
# Determinant
python scripts/math_calculator.py det '[[1,2],[3,4]]'
# → -2

# Inverse
python scripts/math_calculator.py inverse '[[1,2],[3,4]]'

# Eigenvalues
python scripts/math_calculator.py eigenvalues '[[4,2],[1,3]]'
# → {5: 1, 2: 1}

# RREF
python scripts/math_calculator.py rref '[[1,2,3],[4,5,6]]'
```

### Number Theory
```bash
python scripts/math_calculator.py gcd 24 36 48       # 12
python scripts/math_calculator.py lcm 4 6 8         # 24
python scripts/math_calculator.py prime_factors 360  # 2^3 × 3^2 × 5
python scripts/math_calculator.py is_prime 17       # true
python scripts/math_calculator.py nth_prime 100     # 541
python scripts/math_calculator.py binomial 10 3     # 120
```

### Statistics
```bash
python scripts/math_calculator.py mean '[1,2,3,4,5]'      # 3
python scripts/math_calculator.py variance '[1,2,3,4,5]'  # 2
python scripts/math_calculator.py std_dev '[1,2,3,4,5]'   # sqrt(2)
```

### Utilities
```bash
# Numerical evaluation with precision
python scripts/math_calculator.py evaluate "pi" 50

# LaTeX output
python scripts/math_calculator.py latex "x**2 + 1/x"
# → x^{2} + \frac{1}{x}

# Compare expressions
python scripts/math_calculator.py compare "(x+1)**2" "x**2 + 2*x + 1"
# → equal: true
```

## Expression Syntax

- Powers: `x**2` or `x^2`
- Multiplication: `2*x` or `2x` (implicit)
- Functions: `sin(x)`, `cos(x)`, `exp(x)`, `log(x)`, `sqrt(x)`
- Constants: `pi`, `E`, `I` (imaginary), `oo` (infinity)

## Complex Operations (JSON Input)

For operations requiring structured input:

```bash
# Solve system of equations
python scripts/math_calculator.py solve_system \
  '{"equations": ["x + y = 10", "x - y = 2"], "variables": ["x", "y"]}'

# Substitute values
python scripts/math_calculator.py substitute \
  '{"expr_str": "x**2 + y", "substitutions": {"x": 3, "y": 2}}'

# Matrix multiplication
python scripts/math_calculator.py matrix_mult \
  '{"matrix_a": [[1,2],[3,4]], "matrix_b": [[5,6],[7,8]]}'
```

## Full API Reference

See [references/api_reference.md](references/api_reference.md) for complete documentation of all operations, including:
- All operation names and aliases
- Detailed parameter descriptions
- Output format specifications
- Additional examples

## Dependencies

Requires SymPy:
```bash
pip install sympy
```