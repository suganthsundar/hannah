import uuid
import asyncio

import httpx

from hannah.http.mappings import HTTPTrafficMapper


REQUEST_RATE_LIMIT = 50


class HTTPSession:

    def __init__(self, name: str, base_url: str = None,
                 auth: tuple = None,
                 headers: dict = None,
                 ssl_verify: bool = False,
                 raise_on_non_2xx_error: bool = False,
                 request_limit: int = REQUEST_RATE_LIMIT,
                 timeout: float = 10.0):
        self.id = uuid.uuid4()
        self.name = name
        self.base_url = base_url
        self.headers = headers if headers else {}
        self.ssl_verify = ssl_verify
        self.raise_on_non_2xx_error = raise_on_non_2xx_error
        self.semaphore = asyncio.Semaphore(request_limit)
        self.timeout = timeout
        if auth:
            self.set_auth(*auth)

    def __repr__(self):
        return f"HTTPSession<id={self.id},name={self.name}>"

    def set_base_url(self, base_url: str):
        self.base_url = base_url

    def set_auth(self, auth_type: str, token: str):
        self.headers.update({'Authorization': f'{auth_type} {token}'})

    async def request(self, method: str, uri: str, **kwargs):
        async with self.semaphore:
            async with httpx.AsyncClient(headers=self.headers, timeout=self.timeout) as client:
                r = await client.request(method, f'{self.base_url}{uri}', **kwargs)
                if self.raise_on_non_2xx_error and (r.status_code < 200 or r.status_code >= 300):
                    raise HTTPStatusError(HTTPTrafficMapper(r))
                return HTTPTrafficMapper(r)


class BearerToken:

    def __init__(self, token: str):
        self.type = 'BEARER'
        self.token = token


class HTTPStatusError(Exception):

    def __init__(self, traffic: HTTPTrafficMapper):
        self.traffic = traffic

    def __str__(self):
        return f'[{self.traffic.response.status}] {self.traffic.request.method} {self.traffic.request.url}'
