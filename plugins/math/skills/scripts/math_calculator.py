#!/usr/bin/env python3
"""
Math Calculator - Deterministic mathematical operations using SymPy

A comprehensive math engine that handles:
- Basic arithmetic (add, subtract, multiply, divide, modulo, power)
- Algebra (simplify, expand, factor, solve equations)
- Calculus (derivatives, integrals, limits, series)
- Linear algebra (matrices, determinants, eigenvalues)
- Trigonometry and special functions
- Statistics and probability basics
- Number theory (gcd, lcm, prime factorization)

Usage:
    python math_calculator.py <operation> <args...>
    
Examples:
    python math_calculator.py add 5 3
    python math_calculator.py derivative "x**2 + 3*x" x
    python math_calculator.py solve "x**2 - 4" x
    python math_calculator.py integrate "sin(x)" x
"""

import sys
import json
from typing import Union, List, Any

try:
    import sympy as sp
    from sympy import (
        symbols, Symbol, sympify, simplify, expand, factor,
        solve, diff, integrate, limit, series, summation,
        sin, cos, tan, sec, csc, cot, asin, acos, atan,
        sinh, cosh, tanh, exp, log, ln, sqrt, Abs, sign,
        factorial, binomial, gcd, lcm, factorint, isprime, prime,
        Matrix, det, Rational, pi, E, I, oo, zoo, nan,
        latex, pretty, N, Float, Integer
    )
    from sympy.parsing.sympy_parser import parse_expr, standard_transformations, implicit_multiplication_application
except ImportError:
    print("Error: SymPy is required. Install with: pip install sympy")
    sys.exit(1)


def safe_parse(expr_str: str) -> Any:
    """Safely parse a mathematical expression string."""
    transformations = standard_transformations + (implicit_multiplication_application,)
    try:
        return parse_expr(expr_str, transformations=transformations)
    except Exception as e:
        raise ValueError(f"Could not parse expression '{expr_str}': {e}")


def format_result(result: Any, output_format: str = "auto") -> dict:
    """Format the result in multiple representations."""
    output = {
        "success": True,
        "result": str(result),
        "latex": latex(result) if hasattr(result, '__class__') else str(result),
        "numeric": None,
        "type": type(result).__name__
    }
    
    # Try to get numeric approximation
    try:
        if hasattr(result, 'evalf'):
            numeric = result.evalf()
            if numeric.is_number and not numeric.has(I):
                output["numeric"] = float(numeric)
            else:
                output["numeric"] = str(numeric)
    except:
        pass
    
    return output


# ============== BASIC ARITHMETIC ==============

def add(*args):
    """Add numbers or expressions."""
    result = sum(safe_parse(str(a)) for a in args)
    return format_result(simplify(result))


def subtract(a, b):
    """Subtract b from a."""
    result = safe_parse(str(a)) - safe_parse(str(b))
    return format_result(simplify(result))


def multiply(*args):
    """Multiply numbers or expressions."""
    result = safe_parse(str(args[0]))
    for a in args[1:]:
        result *= safe_parse(str(a))
    return format_result(simplify(result))


def divide(a, b):
    """Divide a by b."""
    num = safe_parse(str(a))
    den = safe_parse(str(b))
    if den == 0:
        return {"success": False, "error": "Division by zero"}
    result = num / den
    return format_result(simplify(result))


def modulo(a, b):
    """Calculate a mod b."""
    return format_result(sp.Mod(safe_parse(str(a)), safe_parse(str(b))))


def power(base, exp):
    """Calculate base^exp."""
    result = safe_parse(str(base)) ** safe_parse(str(exp))
    return format_result(simplify(result))


def sqrt_op(x):
    """Calculate square root."""
    return format_result(sqrt(safe_parse(str(x))))


def abs_op(x):
    """Calculate absolute value."""
    return format_result(Abs(safe_parse(str(x))))


def factorial_op(n):
    """Calculate n!"""
    return format_result(factorial(int(n)))


# ============== ALGEBRA ==============

def simplify_expr(expr_str):
    """Simplify an expression."""
    expr = safe_parse(expr_str)
    return format_result(simplify(expr))


def expand_expr(expr_str):
    """Expand an expression."""
    expr = safe_parse(expr_str)
    return format_result(expand(expr))


def factor_expr(expr_str):
    """Factor an expression."""
    expr = safe_parse(expr_str)
    return format_result(factor(expr))


