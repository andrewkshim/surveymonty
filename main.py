#!/usr/bin/env python

import surveymonkey

ACCESS_TOKEN = """UFHR1aBDl2QjFoOzyDhoj91aM1Q3Atp-HtOvcI8kBk.HIBEdrGLtGKLnbSmHGcE-gshszv3.Fq7jYtrx7muQMYaZWWFEupCGMmMz1mmerRk="""
API_KEY = "w2jcncuywg9rep4439z5amvd"


def main():
    api = surveymonkey.SurveyMonkey(ACCESS_TOKEN, API_KEY)
    api.get_survey_list()

if __name__ == "__main__":
    main()
