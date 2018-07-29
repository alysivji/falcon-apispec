import pytest

import falcon
from apispec import APISpec
from falcon_apispec import FalconPlugin


@pytest.fixture()
def spec_factory():
    def _spec(app):
        return APISpec(
            title='Swagger Petstore',
            version='1.0.0',
            description=
            'This is a sample Petstore server.  You can find out more '
            'about Swagger at <a href=\"http://swagger.wordnik.com\">http://swagger.wordnik.com</a> '
            'or on irc.freenode.net, #swagger.  For this sample, you can use the api '
            'key \"special-key\" to test the authorization filters',
            plugins=[FalconPlugin(app)],
        )

    return _spec


@pytest.fixture()
def app():
    falcon_app = falcon.API()
    return falcon_app


class TestPathHelpers:
    def test_gettable_resource(self, app, spec_factory):
        class HelloResource:
            def on_get(self, req, resp):
                """A greeting endpoint.
                ---
                description: get a greeting
                responses:
                    200:
                        description: said hi
                """
                return "dummy"

        expected = {
            'description': 'get a greeting',
            'responses': {
                200: {
                    'description': 'said hi'
                }
            },
        }
        hello_resource = HelloResource()
        app.add_route("/hi", hello_resource)
        spec = spec_factory(app)
        spec.add_path(resource=hello_resource)

        assert spec._paths['/hi']['get'] == expected

    def test_posttable_resource(self, app, spec_factory):
        class HelloResource:
            def on_post(self, req, resp):
                """A greeting endpoint.
                ---
                description: get a greeting
                responses:
                    201:
                        description: posted something
                """
                return "hi"

        expected = {
            'description': 'get a greeting',
            'responses': {
                201: {
                    'description': 'posted something'
                }
            },
        }
        hello_resource = HelloResource()
        app.add_route("/hi", hello_resource)
        spec = spec_factory(app)
        spec.add_path(resource=hello_resource)

        assert spec._paths['/hi']['post'] == expected

    def test_resource_with_metadata(selfself, app, spec_factory):
        class HelloResource:
            """Greeting API.
            ---
            x-extension: global metadata
            """

        hello_resource = HelloResource()
        app.add_route("/hi", hello_resource)
        spec = spec_factory(app)
        spec.add_path(resource=hello_resource)

        assert spec._paths['/hi']['x-extension'] == 'global metadata'
