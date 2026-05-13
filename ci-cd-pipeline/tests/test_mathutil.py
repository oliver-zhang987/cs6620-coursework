import pytest
from src.mathutil import factorial, fibonacci, is_prime, gcd


class TestFactorial:
    def test_base_cases(self):
        assert factorial(0) == 1
        assert factorial(1) == 1

    def test_normal(self):
        assert factorial(5) == 120
        assert factorial(10) == 3628800

    def test_negative(self):
        with pytest.raises(ValueError):
            factorial(-1)

    def test_bad_type(self):
        with pytest.raises(TypeError):
            factorial(3.5)


class TestFibonacci:
    def test_empty_and_small(self):
        assert fibonacci(0) == []
        assert fibonacci(1) == [0]
        assert fibonacci(2) == [0, 1]

    def test_ten(self):
        result = fibonacci(10)
        assert result == [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    def test_negative(self):
        with pytest.raises(ValueError):
            fibonacci(-5)


class TestIsPrime:
    def test_small_primes(self):
        for p in [2, 3, 5, 7, 11, 13]:
            assert is_prime(p)

    def test_not_prime(self):
        for n in [0, 1, 4, 9, 100]:
            assert not is_prime(n)

    def test_negative(self):
        assert not is_prime(-7)


class TestGcd:
    def test_basics(self):
        assert gcd(12, 8) == 4
        assert gcd(7, 13) == 1
        assert gcd(5, 5) == 5

    def test_with_zero(self):
        assert gcd(0, 9) == 9
        assert gcd(0, 0) == 0

    def test_negative(self):
        assert gcd(-12, 8) == 4
