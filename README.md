Crawler
=======

A crawler is a program that starts with a url on the web (ex: http://python.org), fetches the web-page corresponding to that url, and parses all the links on that page into a repository of links. Next, it fetches the contents of any of the url from the repository just created, parses the links from this new content into the repository and continues this process for all links in the repository until stopped or after a given number of links are fetched. 

crawler.py is a python crawler program and it needs two arguments i.e.,

    #   1. Website link to start crawling from. ( http://..............)
    #   2. Number of links to store ( if not provided, 100 is considered as default value)
    
