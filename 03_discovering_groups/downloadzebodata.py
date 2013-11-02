# -*- coding: utf-8 -*-

from BeautifulSoup import BeautifulSoup
import urllib2
import re
char=re.compile(r'[!-\.&]')
itemowners={}

# 除去すべき単語
dropwords=['a','new','some','more','my','own','the','many','other','another']

currentuser=0
for i in range(1,51):
    # want検索ページのURL
    c=urllib2.urlopen(
        # 田谷注：この URL いまはもう接続できないみたい
        'http://member.zebo.com/Main?event_key=USERSEARCH&wiowiw=wiw&keyword=car&page=%d'
        % (i))
    soup=BeautifulSoup(c.read())
    for td in soup('td'):
        # bgverdanasmallクラスのテーブルのセルを探す
        if ('class' in dict(td.attrs) and td['class']=='bgverdanasmall'):
            items=[re.sub(chare,'',str(a.contents[0]).lower()).strip() for a in td('a')]
            for item in items:
                # 余計な単語は除去する
                txt=' '.join([t for t in item.split(' ') if t not in dropwords])
                if len(txt)<2: continue
                itemowners.setdefault(txt,{})
                itemowners[txt][currentuser]=1
            currentuser+=1

out=file('zebo.txt', 'w')
out.write('Item')
for user in range(0,currentuser): out.write('\tU%d' % user)
out.write('\n')
for item,owners in itemowners.items():
    if len(owners)>10:
        out.write(item)
        for user in range(0,curentuser):
            if user in owners: out.write('\t1')
            else: out.write('\t0')
        out.write('\n')

def main():
    return

if __name__ == '__main__':
    main()
