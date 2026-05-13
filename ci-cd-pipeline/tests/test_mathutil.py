"""Tests for src/mathutil.py"""

import pytest
from src.mathutil import factorial, fibonacci, is_prime, gcd  # noqa: E402


# ── factorial ────────────────────────────────────────────────────────

class TestFactorial:
    def test_zero(self):
        assert factorial(0) == 1

    def test_one(self):
        assert factorial(1) == 1

    def test_small(self):
        assert factorial(5) == 120

    def test_larger(self):
        assert factorial(10) == 3628800

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            factorial(-1)

    def test_float_raises(self):
        with pytest.raises(TypeError):
            factorial(3.5)


# ── fibonacci ────────────────────────────────────────────────────────

class TestFibonacci:
    def test_zero(self):
        assert fibonacci(0) == []

    def test_one(self):
        assert fibonacci(1) == [0]

    def test_two(self):
        assert fibonacci(2) == [0, 1]

    def test_ten(self):
        assert fibonacci(10) == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_negative_raises(self):
        with pytest.raises(ValueError):
            fibonacci(-5)

    def test_string_raises(self):
        with pytest.raises(TypeError):
            fibonacci("five")


# ── is_prime ─────────────────────────────────────────────────────────

class TestIsPrime:
    @pytest.mark.parametrize("n", [2, 3, 5, 7, 11, 13, 97])
    def test_primes(self, n):
        assert is_prime(n) is True

    @pytest.mark.parametrize("n", [0, 1, 4, 6, 8, 9, 100])
    def test_non_primes(self, n):
        assert is_prime(n) is False

    def test_negative(self):
        assert is_prime(-7) is False

    def test_float_raises(self):
        with pytest.raises(TypeError):
            is_prime(7.0)


# ── gcd ──────────────────────────────────────────────────────────────

class TestGcd:
    def test_coprime(self):
        assert gcd(7, 13) == 1

    def test_common_factor(self):
        assert gcd(12, 8) == 4

    def test_same(self):
        assert gcd(5, 5) == 5

    def test_zero_and_number(self):
        assert gcd(0, 9) == 9

    def test_both_zero(self):
        assert gcd(0, 0) == 0

    def test_negative_values(self):
        assert gcd(-12, 8) == 4

    def test_float_raises(self):
        with pytest.raises(TypeError):
            gcd(1.5, 3)
