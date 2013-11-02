depends on feedparser and BeautifulSoup

----------------------
http://yoshishi.blog.so-net.ne.jp/2012-11-13
easy_install --> pip --> BeautifulSoup

1. installing easy_install
1-1. wget http://peak.telecommunity.com/dist/ez_setup.py
1-2. python ez_setup.py
--> installed in <python install path>/Scripts/
1-3. add <Python include path>/Scripts/ to PATH
1-4. easy_install --help

2. installing pip
2-1. easy_install pip
--> installed in <python install path>/Scripts/
2-2. pip --version

3. installing BeautifulSoup
3-1. pip install BeautifulSoup
--> <Python install path>/Lib/site-packages/BeautifulSoup.py

----------------------
http://blog.livedoor.jp/forest_caster/archives/1809751.html

1. from http://code.google.com/p/feedparser/
wget https://code.google.com/p/feedparser/downloads/detail?name=feedparser-5.1.3.zip
2. unzip and cd
3. python setup.py install
4. cp build\lib\feedparser.py <python install directory>