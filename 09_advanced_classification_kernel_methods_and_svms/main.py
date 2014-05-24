# -*- coding: utf-8 -*-

import advancedclassify

# 9.1. get data set
def get_dataset():
    print "getting data..."
    agesonly = advancedclassify.loadmatch('agesonly.csv', allnum=True)
    matchmaker = advancedclassify.loadmatch('matchmaker.csv')
    return (agesonly, matchmaker)

# 9.2. visualization
def visualize(agesonly):
    print "visualizing..."
    advancedclassify.plotagematches(agesonly)

# 9.3. linear classification
def get_linear_classification(agesonly):
    avgs = advancedclassify.lineartrain(agesonly)
    print ">>> advancedclassify.dpclassify([30, 30], avgs)"
    print advancedclassify.dpclassify([30, 30], avgs)
    print ">>> advancedclassify.dpclassify([30, 25], avgs)"
    print advancedclassify.dpclassify([30, 25], avgs)
    print ">>> advancedclassify.dpclassify([25, 40], avgs)"
    print advancedclassify.dpclassify([25, 40], avgs)
    print ">>> advancedclassify.dpclassify([48, 20], avgs)"
    print advancedclassify.dpclassify([48, 20], avgs)
    print "oops!!"

# 9.4. categorical data features
def get_geolocation():
    print ">>> advancedclassify.getlocation('1 alewife center, cambridge, ma')"
    print advancedclassify.getlocation('1 alewife center, cambridge, ma')
    print ">>> advancedclassify.milesdistance('cambridge, ma', 'new york, ny')"
    print advancedclassify.milesdistance('cambridge, ma', 'new york, ny')

def get_numericalset():
    numericalset = advancedclassify.loadnumerical()
    print ">>> numericalset[0].data"
    print numericalset[0].data
    return numericalset

# 9.5. data scaling
def get_scaledset(numericalset):
    scaledset, scalef = advancedclassify.scaledata(numericalset)
    avgs = advancedclassify.lineartrain(scaledset)
    print ">>> numericalset[0].match"
    print numericalset[0].match
    print ">>> advancedclassify.dpclassify(scalef(numericalset[0].data), avgs)"
    print advancedclassify.dpclassify(scalef(numericalset[0].data), avgs)
    print ">>> numericalset[11].match"
    print numericalset[11].match
    print ">>> advancedclassify.dpclassify(scalef(numericalset[11].data), avgs)"
    print advancedclassify.dpclassify(scalef(numericalset[11].data), avgs)
    return scaledset, scalef

# 9.6. kernel method
def nlclassify_agesonly(agesonly):
    offset = advancedclassify.getoffset(agesonly)
    print ">>> advancedclassify.nlclassify([30, 30], agesonly, offset)"
    print advancedclassify.nlclassify([30, 30], agesonly, offset)
    print ">>> advancedclassify.nlclassify([30, 25], agesonly, offset)"
    print advancedclassify.nlclassify([30, 25], agesonly, offset)
    print ">>> advancedclassify.nlclassify([25, 40], agesonly, offset)"
    print advancedclassify.nlclassify([25, 40], agesonly, offset)
    print ">>> advancedclassify.nlclassify([48, 20], agesonly, offset)"
    print advancedclassify.nlclassify([48, 20], agesonly, offset)
    print "nice!!"

def nlclassify_scaledset(numericalset,
                         scaledset, scalef):
    ssoffset = advancedclassify.getoffset(scaledset)
    print ">>> numericalset[0].match"
    print numericalset[0].match
    print ">>> advancedclassify.nlclassify(scalef(numericalset[0].data), scaledset, ssoffset)"
    print advancedclassify.nlclassify(scalef(numericalset[0].data), scaledset, ssoffset)
    print ">>> numericalset[1].match"
    print numericalset[1].match
    print ">>> advancedclassify.nlclassify(scalef(numericalset[1].data), scaledset, ssoffset)"
    print advancedclassify.nlclassify(scalef(numericalset[1].data), scaledset, ssoffset)
    print ">>> numericalset[2].match"
    print numericalset[2].match
    print ">>> advancedclassify.nlclassify(scalef(numericalset[2].data), scaledset, ssoffset)"
    print advancedclassify.nlclassify(scalef(numericalset[2].data), scaledset, ssoffset)
    newrow = [28.0, -1, -1, 26.0, -1, 1, 2, 0.8] # 男は子どもを望んでいないが、女は望んでいる
    print "newrow:", newrow, "# 男は子どもを望んでいないが、女は望んでいる"
    print ">>> advancedclassify.nlclassify(scalef(newrow), scaledset, ssoffset)"
    print advancedclassify.nlclassify(scalef(newrow), scaledset, ssoffset)
    newrow = [28.0, -1,  1, 26.0, -1, 1, 2, 0.8] # 両者ともに子どもが欲しい
    print "newrow:", newrow, "# 両者ともに子どもが欲しい"
    print ">>> advancedclassify.nlclassify(scalef(newrow), scaledset, ssoffset)"
    print advancedclassify.nlclassify(scalef(newrow), scaledset, ssoffset)

# 9.8. LIBSVM
def test_svm():
    prob  = svm_problem([1, -1], [[1, 0, 1], [-1, 0, -1]])
    print "prob:", prob
    param = svm_parameter(kernel_type = LINEAR, C = 10)
    print "param:", param
    print ">>> m = svm_model(prob, param)"
    m = svm_model(prob, param)
    print ">>> m.predict([1, 1, 1])"
    m.predict([1, 1, 1])
    # save
    m.save(test.model)
    m = svm_model(test.model)

def svm_matchmaker(scaledset, scalef):
    answers, inputs = [r.match for r in scaledset], [r.data for r in scaledset]
    param = svm_parameter(kernel_type = RBF)
    print "param:", param
    prob = svm_problem(answers, inputs)
    print "prob:", prob
    print ">>> m = svm_model(prob, param)"
    m = svm_model(prob, param)
    newrow = [28.0, -1, -1, 26.0, -1, 1, 2, 0.8] # 男は子どもを望んでいないが、女は望んでいる
    print "newrow:", newrow, "# 男は子どもを望んでいないが、女は望んでいる"
    m.predict(scalef(newrow))
    newrow = [28.0, -1,  1, 26.0, -1, 1, 2, 0.8] # 両者ともに子どもが欲しい
    print "newrow:", newrow, "# 両者ともに子どもが欲しい"
    m.predict(scalef(newrow))
    # cross validation
    guesses = corss_validation(prob, param, 4)
    print ">>> guesses"
    print guesses
    print ">>> sum([abs(answers[i] - guesses[i]) for i in range(len(guesses))])"
    sum([abs(answers[i] - guesses[i]) for i in range(len(guesses))])
    print sum

def main():
    # 9.1. data set
    agesonly, matchmaker = get_dataset()
    # 9.2. visualization
    visualize(agesonly)
    # 9.3. linear classification
    get_linear_classification(agesonly)
    # 9.4. categorical data features
    get_geolocation()
    numericalset = get_numericalset()
    # 9.5. data scaling
    scaledset, scalef = get_scaledset(numericalset)
    # 9.6. kernel method
    nlclassify_agesonly(agesonly)
    nlclassify_scaledset(numericalset,
                         scaledset, scalef)
    # 9.7. SVM
    # 9.8. LIBSVM
    from svm import *
    test_svm()
    svm_matchmaker(scaledset, scalef)
    # 9.9. matching on Facebook

if __name__ == '__main__':
    main()
