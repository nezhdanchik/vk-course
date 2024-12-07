from unittest import TestCase, IsolatedAsyncioTestCase
from unittest.mock import patch, MagicMock
from fetcher import URLDispatcher, ParseURLDispatcherArgs


class TestFetcherSync(TestCase):
    def test_url_generator(self):
        u = URLDispatcher(10, "test_urls.txt")
        urls = list(u.get_url_generator())
        self.assertEqual(
            urls, ["https://www.google.com", "https://www.python.org"]
        )

    def test_parse_args(self):
        self.assertEqual(
            ParseURLDispatcherArgs.parse("10 urls.txt"), (10, "urls.txt")
        )
        self.assertEqual(
            ParseURLDispatcherArgs.parse("-c 10 urls.txt"), (10, "urls.txt")
        )
        with self.assertRaises(ValueError):
            ParseURLDispatcherArgs.parse("10")
        with self.assertRaises(ValueError):
            ParseURLDispatcherArgs.parse("10 urls.txt 10")


class TestFetcherAsync(IsolatedAsyncioTestCase):
    async def test_fetch_all(self):
        u = URLDispatcher(2, "test_urls.txt")
        with patch("fetcher.URLDispatcher.get_title") as mock_get_response:
            mock_get_response.side_effect = ["google", "python"]
            result = await u.fetch_all()
            self.assertEqual(result, ["google", "python"])

    async def test_get_title(self):
        u = URLDispatcher(1, "test_urls.txt")
        fake_session = MagicMock()
        fake_response = MagicMock()
        fake_response.__aenter__.return_value = fake_response

        async def fake_read():
            return "<title>google</title>"

        fake_response.read.return_value = fake_read()
        fake_session.get.return_value = fake_response
        res = await u.get_title("https://www.google.com", fake_session)
        self.assertEqual(res, "google")
