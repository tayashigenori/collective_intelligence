# -*- coding: utf-8 -*-

import searchengine

def test_urllib2():
    import urllib2
    c=urllib2.urlopen('http://kiwitobes.com/')
    contents=c.read()
    print contents[0:100]

def test_crawler():
    pagelist=['http://kiwitobes.com/']
    crawler=searchengine.crawler('')
    crawler.crawl(pagelist)

def test_createindextables():
    crawler=searchengine.crawler('searchindex.db')
    crawler.createindextables()

def main():
    test_urllib2()
    #test_crawler()
    test_createindextables()
    return

if __name__ == '__main__':
    main()
