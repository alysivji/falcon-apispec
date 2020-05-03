import pytest

import falcon
from apispec import APISpec
from falcon_apispec import FalconPlugin


@pytest.fixture()
def spec_factory():
    def _spec(app):
        return APISpec(
            title="Swagger Petstore",
            version="1.0.0",
            openapi_version="3.0.2",
            description="This is a sample Petstore server.  You can find out "
            'more about Swagger at <a href="https://swagger.io"> '
            "http://swagger.wordnik.com</a> or on irc.freenode.net, #swagger."
            'For this sample, you can use the api key "special-key" to test '
            "the authorization filters",
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
            "description": "get a greeting",
            "responses": {"200": {"description": "said hi"}},
        }
        hello_resource = HelloResource()
        app.add_route("/hi", hello_resource)
        spec = spec_factory(app)
        spec.path(resource=hello_resource)

        assert spec._paths["/hi"]["get"] == expected

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
            "description": "get a greeting",
            "responses": {"201": {"description": "posted something"}},
        }
        hello_resource = HelloResource()
        app.add_route("/hi", hello_resource)
        spec = spec_factory(app)
        spec.path(resource=hello_resource)

        assert spec._paths["/hi"]["post"] == expected

    def test_resource_with_metadata(self, app, spec_factory):
        class HelloResource:
            """Greeting API.
            ---
            x-extension: global metadata
            """

        hello_resource = HelloResource()
        app.add_route("/hi", hello_resource)
        spec = spec_factory(app)
        spec.path(resource=hello_resource)

        assert spec._paths["/hi"]["x-extension"] == "global metadata"

    def test_unredundant_basepath_resource_with_slash(self, app, spec_factory):
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
            "description": "get a greeting",
            "responses": {"200": {"description": "said hi"}},
        }
        hello_resource = HelloResource()
        app.add_route("/v1/foo/v1", hello_resource)
        spec = spec_factory(app)
        base_path = '/v1'
        spec.path(resource=hello_resource, base_path=base_path)

        assert spec._paths["/foo/v1"]["get"] == expected

    def test_unredundant_basepath_resource_wo_slash(self, app, spec_factory):
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
            "description": "get a greeting",
            "responses": {"200": {"description": "said hi"}},
        }
        hello_resource = HelloResource()
        app.add_route("/v1/foo/v1", hello_resource)
        spec = spec_factory(app)
        base_path = 'v1'
        spec.path(resource=hello_resource, base_path=base_path)

        assert spec._paths["/foo/v1"]["get"] == expected

    def test_path_with_suffix(self, app, spec_factory):
        class HelloResource:
            def on_get_hello(self):
                """A greeting endpoint.
                ---
                description: get a greeting
                responses:
                    200:
                        description: said hi
                """
                return "dummy"

            def on_get(self):
                """An invalid method.
                ---
                description: this should not pass
                responses:
                    200:
                        description: said hi
                """
                return "invalid"

        expected = {
            "description": "get a greeting",
            "responses": {"200": {"description": "said hi"}},
        }

        hello_resource_with_suffix = HelloResource()
        app.add_route("/hi", hello_resource_with_suffix, suffix="hello")

        spec = spec_factory(app)
        spec.path(resource=hello_resource_with_suffix)

        assert spec._paths["/hi"]["get"] == expected
