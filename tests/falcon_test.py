import pytest
import yaml
import falcon
from apispec import APISpec
from falcon_apispec import FalconPlugin


@pytest.fixture()
def settings():
    OPENAPI_SPEC = """
    openapi: 3.0.2
    info:
      title: Swagger Petstore
      version: 1.0.0
      description: 'This is a sample server Petstore server. You can find out
        more about Swagger at [https://swagger.io](https://swagger.io) or on
        [irc.freenode.net, #swagger](https://swagger.io/irc/).
        For this sample, you can use the api key `special-key` to test
        the authorization filters.'
    servers:
    - url: http://localhost:{port}/{basePath}
      description: The development API server
      variables:
        port:
          enum:
          - '3000'
          - '8888'
          default: '3000'
        basePath:
          default: v1
    """
    return yaml.safe_load(OPENAPI_SPEC)


@pytest.fixture()
def spec_factory(settings):
    def _spec(app):
        # retrieve  title, version, and openapi version
        title = settings["info"].pop("title")
        spec_version = settings["info"].pop("version")
        openapi_version = settings.pop("openapi")
        description = settings["info"].pop("description")

        return APISpec(
            title=title,
            version=spec_version,
            openapi_version=openapi_version,
            description=description,
            plugins=[FalconPlugin(app)],
            **settings
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

    def test_unredundant_basepath_resource(self, app, spec_factory, settings):
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
        full_path = "/v1/foo/v1"
        path_expected = "/foo/v1"
        hello_resource = HelloResource()
        app.add_route(full_path, hello_resource)
        spec = spec_factory(app)
        base_path = \
            settings["servers"][0]["variables"]["basePath"].get("default")
        # in swagger 2 this is simply 'basePath: /v1'
        spec.path(resource=hello_resource, base_path=base_path)

        assert spec._paths.get(path_expected) is not None
        assert spec._paths[path_expected]["get"] == expected
