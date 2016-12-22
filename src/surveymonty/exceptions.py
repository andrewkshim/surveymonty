"""
surveymonty.exceptions
----------------------
"""


class SurveyMontyError(Exception):
    """Base exception."""
    pass


class SurveyMontyAPIError(SurveyMontyError):
    """Error for non-2xx API responses."""

    def __init__(self, resp, *args):
        super(SurveyMontyAPIError, self).__init__(resp.content, *args)
        self.response = resp
