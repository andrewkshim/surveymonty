import surveymonty.utils as utils
import unittest


class TestClient(unittest.TestCase):

    def test_finalize_headers(self):
        stub_access_token = 'STUB_ACCESS_TOKEN'
        expected_headers = {
            'Authorization': 'Bearer {}'.format(stub_access_token),
            'Content-Type': 'application/json'
        }
        self.assertDictEqual(
            utils.finalize_headers({}, stub_access_token),
            expected_headers
        )

    def test_clean_url_fragment(self):
        expected_str = 'hello'
        self.assertEqual(utils.clean_url_fragment('hello/'), expected_str)
        self.assertEqual(utils.clean_url_fragment('/hello/'), expected_str)

    def test_make_url(self):
        expected_url_a = 'https://api.surveymonkey.net/v3/endpoint'
        self.assertEqual(utils.make_url('v3', '/endpoint'), expected_url_a)

        expected_url_b = 'https://test.surveymonty.com/foo/bar'
        self.assertEqual(
                utils.make_url('foo', 'bar', host='https://test.surveymonty.com'),
            expected_url_b
        )

    def test_parse_url_params(self):
        expected_params = ['hello', 'world']
        self.assertEqual(
            utils.parse_url_params('/surveys/{hello}/details/{world}'),
            expected_params
        )

    def test_make_full_endpoint(self):
        expected_endpoint = '/surveys/foo/details/bar'
        self.assertEqual(
            utils.make_full_endpoint(
                '/surveys/{hello}/details/{world}',
                ['hello', 'world'],
                ['foo', 'bar']
            ),
            expected_endpoint
        )

    def test_load_version_config(self):
        self.assertIsInstance(utils.load_version_config(), dict)


if __name__ == "__main__":
    unittest.main()
