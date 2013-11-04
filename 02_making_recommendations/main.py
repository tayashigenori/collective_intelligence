# -*- coding: utf-8 -*-

import sys
import recommendations

def test_critics():
    sys.stderr.write("testing critics dictionary.\n")
    from recommendations import critics
    print critics['Lisa Rose']['Lady in the Water']
    critics['Toby']['Snakes on a Plane'] = 4.5
    print critics['Toby']

def test_distance():
    sys.stderr.write("testing euclidean distance.\n")
    print recommendations.sim_distance(recommendations.critics,
                                       'Lisa Rose', 'Gene Seymour')

def test_pearson():
    sys.stderr.write("testing pearson correlation.\n")
    print recommendations.sim_pearson(recommendations.critics,
                                      'Lisa Rose', 'Gene Seymour')

def test_getRecommendations_userbased():
    test_topMatches()
    test_getRecommendations()

def test_topMatches():
    sys.stderr.write("testing topMatches. (user-based)\n")
    print recommendations.topMatches(recommendations.critics,'Toby',n=3)

def test_getRecommendations():
    sys.stderr.write("testing getRecommendations. (user-based)\n")
    print recommendations.getRecommendations(recommendations.critics,'Toby')
    print recommendations.getRecommendations(recommendations.critics,'Toby',
                                             similarity=recommendations.sim_distance)

def test_getRecommendations_itembased():
    movies=recommendations.transformPrefs(recommendations.critics)
    sys.stderr.write("testing topMatches. (item-based)\n")
    print recommendations.topMatches(movies,'Superman Returns')
    sys.stderr.write("testing getRecommendations. (item-based)\n")
    print recommendations.getRecommendations(movies,'Just My Luck')

def test_pydelicious():
    sys.stderr.write("testing pydelicious.\n")
    import pydelicious
    print pydelicious.get_popular(tag='programming')

def test_del_initializeUserDict():
    sys.stderr.write("testing pydelicious initializeUserDict.\n")
    from deliciousrec import *
    delusers=initializeUserDict('programming')
    delusers ['tsegran']={}
    fillItems(delusers)
    return delusers

def test_getRecommendations_deluser(delusers):
    sys.stderr.write("testing pydelicious recommendations.\n")
    import random
    user=delusers.keys()[random.randint(0,len(delusers)-1)]
    print user
    sys.stderr.write("testing pydelicious recommendations. (user-based)\n")
    print recommendations.topMatches(delusers,user)
    print recommendations.getRecommendations(delusers,user)[0:10]
    sys.stderr.write("testing pydelicious recommendations. (item-based)\n")
    url=recommendations.getRecommendations(deluser,user)[0][1]
    print recommendations.topMatches(recommendations.transformPrefs(delusers),url)

def test_calculateSimilarItems():
    sys.stderr.write("testing calculate similar items.\n")
    itemsim=recommendations.calculateSimilarItems(recommendations.critics)
    print itemsim
    return itemsim

def test_getRecommendedItems(itemsim):
    sys.stderr.write("testing get recommended items.\n")
    print recommendations.getRecommendedItems(recommendations.critics,itemsim,'Toby')

def test_movieLens():
    sys.stderr.write("testing load MovieLens.\n")
    prefs=recommendations.loadMovieLens()
    print prefs['87']
    sys.stderr.write("testing user-based recommendation on MovieLens data.\n")
    print recommendations.getRecommendations(prefs,'87')[0:30]
    sys.stderr.write("testing item-based recommendation on MovieLens data.\n")
    itemsim=recommendations.calculateSimilarItems(prefs,n=50)
    print itemsim
    print recommendations.getRecommendedItems(prefs,itemsim,'87')[0:30]

def main():
    test_critics()
    test_distance()
    test_pearson()
    # user-based recommendations
    test_getRecommendations_userbased()
    # item-based recommendations
    test_getRecommendations_itembased()
    # pydelicious
    test_pydelicious()
    # del.icio.us
    #delusers = test_del_initializeUserDict()
    #test_getRecommendations_deluser(delusers)
    # test item similarities
    itemsim= test_calculateSimilarItems()
    # test getRecomendatedItems
    test_getRecommendedItems(itemsim)
    # test loadMovieLens
    test_movieLens()
    return

if __name__ == '__main__':
    main()
