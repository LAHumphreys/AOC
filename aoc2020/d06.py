from tools.file_loader import load_string_groups
from tools.list_ops import count_items_across_groups


def merge_group(groups):
    result = 0
    for group in groups:
        answers = count_items_across_groups(group)
        result += len(answers)
    return result


def match_group(groups):
    count = 0
    for group in groups:
        answers = count_items_across_groups(group)
        for character in answers.items():
            if character[1] == len(group):
                count += 1
    return count


if __name__ == "__main__":
    def main():
        groups = load_string_groups("input/d06.txt")
        count = merge_group(groups)
        match_count = match_group(groups)
        print("At least one yes: {0}".format(count))
        print("Everyone is yes: {0}".format(match_count))


    main()
