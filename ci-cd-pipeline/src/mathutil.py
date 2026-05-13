"""
Some math helper functions for the CI/CD pipeline assignment.
"""


def factorial(n):
    """Calculate n! iteratively."""
    if not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("n can't be negative")
    result = 1
    for i in range(2, n + 1):
        result *= i
    return result


def fibonacci(n):
    """Return a list of the first n Fibonacci numbers."""
    if not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 0:
        raise ValueError("n can't be negative")
    if n == 0:
        return []
    if n == 1:
        return [0]

    seq = [0, 1]
    for _ in range(2, n):
        seq.append(seq[-1] + seq[-2])
    return seq


def is_prime(n):
    """Check if n is prime. Returns False for anything less than 2."""
    if not isinstance(n, int):
        raise TypeError(f"n must be an int, got {type(n).__name__}")
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    # only check 6k +/- 1
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def gcd(a, b):
    """Euclidean algorithm for GCD."""
    if not isinstance(a, int) or not isinstance(b, int):
        raise TypeError("both args must be ints")
    a, b = abs(a), abs(b)
    while b:
        a, b = b, a % b
    return a
