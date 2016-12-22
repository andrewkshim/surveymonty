import surveymonty.utils
import unittest


class TestClient(unittest.TestCase):

    def test_finalize_headers(self):
        stub_access_token = 'STUB_ACCESS_TOKEN'
        expected_headers = {
            'Authorization': 'Bearer {}'.format(stub_access_token),
            'Content-Type': 'application/json'
        }
        self.assertDictEqual(
            surveymonty.utils.finalize_headers({}, stub_access_token),
            expected_headers
        )


if __name__ == "__main__":
    unittest.main()
