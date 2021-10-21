import pytest

from hannah.http.session import HTTPSession
from hannah.models import SwaggerService

name: str = 'petstore'
url: str = 'https://petstore.swagger.io'


@pytest.mark.asyncio
async def test_swagger_service():
    session = HTTPSession(name, url)
    service = SwaggerService.from_url(name, url, session, swagger_path='/v2/swagger.json')
    await service.findPetsByStatus()
