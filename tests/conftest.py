import pytest


@pytest.fixture()
def test_url() -> str:
    return 'url.com'


@pytest.fixture()
def test_urls() -> tuple[str, str, str]:
    url = 'test1.com'
    url1 = 'test2.com'
    url2 = 'test3.com'
    return url, url1, url2


@pytest.fixture()
def empty_html() -> str:
    return """
    <html>
    <h1> Hello </h1>
    </html>
    """


@pytest.fixture()
def html_with_links(test_urls):
    html = "<html>\n"
    for i in test_urls:
        html += f'<a href="{i}">url</a>\n'
    html += "</html>"

    return html
