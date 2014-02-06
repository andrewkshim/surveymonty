#!/usr/bin/env python
"""
@author: Andrew Shim

Python wrapper for SurveyMonkey API: https://developer.surveymonkey.com/
"""

import json
import os
import requests

SURVEY_MONKEY_HOST = "https://api.surveymonkey.net"
API_VERSION = "v2"

def is_survey_monkey_status_code(status_code):
    return status_code in range(0,6)

class SurveyMontyError(Exception):
  pass

class SurveyMontyAPIError(Exception):
    """
    Custom SurveyMonkey API Exception. Uses status code messages provided at:
    https://developer.surveymonkey.com/mashery/requests_responses
    """
    # Status codes correspond to indicies.
    STATUS_CODE_CATEGORIES = [
        "Success",
        "Not Authenticated",
        "Invalid User Credentials",
        "Invalid Request",
        "Unknown User",
        "System Error"
    ]

    def __init__(self, status_code, message):
        """
        Args:
            status_code: Integer ranging from 0 to 5 inclusive or equal to an
                HTTP status code.
        Returns:
            Called in constructor. Implicitly returns a SurveyMontyAPIError
            instance.
        """
        self.status_code = status_code
        if is_survey_monkey_status_code(status_code):
            self.category = self.STATUS_CODE_CATEGORIES[status_code]
        self.message = message or "No message available."

    def __str__(self):
        """
        Returns:
            String representation of the SurveyMontyAPIError instance.
        """
        return "Status code {status_code} {category} - {message}".format(
            status_code=str(self.status_code),
            category=self.category,
            message=self.message
        )


