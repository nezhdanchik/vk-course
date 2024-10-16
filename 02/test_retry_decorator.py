import io
import unittest
from unittest import mock

from retry_decorator import retry_deco


class TestRetryDeco(unittest.TestCase):
    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_without_params(self, mock_stdout):
        @retry_deco()
        def add(a, b):
            return a + b

        expected = []

        add(4, 2)
        expected += [
            'run "add" with positional args = (4, 2), attempt = 1, result = 6\n'
        ]

        add(4, b=3)
        expected += [
            '''run "add" with positional args = (4,), '''
            '''keyword kwargs = {'b': 3}, attempt = 1, result = 7\n'''
        ]

        add(a=11, b=2)
        expected += [
            '''run "add" with keyword kwargs = {'a': 11, 'b': 2}, '''
            '''attempt = 1, result = 13\n'''
        ]

        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_limit(self, mock_stdout):
        @retry_deco(3)
        def division(a, b):
            return a / b

        division(10, 2)
        expected = [
            '''run "division" with positional args = (10, 2), '''
            '''attempt = 1, result = 5.0\n'''
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

        with self.assertRaises(ZeroDivisionError):
            division(0, 0)
        expected += [
            '''run "division" with positional args = (0, 0), '''
            '''attempt = 1, exception = ZeroDivisionError\n''',
            '''run "division" with positional args = (0, 0), '''
            '''attempt = 2, exception = ZeroDivisionError\n''',
            '''run "division" with positional args = (0, 0), '''
            '''attempt = 3, exception = ZeroDivisionError\n''',
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_limit_with_changing_error_success(self, mock_stdout):
        calls = 0

        @retry_deco(5)
        def three_calls(message):
            nonlocal calls
            calls += 1
            if calls <= 1:
                raise ValueError
            if calls <= 2:
                raise IndexError
            return message

        three_calls('hello world')

        expected = [
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 1, exception = ValueError\n''',
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 2, exception = IndexError\n''',
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 3, result = hello world\n''',
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_limit_with_changing_error_fail(self, mock_stdout):
        calls = 0

        @retry_deco(2)
        def three_calls(message):
            nonlocal calls
            calls += 1
            if calls <= 1:
                raise ValueError
            if calls <= 2:
                raise IndexError
            return message

        with self.assertRaises(IndexError):
            three_calls('hello world')

        expected = [
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 1, exception = ValueError\n''',
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 2, exception = IndexError\n''',
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_exceptions(self, mock_stdout):
        @retry_deco(2, [ValueError])
        def check_int(value=None):
            if value is None:
                raise ValueError()
            return isinstance(value, int)

        check_int(value=1)
        expected = [
            '''run "check_int" with keyword kwargs = {'value': 1}, '''
            '''attempt = 1, result = True\n''',
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

        with self.assertRaises(ValueError):
            check_int(value=None)
        expected += [
            '''run "check_int" with keyword kwargs = {'value': None}, '''
            '''attempt = 1, exception = ValueError\n'''
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))

    @mock.patch('sys.stdout', new_callable=io.StringIO)
    def test_exceptions_with_changing_error(self, mock_stdout):
        calls = 0

        @retry_deco(5, [IndexError, ZeroDivisionError])
        def three_calls(message):
            nonlocal calls
            calls += 1
            if calls <= 1:
                raise ValueError
            if calls <= 2:
                raise IndexError
            return message

        with self.assertRaises(IndexError):
            three_calls('hello world')

        expected = [
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 1, exception = ValueError\n''',
            '''run "three_calls" with positional args = ('hello world',), '''
            '''attempt = 2, exception = IndexError\n''',
        ]
        self.assertEqual(mock_stdout.getvalue(), ''.join(expected))
