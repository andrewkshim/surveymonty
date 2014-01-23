#!/usr/bin/env python
"""
@author: Andrew Shim

Python wrapper for SurveyMonkey API: https://developer.surveymonkey.com/
"""

import json
import requests

SURVEY_MONKEY_HOST = "https://api.surveymonkey.net"
API_VERSION = "v2"


class SurveyMontyError(Exception):
    """
    Custom SurveyMonkey Exception. Uses status code messages provided at:
    https://developer.surveymonkey.com/mashery/requests_responses
    """
    # Status codes correspond to indicies.
    STATUS_CODE_MESSAGES = [
        "Success",
        "Not Authenticated",
        "Invalid User Credentials",
        "Invalid Request",
        "Unknown User",
        "System Error"
    ]

    def __init__(self, status_code):
        """
        Args:
            status_code: Integer ranging from 0 to 5 inclusive.
        Returns:
            Called in constructor. Implicitly returns a SurveyMontyError
            instance.
        Raises:
            ValueError: When status_code is out of range.
        """
        if status_code in range(0,6):
            self.status_code = status_code
        else:
            raise ValueError("Status code out of range.")

    def __str__(self):
        """
        Returns:
            String representation of the SurveyMontyError instance.
        """
        return "SurveyMonkey API Error {status_code}: {message}".format(
            status_code=str(self.status_code),
            message=STATUS_CODE_MESSAGES[self.status_code]
        )


class SurveyMonty(object):
    """
    API object, call SurveyMonkey API methods on this object.
    """

    def __init__(self, access_token, api_key):
        """
        Initialize SurveyMonty instance with an HTTP session. Set the session
        header to contain the access token, and the session params to contain
        the API key. Subsequent calls to the API will be done through the
        instance's session.

        Args:
            access_token: A long alphanumeric string. Tied to a specific
                SurveyMonkey user account, and the owner of the account must
                authorize you (the developer) to access their token.
            api_key: An alphanumeric string (shorter than access_token).
                Specific to your developer account and can be viewed in your
                profile.

        Returns:
            Called in constructor, so you can say this method returns a
            SurveyMonty instance.
        """
        self.session = requests.session()
        self.session.headers = {
            "Authorization": "bearer %s" % access_token,
            "Content-Type": "application/json"
        }
        self.session.params = {
            "api_key": api_key
        }

    def _get_json_response(self, endpoint, options):
        """
        Generic method to query API, used by more specific API methods.

        Args:
            endpoint: A string containing the path to the API endpoint. This
                method constructs the full URI using this endpoint string.
            options: A dictionary containing options to format the JSON
                response. Specific option information is available for each
                API method at https://developer.surveymonkey.com/.

        Returns:
            A dictionary representative of the JSON response.
        """
        uri = "/".join([
            SURVEY_MONKEY_HOST,
            API_VERSION,
            endpoint
        ])
        if options is None:
            options = {}
        response = self.session.post(uri, data=json.dumps(options))
        json_response = response.json()
        if "status" in json_response and json_response["status"] == 0:
            return json_response
        else:
            pass

    # Below are the specific API methods
    # every method has a default option=None arg, may be better way to
    # tease out this requirement to avoid repetition
    def get_survey_list(self, options=None):
        """Return surveys in JSON format"""
        endpoint = "surveys/get_survey_lis"
        json_response = self._get_json_response(endpoint, options)
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
            json_response = self._get_json_response(endpoint, options)
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
            json_response = self._get_json_response(endpoint, options)
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
            json_response = self._get_json_response(endpoint, options)
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
            json_response = self._get_json_response(endpoint, options)
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
            json_response = self._get_json_response(endpoint, options)
        if json_response["data"]:
            response_count = json_response["data"]
        return response_count

    def get_user_details(self, options=None):
        endpoint = "user/get_user_details"
        user_details = {}
        if options is None:
            options = {}
        json_response = self._get_json_response(endpoint, options)
        if json_response["data"]:
            user_details = json_response["data"]
        return user_details

