import pytest
from httpx import Response
from respx import MockRouter

from main import main


@pytest.mark.parse
def test_parse(test_url: str, respx_mock: MockRouter, html_with_links, test_urls, empty_html):
    mock_route_main = respx_mock.get(test_url).mock(
        return_value=Response(200, text=html_with_links)
    )
    mocks = []
    for i in test_urls:
        mocks.append(respx_mock.get(i).mock(return_value=Response(200, text=empty_html)))

    class Args:
        url = test_url
        timeout = 5
        retry_count = 0
        follow_redirect = False
        threads = 5

    main(Args)
    assert mock_route_main.called
    for i in mocks:
        assert i.called