def solve_equation(equation_str, variable_str="x"):
    """Solve an equation. Use '=' for equations or just expression (assumed = 0)."""
    var = Symbol(variable_str)
    
    if "=" in equation_str:
        left, right = equation_str.split("=")
        equation = safe_parse(left.strip()) - safe_parse(right.strip())
    else:
        equation = safe_parse(equation_str)
    
    solutions = solve(equation, var)
    
    return {
        "success": True,
        "solutions": [str(s) for s in solutions],
        "solutions_latex": [latex(s) for s in solutions],
        "solutions_numeric": [float(s.evalf()) if s.is_number and not s.has(I) else str(s.evalf()) for s in solutions],
        "count": len(solutions)
    }


def solve_system(equations: List[str], variables: List[str]):
    """Solve a system of equations."""
    vars = [Symbol(v) for v in variables]
    eqs = []
    
    for eq_str in equations:
        if "=" in eq_str:
            left, right = eq_str.split("=")
            eqs.append(safe_parse(left.strip()) - safe_parse(right.strip()))
        else:
            eqs.append(safe_parse(eq_str))
    
    solutions = solve(eqs, vars)
    
    return {
        "success": True,
        "solutions": str(solutions),
        "type": type(solutions).__name__
    }


def substitute(expr_str, substitutions: dict):
    """Substitute values into an expression."""
    expr = safe_parse(expr_str)
    subs = {Symbol(k): safe_parse(str(v)) for k, v in substitutions.items()}
    result = expr.subs(subs)
    return format_result(simplify(result))


# ============== CALCULUS ==============

def derivative(expr_str, var_str="x", order=1):
    """Calculate the derivative of an expression."""
    expr = safe_parse(expr_str)
    var = Symbol(var_str)
    result = diff(expr, var, int(order))
    return format_result(result)


def partial_derivative(expr_str, *vars):
    """Calculate partial derivatives."""
    expr = safe_parse(expr_str)
    for var_str in vars:
        var = Symbol(var_str)
        expr = diff(expr, var)
    return format_result(expr)


def integral(expr_str, var_str="x", lower=None, upper=None):
    """Calculate definite or indefinite integral."""
    expr = safe_parse(expr_str)
    var = Symbol(var_str)
    
    if lower is not None and upper is not None:
        # Definite integral
        lower_val = safe_parse(str(lower))
        upper_val = safe_parse(str(upper))
        result = integrate(expr, (var, lower_val, upper_val))
    else:
        # Indefinite integral
        result = integrate(expr, var)
    
    return format_result(result)


def limit_op(expr_str, var_str, point, direction=None):
    """Calculate a limit."""
    expr = safe_parse(expr_str)
    var = Symbol(var_str)
    
    if point == "oo" or point == "inf":
        point_val = oo
    elif point == "-oo" or point == "-inf":
        point_val = -oo
    else:
        point_val = safe_parse(str(point))
    
    if direction:
        result = limit(expr, var, point_val, dir=direction)
    else:
        result = limit(expr, var, point_val)
    
    return format_result(result)


def taylor_series(expr_str, var_str="x", point=0, order=6):
    """Calculate Taylor series expansion."""
    expr = safe_parse(expr_str)
    var = Symbol(var_str)
    result = series(expr, var, safe_parse(str(point)), int(order))
    return format_result(result)


def sum_series(expr_str, var_str, start, end):
    """Calculate a summation."""
    expr = safe_parse(expr_str)
    var = Symbol(var_str)
    
    if end == "oo" or end == "inf":
        end_val = oo
    else:
        end_val = safe_parse(str(end))
    
    result = summation(expr, (var, safe_parse(str(start)), end_val))
    return format_result(result)


# ============== TRIGONOMETRY ==============

def trig_simplify(expr_str):
    """Simplify trigonometric expressions."""
    expr = safe_parse(expr_str)
    result = sp.trigsimp(expr)
    return format_result(result)


def trig_expand(expr_str):
    """Expand trigonometric expressions."""
    expr = safe_parse(expr_str)
    result = sp.expand_trig(expr)
    return format_result(result)


def to_radians(degrees):
    """Convert degrees to radians."""
    deg = safe_parse(str(degrees))
    result = deg * pi / 180
    return format_result(simplify(result))


def to_degrees(radians):
    """Convert radians to degrees."""
    rad = safe_parse(str(radians))
    result = rad * 180 / pi
    return format_result(simplify(result))


