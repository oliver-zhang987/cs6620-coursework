"""
strutil.py – Handy string-processing utilities.

Each function is a self-contained helper that is easy to understand
and straightforward to test.
"""

from typing import Dict


def reverse_words(sentence: str) -> str:
    """Reverse the order of words in *sentence* while preserving each word.

    Parameters
    ----------
    sentence : str
        An input string of whitespace-separated words.

    Returns
    -------
    str
        The words in reverse order, separated by a single space.

    Raises
    ------
    TypeError
        If *sentence* is not a string.

    Examples
    --------
    >>> reverse_words("hello world")
    'world hello'
    """
    if not isinstance(sentence, str):
        raise TypeError(f"Expected str, got {type(sentence).__name__}")
    return " ".join(sentence.split()[::-1])


def is_palindrome(text: str) -> bool:
    """Check whether *text* is a palindrome (case-insensitive,
    ignoring non-alphanumeric characters).

    Parameters
    ----------
    text : str
        The string to test.

    Returns
    -------
    bool
        ``True`` if *text* is a palindrome, ``False`` otherwise.

    Raises
    ------
    TypeError
        If *text* is not a string.

    Examples
    --------
    >>> is_palindrome("A man, a plan, a canal: Panama")
    True
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def char_frequency(text: str) -> Dict[str, int]:
    """Return a mapping of each character in *text* to its frequency.

    Parameters
    ----------
    text : str
        The input string.

    Returns
    -------
    dict[str, int]
        Character → count mapping.

    Raises
    ------
    TypeError
        If *text* is not a string.

    Examples
    --------
    >>> char_frequency("aab")
    {'a': 2, 'b': 1}
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str, got {type(text).__name__}")
    freq: Dict[str, int] = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def caesar_cipher(text: str, shift: int) -> str:
    """Apply a Caesar cipher to *text* with the given *shift*.

    Only ASCII letters are shifted; all other characters are left unchanged.
    The shift wraps around the alphabet.

    Parameters
    ----------
    text : str
        The plaintext (or ciphertext) to transform.
    shift : int
        Number of positions to shift each letter.

    Returns
    -------
    str
        The transformed string.

    Raises
    ------
    TypeError
        If *text* is not a string or *shift* is not an integer.

    Examples
    --------
    >>> caesar_cipher("abc", 3)
    'def'
    >>> caesar_cipher("xyz", 3)
    'abc'
    """
    if not isinstance(text, str):
        raise TypeError(f"Expected str for text, got {type(text).__name__}")
    if not isinstance(shift, int):
        raise TypeError(f"Expected int for shift, got {type(shift).__name__}")

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)
