import copy
from unittest import TestCase

from custom_list import CustomList


class TestCustomList(TestCase):

    @staticmethod
    def _was_changed_deco(function):
        def inner(self, a, b, expected):
            before_a = copy.copy(a)
            before_b = copy.copy(b)
            function(self, a, b, expected)
            # проверяем, что a изменились, а b не изменились
            if isinstance(before_a, CustomList):
                self.assertTrue(before_a._eq_elements(a))
            elif isinstance(before_a, list):
                self.assertTrue(before_a == a)

            if isinstance(before_b, CustomList):
                self.assertTrue(before_b._eq_elements(b))
            elif isinstance(before_b, list):
                self.assertTrue(before_b == b)

        return inner

    @_was_changed_deco
    def change_sum(self, a, b, expected):
        self.assertTrue(expected._eq_elements(a + b))
        self.assertTrue(expected._eq_elements(b + a))

    @_was_changed_deco
    def change_sub(self, a, b, expected):
        diff_sign_expected = CustomList([-i for i in expected])
        self.assertTrue(expected._eq_elements(a - b))
        self.assertTrue(diff_sign_expected._eq_elements(b - a))

    def test_custom_list_operate(self):
        a = CustomList([5, 1, 3, 7])
        b = CustomList([1, 2, 7])
        self.change_sum(a, b, CustomList([6, 3, 10, 7]))
        self.change_sub(a, b, CustomList([4, -1, -4, 7]))

        a = CustomList([0])
        b = CustomList([1, 2, 7])
        self.change_sum(a, b, CustomList([1, 2, 7]))
        self.change_sub(a, b, CustomList([-1, -2, -7]))

        a = CustomList([0])
        b = CustomList([0])
        self.change_sum(a, b, CustomList([0]))
        self.change_sub(a, b, CustomList([0]))

        a = CustomList([-4, -2])
        b = CustomList([4, 2, 7])
        self.change_sum(a, b, CustomList([0, 0, 7]))
        self.change_sub(a, b, CustomList([-8, -4, -7]))

        self.change_sum(CustomList(), CustomList([0]), expected=CustomList([0]))
        self.change_sum(CustomList(), CustomList(), expected=CustomList())

        self.change_sub(CustomList(), CustomList([0]), expected=CustomList([0]))
        self.change_sub(CustomList(), CustomList(), expected=CustomList())

    def test_custom_list_operate_int(self):
        self.change_sum(10, CustomList([2, 5]), expected=CustomList([12, 15]))
        self.change_sub(10, CustomList([2, 5]), expected=CustomList([8, 5]))

        self.change_sum(0, CustomList([2, 5]), expected=CustomList([2, 5]))
        self.change_sub(0, CustomList([2, 5]), expected=CustomList([-2, -5]))

        self.change_sum(-2, CustomList([2, 5]), expected=CustomList([0, 3]))
        self.change_sub(-2, CustomList([2, 5]), expected=CustomList([-4, -7]))

        self.change_sum(-10, CustomList([10]), expected=CustomList([0]))
        self.change_sub(10, CustomList([10]), expected=CustomList([0]))

    def test_custom_list_operate_list(self):
        self.change_sum([2, 5], CustomList([10]), expected=CustomList([12, 5]))
        self.change_sub([2, 5], CustomList([10]), expected=CustomList([-8, 5]))

        self.change_sum([-2, 5], CustomList([10]), expected=CustomList([8, 5]))
        self.change_sub([-2, 5], CustomList([10]),
                        expected=CustomList([-12, 5]))

        self.change_sum([], CustomList([10]), expected=CustomList([10]))
        self.change_sub([], CustomList([10]), expected=CustomList([-10]))

        self.change_sum([], CustomList(), expected=CustomList())
        self.change_sub([], CustomList(), expected=CustomList())

    def test_lt(self):
        a = CustomList([5, 1, 3, 7])
        b = CustomList([1, 2, 7])
        self.assertLess(b, a)

    def test_gt(self):
        a = CustomList([5, 1, 3, 7])
        b = CustomList([1, 2, 7])
        self.assertGreater(a, b)

    def test_le(self):
        a = CustomList([1, 2, 3])
        b = CustomList([5, 1])
        c = CustomList([1, 2, -3])
        self.assertLessEqual(b, a)
        self.assertLessEqual(c, b)
        self.assertTrue(c <= b <= a)

    def test_ge(self):
        a = CustomList([1, 2, 3])
        b = CustomList([5, 1])
        c = CustomList([1, 2, -3])
        self.assertGreaterEqual(b, a)
        self.assertGreaterEqual(b, c)
        self.assertTrue(b >= a >= c)

    def test_eq(self):
        self.assertTrue(CustomList([2, 5]) == CustomList([2, 5]))
        self.assertEqual(CustomList([1, 2, 3]), CustomList([3, 3]))
        self.assertEqual(CustomList([1, 2, 3]), CustomList([6]))
