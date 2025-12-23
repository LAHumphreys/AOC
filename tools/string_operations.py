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


def subdivide(string: str, group_size: int) -> list[str]:
    """
    Subdivide a string into a list of parts of a parameter group size.
    Assumes group_size is a valid factor of the string length.
    """
    if len(string) % group_size != 0:
        raise ValueError("group_size must be a factor of string length")
    return [string[i:i + group_size] for i in range(0, len(string), group_size)]
