"""
Tools for manipulating / interrogating text strings
"""


def count_chars(text_string: str, count: dict):
    """
    Update the provided dictionary with a count of each character in the string object s
    """
    for character in text_string:
        if character in count:
            count[character] += 1
        else:
            count[character] = 1
