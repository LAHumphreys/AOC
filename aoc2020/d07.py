import copy
import re


def what_can_hold_me(bag_name, can_hold_map):
    bags = []
    inspected = 0
    if bag_name in can_hold_map:
        bags = copy.copy(can_hold_map[bag_name])

    while len(bags) > inspected:
        for bag in bags[inspected:]:
            inspected += 1
            if bag in can_hold_map:
                for extra_bag in can_hold_map[bag]:
                    if extra_bag not in bags:
                        bags.append(extra_bag)
    return bags


def what_must_I_hold(bag_name, holders):
    def add_bag(bag_name):
        if bag_name in holders:
            for new_bag in holders[bag_name]:
                new_bag_name = new_bag[1]
                new_bag_count = int(new_bag[0])
                for i in range(new_bag_count):
                    bags.append(new_bag_name)

    bags = []
    add_bag(bag_name)

    inspected = 0
    while len(bags) > inspected:
        for bag in bags[inspected:]:
            inspected += 1
            add_bag(bag)
    return bags
    pass


class PatternFailure(Exception):
    pass


if __name__ == "__main__":
    def main():
        name_pattern = re.compile("^([a-z]+ [a-z]+) bags contain")
        first_mandated_contain = re.compile("contain ([0-9]+) ([a-z]+ [a-z]+) bag")
        further_contains = re.compile(", ([0-9]+) ([a-z]+ [a-z]+) bag")
        no_other_bags = re.compile("contain no other")
        contains = {}
        can_hold_bag = {}
        contains_none = []
        with open("input/d07.txt") as f:
            for line in f.readlines():
                if line[-1] == "\n":
                    line = line[:-1]
                name_match = name_pattern.search(line)
                first_bag_match = first_mandated_contain.search(line)
                no_bags_match = no_other_bags.search(line)
                if name_match is None:
                    raise PatternFailure
                name = name_match.group(1)

                if no_bags_match is not None:
                    contains_none.append(name)
                    print("{0} <NONE>: {1}".format(name, line))
                elif first_bag_match is None:
                    raise PatternFailure
                else:
                    this_bag_contains = []
                    first_bag_count = first_bag_match.group(1)
                    first_bag_name = first_bag_match.group(2)
                    this_bag_contains.append((first_bag_count, first_bag_name))
                    for further_match in re.finditer(further_contains, line):
                        next_bag_count = further_match.group(1)
                        next_bag_name = further_match.group(2)
                        this_bag_contains.append((next_bag_count, next_bag_name))
                    print("{0} : {1}".format(name, line))
                    for bag in this_bag_contains:
                        print("    {0} {1}".format(bag[0], bag[1]))
                        inner_bag_name = bag[1]
                        if inner_bag_name not in can_hold_bag:
                            can_hold_bag[inner_bag_name] = [name]
                        else:
                            can_hold_bag[inner_bag_name].append(name)
                    contains[name] = this_bag_contains
            print(contains["shiny gold"])
            if "shiny gold" in can_hold_bag:
                print("Contains:")
                print(can_hold_bag["shiny gold"])
                holders = what_can_hold_me("shiny gold", can_hold_bag)
                print(holders)
                print(len(holders))
            if "shiny gold" in contains:
                print("I contain")
                children = what_must_I_hold("shiny gold", contains)
                print(children)
                print(len(children))


    main()
