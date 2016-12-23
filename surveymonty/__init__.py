import pkg_resources

from .client import Client


__version__ = pkg_resources.resource_string(
    'surveymonty', 'VERSION'
).decode('utf-8').strip()
