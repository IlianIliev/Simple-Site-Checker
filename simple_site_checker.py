import argparse
import logging
import os
import sys
import urllib2

from lxml import etree


XMLNS = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}


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


class HeadRequest(urllib2.Request):
    def get_method(self):
        return "HEAD"


def main():
    parser = argparse.ArgumentParser(description='Simple Site Checker',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('sitemap', metavar='s', type=str,
                   help='XML sitemap URL/path')

    parser.add_argument('-v', '--verbose', type=int, required=False,
                        help=VERBOSE_HELP, default = 0, choices=LOGGING_LEVELS)

    args = parser.parse_args()

    logger = logging.getLogger(__name__)
    logging.basicConfig(format='%(levelname)s: %(message)s',
                        level = LOGGING_LEVELS[args.verbose])
    
    url = args.sitemap
    if '://' in url:
        try:
            sitemap = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            if e.code == 404:
                logger.error('Sitemap not found.')
            elif e.code == 500:
                logger.error('Server error when accessing sitemap.')
            sys.exit(1)
        except Exception, e: 
            logger.exception('Unexpected error', e)
            sys.exit(1)
    else:
        try:
            path = os.path.abspath(url)
            sitemap = open(url)
        except Exception, e:
            logger.exception(e)
            sys.exit(1)

    tree = etree.parse(sitemap)
    loc_tags = tree.xpath('//sitemap:loc', namespaces=XMLNS)
    total = len(loc_tags)
    logger.info('%i URLs found' % total)
    succeeded = 0
    failed = []

    for tag in loc_tags:
        loc_url = tag.text
        logger.debug('Checking %s' % loc_url)
        try:
            response = urllib2.urlopen(HeadRequest(loc_url))
            succeeded += 1
        except urllib2.HTTPError, e:
            failed.append((loc_url, e))
            logger.debug(loc_url, e)
        except Exception, e:
            failed.append((loc_url, e))
            logger.debug(loc_url, e)

    failed_number = len(failed)
    logger.info('Checked %i, succeeded %i, failed %i' %
                (total, succeeded, failed_number))
    if failed_number > 0:
        for url in failed:
            logger.error(url)


if __name__ == '__main__':
    main()
