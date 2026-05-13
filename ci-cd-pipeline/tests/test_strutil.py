import pytest
from src.strutil import reverse_words, is_palindrome, char_frequency, caesar_cipher


class TestReverseWords:
    def test_basic(self):
        assert reverse_words("hello world") == "world hello"

    def test_single_word(self):
        assert reverse_words("hello") == "hello"

    def test_empty(self):
        assert reverse_words("") == ""

    def test_extra_spaces(self):
        # split() handles multiple spaces
        assert reverse_words("  hello   world  ") == "world hello"


class TestIsPalindrome:
    def test_simple(self):
        assert is_palindrome("racecar")
        assert not is_palindrome("hello")

    def test_ignores_case_and_punctuation(self):
        assert is_palindrome("A man, a plan, a canal: Panama")

    def test_empty_and_single(self):
        assert is_palindrome("")
        assert is_palindrome("x")


class TestCharFrequency:
    def test_basic(self):
        assert char_frequency("aab") == {"a": 2, "b": 1}

    def test_empty(self):
        assert char_frequency("") == {}

    def test_with_spaces(self):
        result = char_frequency("a b")
        assert result["a"] == 1
        assert result[" "] == 1


class TestCaesarCipher:
    def test_shift(self):
        assert caesar_cipher("abc", 3) == "def"
        assert caesar_cipher("xyz", 3) == "abc"

    def test_uppercase(self):
        assert caesar_cipher("ABC", 3) == "DEF"

    def test_roundtrip(self):
        msg = "Hello World"
        assert caesar_cipher(caesar_cipher(msg, 13), -13) == msg

    def test_non_alpha_stays(self):
        assert caesar_cipher("123!!", 5) == "123!!"
