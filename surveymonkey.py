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
        json_response = response.json()
        return json_response

    # Below are the specific API methods
    # every method has a default option=None arg, may be better way to
    # tease out this requirement to avoid repetition
    def get_survey_list(self, options=None):
        """Return surveys in JSON format"""
        endpoint = "surveys/get_survey_list"
        json_response = self.get_json_response(endpoint, options)
        survey_list = []
        if (json_response["data"] and json_response["data"]["surveys"]):
            survey_list = json_response["data"]["surveys"]
        else:
            print("No surveys available")
        return survey_list

    def get_survey_details(self, survey_id, options=None):
        """Return survey information in JSON format"""
        endpoint = "surveys/get_survey_details"
        json_response = {}
        survey = {}
        if survey_id:
            if options is None:
                options = {}
            options["survey_id"] = survey_id
            json_response = self.get_json_response(endpoint, options)
        if json_response["data"]:
            survey = json_response["data"]
        else:
            print("Survey {id} could not be found.").format(survey_id)
        return survey

    def get_collector_list(self, survey_id, options=None):
        endpoint = "surveys/get_collector_list"
        json_response = {}
        collector_list = {}
        if survey_id:
            if options is None:
                options = {}
            options["survey_id"] = survey_id
            json_response = self.get_json_response(endpoint, options)
        if json_response["data"]:
            collector_list = json_response["data"]
        else:
            print("Collectors for survey {id} not found.").format(survey_id)
        return collector_list

    def get_respondent_list(self, survey_id, options=None):
        endpoint = "surveys/get_respondent_list"
        respondent_list = {}
        if survey_id:
            if options is None:
                options = {}
            options["survey_id"] = survey_id
            json_response = self.get_json_response(endpoint, options)
        if json_response["data"]:
            respondent_list = json_response["data"]
        else:
            print("Respondents for survey {id} not found.").format(survey_id)
        return respondent_list

    # RESPONDENT_IDS have to be strings
    def get_reponses(self, respondent_ids, survey_id, options=None):
        endpoint = "surveys/get_responses"
        response_list = {}
        if respondent_ids and survey_id:
            if options is None:
                options = {}
            options["respondent_ids"] = respondent_ids
            options["survey_id"] = survey_id
            json_response = self.get_json_response(endpoint, options)
        print json_response
        if json_response["data"]:
            response_list = json_response["data"]
        else:
            print("Responses for survey {id} not found.").format(survey_id)
        return response_list

    def get_response_count(self, collector_id, options=None):
        endpoint = "surveys/get_response_counts"
        response_count = 0
        if collector_id:
            if options is None:
                options = {}
            options["collector_id"] = collector_id
            json_response = self.get_json_response(endpoint, options)
        if json_response["data"]:
            response_count = json_response["data"]
        return response_count

    def get_user_details(self, options=None):
        endpoint = "user/get_user_details"
        user_details = {}
        if options is None:
            options = {}
        json_response = self.get_json_response(endpoint, options)
        if json_response["data"]:
            user_details = json_response["data"]
        return user_details


class Survey(object):

    def __init__(self):
        pass
