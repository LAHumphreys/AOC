def count_chars(s: str, count: dict):
    for c in s:
        if c in count:
            count[c] += 1
        else:
            count[c] = 1
