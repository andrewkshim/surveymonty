#!/usr/bin/env python
"""
**Author** [Andrew Shim][https://github.com/andrewkshim]

TODO: Documentation 


"""

from surveymonty import surveymonty

ACCESS_TOKEN = "UFHR1aBDl2QjFoOzyDhoj91aM1Q3Atp-HtOvcI8kBk.HIBEdrGLtGKLnbSmHGcE-2xNoyqTLF6eslRU6OHaDVsngtjs4BBnxnpzIugp2hUY="
API_KEY = "w2jcncuywg9rep4439z5amvd"

def main():
  surveymonty.SurveyMonty(ACCESS_TOKEN, API_KEY)

if __name__ == "__main__":
  main()
