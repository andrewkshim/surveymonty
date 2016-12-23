import requests
import surveymonty.client
import surveymonty.utils as utils
import unittest
import unittest.mock


class TestClient(unittest.TestCase):

    def setUp(self):
        self.access_token = 'stub_access_token'
        self.client = surveymonty.Client(self.access_token)

    def assert_request_mock_called(self, mock_request, method, endpoint, **kwargs):
        url = utils.make_url(self.client.version, endpoint)
        headers = utils.finalize_headers({}, self.access_token)
        mock_request.assert_called_once_with(method, url, headers=headers, **kwargs)

    def test_v3(self):
        config = utils.load_version_config(version='v3')
        for api_spec in config['endpoints']:
            name = api_spec['name']
            endpoint = api_spec['endpoint']
            url_param_names = utils.parse_url_params(endpoint)
            api_fn = getattr(self.client, name)

            with unittest.mock.patch('requests.request') as mock_request:
                api_fn(*url_param_names)

            full_endpoint = utils.make_full_endpoint(
                endpoint,
                url_param_names,
                url_param_names
            )
            self.assert_request_mock_called(mock_request, api_spec['method'], full_endpoint)


if __name__ == "__main__":
    unittest.main()
