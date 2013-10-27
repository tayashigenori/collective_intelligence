# -*- coding: utf-8 -*-

import re
import math

def getwords(doc):
    splitter=re.compile('\\W*')
    # 単語を非アルファベットの文字で分割する
    words=[s.lower() for s in splitter.split(doc)
           if len(s)>2 and len(s)<20]
    # ユニークな単語のみの集合を返す
    return dict([(w,1) for w in words])

def sampletrain(cl):
    cl.train('Nobody owns the water', 'good')
    cl.train('the quick rabbit jumps fences', 'good')
    cl.train('buy pharmaceuticals now', 'bad')
    cl.train('make quick money at the online casino', 'bad')
    cl.train('the quick brown fox jumps', 'good')

class classifier:
    def __init__(self,getfeatures,filename=None):
        # 特徴/カテゴリのカウント
        # e.g. {'python': {'bad': 0, 'good': 6}, 'the': {'bad': 3, 'good': 3}}
        self.fc={}
        # それぞれのカテゴリ中のドキュメント数
        self.cc={}
        self.getfeatures=getfeatures

    # 特徴/カテゴリのカウントを増やす
    def incf(self,f,cat):
        self.fc.setdefault(f,{})
        self.fc[f].setdefault(cat,0)
        self.fc[f][cat]+=1

    # カテゴリのカウントを増やす
    def incc(self,cat):
        self.cc.setdefault(cat,0)
        self.cc[cat]+=1

    # あるカテゴリの中に特徴が現れた回数
    def fcount(self,f,cat):
        if f in self.fc and cat in self.fc[f]:
            return float(self.fc[f][cat])
        return 0.0

    # あるカテゴリのアイテムたちの数
    def catcount(self,cat):
        if cat in self.cc:
            return float(self.cc[cat])
        return 0.0

    # アイテムたちの総数
    def totalcount(self):
        return sum(self.cc.values())

    # すべてのカテゴリたちのリスト
    def categories(self):
        return self.cc.keys()

    # train
    def train(self,item,cat):
        features=self.getfeatures(item)
        # このカテゴリの中の特徴たちのカウントを増やす
        for f in features:
            self.incf(f,cat)
        # このカテゴリのカウントを増やす
        self.incc(cat)

    # compute Pr(word | category)
    def fprob(self,f,cat):
        if self.catcount(cat)==0: return 0
        # このカテゴリ中にこの特徴が出現する回数を、このカテゴリ中のアイテムの総数で割る
        return self.fcount(f,cat)/self.catcount(cat)

    # unknown words smoothing: (weight*aprob + count*fprob)/(count+weight)
    def weightedprob(self,f,cat,prf,weight=1.0,ap=0.5):
        # 現在の確率を計算する
        basicprob=prf(f,cat)

        # この特徴がすべてのカテゴリ中に出現する回数を数える
        totals=sum([self.fcount(f,c) for c in self.categories()])

        # 重み付けした平均を計算
        bp=((weight*ap)+(totals*basicprob))/(weight+totals)
        return bp

class naivebayes(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        # parameter for minimizing false positives
        self.thresholds={}
    def setthreshold(self,cat,t):
        self.thresholds[cat]=t
    def getthreshold(self,cat):
        if cat not in self.thresholds: return 1.0
        return self.thresholds[cat]

    # computes Pr(doc | category)
    def docprob(self,item,cat):
        features=self.getfeatures(item)
        # すべての特徴の確率を掛け合わせる
        p=1
        for f in features: p*=self.weightedprob(f,cat,self.fprob)
        return p

    # computes P(doc | category) * Pr(category)
    def prob(self,item,cat):
        catprob=self.catcount(cat)/self.totalcount()
        docprob=self.docprob(item,cat)
        return docprob*catprob

    # classify!
    def classify(self,item,default=None):
        probs={}
        # 最も確率の高いカテゴリを探す
        max_prob=0.0
        for cat in self.categories():
            probs[cat]=self.prob(item,cat)
            if probs[cat]>max_prob:
                max_prob=probs[cat]
                best_cat=cat
        # 確率が threshold * (2番めにベストなもの) を超えているかを確認する
        for cat in probs:
            if cat==best_cat: continue
            if probs[cat]*self.getthreshold(best_cat)>probs[best_cat]: return default
        return best_cat

class fisherclassifier(classifier):
    def __init__(self,getfeatures):
        classifier.__init__(self,getfeatures)
        self.minimums={}
    def setminimum(self,cat,minimum):
        self.minimums[cat]=minimum
    def getminimum(self,cat):
        if cat not in self.minimums: return 0
        return self.minimums[cat]

    # computes Pr(category | feature)
    def cprob(self,f,cat):
        # このカテゴリ中でのこの特徴の頻度
        clf=self.fprob(f,cat)
        if clf==0: return 0
        # すべてのカテゴリ中でのこの特徴の頻度
        freqsum=sum([self.fprob(f,c) for c in self.categories()])
        # 確率はこのカテゴリでの頻度を全体の頻度で割ったもの
        p=clf/(freqsum)
        return p

    def fisherprob(self,item,cat):
        # すべての確率を掛け合わせる
        p=1
        features=self.getfeatures(item)
        for f in features:
            p*=(self.weightedprob(f,cat,self.cprob))
        # 自然対数をとり -2 を掛け合わせる
        fscore=-2*math.log(p)
        # 関数 invchi2 (カイ2乗の逆数) を利用して確率を得る
        return self.invchi2(fscore,len(features)*2)

    def invchi2(self,chi,df):
        m = chi / 2.0
        sum_chi = term = math.exp(-m)
        for i in range(1, df//2):
            term *= m / i
            sum_chi += term
        return min(sum_chi, 1.0)

    def classify(self,item,default=None):
        # 最も良い結果を探してループする
        best_cat=default
        max_prob=0.0
        for c in self.categories():
            p=self.fisherprob(item,c)
            # 下限値を超えていることを確認する
            if p>self.getminimum(c) and p>max_prob:
                best_cat=c
                max_prob=p
        return best_cat

def main():
    return

if __name__ == '__main__':
    main()
