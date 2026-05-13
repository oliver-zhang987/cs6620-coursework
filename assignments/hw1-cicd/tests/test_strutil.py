"""Tests for src/strutil.py"""

import pytest
from src.strutil import reverse_words, is_palindrome, char_frequency, caesar_cipher  # noqa: E402


# ── reverse_words ────────────────────────────────────────────────────

class TestReverseWords:
    def test_basic(self):
        assert reverse_words("hello world") == "world hello"

    def test_single_word(self):
        assert reverse_words("hello") == "hello"

    def test_empty(self):
        assert reverse_words("") == ""

    def test_extra_spaces(self):
        assert reverse_words("  hello   world  ") == "world hello"

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            reverse_words(123)


# ── is_palindrome ────────────────────────────────────────────────────

class TestIsPalindrome:
    def test_simple_true(self):
        assert is_palindrome("racecar") is True

    def test_simple_false(self):
        assert is_palindrome("hello") is False

    def test_mixed_case(self):
        assert is_palindrome("Madam") is True

    def test_with_punctuation(self):
        assert is_palindrome("A man, a plan, a canal: Panama") is True

    def test_empty(self):
        assert is_palindrome("") is True

    def test_single_char(self):
        assert is_palindrome("x") is True

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            is_palindrome(12321)


# ── char_frequency ───────────────────────────────────────────────────

class TestCharFrequency:
    def test_basic(self):
        assert char_frequency("aab") == {"a": 2, "b": 1}

    def test_empty(self):
        assert char_frequency("") == {}

    def test_spaces_counted(self):
        freq = char_frequency("a b")
        assert freq == {"a": 1, " ": 1, "b": 1}

    def test_non_string_raises(self):
        with pytest.raises(TypeError):
            char_frequency(42)


# ── caesar_cipher ────────────────────────────────────────────────────

class TestCaesarCipher:
    def test_shift_3(self):
        assert caesar_cipher("abc", 3) == "def"

    def test_wrap_around(self):
        assert caesar_cipher("xyz", 3) == "abc"

    def test_uppercase(self):
        assert caesar_cipher("ABC", 3) == "DEF"

    def test_mixed(self):
        assert caesar_cipher("Hello, World!", 13) == "Uryyb, Jbeyq!"

    def test_negative_shift(self):
        assert caesar_cipher("def", -3) == "abc"

    def test_non_alpha_unchanged(self):
        assert caesar_cipher("123!@#", 5) == "123!@#"

    def test_roundtrip(self):
        original = "The quick brown fox"
        encrypted = caesar_cipher(original, 7)
        decrypted = caesar_cipher(encrypted, -7)
        assert decrypted == original

    def test_non_string_text_raises(self):
        with pytest.raises(TypeError):
            caesar_cipher(123, 3)

    def test_non_int_shift_raises(self):
        with pytest.raises(TypeError):
            caesar_cipher("abc", 3.0)
