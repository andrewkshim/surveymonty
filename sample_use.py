#!/usr/bin/env python
"""
@author: Andrew Shim

Code example of SurveyMonty in use.
"""

import surveymonty

def main():
  api = surveymonty.Client()
  print api.get_responses(["3055851426"], 48642975)

if __name__ == "__main__":
  main()
