import json
import logging
import requests

from . import constants, utils
from .exceptions import SurveyMontyAPIError


_logger = logging.getLogger(__name__)


class SurveyMontyClient(object):

    def __init__(self, access_token, version=constants.DEFAULT_VERSION):
        self.version = version

        config = utils.load_version_config(version)
        for api_spec in config['endpoints']:
            api_fn = self._make_api_fn(api_spec, access_token)
            setattr(self, api_spec['name'], api_fn)

    def _make_api_fn(self, api_spec, access_token):
        endpoint = api_spec['endpoint']
        name = api_spec['name']
        url_param_names = utils.parse_url_params(endpoint)

        def api_fn(*args, **request_kwargs):
            if len(args) != len(url_param_names):
                msg = '{} expects {} arg(s) but received {}'.format(
                    name,
                    len(url_param_names),
                    len(args)
                )
                raise ValueError(msg)

            return self._request(
                api_spec['method'],
                utils.make_full_endpoint(endpoint, url_param_names, args),
                access_token,
                **request_kwargs
            )

        api_fn.__name__ = str(name)
        return api_fn

    def _request(self, method, endpoint, access_token, **request_kwargs):
        request_kwargs['headers'] = utils.finalize_headers(
            request_kwargs.get('headers', {}),
            access_token
        )
        url = utils.make_url(self.version, endpoint)
        resp = requests.request(method, url, **request_kwargs)

        if not resp.ok:
            raise SurveyMontyAPIError(resp)

        try:
            payload = resp.json()
        except ValueError:
            msg = 'unexpected SurveyMonkey API response, no JSON payload'
            raise SurveyMontyAPIError(resp, msg)

        _logger.debug('response for %s %s %r', method, endpoint, payload)
        return payload