# ============== LINEAR ALGEBRA ==============

def matrix_create(rows: List[List]):
    """Create a matrix from rows."""
    m = Matrix(rows)
    return {
        "success": True,
        "matrix": str(m),
        "latex": latex(m),
        "shape": list(m.shape)
    }


def matrix_determinant(rows: List[List]):
    """Calculate matrix determinant."""
    m = Matrix(rows)
    result = det(m)
    return format_result(result)


def matrix_inverse(rows: List[List]):
    """Calculate matrix inverse."""
    m = Matrix(rows)
    try:
        result = m.inv()
        return {
            "success": True,
            "matrix": str(result),
            "latex": latex(result)
        }
    except Exception as e:
        return {"success": False, "error": str(e)}


def matrix_multiply(matrix_a: List[List], matrix_b: List[List]):
    """Multiply two matrices."""
    a = Matrix(matrix_a)
    b = Matrix(matrix_b)
    result = a * b
    return {
        "success": True,
        "matrix": str(result),
        "latex": latex(result)
    }


def matrix_eigenvalues(rows: List[List]):
    """Calculate eigenvalues of a matrix."""
    m = Matrix(rows)
    eigenvals = m.eigenvals()
    return {
        "success": True,
        "eigenvalues": {str(k): v for k, v in eigenvals.items()},
        "latex": {latex(k): v for k, v in eigenvals.items()}
    }


def matrix_eigenvectors(rows: List[List]):
    """Calculate eigenvectors of a matrix."""
    m = Matrix(rows)
    eigenvects = m.eigenvects()
    result = []
    for eigenval, multiplicity, eigenvects_list in eigenvects:
        result.append({
            "eigenvalue": str(eigenval),
            "multiplicity": multiplicity,
            "eigenvectors": [str(v) for v in eigenvects_list]
        })
    return {"success": True, "eigenvectors": result}


def matrix_rref(rows: List[List]):
    """Calculate reduced row echelon form."""
    m = Matrix(rows)
    rref_matrix, pivot_columns = m.rref()
    return {
        "success": True,
        "rref": str(rref_matrix),
        "latex": latex(rref_matrix),
        "pivot_columns": list(pivot_columns)
    }


# ============== NUMBER THEORY ==============

def gcd_op(*numbers):
    """Calculate greatest common divisor."""
    nums = [int(n) for n in numbers]
    result = nums[0]
    for n in nums[1:]:
        result = gcd(result, n)
    return format_result(result)


def lcm_op(*numbers):
    """Calculate least common multiple."""
    nums = [int(n) for n in numbers]
    result = nums[0]
    for n in nums[1:]:
        result = lcm(result, n)
    return format_result(result)


def prime_factors(n):
    """Get prime factorization."""
    factors = factorint(int(n))
    return {
        "success": True,
        "factors": {str(k): v for k, v in factors.items()},
        "factorization": " × ".join(f"{p}^{e}" if e > 1 else str(p) for p, e in factors.items())
    }


def is_prime_op(n):
    """Check if a number is prime."""
    return {"success": True, "is_prime": isprime(int(n)), "number": int(n)}


def nth_prime(n):
    """Get the nth prime number."""
    return format_result(prime(int(n)))


def binomial_coeff(n, k):
    """Calculate binomial coefficient (n choose k)."""
    return format_result(binomial(int(n), int(k)))


# ============== STATISTICS ==============

def mean(numbers: List):
    """Calculate arithmetic mean."""
    nums = [safe_parse(str(n)) for n in numbers]
    result = sum(nums) / len(nums)
    return format_result(simplify(result))


def variance(numbers: List, population=True):
    """Calculate variance."""
    nums = [safe_parse(str(n)) for n in numbers]
    n = len(nums)
    m = sum(nums) / n
    if population:
        var = sum((x - m)**2 for x in nums) / n
    else:
        var = sum((x - m)**2 for x in nums) / (n - 1)
    return format_result(simplify(var))


def std_dev(numbers: List, population=True):
    """Calculate standard deviation."""
    var_result = variance(numbers, population)
    result = sqrt(safe_parse(var_result["result"]))
    return format_result(result)


# ============== UTILITY ==============

def evaluate(expr_str, precision=15):
    """Numerically evaluate an expression."""
    expr = safe_parse(expr_str)
    result = N(expr, int(precision))
    return {
        "success": True,
        "result": str(result),
        "numeric": float(result) if result.is_number and not result.has(I) else str(result)
    }


