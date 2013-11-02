
import clusters

def test_hcluster(blognames,words,data):
    test_blogclust(blognames,data)
    test_wordclust(words,data)

def test_blogclust(blognames,data):
    clust=clusters.hcluster(data)
    # printclust
    clusters.printclust(clust,labels=blognames)
    # draw dendrogram
    clusters.drawdendrogram(clust,blognames,jpeg='img/blogclust.jpeg')

def test_wordclust(words,data):
    rdata=clusters.rotatematrix(data)
    wordclust=clusters.hcluster(rdata)
    # printclust
    clusters.printclust(wordclust,labels=words)
    # draw dendrogram
    clusters.drawdendrogram(wordclust,labels=words,jpeg='img/wordclust.jpg')


def test_kcluster(blognames,data):
    kclust=clusters.kcluster(data,k=10)
    for kk in range(10):
        print [blognames[r] for r in kclust[kk]]

def test_beautifulsoup():
    import urllib2
    from BeautifulSoup import BeautifulSoup
    c=urllib2.urlopen("http://kiwitobes.com/")
    soup=BeautifulSoup(c.read())
    links=soup('a')
    print links[10]
    print links[10]['href']

def test_hcluster2(wants,data):
    clust=clusters.hcluster(data,distance=clusters.tanimoto)
    clusters.drawdendrogram(clust,wants)

def test_mds(blognames,data):
    coords=clusters.scaledown(data)
    clusters.draw2d(coords,blognames,jpeg="img/blogs2d.jpg")

def main():
    # blog data
    blognames,words,data=clusters.readfile('txt/blogdata.txt')
    test_hcluster(blognames,words,data)
    test_kcluster(blognames,data)
    test_beautifulsoup()
    # zebo data
    wants,people,data=clusters.readfile('txt/zebo.txt')
    test_hcluster2(wants,data)
    # mds (multidimentional scaling) with blog data
    test_mds(blognames,data)

if __name__ == '__main__':
    main()
