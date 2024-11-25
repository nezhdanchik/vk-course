def profile_deco(func):
    def inner(*args, **kwargs):
        res = func(*args, **kwargs)
        # inner.count_calls += 1
        return res
    return inner

@profile_deco
def add(a, b):
    return a + b

add(1,2)
add(3,2)
print(add.count_calls)