def to_latex(expr_str):
    """Convert expression to LaTeX."""
    expr = safe_parse(expr_str)
    return {"success": True, "latex": latex(expr)}


def compare(a, b):
    """Compare two expressions for equality."""
    expr_a = safe_parse(str(a))
    expr_b = safe_parse(str(b))
    diff = simplify(expr_a - expr_b)
    equal = diff == 0
    return {
        "success": True,
        "equal": equal,
        "difference": str(diff) if not equal else "0"
    }


# ============== MAIN ==============

OPERATIONS = {
    # Arithmetic
    "add": add,
    "subtract": subtract,
    "multiply": multiply,
    "divide": divide,
    "mod": modulo,
    "power": power,
    "sqrt": sqrt_op,
    "abs": abs_op,
    "factorial": factorial_op,
    
    # Algebra
    "simplify": simplify_expr,
    "expand": expand_expr,
    "factor": factor_expr,
    "solve": solve_equation,
    "solve_system": solve_system,
    "substitute": substitute,
    
    # Calculus
    "derivative": derivative,
    "diff": derivative,
    "partial": partial_derivative,
    "integrate": integral,
    "integral": integral,
    "limit": limit_op,
    "series": taylor_series,
    "taylor": taylor_series,
    "sum": sum_series,
    
    # Trigonometry
    "trig_simplify": trig_simplify,
    "trig_expand": trig_expand,
    "to_radians": to_radians,
    "to_degrees": to_degrees,
    
    # Linear Algebra
    "matrix": matrix_create,
    "det": matrix_determinant,
    "determinant": matrix_determinant,
    "inverse": matrix_inverse,
    "matrix_mult": matrix_multiply,
    "eigenvalues": matrix_eigenvalues,
    "eigenvectors": matrix_eigenvectors,
    "rref": matrix_rref,
    
    # Number Theory
    "gcd": gcd_op,
    "lcm": lcm_op,
    "prime_factors": prime_factors,
    "is_prime": is_prime_op,
    "nth_prime": nth_prime,
    "binomial": binomial_coeff,
    
    # Statistics
    "mean": mean,
    "variance": variance,
    "std_dev": std_dev,
    
    # Utility
    "evaluate": evaluate,
    "eval": evaluate,
    "latex": to_latex,
    "compare": compare,
}


def print_help():
    """Print usage information."""
    print(__doc__)
    print("\nAvailable operations:")
    for category, ops in [
        ("Arithmetic", ["add", "subtract", "multiply", "divide", "mod", "power", "sqrt", "abs", "factorial"]),
        ("Algebra", ["simplify", "expand", "factor", "solve", "solve_system", "substitute"]),
        ("Calculus", ["derivative", "partial", "integrate", "limit", "series", "sum"]),
        ("Trigonometry", ["trig_simplify", "trig_expand", "to_radians", "to_degrees"]),
        ("Linear Algebra", ["matrix", "det", "inverse", "matrix_mult", "eigenvalues", "eigenvectors", "rref"]),
        ("Number Theory", ["gcd", "lcm", "prime_factors", "is_prime", "nth_prime", "binomial"]),
        ("Statistics", ["mean", "variance", "std_dev"]),
        ("Utility", ["evaluate", "latex", "compare"]),
    ]:
        print(f"\n  {category}: {', '.join(ops)}")


def main():
    if len(sys.argv) < 2 or sys.argv[1] in ["-h", "--help", "help"]:
        print_help()
        sys.exit(0)
    
    operation = sys.argv[1].lower()
    
    if operation not in OPERATIONS:
        print(f"Unknown operation: {operation}")
        print("Use --help to see available operations")
        sys.exit(1)
    
    args = sys.argv[2:]
    
    # Handle JSON input for complex operations
    if len(args) == 1 and args[0].startswith("{"):
        try:
            kwargs = json.loads(args[0])
            result = OPERATIONS[operation](**kwargs)
        except json.JSONDecodeError:
            result = OPERATIONS[operation](args[0])
    elif len(args) == 1 and args[0].startswith("["):
        try:
            list_args = json.loads(args[0])
            result = OPERATIONS[operation](list_args)
        except json.JSONDecodeError:
            result = OPERATIONS[operation](args[0])
    else:
        try:
            result = OPERATIONS[operation](*args)
        except TypeError as e:
            print(f"Error: {e}")
            sys.exit(1)
    
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()