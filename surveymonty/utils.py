"""
surveymonty.utils
-----------------
"""
import json
import pkg_resources
import re

from . import constants


def finalize_headers(headers, access_token):
    """
    Args:
        - headers: (dict-like) HTTP headers
        - access_token: (str) SurveyMonkey access token

    Returns: (dict) headers updated with values that should be in all requests
    """
    new_headers = dict(headers)
    new_headers.update({
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    })
    return new_headers


def clean_url_fragment(f):
    """
    Args:
        - f: (str)

    Returns: (str)
    """
    return f.strip('/')


def make_url(version, endpoint, host=constants.DEFAULT_HOST):
    """
    Args:
        - version: (str) e.g. "v3"
        - endpoint: (str): e.g. "/surveys"

    Kwargs:
        - host: (str) e.g. "https://api.surveymonkey.net"

    Returns: (str) full URL to be queried
    """
    return '{}/{}/{}'.format(
        clean_url_fragment(host),
        clean_url_fragment(version),
        clean_url_fragment(endpoint)
    )


def parse_url_params(endpoint):
    """
    Args:
        - endpoint: (str) e.g. "/survey/{survey_id}"

    Returns: (list of str) e.g. ["survey_id"]
    """
    return re.findall(r'{(\w+)}', endpoint)


def make_full_endpoint(endpoint, url_param_names, fn_args):
    """
    Args:
        - endpoint: (str) e.g. "/survey/{survey_id}"
        - url_param_names: (list of str) e.g. ["survey_id"]
        - fn_args: (list) e.g. ["id_1"]

    Returns: (str) the endpoint interpolated with the given args
             e.g. "/survey/id_1"
    """
    url_params = {
        param_name: fn_args[index]
        for index, param_name in enumerate(url_param_names)
    }
    return endpoint.format(**url_params)


def load_version_config(version=constants.DEFAULT_VERSION):
    """
    Kwargs:
        - version: (str) e.g. "v3" 

    Returns: (dict) endpoint config object for the given version
    """
    version_filename = '{}.json'.format(version)
    config = pkg_resources.resource_string(
        constants.VERSIONS_MODULE, version_filename
    ).decode('utf-8')
    return json.loads(config)
