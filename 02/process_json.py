'''
json может состоять из вложенных словарей.
если ключ, указанный в required_keys, содержит вложенный словарь,
решение будет искать токены во всём вложенном словаре.

если встречается несколько вхождений токена в строку,
учитываются только с разным регистром

'''

import json
from typing import Callable


def find_suitable_keys(d: dict, required_keys: set[str] | None = None,
                       _in_required=False,
                       _result: list[tuple[str, str]] | None = None) \
        -> list[tuple[str, str]]:
    '''
    Рекурентно ищет пары (key, value) в словаре d с подходящими
    ключами и строчными значениями.

    Если ключ находится в required_keys, он и все вложенные ключи
    считаются подходящими (_in_required=True).

    :returns Пара (key, value), где value - строка, _in_required=True.
    '''
    if _result is None:
        _result = []
    for key in d:
        if isinstance(d[key], dict):
            find_suitable_keys(d[key],
                               _in_required=key in required_keys or
                               _in_required,
                               required_keys=required_keys, _result=_result)
        else:
            if isinstance(d[key], str) and (
                    _in_required or key in required_keys):
                _result.append((key, d[key]))
    return _result


def process_value(key: str, value: str, tokens: list[str] | None = None,
                  callback: Callable[[str, str], None] | None = None) -> None:
    if not isinstance(value, str):
        return
    value_lower = value.lower()
    for token in tokens:
        if token.lower() in value_lower:
            callback(key, token)


def process_json(
        json_str: str,
        required_keys: list[str] | None = None,
        tokens: list[str] | None = None,
        callback: Callable[[str, str], None] | None = None,
) -> None:
    parsed = json.loads(json_str)
    suitable_pairs = find_suitable_keys(parsed,
                                        required_keys=set(required_keys))
    unique_tokens = []
    for token in tokens:
        if token not in unique_tokens:
            unique_tokens.append(token)
    tokens = unique_tokens

    for key, value in suitable_pairs:
        process_value(key, value, tokens=tokens, callback=callback)
