# Math Tools Plugin for Claude Code

Deterministic mathematical computation using SymPy. All calculations use symbolic math—no LLM estimation or hallucination.

## What It Does

Ensures mathematical accuracy by running actual computations instead of letting Claude guess:

| Category | Operations |
|----------|------------|
| **Arithmetic** | add, subtract, multiply, divide, mod, power, sqrt, abs, factorial |
| **Algebra** | simplify, expand, factor, solve equations, solve systems, substitute |
| **Calculus** | derivatives, partial derivatives, integrals, limits, Taylor series, summations |
| **Linear Algebra** | matrices, determinants, inverse, eigenvalues/eigenvectors, RREF |
| **Trigonometry** | simplify, expand, degree/radian conversion |
| **Number Theory** | GCD, LCM, prime factorization, primality test, nth prime, binomial coefficients |
| **Statistics** | mean, variance, standard deviation |

## Examples

```bash
# Solve x² - 5x + 6 = 0
python math_calculator.py solve "x**2 - 5*x + 6" x
# → [2, 3]

# Derivative of x³ + sin(x)
python math_calculator.py derivative "x**3 + sin(x)" x
# → 3*x**2 + cos(x)

# Definite integral from 0 to 1
python math_calculator.py integrate "x**2" x 0 1
# → 1/3

# Prime factorization
python math_calculator.py prime_factors 360
# → 2³ × 3² × 5

# Matrix determinant
python math_calculator.py det '[[1,2],[3,4]]'
# → -2
```

## Installation

### Requirements

- Python 3.8+
- SymPy library

```bash
pip install sympy
```

### Plugin Setup

1. Clone or download this repository
2. Install in Claude Code:
   
First add this marketplace to Claude Code:

```bash
/plugin marketplace add ananddtyagi/cc-marketplace
```

```bash
/plugin install math@cc-marketplace
```

### Manual Skill Install (without plugin)

Copy the `math` folder to:
- **Personal**: `~/.claude/skills/math/`
- **Project**: `.claude/skills/math/`

## Folder Structure

```
math/
├── .claude-plugin/
│   └── plugin.json
├── skills/
│   ├── SKILL.md
│   ├── scripts/
│   │   └── math_calculator.py
│   └── references/
│       └── api_reference.md
└── README.md
```

## Usage

Once installed, Claude automatically invokes the skill when you ask math questions. Just ask naturally:

- "What's the derivative of x³ + 2x?"
- "Solve x² - 4 = 0"
- "Factor x³ - 8"
- "What's the integral of sin(x) from 0 to π?"
- "Is 97 prime?"