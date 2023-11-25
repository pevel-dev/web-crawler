from src.cache import Cache
from src.crawler import Crawler

if __name__ == "__main__":
    cache_1 = Cache('1.txt', set())
    cache_2 = Cache('1.txt', set())
    crawler = Crawler("https://www.wikipedia.org/", [lambda x: 'wikipedia.org' in x.netloc], cache_1, cache_2)
    crawler.start()
