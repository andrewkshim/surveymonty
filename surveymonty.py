#!/usr/bin/env python
"""
@author: Andrew Shim

Python wrapper for SurveyMonkey API: https://developer.surveymonkey.com/
"""
import json
import math
import os
import requests
import time


SURVEY_MONKEY_HOST = "https://api.surveymonkey.net"
API_VERSION = "v2"


__version__ = "0.1.19"


def is_survey_monkey_status_code(status_code):
    return status_code in range(0, 6)


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
    MAX_QUERY_ATTEMPTS = 5  # number of times to ping API until giving up
    NUM_RESPONSES_PER_CALL = 100

    def __init__(self, access_token=None, api_key=None):
        """
        Access token and api key must be passed in or set in environment
        variables.

        Arguments:
            access_token: A long alphanumeric string. Tied to a specific
                SurveyMonkey user account, and the owner of the account must
                authorize you (the developer) to access their token.
            api_key: An alphanumeric string (shorter than access_token).
                Specific to your developer account and can be viewed in your
                profile.

        Returns:
            Called in constructor, so you can say this method returns a
            SurveyMonty instance.

        Raises:
            SurveyMontyError if access token and api key are not available.
        """
        if access_token and api_key:
            self._create_session(access_token, api_key)
        else:
            is_access_token_present = self.ACCESS_TOKEN_NAME in os.environ
            is_api_key_present = self.API_KEY_NAME in os.environ
            if is_access_token_present and is_api_key_present:
                access_token = os.environ[self.ACCESS_TOKEN_NAME]
                api_key = os.environ[self.API_KEY_NAME]
                self._create_session(access_token, api_key)
            else:
                raise SurveyMontyError(
                    "Missing {access_token} and {api_key} in env.".format(
                        access_token=self.ACCESS_TOKEN_NAME,
                        api_key=self.API_KEY_NAME
                    )
                )

    def _create_session(self, access_token, api_key):
        """
        Create HTTP session for API communication. Set the session
        header to contain the access token, and the session params to contain
        the API key. Subsequent calls to the API will be done through the
        instance's session.

        Arguments:
            access_token: A long alphanumeric string. Tied to a specific
                SurveyMonkey user account, and the owner of the account must
                authorize you (the developer) to access their token.
            api_key: An alphanumeric string (shorter than access_token).
                Specific to your developer account and can be viewed in your
                profile.
        """
        self.session = requests.session()
        self.session.headers = {
            "Authorization": "bearer %s" % access_token,
            "Content-Type": "application/json"
        }
        self.session.params = {
            "api_key": api_key
        }

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
        Raise a SurveyMontyAPIError based on the error message in the API
        response (if it exists).

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
        json_response = None
        for i in range(0, self.MAX_QUERY_ATTEMPTS):
            try:
                json_response = response.json()
            except ValueError:
                time.sleep(1)  # may have hit per second query limit
                response = self.session.post(uri, data=json.dumps(options))
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
                print("Collectors for survey {id} not found.").format(
                    survey_id
                )
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

    def _get_page_boundary_indicies(self, page_index, page_size, limit):
      """
      Convenience method to get the start and end indicies that will be used
      within an interable to get the elements for the corresponding page_index.
      For example, if a list has 200 elements and the page_size is 100, then
      that array has two pages. The first page has start_index 0 and end_index
      100 and corresponds to the first 100 elements. The second page has 100
      and 200 as its inidices and corresponds to the second 100 elements.

      Args:
          page_index: Integer index of page.
          page_size: Size of each page.
          limit: The maximum number of elements in the iterable.

      Returns:
          Tuple (integer, integer) corresponding to (start_index, end_index) of
          the page for the given page_index.
      """
      start_index = page_index * page_size
      if start_index > limit:
          raise SurveyMontyError("Page_index out of bounds.")
      end_index = start_index + page_size
      if end_index > limit:
          end_index = limit
      return start_index, end_index

    def get_responses(
        self, survey_id, respondent_ids,
        options=None, page_index=0
    ):
        """
        API method to get list of responses from respondents of a survey.
        https://developer.surveymonkey.com/mashery/get_responses

        SurveyMonkey limits the number of responses per request to 100, so this
        method returns the 100 responses that correspond to the page_index.
        If you want to get all of the responses, use the get_all_responses()
        convenience method.

        Args:
            survey_id: String representation of a survey ID number. Survey IDs
                can be obtained from get_survey_list().
            respondent_ids: List of respondent ID strings. Respondent IDs can
                be obtained from get_respondent_list().
            options: Same as other API methods.
            page_index: Integer index of results page. Index 0 corresponds to
                the first 100 responses, index 1 to the next 100, and so on.

        Returns:
            Dictionary containing the response information.
        """
        endpoint = "surveys/get_responses"
        response_list = {}
        if respondent_ids and survey_id:
            options = options or {}
            start_index, end_index = self._get_page_boundary_indicies(
                page_index,
                self.NUM_RESPONSES_PER_CALL,
                len(respondent_ids)
            )
            options["respondent_ids"] = [
                str(respondent_id) for respondent_id
                in respondent_ids[start_index: end_index]
            ]
            options["survey_id"] = str(survey_id)
            json_response = self._get_json_response(endpoint, options)
            if self._is_json_response_valid(json_response):
                response_list = json_response["data"]
            else:
                print("Responses for survey {id} not found.").format(survey_id)
        return response_list

    def get_all_responses(self, survey_id, respondent_ids, options=None):
        """
        Convenience method for getting all responses from a survey. Otherwise,
        provides same functionality as get_reponses().

        Args:
            survey_id: String representation of a survey ID number. Survey IDs
                can be obtained from get_survey_list().
            respondent_ids: List of respondent ID strings. Respondent IDs can
                be obtained from get_respondent_list().
            options: Same as other API methods.
            page_index: Integer index of results page. Index 0 corresponds to
                the first 100 responses, index 1 to the next 100, and so on.

        Returns:
            Dictionary containing the response information.
        """
        num_pages = int(math.ceil(
            len(respondent_ids) / float(self.NUM_RESPONSES_PER_CALL)
        ))
        all_reponses = []
        for page_index in range(0, num_pages):
          next_responses = self.get_responses(
            survey_id, respondent_ids, options, page_index
          )
          all_reponses += next_responses
        return all_reponses

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
