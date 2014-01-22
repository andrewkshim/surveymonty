#!/usr/bin/env python

import surveymonkey

ACCESS_TOKEN = """UFHR1aBDl2QjFoOzyDhoj91aM1Q3Atp-HtOvcI8kBk.HIBEdrGLtGKLnbSmHGcE-gshszv3.Fq7jYtrx7muQMYaZWWFEupCGMmMz1mmerRk="""
API_KEY = "w2jcncuywg9rep4439z5amvd"
SURVEY_ID = "48099026"
COLLECTOR_ID = "49097122"
RESPONDENT_IDS = ["3022778452"]


def main():
    api = surveymonkey.SurveyMonkey(ACCESS_TOKEN, API_KEY)
    # Test API methods, cannot do more than 2 at a time due to 2 requests per
    # second limit set by SurveyMonkey
    #print api.get_survey_list()
    #print api.get_survey_details(SURVEY_ID)
    #print api.get_collector_list(SURVEY_ID)
    #print api.get_respondent_list(SURVEY_ID)
    #print api.get_reponses(RESPONDENT_IDS, SURVEY_ID)
    #print api.get_response_count(COLLECTOR_ID)
    #print api.get_user_details()

if __name__ == "__main__":
    main()
