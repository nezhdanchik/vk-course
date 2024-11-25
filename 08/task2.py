import cProfile, pstats, io
from task1 import Point, PointSlots, PointWithWeakRef, test_point_class_speed

point_classes = Point, PointSlots, PointWithWeakRef

for point_class in point_classes:
    print(
        f'---------------------------------------------'
        f' Профилирование класса {point_class.__name__} '
        f'---------------------------------------------'
    )
    pr = cProfile.Profile()
    pr.enable()
    test_point_class_speed(cls=point_class)
    pr.disable()

    s = io.StringIO()
    sortby = 'cumulative'
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())
