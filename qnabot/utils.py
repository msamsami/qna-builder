from typing import Any


def parse_list_options(options: list) -> str:
    """Returns the parsed version of a list of options in string.

    Args:
        options (list): a list of options, parameters, or items to be parsed.

    Returns:
        str: comma-separated sequence of options with an 'or' after the last comma.
    """
    check_type_error('options', options, list())

    options_str = ', '.join([str(option) for option in options])
    last_comma_idx = options_str.rfind(',')

    if len(options) == 2:
        return options_str[:last_comma_idx] + ' or' + options_str[last_comma_idx + 1:]
    else:
        return options_str[:last_comma_idx + 2] + 'or' + options_str[last_comma_idx + 1:]


def value_error_message(name: str, value: Any, options: list) -> str:
    if len(options) == 1:
        return f"{value} is not a valid {name}. Only {options[0]} is supported"
    else:
        return f"{value} is not a valid {name}. Must be either {parse_list_options(options)}"


def type_error_message(name: str, value: Any, acceptable: Any) -> str:
    return f"{name} must be of type {type(acceptable).__name__}, {type(value).__name__} was given instead"


def check_value_error(name: str, value: Any, options: list):
    if value not in options:
        raise ValueError(value_error_message(name, value, options))


def check_type_error(name: str, value: Any, acceptable: Any):
    if not isinstance(value, type(acceptable)):
        raise TypeError(type_error_message(name, value, acceptable))
