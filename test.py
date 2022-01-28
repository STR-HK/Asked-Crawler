from askedCrawl import Crawler

c = Crawler('id', 50)
c.save_on('filename.txt')
c.crawl()