"""
This module contains functions for validating names of variables and replacement strings.
"""

import string
from typing import Optional

ALLOWED_PUNCTUATION = "!#%&*+,-./ :;<=>?@^_`|~"
VALID_VARIABLE_CHARS = string.ascii_letters + " " + string.digits + ALLOWED_PUNCTUATION
VALID_REPLACEMENT_STR_CHARS = string.ascii_letters + ALLOWED_PUNCTUATION


class NamingError(Exception):
    """Exception raised for errors in naming objects.
    Atributes:
        - char: The character which caused the error
        - message: explanation of the error
    """

    def __init__(
        self, name: str, char: Optional[str] = None, message: Optional[str] = None
    ) -> None:
        self.name = name
        self.char = char

        if char:
            default_message = f"Unexpected character '{char}' in '{name}'"
        else:
            default_message = f"Invalid name: {name}"

        message = message + f" (name : {name})" if message else default_message
        super().__init__(message)


def check_name_valid(var_name: str):
    """
    Variable names must follow the following rules:
    - Can only contain letters, numbers, spaces and allowed punctuation
    """
    if var_name.replace(" ", "") == "":
        raise NamingError(var_name, message=f"Cannot use empty string as variable name")

    for char in var_name:
        if not char in VALID_VARIABLE_CHARS:
            raise NamingError(var_name, char)


def check_replacement_string_valid(replacement_str: str):
    """
    Replacement strings must follow the following rules:
    - Can only contain letters, allowed punctuation and replacment specifiers, denoted by $ followed by a number
    To ensure that the replacement string is valid, we must check that:
    - Cannot start with a number
    - Cannot end with a $
    - All $ must be followed by a number
    - All numbers must be preceded by a $
    """

    if replacement_str.replace(" ", "") == "":
        raise NamingError(
            replacement_str, message=f"Cannot use empty string as variable name"
        )

    for i, char in enumerate(replacement_str):
        if char not in VALID_REPLACEMENT_STR_CHARS + "123456789$":
            raise NamingError(replacement_str, char)

        if char == "$":
            # All $ are followed by numbers
            if i == len(replacement_str) - 1:
                raise NamingError(
                    replacement_str, message="Replacement string cannot end with $"
                )

            next_char = replacement_str[i + 1]
            if not next_char.isdigit() or next_char == "0":
                raise NamingError(
                    replacement_str,
                    next_char,
                    message=f"Only positive numbers can follow '$' in replacement string. Not {next_char}",
                )

        if char.isdigit():
            # All numbers are following $s
            if i == 0:
                raise NamingError(
                    replacement_str,
                    message=f"Cant start replacement string with number",
                )

            prev_char = replacement_str[i - 1]
            if not prev_char in "0123456789$":
                raise NamingError(
                    replacement_str,
                    prev_char,
                    message=f"Digit must be acompaining '$' in replacement st",
                )
