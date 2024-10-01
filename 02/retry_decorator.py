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
                except Exception as err:  # pylint: disable=broad-except
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
