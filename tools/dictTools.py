def build_dicts(definition):
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
