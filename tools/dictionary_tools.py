"""
Utilities for manipulating dictionary objects
"""


def build_dicts(definition: str):
    """
    Build a list of dictionaries based on a string definition of
    the form:
        key1:value1 key2:value2
        key3:value3

        key1:value1
        key2:value2 key3:value3
    :param definition: The string providing the definition in the format
                       specified above
    :return: A list, where each item corresponds to a dictionary defined
             in the string provided.
    """
    results = []
    this_dict = {}
    for line in definition.split("\n"):
        tokens = line.strip()
        if tokens == "":
            if len(this_dict) != 0:
                results.append(this_dict)
            this_dict = {}
        else:
            for pair in tokens.split(" "):
                parts = pair.split(":")
                if len(parts) != 2:
                    raise ValueError
                this_dict[parts[0]] = parts[1]

    if len(this_dict) != 0:
        results.append(this_dict)
    return results
