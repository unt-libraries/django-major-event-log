from setuptools import setup
from codecs import open
from os import path
import re

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'major-event-log', '__init__.py'), 'r') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    readme = f.read()

setup(
    name='django-major-event-log',
    version=version,
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
