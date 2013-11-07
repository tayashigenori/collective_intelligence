# -*- coding: utf-8 -*-

import sys
import searchengine
import nn

"""
search engine
"""
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
    print e.getmatchrows('programming')

def test_query():
    sys.stderr.write("testing query...\n")
    e=searchengine.searcher('searchindex.db')
    print e.query('programming')

def test_query_ranking(weightFunc):
    sys.stderr.write("testing query with weighting function '%s'...\n" % weightFunc)
    e=searchengine.searcher('searchindex.db')
    print e.query('programming',weightFunc)

def test_calculate_pagerank():
    sys.stderr.write("testing pagerank calculation...\n")
    crawler=searchengine.crawler('searchindex.db')
    crawler.calculatepagerank()
    sys.stderr.write("checking pagerank result...\n")
    cur=crawler.con.execute('select * from pagerank order by score desc')
    for i in range(3): print cur.next()
    sys.stderr.write("checking pagerank top url...\n")
    e=searchengine.searcher('searchindex.db')
    urlid=cur.next()[0]
    print e.geturlname(urlid)

"""
neural net
"""
def test_select():
    sys.stderr.write("testing create hiddennodes...\n")
    mynet=nn.searchnet('nn.db')
    mynet.maketables()
    wWorld,wRiver,wBank =101,102,103
    uWorldBank,uRiver,uEarth =201,202,203
    mynet.generatehiddennode([wWorld,wBank],[uWorldBank,uRiver,uEarth])
    sys.stderr.write("testing 'select * from wordhidden'...\n")
    for c in mynet.con.execute('select * from wordhidden'): print c
    sys.stderr.write("testing 'select * from hiddenurl'...\n")
    for c in mynet.con.execute('select * from hiddenurl'): print c

def test_feedforward():
    sys.stderr.write("testing feedforward (without training)...\n")
    mynet=nn.searchnet('nn.db')
    wWorld,wRiver,wBank =101,102,103
    uWorldBank,uRiver,uEarth =201,202,203
    print mynet.getresult([wWorld,wBank],[uWorldBank,uRiver,uEarth])

def main():
    # test search engine
    test_urllib2()
    #test_crawler()
    test_createindextables()
    test_crawler2()
    test_getmatchrows()
    test_query()
    test_query_ranking('frequencyscore')
    test_query_ranking('locationscore')
    test_query_ranking(['frequencyscore', 'locationscore'])
    test_query_ranking({'frequencyscore':1.0, 'locationscore':1.5})
    test_query_ranking('distancescore')
    test_query_ranking('inboundlinkscore')
    test_calculate_pagerank()
    test_query_ranking({'frequencyscore':1.0,
                        'locationscore':1.0,
                        'pagerankscore':1.0,
                        })
    test_query_ranking({'linktextscore':1.0})
    
    # test neural net
    test_select()
    test_feedforward()
    return

if __name__ == '__main__':
    main()
