===========
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
python simple_site_checker.py http://example.com/sitemap.xml


Todo:
=====

* Allow the usage of relative path for local XML 
* Add command line options for less/more output
* Add command line option for email notification 
