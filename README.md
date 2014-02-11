# SurveyMonty

This is a Python wrapper for the SurveyMonkey API. Why the name? Because this
is a wrapper in Python, and Python makes me think of [Monty Python][1]. Also,
"monkey" and "Monty" both start with "mon", hence SurveyMonty.

[1]:http://en.wikipedia.org/wiki/Monty_Python

# Installation
```bash
$ pip install surveymonty
```

# Example
This wrapper is very lightweight and provides no object encapsulation of the
responses. Rather, it provides the API methods in Python form, through which
you can obtain the JSON responses and do with them as you please.

Note, the API requires an access token and api key. You can provide these
either through environment variables or in the code itself.

### Setting credentials through environment variables
```bash
export SURVEY_MONKEY_ACCESS_TOKEN="YOUR_ACCESS_TOKEN"
export SURVEY_MONKEY_API_KEY="YOUR_API_KEY"
```

Sample Python script using SurveyMonty:
```python
import surveymonty

api = surveymonty.Client()
api.get_survey_list() # retrieve survey ids
api.get_survey_details(SURVEY_ID) # use a SURVEY_ID from above
```

### Setting credentials in code
Sample Python script using SurveyMonty:
```python
import surveymonty

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
API_KEY = "YOUR_API_KEY"

api = surveymonty.Client(ACCESS_TOKEN, API_KEY)
api.get_survey_list() # retrieve survey ids
api.get_survey_details(SURVEY_ID) # use a SURVEY_ID from above
```

## Available API Methods
- get\_survey\_details()
- get\_survey\_list()
- get\_collector\_list()
- get\_respondent\_list()
- get\_responses()
- get\_response\_count()
- get\_user\_details()

# License
This content is released under the [MIT License](./LICENSE.md).

