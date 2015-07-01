from setuptools import setup
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='django-major-event-log',
    version='0.1.0',
    description='Django app for keeping track of major premis events.',
    long_description=readme,
    url='https://github.com/unt-libraries/django-major-event-log',
    author='University of North Texas Libraries',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    classifiers=[
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Framework :: Django'
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7'
    ]
)
