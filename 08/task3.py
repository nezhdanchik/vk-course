import cProfile
import pstats
import io


def profile_deco(func):
    all_stats = []

    def inner(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        res = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        sortby = "cumulative"
        ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
        ps.print_stats()
        all_stats.append(s.getvalue())
        return res

    def print_stat():
        print(f"Статистика для {func.__name__}".center(80, "-"))
        print(f"Всего было выполнено {len(all_stats)} вызовов".center(80, "-"))
        for ind, stat in enumerate(all_stats):
            print(f"Вызов {ind + 1}".center(80, "-"))
            print(stat)

    setattr(inner, "print_stat", print_stat)
    return inner


@profile_deco
def add(a, b):
    return a + b


@profile_deco
def sub(a, b):
    return a - b


add(1, 2)
add(4, 5)
sub(4, 5)

add.print_stat()
sub.print_stat()
