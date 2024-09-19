import unittest
from unittest import mock

from unittest.mock import patch
from predict import predict_message_mood


class TestPredictMessageMood(unittest.TestCase):
    def test_bad(self):
        with patch('predict.SomeModel.predict') as mock_model_predict:
            mock_model_predict.return_value = 0.1
            result = predict_message_mood('message', 0.2, 0.4)
            self.assertEqual('неуд', result)

            calls = [
                mock.call('message'),
            ]
            self.assertEqual(calls, mock_model_predict.mock_calls)

    def test_good(self):
        with patch('predict.SomeModel.predict') as mock_model_predict:
            mock_model_predict.return_value = 0.5
            result = predict_message_mood('hello', 0.2, 0.4)
            self.assertEqual('отл', result)

            calls = [
                mock.call('hello'),
            ]
            self.assertEqual(calls, mock_model_predict.mock_calls)

    def test_norm(self):
        with patch('predict.SomeModel.predict') as mock_model_predict:
            mock_model_predict.return_value = 0.3
            result = predict_message_mood('hello', 0.1, 0.4)
            self.assertEqual('норм', result)

            calls = [
                mock.call('hello'),
            ]
            self.assertEqual(calls, mock_model_predict.mock_calls)

    def test_args(self):
        with patch('predict.SomeModel.predict') as mock_model_predict:
            mock_model_predict.side_effect = [0.1, 0.4]

            one_arg = predict_message_mood('smth')
            self.assertEqual(one_arg, 'неуд')

            two_args = predict_message_mood('smth', good_thresholds=0.45)
            self.assertEqual(two_args, 'норм')

    @patch('predict.SomeModel.predict')
    def test_borders(self, mock_model_predict):
        mock_model_predict.return_value = 0.2
        result = predict_message_mood('qwerty',
                                      bad_thresholds=0.2,
                                      good_thresholds=0.9
                                      )
        self.assertEqual(result, 'норм')

    def test_changed_args(self):
        with self.assertRaises(ValueError):
            predict_message_mood('qwerty',
                                 bad_thresholds=0.9,
                                 good_thresholds=0.2
                                 )
