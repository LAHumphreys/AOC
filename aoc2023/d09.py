from dataclasses import dataclass
from tools.file_loader import load_string_groups
from itertools import pairwise
from math import factorial, fabs


@dataclass
class PolynomialTerm:
    coefficient: float
    power: int


def get_diffs(series: list[int]) -> list[int]:
    return [b - a for a, b in pairwise(series)]


def apply_polynomial(number: float, terms: list[PolynomialTerm]):
    result = 0
    for term in terms:
        result += term.coefficient * number ** term.power
    return result


def calculate_top_order_term(series: list[int]) -> PolynomialTerm:
    diffs = [series]
    while sum([fabs(x) for x in diffs[-1]]) / len(diffs) > 0.01:
        diffs += [get_diffs(diffs[-1])]
    polynomial_order = len(diffs)-2
    return PolynomialTerm(
         coefficient=diffs[-2][0]/factorial(polynomial_order),
         power=polynomial_order)


def reduce_series(series: list[int], terms: list[PolynomialTerm]) -> list[int]:
    reduced_series = (x - apply_polynomial(n + 1, terms) for n, x in enumerate(series))
    return [x for x in reduced_series]


def get_series_calculator(series: list[int]) -> list[PolynomialTerm]:
    term = calculate_top_order_term(series)
    terms = [term]
    while terms[-1].power > 1:
        reduced_series = reduce_series(series, terms)
        terms += [calculate_top_order_term(reduced_series)]
        if terms[-1].power >= terms[-2].power:
            raise ValueError
    if terms[-1].power == 1:
        # Need to calculate the final constant
        terms += [PolynomialTerm(
            power=0,
            coefficient=series[0] - apply_polynomial(1, terms))]

    return terms


def get_item(series: list[int], n: int = -1) -> int:
    if n < 0:
        n = len(series) + 1
    terms = get_series_calculator(series)
    return round(apply_polynomial(n, terms), 7)


def load_series(file_name: str) -> list[list[int]]:
    all_series = []
    with open(file_name) as input_file:
        for line in (line.replace("\n", "") for line in input_file.readlines()):
            all_series.append([int(x) for x in line.split()])
    return all_series


def part_one(all_series: list[list[int]]) -> int:
    total = 0
    for n, series in enumerate(all_series):
        total += round(get_item(series, len(series) + 1))
    return total


def part_two(all_series: list[list[int]]) -> int:
    total = 0
    for n, series in enumerate(all_series):
        total += round(get_item(series, 0))
    return total


def main():
    all_series = load_series("input/d09.txt")
    print(part_one(all_series))
    print(part_two(all_series))
    pass


if __name__ == "__main__":
    main()
