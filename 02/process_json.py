'''
json может состоять из вложенных словарей.
если ключ, указанный в required_keys, содержит вложенный словарь,
решение будет искать токены во всём вложенном словаре.

если встречается несколько вхождений токена в строку,
учитываются только с разным регистром

в задаче не было сказано, что порядок важен, поэтому
порядок может быть изменён из-за использования set
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
            find_suitable_keys(d[key], _in_required=key in required_keys,
                               required_keys=required_keys, _result=_result)
        else:
            if _in_required or key in required_keys:
                _result.append((key, d[key]))
    return _result


def process_value(key: str, value: str, tokens: set[str] | None = None,
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
    required_keys = set(required_keys)
    tokens = set(tokens)
    suitable_pairs = find_suitable_keys(parsed, required_keys=required_keys)
    for key, value in suitable_pairs:
        process_value(key, value, tokens=tokens, callback=callback)

# required_keys = ["key1", "key2"]
# tokens = ["sub", "word2"]
# result = []
# process_json(json_str2, required_keys, tokens,
#              lambda key, token: result.append((key, token)))
# print(result)

#
# '''
# json может состоять из вложенных словарей.
# если ключ, указанный в required_keys, содержит вложенный словарь,
# функция будет искать токены во всём вложенном словаре.
# '''
#
# import json
# from typing import Callable
#
#
# def find_keys(d: dict, required_keys: set[str] | None = None,
#               tokens: set[str] | None = None,
#               callback: Callable[[str, str], None] | None = None,
#               _in_required=False):
#     '''
#     Рекурентно ищет ключи словаря d, значение по которым не содержат словарей.
#     Если ключ находится в required_keys, он и все вложенные ключи
#     считаются подходящими (_in_required=True). Для значений конечных
#     ключей с _in_required=True выполняется обработка по заданию
#     '''
#     for key in d:
#         if key in required_keys:
#             _in_required = True
#         if isinstance(d[key], dict):
#             find_keys(d[key], _in_required=_in_required,
#                       required_keys=required_keys, tokens=tokens,
#                       callback=callback)
#         else:
#             if _in_required:
#                 process_values(key, d[key], tokens=tokens, callback=callback)
#
#
# def process_values(key: str, value: str, tokens: set[str] | None = None,
#                    callback: Callable[[str, str], None] | None = None):
#     if isinstance(value, str):
#         value_lower = value.lower()
#         for token in tokens:
#             if token in value_lower:
#                 token_start_index = value_lower.index(token)
#                 token_with_registor = value[
#                                       token_start_index:token_start_index + len(
#                                           token)
#                                       ]
#                 callback(key, token_with_registor)
#
#
# def process_json(
#         json_str: str,
#         required_keys: list[str] | None = None,
#         tokens: list[str] | None = None,
#         callback: Callable[[str, str], None] | None = None,
# ) -> None:
#     parsed = json.loads(json_str)
#
#     required_keys = set(required_keys)
#     tokens = {i.lower() for i in tokens}
#
#     find_keys(parsed, required_keys=required_keys, tokens=tokens,
#               callback=callback)
#
# # d = {
# #     'key1': 'val1',
# #     'key2': {
# #         'subkey1': 'Word1 word2',
# #         'subkey2': ['word2', 'word3'],
# #         'subkey3': {
# #             'subsub': 'word1 word3'
# #         }
# #     }
# # }
# # # print(json.dumps(d, indent='    '))
#
# json_str = '{"key1": "Word1 word2", "key2": "word2 word3"}'
# required_keys = ["key1", "KEY2"]
# tokens = ["WORD1", "word2"]
# result = []
# process_json(json_str, required_keys, tokens,
#              lambda key, token: result.append((key, token)))
# print(result)


# def process_value(key: str, value: str, tokens: set[str] | None = None,
#                   callback: Callable[[str, str], None] | None = None) -> None:
#     if not isinstance(value, str):
#         return
#     value_lower = value.lower()
#     tokens = {i.lower() for i in tokens}
#     processed_tokens = set()
#     for token in tokens:
#         start_find_index = 0
#         while True:
#             if token in value_lower:
#                 token_start_index = value_lower.find(token,
#                                                      start_find_index)
#                 if token_start_index == -1: break
#                 token_with_registor = value[
#                                       token_start_index:token_start_index + len(
#                                           token)
#                                       ]
#
#                 # для поиска дальнейших совпадений
#                 start_find_index = token_start_index + 1
#
#                 if token_with_registor in processed_tokens: continue
#                 callback(key, token_with_registor)
#                 processed_tokens.add(token_with_registor)
#
#
#             else:
#                 break
