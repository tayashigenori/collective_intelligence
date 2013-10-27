# -*- coding: utf-8 -*-

import sys
import docclass

def test_train():
    sys.stderr.write("testing training...\n")
    cl=docclass.classifier(docclass.getwords)
    cl.train('the quick brown fox jumps over the lazy dog', 'good')
    cl.train('make quick money in the online casino', 'bad')
    fcount1 = cl.fcount('quick', 'good')
    sys.stdout.write("%f\n" %(fcount1)) # 1.0
    fcount2 = cl.fcount('quick', 'bad')
    sys.stdout.write("%f\n" %(fcount2)) # 1.0

def test_fprob():
    sys.stderr.write("testing sampletrain and computation of feature probability...\n")
    reload(docclass)
    cl=docclass.classifier(docclass.getwords)
    docclass.sampletrain(cl)
    fprob = cl.fprob('quick', 'good')
    sys.stdout.write("%f\n" %(fprob)) # 0.6666...

def test_weightedprob():
    sys.stderr.write("testing computation of weightedprob (probability for unseen words)...\n")
    reload(docclass)
    cl=docclass.classifier(docclass.getwords)
    docclass.sampletrain(cl)
    wp1 = cl.weightedprob('money', 'good', cl.fprob)
    sys.stdout.write("%f\n" %(wp1)) # 0.25
    docclass.sampletrain(cl)
    wp2 = cl.weightedprob('money', 'good', cl.fprob)
    sys.stdout.write("%f\n" %(wp2)) # 0.1666...

def test_nb_prob():
    sys.stderr.write("testing computation of naive bayes probability...\n")
    reload(docclass)
    cl=docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    p1 = cl.prob('quick rabbit', 'good')
    sys.stdout.write("%f\n" %(p1)) # 0.15624999..
    p2 = cl.prob('quick rabbit', 'bad')
    sys.stdout.write("%f\n" %(p2)) # 0.05000000...

def test_nb_classify():
    sys.stderr.write("testing naive bayes classification...\n")
    reload(docclass)
    cl=docclass.naivebayes(docclass.getwords)
    docclass.sampletrain(cl)
    c1 = cl.classify('quick rabbit', default='unknown')
    sys.stdout.write("%s\n" %(c1)) # 'good'
    c2 = cl.classify('quick money', default='unknown')
    sys.stdout.write("%s\n" %(c2)) # 'bad'
    # test threshold
    cl.setthreshold('bad', 3.0)
    c3 = cl.classify('quick money', default='unknown')
    sys.stdout.write("%s\n" %(c3)) # 'unknown'
    for i in range(10): docclass.sampletrain(cl)
    c4 = cl.classify('quick money', default='unknown')
    sys.stdout.write("%s\n" %(c4)) # 'bad'

def test_fisher_cprob():
    sys.stderr.write("testing computation of fisher cprob...\n")
    reload(docclass)
    cl=docclass.fisherclassifier(docclass.getwords)
    docclass.sampletrain(cl)
    cp1 = cl.cprob('quick', 'good')
    sys.stdout.write("%f\n" %(cp1)) # 0.57142857...
    cp2 = cl.cprob('money', 'bad')
    sys.stdout.write("%f\n" %(cp2)) # 1.0

def test_fisher_weightedprob():
    sys.stderr.write("testing computation of fisher weightedprob...\n")
    reload(docclass)
    cl=docclass.fisherclassifier(docclass.getwords)
    docclass.sampletrain(cl)
    wp = cl.weightedprob('money', 'bad', cl.cprob)
    sys.stdout.write("%f\n" %(wp)) # 0.75

def test_fisher_fisherprob():
    sys.stderr.write("testing computation of fisher fisherprob...\n")
    reload(docclass)
    cl=docclass.fisherclassifier(docclass.getwords)
    docclass.sampletrain(cl)
    # cprob
    cp = cl.cprob('quick', 'good')
    sys.stdout.write("%f\n" %(cp)) # 0.57142857...
    # fisher prob
    fp1 = cl.fisherprob('quick rabbit', 'good')
    sys.stdout.write("%f\n" %(fp1)) # 0.780139
    fp2 = cl.fisherprob('quick rabbit', 'bad')
    sys.stdout.write("%f\n" %(fp2)) # 0.356335

def test_fisher_classify():
    sys.stderr.write("testing fisher classification...\n")
    reload(docclass)
    cl=docclass.fisherclassifier(docclass.getwords)
    docclass.sampletrain(cl)
    # classify
    c1 = cl.classify('quick rabbit')
    sys.stdout.write("%s\n" %(c1)) # 'good'
    c2 = cl.classify('quick money')
    sys.stdout.write("%s\n" %(c2)) # 'bad'
    # set minimum for 'bad'
    cl.setminimum('bad', 0.8)
    c3 = cl.classify('quick money')
    sys.stdout.write("%s\n" %(c3)) # 'good'
    # set minimum for 'good'
    cl.setminimum('good', 0.4)
    c4 = cl.classify('quick money')
    sys.stdout.write("%s\n" %(c4)) # 'good'

def main():
    # simple classifier
    test_train()
    test_fprob()
    test_weightedprob()
    # naive bayes
    test_nb_prob()
    test_nb_classify()
    # fisher classifier
    test_fisher_cprob()
    test_fisher_weightedprob()
    test_fisher_fisherprob()
    test_fisher_classify()
    return

if __name__ == '__main__':
    main()
