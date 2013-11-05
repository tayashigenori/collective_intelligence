# -*- coding: utf-8 -*-

import sys
import searchengine

def test_urllib2():
    sys.stderr.write("testing urllib2...\n")
    import urllib2
    c=urllib2.urlopen('http://kiwitobes.com/')
    contents=c.read()
    print contents[0:100]

def test_crawler():
    sys.stderr.write("testing crawler...\n")
    pagelist=['http://kiwitobes.com/']
    crawler=searchengine.crawler('')
    crawler.crawl(pagelist)

def test_createindextables():
    sys.stderr.write("testing create index tables...\n")
    crawler=searchengine.crawler('searchindex.db')
    crawler.createindextables()

def test_crawler2():
    sys.stderr.write("testing crawler...\n")
    crawler=searchengine.crawler('searchindex.db')
    pages= \
           ['http://kiwitobes.com/']
    #crawler.crawl(pages)
    print [row for row in crawler.con.execute(
        'select rowid from wordlocation where wordid=1')]

def test_getmatchrows():
    sys.stderr.write("testing get match rows...\n")
    e=searchengine.searcher('searchindex.db')
    print e.getmatchrows('functional programming')

def main():
    test_urllib2()
    #test_crawler()
    test_createindextables()
    test_crawler2()
    test_getmatchrows()
    return

if __name__ == '__main__':
    main()
