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
    in version control. The config should be a JSON object that looks like:

    {
        "access_token": "your_access_token",
        "test_survey_id": "id_for_a_survey_you_created"
    }

    The file should be named "surveymonkey.config.json" and should live in the
    root of this repo.

    Returns: (dict) the config
    """
    with open('./surveymonkey.config.json', 'r') as config:
        return json.load(config)


class TestAPI(unittest.TestCase):
    """Some very basic tests against the actual SurveyMonkey API."""

    def setUp(self):
        self.config = load_local_surveymonkey_config()
        self.client = surveymonty.Client(self.config['access_token'])

    def test_get_me(self):
        self.assertIsInstance(self.client.get_me(), dict)

    def test_get_groups(self):
        self.assertIsInstance(self.client.get_groups(), dict)

    def test_get_surveys(self):
        self.assertIsInstance(self.client.get_surveys(), dict)

    def test_get_survey(self):
        survey_id = self.config['test_survey_id']
        survey = self.client.get_survey(survey_id)
        self.assertIsInstance(survey, dict)
        self.assertEqual(survey['id'], survey_id)


if __name__ == "__main__":
    unittest.main()