class Client(object):
    """
    API object, call SurveyMonkey API methods on this object.
    """
    ACCESS_TOKEN_NAME = "SURVEY_MONTY_ACCESS_TOKEN"
    API_KEY_NAME = "SURVEY_MONTY_API_KEY"

    def __init__(self):
        """
        Initialize SurveyMonty instance with an HTTP session. Set the session
        header to contain the access token, and the session params to contain
        the API key. Subsequent calls to the API will be done through the
        instance's session.

        Access token and api key must be set in environment variables.

        Returns:
            Called in constructor, so you can say this method returns a
            SurveyMonty instance.

        Raises:
            SurveyMontyError if access token and api key are not available.
        """
        is_access_token_present = self.ACCESS_TOKEN_NAME in os.environ
        is_api_key_present = self.API_KEY_NAME in os.environ
        if is_access_token_present and is_api_key_present:
          access_token = os.environ[self.ACCESS_TOKEN_NAME]
          api_key = os.environ[self.API_KEY_NAME]
          self.session = requests.session()
          self.session.headers = {
              "Authorization": "bearer %s" % access_token,
              "Content-Type": "application/json"
          }
          self.session.params = {
              "api_key": api_key
          }
        else:
          raise SurveyMontyError(
              "Missing {access_token} and {api_key} in environment.".format(
                access_token=self.ACCESS_TOKEN_NAME,
                api_key=self.API_KEY_NAME
              )
          )

    def _is_json_response_valid(self, json_response):
        """
        Check if JSON response is valid.

        Args:
            json_response: Dictionary representation of JSON.

        Returns:
            Boolean. True if valid, else False.
        """
        return "data" in json_response

    def _create_complete_uri(self, endpoint):
        """
        Construct the complete URI to query the SurveyMonkey API.

        Args:
            endpoint: A string representation of the path to the API endpoint.

        Returns:
            A string representation of the complete URI to the API endpoint.
        """
        return "/".join([
            SURVEY_MONKEY_HOST,
            API_VERSION,
            endpoint
        ])

    def _raise_exception(self, json_response):
        """
        Raise a SurveyMontyAPIError based on the error message in the API response
        (if it exists).

        Args:
            json_response: Dictionary containing the response data. This
                method should not be called unless there is an error, so we
                know the response should contain an error at this point.

        Returns:
            None

        Raises:
            SurveyMontyAPIError: If JSON response contains appropriate info.
            SurveyMontyError: If cannot find info in response.
        """

        message_key = "errmsg"
        status_key = "status"
        if status_key in json_response:
            status_code = int(json_response[status_key])
            if (is_survey_monkey_status_code(status_code) and
                    message_key in json_response):
                message = json_response[message_key]
                raise SurveyMontyAPIError(status_code, message)
        else:
            raise SurveyMontyError("Unknown error with API.")

    def _get_json_response(self, endpoint, options):
        """
        Generic method to query API, used by more specific API methods.

        Args:
            endpoint: A string representation of the path to the API endpoint.
            options: A dictionary containing options to format the JSON
                response. Specific option information is available for each
                API method at https://developer.surveymonkey.com/.

        Returns:
            A dictionary representation of the JSON response.
        """
        uri = self._create_complete_uri(endpoint)
        status_key = "status"
        if options is None:
            options = {}
        response = self.session.post(uri, data=json.dumps(options))
        json_response = response.json()
        is_json_okay = (
            json_response and
            status_key in json_response and
            json_response[status_key] == 0
        )
        if is_json_okay:
            return json_response
        else:
            self._raise_exception(json_response)

    def get_survey_list(self, options=None):
        """
        API method to get list of all surveys pertaining to user access token.
        https://developer.surveymonkey.com/mashery/get_survey_list

        Args:
            options: Optional dictionary to be sent as request data. Options
                for this particular methods can be found at respective link.

        Returns:
            Dictionary containing the survey list information.
        """
        endpoint = "surveys/get_survey_list"
        json_response = self._get_json_response(endpoint, options)
        survey_list = []
        if self._is_json_response_valid(json_response):
            survey_list = json_response["data"]
        else:
            print("No surveys available.")
        return survey_list

    def get_survey_details(self, survey_id, options=None):
        """
        API method to get details for a single survey.
        https://developer.surveymonkey.com/mashery/get_survey_details

        Args:
            survey_id: String representation of a survey ID number. Survey IDs
                can be obtained from get_survey_list().
            options: Same as get_survey_list().

        Returns:
            Dictionary containing the survey object.
        """
        endpoint = "surveys/get_survey_details"
        survey = {}
        if survey_id:
            options = options or {}
            options["survey_id"] = str(survey_id)
            json_response = self._get_json_response(endpoint, options)
            print json_response
            if self._is_json_response_valid(json_response):
                survey = json_response["data"]
            else:
                print("Survey {id} could not be found.").format(survey_id)
        return survey

    def get_collector_list(self, survey_id, options=None):
        """
        API method to get list of collectors for a survey. A collector is an
        instance of a survey and is what the survey-takers interact with.
        https://developer.surveymonkey.com/mashery/get_collector_list

        Args:
            Same as get_survey_details().

        Returns:
            Dictionary containing the collector information.
        """
        endpoint = "surveys/get_collector_list"
        collector_list = {}
        if survey_id:
            options = options or {}
            options["survey_id"] = str(survey_id)
            json_response = self._get_json_response(endpoint, options)
            if self._is_json_response_valid(json_response):
                collector_list = json_response["data"]
            else:
                print("Collectors for survey {id} not found.").format(survey_id)
        return collector_list

    def get_respondent_list(self, survey_id, options=None):
        """
        API method to get list of respondents for a survey.
        https://developer.surveymonkey.com/mashery/get_respondent_list

        Args:
            Same as get_survey_details().

        Returns:
            Dictionary containing the respondent information.
        """
        endpoint = "surveys/get_respondent_list"
        respondent_list = {}
        if survey_id:
            options = options or {}
            options["survey_id"] = str(survey_id)
            json_response = self._get_json_response(endpoint, options)
        if self._is_json_response_valid(json_response):
            respondent_list = json_response["data"]
        else:
            print("Respondents for survey {id} not found.").format(survey_id)
        return respondent_list

    def get_responses(self, respondent_ids, survey_id, options=None):
        """
        API method to get list of responses from respondents of a survey.
        https://developer.surveymonkey.com/mashery/get_responses

        Args:
            respondent_ids: List of respondent ID strings. Respondent IDs can
                be obtained from get_respondent_list().
            survey_id: String representation of a survey ID number. Survey IDs
                can be obtained from get_survey_list().
            options: Same as other API methods.

        Returns:
            Dictionary containing the response information.
        """
        endpoint = "surveys/get_responses"
        response_list = {}
        if respondent_ids and survey_id:
            options = options or {}
            options["respondent_ids"] = [str(respondent_id) for respondent_id
                in respondent_ids]
            options["survey_id"] = str(survey_id)
            json_response = self._get_json_response(endpoint, options)
            if self._is_json_response_valid(json_response):
                response_list = json_response["data"]
            else:
                print("Responses for survey {id} not found.").format(survey_id)
        return response_list

    def get_response_count(self, collector_id, options=None):
        """
        API method to get count of reponses for a collector.
        https://developer.surveymonkey.com/mashery/get_responses

        Args:
            collector_id: String representation of collector ID number.
                Collector IDs can be obtained from get_collector_list().
            options: Same as other API methods.

        Returns:
            Dictionary containing the counts of the response types.
        """
        endpoint = "surveys/get_response_counts"
        response_count = 0
        if collector_id:
            options = options or {}
            options["collector_id"] = str(collector_id)
            json_response = self._get_json_response(endpoint, options)
            if self._is_json_response_valid(json_response):
                response_count = json_response["data"]
        return response_count

    def get_user_details(self, options=None):
        """
        API method to get details on the user pertaining to the access token.
        https://developer.surveymonkey.com/mashery/get_user_details

        Args:
            options: Same as other API methods.

        Returns:
            Dictionary containing the user information.
        """
        endpoint = "user/get_user_details"
        user_details = {}
        json_response = self._get_json_response(endpoint, options)
        if self._is_json_response_valid(json_response):
            user_details = json_response["data"]
        return user_details

