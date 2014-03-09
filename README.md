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
```python
import surveymonty

ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
API_KEY = "YOUR_API_KEY"

api = surveymonty.Client(ACCESS_TOKEN, API_KEY)
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

# License
This content is released under the [MIT License](./LICENSE.md).

# Changes
### 0.1.15
Bugfix

### 0.1.14
Bugfix

### 0.1.13
Bugfix

### 0.1.12
Changed order of arguments in `get_response`.

### 0.1.11
Updated `get_response` method to work with paged results.

### 0.1.10
Use wheel.

### 0.1.9
Fix.

### 0.1.8
Reattempt failed queries.

### 0.1.7
Remove print statement.

### 0.1.6
Bug fix.

### 0.1.5
Bug fix.

### 0.1.4
Input accepts numbers for IDs.

### 0.1.3
Made error handling more robust.

### 0.1.2
Bug fix.

### 0.1.1
Moved ACCESS\_TOKEN and API\_KEY access to environment variables.

