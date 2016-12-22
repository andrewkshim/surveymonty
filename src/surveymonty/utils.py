"""
surveymonty.utils
-----------------
"""
import json
import pkg_resources
import re

from . import constants


def finalize_headers(headers, access_token):
    new_headers = dict(headers)
    new_headers.update({
        'Authorization': 'Bearer {}'.format(access_token),
        'Content-Type': 'application/json'
    })
    return new_headers


def clean_url_fragment(f):
    return f.strip('/')


def make_url(version, endpoint, host=constants.DEFAULT_HOST):
    return '{}/{}/{}'.format(
        clean_url_fragment(host),
        clean_url_fragment(version),
        clean_url_fragment(endpoint)
    )


def parse_url_params(endpoint):
    return re.findall(r'{(\w+)}', endpoint)


def make_full_endpoint(endpoint, url_param_names, fn_args):
    url_params = {
        param_name: fn_args[index]
        for index, param_name in enumerate(url_param_names)
    }
    return endpoint.format(**url_params)


def load_version_config(version=constants.DEFAULT_VERSION):
    version_filename = '{}.json'.format(version)
    config_bytes = pkg_resources.resource_string(
        constants.VERSIONS_MODULE, version_filename
    )
    config_str = config_bytes.decode('utf-8')
    config = json.loads(config_str)
    return config
