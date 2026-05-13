"""
mathutil.py – A small collection of pure-Python math helpers.

These functions are intentionally simple so they can be covered by
meaningful unit tests without pulling in heavy dependencies.
"""

from typing import List


def factorial(n: int) -> int:
    """Return n! for a non-negative integer *n*.

    Parameters
    ----------
    n : int
        A non-negative integer.

    Returns
    -------
    int
        The factorial of *n*.

    Raises
    ------
    ValueError
        If *n* is negative.
    TypeError
        If *n* is not an integer.
    """
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n: int) -> List[int]:
    """Return the first *n* Fibonacci numbers.

    Parameters
    ----------
    n : int
        How many Fibonacci numbers to generate (must be >= 0).

    Returns
    -------
    list[int]
        A list of the first *n* Fibonacci numbers.

    Raises
    ------
    ValueError
        If *n* is negative.
    TypeError
        If *n* is not an integer.
    """
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("n must be non-negative")
    if n == 0:
        return []
    if n == 1:
        return [0]
    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq


def is_prime(n: int) -> bool:
    """Check whether *n* is a prime number.

    Parameters
    ----------
    n : int
        The integer to test.

    Returns
    -------
    bool
        ``True`` if *n* is prime, ``False`` otherwise.

    Raises
    ------
    TypeError
        If *n* is not an integer.
    """
    if not isinstance(n, int):
        raise TypeError(f"Expected int, got {type(n).__name__}")
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a: int, b: int) -> int:
    """Return the greatest common divisor of *a* and *b* using the
    Euclidean algorithm.

    Parameters
    ----------
    a, b : int
        Two integers (may be negative; the result is always non-negative).

    Returns
    -------
    int
        The GCD of *a* and *b*.

    Raises
    ------
    TypeError
        If either argument is not an integer.
    """
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("Both arguments must be integers")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a
