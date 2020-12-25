import re

letter_rule = re.compile('"([a-z])"')

rule_pattern = re.compile(" *([0-9]+): (.*)")
single_rule_group = re.compile("^[ 0-9]*$")
double_rule_group = re.compile("^([ 0-9]* )[|]([ 0-9]*)$")
rule_extractor = re.compile("([0-9]+)")


class UnknownRule(Exception):
    pass


class UnknownDefinition(Exception):
    pass


def patch_rules(rules):
    rules["8"] = Rule("42 | 42 8")
    rules["11"] = Rule("42 31 | 42 11 31")


def get_matching_images(rule, rules, images):
    return [image for image in images if rule.exactly_matches(image, rules)]


def parse_input(path):
    with open(path) as file:
        result = parse_rules_and_images(file.read())
    return result


def parse_rules_and_images(definition):
    rules = {}
    images = []
    parsing_rules = True
    for line in definition.split("\n"):
        if line == "":
            parsing_rules = False
        elif parsing_rules:
            rule_match = rule_pattern.match(line)
            if rule_match:
                rules[rule_match.group(1)] = Rule(rule_match.group(2))
        else:
            images.append(line)

    return rules, images


def parse_ruleset(definition):
    return parse_rules_and_images(definition)[0]


class Rule:
    def __init__(self, definition):
        letter_match = letter_rule.match(definition)
        rule_group_match = single_rule_group.match(definition)
        double_group_match = double_rule_group.match(definition)
        self.starts_with = None
        self.sub_rules = []
        if letter_match is not None:
            self.starts_with = letter_match.group(1)
        elif rule_group_match:
            self.sub_rules.append(rule_extractor.findall(definition))
        elif double_group_match:
            self.sub_rules.append(rule_extractor.findall(double_group_match.group(1)))
            self.sub_rules.append(rule_extractor.findall(double_group_match.group(2)))
        else:
            raise UnknownDefinition

    def ruleset_matches(self, line, rules, ruleset):
        if len(ruleset) == 0:
            yield line
        else:
            if ruleset[0] not in rules:
                raise UnknownRule
            active_rule = rules[ruleset[0]]
            remaining_rules = ruleset[1:]
            for match in active_rule.get_matches(line, rules):
                for subset_match in self.ruleset_matches(match, rules, remaining_rules):
                    yield subset_match

    def get_matches(self, line, rules):
        if self.starts_with is not None:
            if len(line) > 0 and line[0] == self.starts_with:
                yield line[1:]
        else:
            for ruleset in self.sub_rules:
                for match in self.ruleset_matches(line, rules, ruleset):
                    yield match

    def matches(self, line, rules):
        matches = list(self.get_matches(line, rules))
        if len(matches) > 0:
            return True, matches[0]
        else:
            return False, ""

    def exactly_matches(self, line, rules):
        matches = self.matches(line, rules)
        return matches[0] and matches[1] == ""


if __name__ == "__main__":
    def main():
        rules, images = parse_input("input/d19.txt")
        matches = get_matching_images(rules["0"], rules, images)
        print("Number of matches: {0}".format(len(matches)))
        patch_rules(rules)
        matches = get_matching_images(rules["0"], rules, images)
        print("Number of matches (patched): {0}".format(len(matches)))


    main()
