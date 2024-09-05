Simple Site Checker
===========

This is the repository or Simple Site Checker.

Simple Site Checker is a command line tool that allows you to run a website
pages check using XML sitemap. You should provide the sitemap URL or absolute
path. The script will check all URLs and list the error ones.

The purpose of this script is to be use as a website monitor and to report for
broken link in the sitemap.


Usage:
======
you should have python3 and pip setup in your environment

> install argparse and lxml

    pip install argparse lxml
> run to check your setup

    python setup.py setup
> run your the script and provide the path to your sitemap.xml file as the first params

    python simple_site_checker.py ./sitemap.xml



Dependencies:
=============

Simple Site Checker depends on the following modules:
* argparse
* lxml


Feel free to add any issues, bug reports, comments or advices to [IlianIliev](https://github.com/IlianIliev/Simple-Site-Checker)



* http://ilian.i-n-i.org/simple-site-checker/
