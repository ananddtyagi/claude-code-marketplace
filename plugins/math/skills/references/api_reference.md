# Math Tools API Reference

Complete reference for all mathematical operations available in the math_calculator.py script.

## Table of Contents

1. [Basic Arithmetic](#basic-arithmetic)
2. [Algebra](#algebra)
3. [Calculus](#calculus)
4. [Trigonometry](#trigonometry)
5. [Linear Algebra](#linear-algebra)
6. [Number Theory](#number-theory)
7. [Statistics](#statistics)
8. [Utility Functions](#utility-functions)

---

## Basic Arithmetic

### add
Add multiple numbers or expressions.
```bash
python math_calculator.py add 5 3 2
# Result: 10
```

### subtract
Subtract second value from first.
```bash
python math_calculator.py subtract 10 3
# Result: 7
```

### multiply
Multiply multiple numbers or expressions.
```bash
python math_calculator.py multiply 2 3 4
# Result: 24
```

### divide
Divide first by second. Returns simplified fraction when applicable.
```bash
python math_calculator.py divide 10 4
# Result: 5/2
```

### mod
Modulo operation.
```bash
python math_calculator.py mod 17 5
# Result: 2
```

### power
Raise base to exponent.
```bash
python math_calculator.py power 2 10
# Result: 1024
```

### sqrt
Square root. Returns symbolic result (e.g., `2*sqrt(2)` for sqrt(8)).
```bash
python math_calculator.py sqrt 8
# Result: 2*sqrt(2)
```

### abs
Absolute value.
```bash
python math_calculator.py abs "-5"
# Result: 5
```

### factorial
Calculate n!
```bash
python math_calculator.py factorial 5
# Result: 120
```

---

## Algebra

### simplify
Simplify algebraic expressions.
```bash
python math_calculator.py simplify "(x**2 - 1)/(x - 1)"
# Result: x + 1
```

### expand
Expand algebraic expressions.
```bash
python math_calculator.py expand "(x + 1)**3"
# Result: x**3 + 3*x**2 + 3*x + 1
```

### factor
Factor polynomials.
```bash
python math_calculator.py factor "x**2 - 4"
# Result: (x - 2)*(x + 2)
```

### solve
Solve equations. Use `=` for equations or expression alone (assumed = 0).
```bash
# Solve x^2 - 4 = 0
python math_calculator.py solve "x**2 - 4" x
# Solutions: [-2, 2]

# Solve 2x + 3 = 7
python math_calculator.py solve "2*x + 3 = 7" x
# Solutions: [2]
```

### solve_system
Solve systems of equations. Pass JSON.
```bash
python math_calculator.py solve_system '{"equations": ["x + y = 10", "x - y = 2"], "variables": ["x", "y"]}'
# Solutions: {x: 6, y: 4}
```

### substitute
Substitute values into expressions. Pass JSON.
```bash
python math_calculator.py substitute '{"expr_str": "x**2 + y", "substitutions": {"x": 3, "y": 2}}'
# Result: 11
```

---

## Calculus

### derivative (or diff)
Differentiate expressions. Optional: specify order for higher derivatives.
```bash
# First derivative
python math_calculator.py derivative "x**3 + 2*x" x
# Result: 3*x**2 + 2

# Second derivative
python math_calculator.py derivative "x**3 + 2*x" x 2
# Result: 6*x
```

### partial
Partial derivatives. List variables in order of differentiation.
```bash
python math_calculator.py partial "x**2*y + y**2*z" x y
# Result: 2*x
```

### integrate (or integral)
Indefinite or definite integration.
```bash
# Indefinite
python math_calculator.py integrate "x**2" x
# Result: x**3/3

# Definite (0 to 1)
python math_calculator.py integrate "x**2" x 0 1
# Result: 1/3
```

### limit
Calculate limits. Use "oo" or "inf" for infinity.
```bash
# Finite limit
python math_calculator.py limit "sin(x)/x" x 0
# Result: 1

# Limit at infinity
python math_calculator.py limit "1/x" x oo
# Result: 0

# One-sided limit (direction: '+' or '-')
python math_calculator.py limit "1/x" x 0 "+"
# Result: oo
```

### series (or taylor)
Taylor series expansion around a point.
```bash
# Expand exp(x) around 0, 6 terms
python math_calculator.py series "exp(x)" x 0 6
# Result: 1 + x + x**2/2 + x**3/6 + x**4/24 + x**5/120 + O(x**6)
```

### sum
Summation. Use "oo" for infinite series.
```bash
# Sum of i from 1 to 10
python math_calculator.py sum "i" i 1 10
# Result: 55

# Infinite geometric series
python math_calculator.py sum "1/2**n" n 1 oo
# Result: 1
```

---

## Trigonometry

### trig_simplify
Simplify trigonometric expressions.
```bash
python math_calculator.py trig_simplify "sin(x)**2 + cos(x)**2"
# Result: 1
```

### trig_expand
Expand trigonometric expressions using identities.
```bash
python math_calculator.py trig_expand "sin(2*x)"
# Result: 2*sin(x)*cos(x)
```

### to_radians
Convert degrees to radians (returns exact value with pi).
```bash
python math_calculator.py to_radians 180
# Result: pi
```

### to_degrees
Convert radians to degrees.
```bash
python math_calculator.py to_degrees "pi/6"
# Result: 30
```

---

## Linear Algebra

All matrix operations accept JSON array format for matrices.

### matrix
Create and display a matrix.
```bash
python math_calculator.py matrix '[[1,2,3],[4,5,6]]'
```

### det (or determinant)
Calculate determinant.
```bash
python math_calculator.py det '[[1,2],[3,4]]'
# Result: -2
```

### inverse
Calculate matrix inverse.
```bash
python math_calculator.py inverse '[[1,2],[3,4]]'
# Result: Matrix([[-2, 1], [3/2, -1/2]])
```

### matrix_mult
Multiply two matrices.
```bash
python math_calculator.py matrix_mult '{"matrix_a": [[1,2],[3,4]], "matrix_b": [[5,6],[7,8]]}'
# Result: [[19, 22], [43, 50]]
```

### eigenvalues
Calculate eigenvalues with multiplicities.
```bash
python math_calculator.py eigenvalues '[[4,2],[1,3]]'
# Result: {5: 1, 2: 1}
```

### eigenvectors
Calculate eigenvectors.
```bash
python math_calculator.py eigenvectors '[[4,2],[1,3]]'
```

### rref
Reduced row echelon form.
```bash
python math_calculator.py rref '[[1,2,3],[4,5,6],[7,8,9]]'
```

---

## Number Theory

### gcd
Greatest common divisor (multiple numbers supported).
```bash
python math_calculator.py gcd 24 36 48
# Result: 12
```

### lcm
Least common multiple (multiple numbers supported).
```bash
python math_calculator.py lcm 4 6 8
# Result: 24
```

### prime_factors
Prime factorization.
```bash
python math_calculator.py prime_factors 360
# Result: 2^3 × 3^2 × 5
```

### is_prime
Check if number is prime.
```bash
python math_calculator.py is_prime 17
# Result: {"is_prime": true}
```

### nth_prime
Get the nth prime number.
```bash
python math_calculator.py nth_prime 100
# Result: 541
```

### binomial
Binomial coefficient (n choose k).
```bash
python math_calculator.py binomial 10 3
# Result: 120
```

---

## Statistics

### mean
Arithmetic mean. Pass JSON array.
```bash
python math_calculator.py mean '[1, 2, 3, 4, 5]'
# Result: 3
```

### variance
Calculate variance. Default is population variance.
```bash
python math_calculator.py variance '[1, 2, 3, 4, 5]'
# Result: 2
```

### std_dev
Standard deviation.
```bash
python math_calculator.py std_dev '[1, 2, 3, 4, 5]'
# Result: sqrt(2)
```

---

## Utility Functions

### evaluate (or eval)
Numerical evaluation with specified precision.
```bash
python math_calculator.py evaluate "pi" 50
# Result: 3.1415926535897932384626433832795028841971693993751

python math_calculator.py eval "sqrt(2)"
# Result: 1.41421356237310
```

### latex
Convert expression to LaTeX.
```bash
python math_calculator.py latex "x**2 + 1/x"
# Result: x^{2} + \frac{1}{x}
```

### compare
Check if two expressions are mathematically equal.
```bash
python math_calculator.py compare "(x+1)**2" "x**2 + 2*x + 1"
# Result: {"equal": true}
```

---

## Expression Syntax

The calculator uses SymPy's parser with implicit multiplication. Supported syntax:

| Operation | Syntax |
|-----------|--------|
| Addition | `a + b` |
| Subtraction | `a - b` |
| Multiplication | `a*b` or `2x` (implicit) |
| Division | `a/b` |
| Power | `a**b` or `a^b` |
| Square root | `sqrt(x)` |
| Absolute value | `Abs(x)` |
| Trigonometric | `sin(x)`, `cos(x)`, `tan(x)`, etc. |
| Inverse trig | `asin(x)`, `acos(x)`, `atan(x)` |
| Hyperbolic | `sinh(x)`, `cosh(x)`, `tanh(x)` |
| Exponential | `exp(x)` |
| Logarithm | `log(x)` (natural), `log(x, base)` |
| Constants | `pi`, `E` (Euler's), `I` (imaginary), `oo` (infinity) |

## Output Format

All operations return JSON with:
- `success`: Boolean indicating success
- `result`: String representation of result
- `latex`: LaTeX representation (when applicable)
- `numeric`: Floating-point approximation (when applicable)
- `type`: SymPy type of result