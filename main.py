import argparse
import sys

from src.cache import Cache
from src.crawler import Crawler
from src.file_save import FileSave


arg_parse = argparse.ArgumentParser(
    prog='Web Crawler'
)
arg_parse.add_argument('-u', '--url', type=str, default="https://ru.wikipedia.org", help='Target url for start crawling')
arg_parse.add_argument('-t', '--timeout', type=float, default=5, help='Request timeout')
arg_parse.add_argument('-c', '--retry_count', type=int, default=1, help='Max retry count for request')
arg_parse.add_argument('-r', '--follow_redirect', type=bool, default=True, help='Allow redirects')
arg_parse.add_argument('-th', '--threads', type=int, default=10, help='Max count threads')
arg_parse.add_argument('-s', '--from_save', type=bool, default=True)


if __name__ == "__main__":
    need_visit_cache = Cache('need_visit_cache.pickle', set())
    visited_cache = Cache('visited_cache.pickle', set())
    need_visit_cache.load()
    visited_cache.load()
    args = arg_parse.parse_args()
    file_saver = FileSave('save')
    url_filters = [lambda x: 'wikipedia.org' in x.netloc]
    crawler = Crawler(
        str(args.url),
        url_filters,
        need_visit_cache,
        visited_cache,
        file_saver,
        args.timeout,
        args.retry_count,
        args.follow_redirect,
        args.threads,
    )
    try:
        crawler.start()
    except KeyboardInterrupt:
        sys.exit(0)
