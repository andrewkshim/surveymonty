# SurveyMonty

This is a Python wrapper for the SurveyMonkey API. Why the name? Because this
is a wrapper in Python, and Python makes me think of [Monty Python][1]. Also,
"monkey" and "Monty" both start with "mon", hence SurveyMonty.

[1]:http://en.wikipedia.org/wiki/Monty_Python

# Installation
Simply copy [surveymonty.py](./surveymonty.py) to the directory of the calling
Python file.

# Example
This wrapper is very lightweight and provides no object encapsulation of the
responses. Rather, it provides the API methods in Python form, through which
you can obtain the JSON responses and do with them as you please.

Sample Python script using SurveyMonty:
```python
import surveymonty

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN" # A very long string of characters
API_KEY = "YOUR_API_KEY" # A not-as-long string of alphanumeric characters

api = surveymonty.SurveyMonty(ACCESS_TOKEN, API_KEY)
api.get_survey_list()
api.get_survey_details(SURVEY_ID)
```

## Available API Methods
- get\_survey\_details()
- get\_survey\_list()
- get\_collector\_list()
- get\_respondent\_list()
- get\_responses()
- get\_response\_count()
- get\_user\_details()

## TODO
- Make available through `pip`

# License
This content is provided under the [MIT License](./LICENSE.md).

