import httpx


class Parser:
    @staticmethod
    def download_url(
            url: str,
            user_agent: str = "Mozilla/5.0 (compatible; IndexBot/0.1)",
            timeout: float = 1,
            retry_max_count: int = 0,
            follow_redirects: bool = False,
    ) -> tuple[str, str] | None:
        retry_count = 0
        while True:
            try:
                request = httpx.get(
                    url,
                    timeout=timeout,
                    headers={"user-agent": user_agent},
                    follow_redirects=follow_redirects,
                )
                if request.status_code == httpx.codes.OK:
                    return request.url, request.text
            except Exception as ex:
                pass
            retry_count += 1
            if retry_count > retry_max_count:
                return None, None

    @staticmethod
    def is_html(body: str):
        return body is not None and "<html" in body.lower()
