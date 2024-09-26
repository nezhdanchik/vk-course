def retry_deco(limit=1, exceptions=None):
    if not exceptions:
        exceptions = []

    def outer(function):
        def inner(*args, **kwargs):
            log = f'run "{function.__name__}"'
            if args or kwargs:
                log += ' with '
            if args:
                log += f'positional args = {args}, '
            if kwargs:
                log += f'keyword kwargs = {kwargs}, '
            for i in range(1, limit + 1):
                log_attempt = log + f'attempt = {i}, '
                try:
                    res = function(*args, **kwargs)
                except Exception as err:
                    err_type = err.__class__
                    print(log_attempt + f'exception = {err_type.__name__}')
                    if err_type in exceptions:
                        return None
                else:
                    print(log_attempt + f'result = {res}')
                    return res
            return None

        return inner

    return outer


# @retry_deco(3)
# def add(a, b):
#     return a + b
#
#
# add(4, 2)
# # run "add" with positional args = (4, 2), attempt = 1, result = 6
# #
# add(4, b=3)
#
#
# # run "add" with positional args = (4,), keyword kwargs = {"b": 3}, attempt = 1, result = 7
#
#
# @retry_deco(3)
# def check_str(value=None):
#     if value is None:
#         raise ValueError()
#
#     return isinstance(value, str)
#
#
# check_str(value="123")
# # run "check_str" with keyword kwargs = {"value": "123"}, attempt = 1, result = True
#
# check_str(value=1)
# # run "check_str" with keyword kwargs = {"value": 1}, attempt = 1, result = False
#
# check_str(value=None)
#
#
# # run "check_str" with keyword kwargs = {"value": None}, attempt = 1, exception = ValueError
# # run "check_str" with keyword kwargs = {"value": None}, attempt = 2, exception = ValueError
# # run "check_str" with keyword kwargs = {"value": None}, attempt = 3, exception = ValueError
#
#
# @retry_deco(2, [ValueError])
# def check_int(value=None):
#     if value is None:
#         raise ValueError()
#
#     return isinstance(value, int)
#
#
# check_int(value=1)
# # run "check_int" with keyword kwargs = {"value": 1}, attempt = 1, result = True
#
# check_int(value=None)
# # run "check_int" with keyword kwargs = {"value": None}, attempt = 1, exception = ValueError # нет перезапуска
