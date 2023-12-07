import threading
import time
import urllib.parse
from threading import Lock, Thread

from src.cache import Cache
from src.file_save import FileSave
from src.link_parser import LinkParser
from src.parser import Parser


class Crawler:
    def __init__(
            self,
            start_url: str,
            url_filter_predicates: list,
            need_visit_cache: Cache,
            visited_cache: Cache,
            file_save: FileSave,
            timeout: int,
            retry_count: int,
            follow_redirects: bool,
            max_threads: int = 5000,
    ):
        self._start_url = start_url
        self._url_filter_predicates = url_filter_predicates
        self._need_visit_cache = need_visit_cache
        self._need_visit = need_visit_cache.cache
        self._visited_cache = visited_cache
        self._visited = visited_cache.cache
        self._max_threads = max_threads
        self._lock = Lock()
        self._file_save_service = file_save
        self._timeout = timeout
        self._retry_count = retry_count
        self._follow_redirects = follow_redirects

        self.SAVE_TASKS_COUNT = 5000

    def start(self):
        # self.check_robots(self._start_url)
        count = 0
        self._need_visit.add(self._start_url)
        while len(self._need_visit) > 0 or threading.active_count() > 1:
            if threading.active_count() > self._max_threads or len(self._need_visit) == 0:  # wait end started tasks
                time.sleep(0.01)
                continue
            self._lock.acquire()
            current_link = self._need_visit.pop()
            self._visited.add(current_link)
            self._lock.release()

            new_task = Thread(target=self.crawler_task, args=(current_link,))
            new_task.start()
            if count % self.SAVE_TASKS_COUNT == 0:
                self._lock.acquire()

                self._visited_cache.save()
                self._need_visit_cache.save()

                self._lock.release()

    def update_links(self, base_url: str, new_links: list[str]) -> None:
        for link in new_links:
            try:
                parsed_link = urllib.parse.urlparse(link)
                if not parsed_link.netloc:
                    parsed_link = urllib.parse.urljoin(str(base_url), link)
                else:
                    parsed_link = parsed_link.geturl()
                if parsed_link not in self._visited:
                    self.add_link(parsed_link)
            except Exception as ex:
                pass

    def add_link(self, link: str) -> None:
        parsed_link = urllib.parse.urlparse(link)
        for filter_predicate in self._url_filter_predicates:
            if not filter_predicate(parsed_link):
                return
        self._lock.acquire()
        self._need_visit.add(parsed_link.geturl())
        self._lock.release()

    def crawler_task(self, current_url: str) -> None:
        url, body = Parser.download_url(url=current_url, timeout=self._timeout, retry_max_count=self._retry_count, follow_redirects=self._follow_redirects)
        if Parser.is_html(body):
            links = LinkParser()
            links.feed(body)
            self.update_links(url, links.links)
            self._file_save_service.html_save(str(url), body)

    def check_robots(self, url):
        not_in_url = []
        _, body = Parser.download_url(url + 'robots.txt', follow_redirects=True)
        all_user_agent = False
        for i in body.split('\n'):
            splited = i.split(':')
            if len(splited) == 2:
                option, value = splited
                if option.lower() == 'user-agent':
                    all_user_agent = value.strip() == '*'
                if option.lower() == 'disallow' and all_user_agent:
                    not_in_url.append((url + value.strip()).replace('//', '/'))
        self._url_filter_predicates.append(
            lambda url: url not in not_in_url
        )
