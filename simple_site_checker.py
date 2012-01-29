import sys
import urllib2

from lxml import etree

XMLNS = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

class HeadRequest(urllib2.Request):
     def get_method(self):
         return "HEAD"

def main():
    try:
        url = sys.argv[1]
    except IndexError:
        print 'Please provide XML sitemap URL'
        sys.exit(2)

    if '://' in url:
        try:
            sitemap = urllib2.urlopen(url)
        except urllib2.HTTPError, e:
            if e.code == 404:
                print 'Sitemap not found'
            elif e.code == 500:
                print 'Server error when accessing sitemap.'
            sys.exit(1)
        except Exception, e: 
            print 'Unexpected error', e
            sys.exit(1)
    else:
        try:
            sitemap = open(url)
        except IOError, e:
            print 'IOError', e
            sys.exit(1)
        except Exception, e:
            print 'Unexpected error', e
            sys.exit(1)

    tree = etree.parse(sitemap)

    loc_tags = tree.xpath('//sitemap:loc', namespaces=XMLNS)
    total = len(loc_tags)
    print '%i URLs found' % total
    succeeded = failed = 0
    failed_urls = []
    for tag in loc_tags:
        loc_url = tag.text
        print 'Checking: %s' % loc_url
        try:
            response = urllib2.urlopen(HeadRequest(loc_url))
            succeeded += 1
        except urllib2.HTTPError, e:
            failed += 1
            failed_urls.append((loc_url, e))
            print e
        except Exception, e:
            failed += 1
            failed_urls.append((loc_url, e))
            print 'Unexpected error:', e

    print 'Checked %i, succeeded %i, failed %i' % (total, succeeded, failed)
    if failed > 0:
        print '-' * 79
        print 'Failed'
        print '-' * 79
        for url in failed_urls:
            print '%s -> %s' % (url[0], url[1])

if __name__ == '__main__':
    main()
