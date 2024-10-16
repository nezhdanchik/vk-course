def retry_deco(limit=1, allowed_exceptions:list[Exception]|None=None):
    if not allowed_exceptions:
        allowed_exceptions = []

    allowed_exceptions = tuple(allowed_exceptions)

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
                except allowed_exceptions as err: # pylint: disable=catching-non-exception
                    print(log_attempt + f'exception = {err.__class__.__name__}')
                    raise err
                except Exception as err:  # pylint: disable=broad-except
                    print(log_attempt + f'exception = {err.__class__.__name__}')
                    if i == limit:
                        raise err
                else:
                    print(log_attempt + f'result = {res}')
                    return res
            return None

        return inner

    return outer
