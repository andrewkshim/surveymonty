import json
import logging
import os
import surveymonty.client
import sys
import unittest


def load_local_surveymonkey_config():
    """
    Loads your local SurveyMonkey config. This is a secret config that should 
    contain, among other things, your access token. Do not place this config
    in version control.

    Returns: (dict) the config
    """
    with open('./surveymonkey.config.json', 'r') as config:
        return json.load(config)


class TestAPI(unittest.TestCase):
    """Some very basic tests against the actual SurveyMonkey API."""

    def setUp(self):
        self.config = load_local_surveymonkey_config()
        self.client = surveymonty.client.SurveyMontyClient(self.config['access_token'])

    def test_get_me(self):
        self.assertIsInstance(self.client.get_me(), dict)

    def test_get_surveys(self):
        self.assertIsInstance(self.client.get_surveys(), dict)

    def test_get_groups(self):
        self.assertIsInstance(self.client.get_groups(), dict)


if __name__ == "__main__":
    if 'DEBUG' in os.environ:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
    unittest.main()
