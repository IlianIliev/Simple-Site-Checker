#!/usr/bin/env python
import argparse
from datetime import datetime
import logging
import os
import sys
import urllib2

from lxml import etree

USER_AGENT = ''

SITEMAP_NAMESPACE = 'http://www.sitemaps.org/schemas/sitemap/0.9'
XMLNS = {'sitemap': SITEMAP_NAMESPACE}


DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'


VERBOSE_HELP = (
    """Verbose mode. Controls the script output
    0 - print output only in case of errors
    1 - prints the result count plus list of failed URLs(if any)
    2 - print all checked URLs \n""")

LOGGING_LEVELS = {
    0: logging.ERROR,
    1: logging.INFO,
    2: logging.DEBUG,
}


logger = logging.getLogger(__name__)


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


class XMLSitemapParser(object):
    total = 0
    succeeded = 0
    failed = []
    sitemaps = {}

    def load_sitemap(self, url):
        logger.debug('Loading sitemap %s' % url)
        if '://' in url:
            try:
                sitemap = urllib2.urlopen(urllib2.Request(url, headers={'User-Agent': USER_AGENT}))
            except urllib2.HTTPError, e:
                if e.code == 404:
                    logger.error('Sitemap not found as %s' % url)
                elif e.code == 500:
                    logger.error('Server error when accessing sitemap as %s' % url)
                else:
                    logger.error('Server error \'%s\' when accessing sitemap as %s' % (e, url))
                sys.exit(1)
            except Exception, e: 
                logger.debug('Unexpected error', e)
                logger.error('Unexpected error while loading sitemap.')
                sys.exit(1)
        else:
            try:
                path = os.path.abspath(url)
                sitemap = open(url)
            except Exception, e:
                logger.error('Unable to load sitemap file from %s' % path)
                logger.debug(e)
                sys.exit(1)
        try:
            tree = etree.parse(sitemap)
        except Exception, e:
            logger.debug('Unexpected error', e)
            logger.error('Unexpected error while parsing sitemap XML from %s' % url)
        else:
            root = tree.getroot()
            if root.tag == '{%s}sitemapindex' % SITEMAP_NAMESPACE:
                self.process_sitemapindex(tree)
            else:
                self.sitemaps[url] = tree

    def process_sitemapindex(self, tree):
        logger.debug('Processing sitemapindex')
        for tag in tree.xpath('//sitemap:sitemap/sitemap:loc', namespaces=XMLNS):
            sitemap_loc = tag.text
            self.load_sitemap(sitemap_loc)

    def process_sitemap(self, sitemap):
        tree = self.sitemaps[sitemap]
        logger.debug('Processing sitemap %s' % sitemap)
        loc_tags = tree.xpath('//sitemap:loc', namespaces=XMLNS)
        urls_found = len(loc_tags)
        self.total += urls_found
        logger.info('%i URLs found' % urls_found)
    
        for tag in loc_tags:
            loc_url = tag.text
            logger.debug('Checking %s' % loc_url)
            try:
                response = urllib2.urlopen(HeadRequest(loc_url, headers={'User-Agent': USER_AGENT}))
                self.succeeded += 1
                logger.info('%s - OK' % loc_url)
            except Exception, e:
                self.failed.append((loc_url, e))
                logger.error('%s -> %s' % (loc_url, e))

    def process_sitemaps(self):
        for sitemap in self.sitemaps:
            self.process_sitemap(sitemap)


def time_info(start, end):
    hours, remainder = divmod((end-start).seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    logger.info('Start - %s' % start.strftime(DATETIME_FORMAT))
    logger.info('End   - %s' % end.strftime(DATETIME_FORMAT))
    logger.info('Time elapsed %s:%s:%s' % (hours, minutes, seconds))


def main():
    arg_parser = argparse.ArgumentParser(description='Simple Site Checker',
                                     formatter_class=argparse.RawTextHelpFormatter)
    arg_parser.add_argument('sitemap', metavar='s', type=str,
                   help='XML sitemap URL/path')
    arg_parser.add_argument('-v', '--verbose', type=int, required=False,
                        help=VERBOSE_HELP, default = 0, choices=LOGGING_LEVELS)

    args = arg_parser.parse_args()

    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level = LOGGING_LEVELS[args.verbose])

    start = datetime.now()

    url = args.sitemap
    parser = XMLSitemapParser()
    parser.load_sitemap(url)
    parser.process_sitemaps()

    end = datetime.now()

    failed_number = len(parser.failed)
    logger.info('Result - Checked %i, succeeded %i, failed %i' %
                (parser.total, parser.succeeded, failed_number))
    time_info(start, end)


if __name__ == '__main__':
    main()
