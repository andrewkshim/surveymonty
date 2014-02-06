#!/usr/bin/env python
"""
@author: Andrew Shim

Code example of SurveyMonty in use.
"""

import surveymonty

def main():
  api = surveymonty.Client()
  print api.get_survey_list()

if __name__ == "__main__":
  main()
