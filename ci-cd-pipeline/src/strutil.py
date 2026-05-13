"""
String utility functions.
"""


def reverse_words(sentence):
    """Reverse word order in a sentence."""
    if not isinstance(sentence, str):
        raise TypeError(f"expected str, got {type(sentence).__name__}")
    return " ".join(sentence.split()[::-1])


def is_palindrome(text):
    """Check if text is a palindrome (ignoring case and non-alphanumeric chars)."""
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    cleaned = "".join(ch.lower() for ch in text if ch.isalnum())
    return cleaned == cleaned[::-1]


def char_frequency(text):
    """Count how many times each character appears."""
    if not isinstance(text, str):
        raise TypeError(f"expected str, got {type(text).__name__}")
    freq = {}
    for ch in text:
        freq[ch] = freq.get(ch, 0) + 1
    return freq


def caesar_cipher(text, shift):
    """Shift each letter by `shift` positions. Non-letters stay the same."""
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")
    if not isinstance(shift, int):
        raise TypeError(f"shift must be int, got {type(shift).__name__}")

    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base + shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)
