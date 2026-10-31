"""Arithmetic with whole-number results, independent of the Flet interface."""

import re
from fractions import Fraction


def calculate(expression: str) -> int:
    """Evaluate basic arithmetic with precedence, truncating only the final result."""
    if any(character not in "0123456789+-/*" for character in expression):
        raise ValueError("Only use 0-9 and +-/*.")
    if not expression:
        raise ValueError("Enter a calculation.")

    tokens = re.findall(r"[0-9]+|[+*/-]", expression)
    position = 0

    def read_number():
        nonlocal position
        sign = 1
        if position < len(tokens) and tokens[position] in ("+", "-"):
            sign = -1 if tokens[position] == "-" else 1
            position += 1
        if position >= len(tokens) or not tokens[position].isdigit():
            raise ValueError("Enter a valid calculation, such as 12+6/3.")
        try:
            number = Fraction(int(tokens[position]) * sign)
        except ValueError:
            raise ValueError("That number is too long.") from None
        position += 1
        return number

    total = Fraction(0)
    term = read_number()
    while position < len(tokens):
        operator = tokens[position]
        position += 1
        number = read_number()
        if operator == "*":
            term *= number
        elif operator == "/":
            if number == 0:
                raise ValueError("Cannot divide by zero.")
            term /= number
        else:
            total += term
            term = number if operator == "+" else -number

    # Keep intermediate fractions exact and truncate toward zero at the end.
    return int(total + term)
