#!/usr/bin/env python
"""
@author: Andrew Shim

"""

import json
import requests

SURVEY_MONKEY_HOST = "https://api.surveymonkey.net"
API_VERSION = "v2"


class SurveyMonkey(object):

    def __init__(self, access_token, api_key):
        self.client = requests.session()
        self.client.headers = {
            "Authorization": "bearer %s" % access_token,
            "Content-Type": "application/json"
        }
        self.client.params = {
            "api_key": api_key
        }

    def get_json_response(self, endpoint, options):
        """Generic method to query api, used by more specific methods"""
        uri = "/".join([
            SURVEY_MONKEY_HOST,
            API_VERSION,
            endpoint
        ])
        if options is None:
            options = {}
        response = self.client.post(uri, data=json.dumps(options))
        json_reponse = response.json()
        return json_reponse

    def get_survey_list(self, options=None):
        """Return surveys in JSON format"""
        endpoint = "surveys/get_survey_list"
        json_reponse = self.get_json_response(endpoint, options)
        survey_list = []
        if (json_reponse["data"] and json_reponse["data"]["surveys"]):
            survey_list = json_reponse["data"]["surveys"]
        else:
            print("No surveys available")
        return survey_list

    def get_survey_details(self, survey_id, options=None):
        endpoint = "surveys/get_survey_details"
        json_reponse = self.get_json_response(endpoint, options)
        survey = {}
        if (json_reponse["data"]):
            survey = json_reponse["data"]
        else:
            print("Survey {id} could not be found.").format(survey_id)
        return survey

    def get_collector_list(self):
        pass

    def get_respondent_list(self):
        pass

    def get_reponses(self):
        pass

    def get_response_count(self):
        pass

    def get_user_details(self):
        pass


class Survey(object):

    def __init__(self):
        pass


def main():
    api = SurveyMonkey()
    api.get_survey_list()

if __name__ == "__main__":
    main()
