# hannah

`hannah` is a async swagger http client.

## installation

```
pip install hannah
```

## example

```python
from hannah.http.session import HTTPSession
from hannah.models import SwaggerService

session = HTTPSession(f'pet-store')
service = SwaggerService.from_url('pet-store', 'https://petstore.swagger.io',
                                  session, swagger_path='/v2/swagger.json')}
response = await service.getPetById(petId=1)
print(response)
```