# -*- coding: utf-8 -*-

import urllib2
from BeautifulSoup import *
from urlparse import urljoin

try:
    # version >= 2.5
    from sqlite3 import dbapi2 as sqlite
except ImportError:
    try:
        from pysqlite2 import dbapi2 as sqlite
    except ImportError:
        print 'Please install pusqlite2'
        exit(1)

# 無視すべき単語のリストを作る
ignorewords=set(['the','of','to','and','a','in','is','it',])

class crawler:
    # データベースの名前でクローラを初期化する
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)
        pass

    def __del__(self):
        self.con.close()
        pass

    def dbcommit(self):
        self.con.commit()
        pass

    # エントリIDを取得したり、それが存在しない場合には追加
    # するための補助関数
    def getentryid(self,table,field,value,cretenew=True):
        return None

    # 個々のページをインデックスする
    def addtoindex(self,url,soup):
        print 'Indexing %s' % url

    # HTMLのページからタグのない状態でテキストを抽出する
    def gettextonly(self,soup):
        return None

    # 空白以外の文字で単語を分割する
    def separatewords(self,text):
        return None

    # URLが既にインデックスされていたらtrueを返す
    def isindexed(self,utl):
        return False

    # 2つのページの間にリンクを付け加える
    def addlinkref(self,urlFrom,utlTo,linkText):
        pass

    # ページのリストを受け取り、与えられた深さで幅優先の検索を行ない
    # ページをインデクシングする
    def crawl(self,pages,depth=2):
        pass
    
    # データベースのテーブルを作る
    def createindextables(self):
        pass

    def crawl(self,pages,depth=2):
        for i in range(depth):
            newpages=set()
            for page in pages:
                try:
                    c=urllib2.urlopen(page)
                except:
                    print 'Could not oren %s' % page
                    continue
                soup=BeautifulSoup(c.read())
                self.addtoindex(page,soup)

                links=soup('a')
                for link in links:
                    if ('href' in dict(link.attrs)):
                        url=urljoin(page,link['href'])
                        if url.find("'") != -1: continue
                        url=url.split('#')[0] # アンカーを取り除く
                        if url[0:4]== 'http' and not self.isindexed(url):
                            newpages.add(url)
                        linkText=self.gettextonly(link)
                        self.addlinkref(page,url,linkText)

                self.dbcommit()
            pages=newpages

    def createindextables(self):
        # create table
        self.con.execute('create table if not exists urllist(url)')
        self.con.execute('create table if not exists wordlist(word)')
        self.con.execute('create table if not exists wordlocation(urlid,wordid,location)')
        self.con.execute('create table if not exists link(fromid integer,toid integer)')
        self.con.execute('create table if not exists linkwords(wordid,linkid)')
        # create index
        self.con.execute('create index if not exists wordidx on wordlist(word)')
        self.con.execute('create index if not exists urlidx on urllist(url)')
        self.con.execute('create index if not exists wordurlidx on wordlocation(wordid)')
        self.con.execute('create index if not exists urltoidx on link(toid)')
        self.con.execute('create index if not exists urlfromidx on link(fromid)')
        # commit
        self.dbcommit()

def main():
    return

if __name__ == '__main__':
    main()
