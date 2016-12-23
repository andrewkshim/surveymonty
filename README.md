# SurveyMonty

**!!! NOTICE 2016-12-22 !!!** This project is no longer actively maintained.
It will work with the latest SurveyMonkey API (v3), but there are no
guarantees for later versions. This is a very light wrapper though,
read through the rest of this doc and you'll have a good idea on
how things work, so you'll be able to modify it yourself if you need to 😀.

SurveyMonty is a Python wrapper for the SurveyMonkey API. Why the name?
Because this is a wrapper in Python, and Python makes me think of
[Monty Python](http://en.wikipedia.org/wiki/Monty_Python).
Also, "monkey" and "Monty" both start with "mon".

This content is released under the [MIT License](./LICENSE.md).


# Installation
```bash
$ pip install surveymonty
```


# Usage
The SurveyMonty `Client` is a very lightweight wrapper over the
SurveyMonkey API and only exists for minor convenience.

The client requires your SurveyMonkey access token as its only argument:

```python
import surveymonty

client = surveymonty.Client("YOUR_ACCESS_TOKEN")
```

You should be able to find the access tokens in the Settings for
your SurveyMonkey apps: https://developer.surveymonkey.com/apps

The `client` has methods that correspond to the SurveyMonkey API
endpoints:

```python
# GET /surveys
surveys = client.get_surveys()
print(surveys)
{
  'page': 1,
  'data': [
    {
      'id': 'FOO',
      'href': 'https://api.surveymonkey.net/v3/surveys/FOO',
      'nickname': '',
      'title': 'FOO Survey'
    },
    {
      'id': 'BAR',
      'href': 'https://api.surveymonkey.net/v3/surveys/BAR',
      'nickname': '',
      'title': 'BAR Survey'
    }
  ],
  'total': 2,
  'per_page': 50,
  'links': {
    'self': 'https://api.surveymonkey.net/v3/surveys?page=1&per_page=50'
  }
}
```

You can find all of the supported API methods in the
[V3 config file](./surveymonty/versions/v3.json) which drives the
client. There's one entry for each endpoint e.g.:

```json
  {
    "name": "get_surveys",
    "method": "GET",
    "endpoint": "/surveys"
  }
```

The `name` corresponds to the method name on the `client` object,
while the `method` and `endpoint` correspond to a SurveyMonkey
API endpoint.

For API endpoints that require URL params, you must supply the
`client` method with corresponding arguments:

```python
# GET /surveys/your_survey_id
client.get_survey("your_survey_id")
```

To supply request body payloads or query params, you do the same
as you would with the [Python requests library](http://docs.python-requests.org/en/master/user/quickstart/):

```python
# GET /surveys?per_page=1
client.get_surveys(params={"per_page": 1})

# POST /surveys
client.create_survey(json={"title": "New Survey"})
```

In fact, any `**kwargs` that you pass into the `client` methods
will just get passed through to the `requests.request` method.


# Resources
- [SurveyMonkey API docs](https://developer.surveymonkey.com/api/v3/)
