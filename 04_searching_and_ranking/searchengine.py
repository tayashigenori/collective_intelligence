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
        cur=self.con.execute(
            "select rowid from %s where %s='%s'" % (table,field,value))
        res=cur.fetchone()
        if res==None:
            cur=self.con.execute(
                "insert into %s (%s) values ('%s')" % (table,field,value))
            return cur.lastrowid
        else:
            return res[0]

    # 個々のページをインデックスする
    def addtoindex(self,url,soup):
        if self.isindexed(url): return
        print 'Indexing %s' % url

        # 個々の単語を取得する
        text=self.gettextonly(soup)
        words=self.separatewords(text)

        # URL id を取得する
        urlid=self.getentryid('urllist','url',url)

        # それぞれの単語と、このurlのリンク
        for i in range(len(words)):
            word=words[i]
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into wordlocation(urlid,wordid,location) \
                values (%d,%d,%d)" % (urlid,wordid,i))

    # HTMLのページからタグのない状態でテキストを抽出する
    def gettextonly(self,soup):
        v=soup.string
        if v==None:
            c=soup.contents
            resulttext=''
            for t in c:
                subtext=self.gettextonly(t)
                resulttext+=subtext+'\n'
            return resulttext
        else:
            return v.strip()

    # 空白以外の文字で単語を分割する
    def separatewords(self,text):
        splitter=re.compile('\\W*')
        return [s.lower() for s in splitter.split(text) if s != '']

    # URLが既にインデックスされていたらtrueを返す
    def isindexed(self,url):
        u=self.con.execute \
           ("select rowid from urllist where url='%s'" %url).fetchone()
        if u != None:
            # URL が実際にクロールされているかどうかチェックする
            v=self.con.execute(
                'select * from wordlocation where urlid=%d' % u[0]).fetchone()
            if v != None: return True
        return False

    # 2つのページの間にリンクを付け加える
    def addlinkref(self,urlFrom,urlTo,linkText):
        words=self.separatewords(linkText)
        fromid=self.getentryid('urllist','url',urlFrom)
        toid=self.getentryid('urllist','url',urlTo)
        if fromid==toid: return
        cur=self.con.execute("insert into link(fromid,toid) values (%d,%d)" % (fromid,toid))
        linkid=cur.lastrowid
        for word in words:
            if word in ignorewords: continue
            wordid=self.getentryid('wordlist','word',word)
            self.con.execute("insert into linkwords(linkid,wordid) values (%d,%d)" % (linkid,wordid))

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

class searcher:
    def __init__(self,dbname):
        self.con=sqlite.connect(dbname)

    def __del__(self):
        self.con.close()

    def getmatchrows(self,q):
        # クエリを作るための文字列
        fieldlist='w0.urlid'
        tablelist=''
        clauselist=''
        wordids=[]

        # 空白で単語を分ける
        words=q.split(' ')
        tablenumber=0

        for word in words:
            # 単語のIDを取得
            wordrow=self.con.execute(
                "select rowid from wordlist where word='%s'" % word).fetchone()
            if wordrow != None:
                wordid=wordrow[0]
                wordids.append(wordid)
                if tablenumber>0:
                    tablelist+=','
                    clauselist+=' and '
                    clauselist+='w%d.urlid=w%d.urlid and ' % (tablenumber-1,tablenumber)
                fieldlist+=',w%d.location' % tablenumber
                tablelist+='wordlocation w%d' % tablenumber
                clauselist+='w%d.wordid=%d' % (tablenumber,wordid)
                tablenumber+=1

        # 分割されたパーツからクエリを構築
        fullquery='select %s from %s where %s' % (fieldlist,tablelist,clauselist)
        cur=self.con.execute(fullquery)
        rows=[row for row in cur]

        return rows,wordids

def main():
    return

if __name__ == '__main__':
    main()
