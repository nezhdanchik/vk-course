import cProfile
import pstats
import io

# pylint: disable=E0401
from task1 import (
    PersonDictAttrs,
    PersonSlots,
    PersonWithWeakRef,
    test_class_speed,
)

classes = PersonDictAttrs, PersonSlots, PersonWithWeakRef

for cls in classes:
    print(
        f"---------------------------------------------"
        f" Профилирование класса {cls.__name__} "
        f"---------------------------------------------"
    )
    pr = cProfile.Profile()
    pr.enable()
    test_class_speed(cls=cls, count=10**6 * 5)
    pr.disable()

    s = io.StringIO()
    SORT_BY = "cumulative"
    ps = pstats.Stats(pr, stream=s).sort_stats(SORT_BY)
    ps.print_stats()
    print(s.getvalue())
