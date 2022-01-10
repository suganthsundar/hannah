import pytest
from hannah.http.session import HTTPSession, HTTPStatusError

name: str = 'Users'
url: str = 'https://reqres.in'
session = HTTPSession(name, url)


@pytest.mark.asyncio
async def test_session_auth():
    auth = ('Bearer', '234234233252352523')
    session.set_auth(*auth)
    assert session.headers['Authorization'] == '{} {}'.format(*auth)


@pytest.mark.asyncio
async def test_200_ok():
    traffic = await session.request('GET', '/api/users')
    assert traffic.response.status == 200
    assert type(traffic.response.body) == dict
    assert traffic.response.body['page'] == 1


@pytest.mark.asyncio
async def test_404_not_found():
    traffic = await session.request('GET', '/api/users/unknown')
    assert traffic.response.status == 404


@pytest.mark.asyncio
async def test_404_not_found_with_raise_status_error():
    with pytest.raises(HTTPStatusError):
        s = HTTPSession(name, url, raise_on_non_2xx_error=True)
        await s.request('GET', '/api/user/unknown')


@pytest.mark.asyncio
async def test_request_limit():
    s = HTTPSession(name, url, raise_on_non_2xx_error=True, request_limit=10)
    assert s.semaphore._value == 10
