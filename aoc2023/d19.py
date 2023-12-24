from enum import Enum
from dataclasses import dataclass
from typing import Optional
from tools.file_loader import load_string_groups


@dataclass
class Condition:
    variable: str
    destination: str
    min_value: Optional[int] = None
    max_value: Optional[int] = None


@dataclass
class Rule:
    name: str
    conditions: list[Condition]
    fallback: str


@dataclass
class Part:
    vars: dict[str, int]


@dataclass
class Input:
    parts: list[Part]
    rules: dict[str, Rule]


def load_input(file_name: str) -> Input:
    rules, parts = load_string_groups(file_name)
    return Input(parts=[parse_part(part) for part in parts],
                 rules={rule.name: rule for rule in (parse_rule(rule) for rule in rules)})


def is_part_accepted(part: Part, rules: dict[str, Rule]) -> bool:
    rule = rules["in"]
    while True:
        condition_met = False
        for condition in rule.conditions:
            condition_met = False
            value = part.vars[condition.variable]
            if condition.max_value is not None:
                condition_met = value < condition.max_value
            elif condition.min_value is not None:
                condition_met = value > condition.min_value
            if condition_met:
                if condition.destination == "A":
                    return True
                elif condition.destination == "R":
                    return False
                else:
                    rule = rules[condition.destination]
                break
        if not condition_met:
            if rule.fallback == "A":
                return True
            elif rule.fallback == "R":
                return False
            else:
                rule = rules[rule.fallback]


def parse_part(part_str: str) -> Part:
    return Part(vars={key: int(value) for key, value in (part.split("=") for part in part_str[1:-1].split(","))})




def parse_rule(details: str) -> Rule:
    name, rest = details.split("{")
    conditions = []
    tokens = rest[:-1].split(",")
    for token in tokens[:-1]:
        condition_str, destination = token.split(":")
        if ">" in condition_str:
            variable, value = condition_str.split(">")
            conditions.append(Condition(variable=variable, destination=destination, min_value=int(value)))
        else:
            variable, value = condition_str.split("<")
            conditions.append(Condition(variable=variable, destination=destination, max_value=int(value)))

    return Rule(name=name, conditions=conditions, fallback=tokens[-1])


def part_one(details: Input) -> int:
    total = 0
    for part in details.parts:
        if is_part_accepted(part, details.rules):
            total += sum(part.vars.values())
    return total


def main():
    details = load_input("input/d19.txt")
    print(part_one(details))
    pass


if __name__ == "__main__":
    main()
