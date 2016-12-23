from setuptools import setup, find_packages


with open('./surveymonty/VERSION', 'r') as version_file:
    version = version_file.read().strip()


setup(
    name='surveymonty',
    version=version,

    install_requires=[
        'requests>=2.12.4,<3.0'
    ],

    packages=find_packages(),
    include_package_data=True,

    author='Andrew Shim',
    author_email='andrewkshim92@gmail.com',
    description='Python wrapper for SurveyMonkey API',
    license='MIT',
    keywords=['SurveyMonkey'],
    url='https://github.com/andrewkshim/SurveyMonty',
)
