# falcon-apispec

[![Build Status](https://travis-ci.org/alysivji/falcon-apispec.svg?branch=master)](https://travis-ci.org/alysivji/falcon-apispec) [![codecov](https://codecov.io/gh/alysivji/falcon-apispec/branch/master/graph/badge.svg)](https://codecov.io/gh/alysivji/falcon-apispec) [![PyPI](https://img.shields.io/pypi/v/falcon-apispec.svg)](https://pypi.org/project/falcon-apispec/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

[apispec](https://github.com/marshmallow-code/apispec) plugin that generates OpenAPI specification (aka Swagger) for [Falcon](https://falconframework.org/) web applications.

Apispec uses three sources of information. Basic information is directly given to `APISpec()`. The plugin reads information about paths from the Falcon app. Information about an object could be given by [marshmallow](https://marshmallow.readthedocs.io/en/stable/) specification

## Installation

```console
pip install falcon-apispec
```

Optionaly:
```console
pip install marshmallow
```


Works with `apispec v1.0+`.

## Example Application

```python
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
import falcon
from falcon_apispec import FalconPlugin
from marshmallow import Schema, fields


# Optional marshmallow support
class CategorySchema(Schema):
    id = fields.Int()
    name = fields.Str(required=True)

class PetSchema(Schema):
    category = fields.Nested(CategorySchema, many=True)
    name = fields.Str()


# Create Falcon web app
app = falcon.API()

class PetResource:
    def on_get(self, req, resp):
        """A cute furry animal endpoint.
        ---
        description: Get a random pet
        responses:
            200:
                description: A pet to be returned
                schema: PetSchema
        """
        pet = get_random_pet()  # returns JSON
        resp.media = pet
    
    def on_get_one(self, req, resp, pet):
        """A cute furry animal endpoint.
        ---
        description: Get a random pet
        parameters:
            - in: path
              name: pet
              required: true
              schema:
                type: string
        responses:
            200:
                description: A pet to be returned
                schema: PetSchema
        """
        pet = get_pet(pet)  # returns JSON
        resp.media = pet

# create instance of resource
pet_resource = PetResource()
# pass into `add_route` for Falcon
app.add_route("/random", pet_resource)
app.add_route("/{pet}", pet_resource, suffix="one")


# Create an APISpec
spec = APISpec(
    title='Swagger Petstore',
    version='1.0.0',
    openapi_version='2.0',
    plugins=[
        FalconPlugin(app),
        MarshmallowPlugin(),
    ],
)

# Register entities and paths
spec.components.schema('Category', schema=CategorySchema)
spec.components.schema('Pet', schema=PetSchema)
# pass created resource into `path` for APISpec
# should be passed twice so the suffix is registered
# path should be called n + 1 times where n is the number of suffixes
spec.path(resource=random_pet_resource)
spec.path(resource=random_pet_resource)
```

### Generated OpenAPI Spec

```python
spec.to_dict()
# {
#   "info": {
#     "title": "Swagger Petstore",
#     "version": "1.0.0"
#   },
#   "swagger": "2.0",
#   "paths": {
#     "/random": {
#       "get": {
#         "description": "A cute furry animal endpoint.",
#         "responses": {
#           "200": {
#             "schema": {
#               "$ref": "#/definitions/Pet"
#             },
#             "description": "A pet to be returned"
#           }
#         }
#       }
#     },
#     "/v1/client/{team}/{client_uuid:uuid}": {
#       "get": {
#         "description": "A cute furry animal endpoint.",
#         "parameters": [
#           {
#             "in": "path",
#             "name": "pet",
#             "required": true,
#             "schema": {
#               "type": "string"
#             }
#           }
#         ],
#         "responses": {
#           "200": {
#             "schema": {
#               "$ref": "#/definitions/Pet"
#             },
#             "description": "A pet to be returned"
#           }
#         }
#       }
#     }
#   },
#   "definitions": {
#     "Pet": {
#       "properties": {
#         "category": {
#           "type": "array",
#           "items": {
#             "$ref": "#/definitions/Category"
#           }
#         },
#         "name": {
#           "type": "string"
#         }
#       }
#     },
#     "Category": {
#       "required": [
#         "name"
#       ],
#       "properties": {
#         "name": {
#           "type": "string"
#         },
#         "id": {
#           "type": "integer",
#           "format": "int32"
#         }
#       }
#     }
#   }
# }

spec.to_yaml()
# definitions:
#   Pet:
#     enum: [name, photoUrls]
#     properties:
#       id: {format: int64, type: integer}
#       name: {example: doggie, type: string}
# info: {description: 'This is a sample Petstore server.  You can find out more ', title: Swagger Petstore, version: 1.0.0}
# parameters: {}
# paths: {}
# security:
# - apiKey: []
# swagger: '2.0'
# tags: []
```

## Contributing

### Setting Up for Local Development

1. Fork falcon-apispec on Github
2. Install development requirements. Virtual environments are highly recommended

```console
pip install -r requirements.txt
```

### Running Tests

```console
pytest
```
