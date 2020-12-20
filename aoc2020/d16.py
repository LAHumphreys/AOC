import re
from enum import Enum

rule_parser = re.compile("([^:]+): ([0-9]+)-([0-9]+) or ([0-9]+)-([0-9]+)")


class TicketData:
    def __init__(self, lines):
        class ParseState(Enum):
            RULES = 1,
            SKIPPING = 2,
            YOUR_TICKET = 3,
            OTHER_TICKETS = 4

        state = ParseState.RULES
        self.all_tickets = []
        self.rules = {}

        for line in lines:
            if state == ParseState.RULES:
                match = rule_parser.match(line)
                if match:
                    rule_name = match.group(1)
                    first_range = (int(match.group(2)), int(match.group(3)))
                    second_range = (int(match.group(4)), int(match.group(5)))
                    self.rules[rule_name] = (first_range, second_range)
                else:
                    state = ParseState.SKIPPING
            if state == ParseState.YOUR_TICKET:
                self.your_ticket = [int(i) for i in line.split(",")]
                self.all_tickets.append(self.your_ticket)
                state = ParseState.SKIPPING
            elif state == ParseState.OTHER_TICKETS:
                self.all_tickets.append([int(i) for i in line.split(",")])
            elif state == ParseState.SKIPPING:
                if line == "your ticket:":
                    state = ParseState.YOUR_TICKET
                elif line == "nearby tickets:":
                    state = ParseState.OTHER_TICKETS

    def get_ticket(self):
        return self.your_ticket

    def get_all_tickets(self):
        return self.all_tickets

    def get_other_tickets(self):
        return self.all_tickets[1:]

    def get_rules(self):
        return self.rules


def number_is_valid(rule, number):
    valid = False
    if rule[0][0] <= number <= rule[0][1]:
        valid = True
    elif rule[1][0] <= number <= rule[1][1]:
        valid = True
    return valid


def validate_fields(rules, ticket):
    valid_fields = []
    for value in ticket:
        valid = []
        for rule_name in rules:
            if number_is_valid(rules[rule_name], value):
                valid.append(rule_name)
        valid_fields.append(valid)
        pass
    return valid_fields


def sum_invalid(ticket_data: TicketData):
    error_sum = 0
    for ticket in ticket_data.get_other_tickets():
        validation = validate_fields(ticket_data.get_rules(), ticket)
        for index, valid_values in enumerate(validation):
            if len(valid_values) == 0:
                error_sum += ticket[index]
    return error_sum


def determine_fields(ticket_data: TicketData):
    rules = ticket_data.get_rules()
    tickets = ticket_data.get_other_tickets()

    validation = [validate_fields(rules, ticket) for ticket in tickets]
    validation = [valid for valid in validation if [] not in valid]

    reference_ticket = validation[0]
    other_tickets = validation[1:]

    for index, field_list in enumerate(reference_ticket):
        def valid_for_all_tickets(field_to_check):
            return all([field_to_check in ticket[index] for ticket in other_tickets])

        reference_ticket[index] = [field for field in field_list
                                   if valid_for_all_tickets(field)]

    locked = {}
    while len(locked) != len(reference_ticket):
        locked = {field_list[0]: index
                  for index, field_list in enumerate(reference_ticket)
                  if len(field_list) == 1}

        for index, field_list in enumerate(reference_ticket):
            def valid_for_index(field_name):
                return field_name not in locked or locked[field_name] == index

            reference_ticket[index] = [field for field in field_list if valid_for_index(field)]

    return [item[0] for item in reference_ticket]


if __name__ == "__main__":
    def main():
        path = "input/d16.txt"
        with open(path) as file:
            lines = file.read().split("\n")
            data = TicketData(lines)
        print("error rate: {0}".format(sum_invalid(data)))
        product = 1
        for index, name in enumerate(determine_fields(data)):
            if "departure" in name:
                ticket_value = data.get_ticket()[index]
                product *= ticket_value
                print("{0}: {1} => {2}".format(index, name, ticket_value))
        print("Product: {0}".format(product))


    main()
