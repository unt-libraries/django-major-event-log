from setuptools import setup, find_packages

setup(
    name='django-major-event-log',
    version='3.0.0',
    packages=find_packages(exclude=['tests*']),
    description='Django app for keeping track of major premis events.',
    long_description='See the home page for more information.',
    include_package_data=True,
    url='https://github.com/unt-libraries/django-major-event-log',
    author='University of North Texas Libraries',
    author_email='mark.phillips@unt.edu',
    license='BSD',
    keywords=['django', 'premis', 'event', 'log'],
    classifiers=[
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Framework :: Django :: 4.2',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ]
)
