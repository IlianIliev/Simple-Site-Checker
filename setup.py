from setuptools import setup

setup(
    name='SimpleSiteChecker',
    description='Simple Site Checker is a command line tool that allows you to run a website pages check using XML sitemap',
    version='0.1.03',
    author='Ilian Iliev',
    author_email='ilian@i-n-i.org',
    scripts=['simple_site_checker.py'],
    url='http://pypi.python.org/pypi/SimpleSiteChecker/',
    license='LICENSE',
    long_description=open('./README.rst').read(),
    install_requires=[
        'argparse',
        'lxml',
    ],
)
