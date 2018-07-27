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
            description='This is a sample Petstore server.  You can find out more '
            'about Swagger at <a href=\"http://swagger.wordnik.com\">http://swagger.wordnik.com</a> '
            'or on irc.freenode.net, #swagger.  For this sample, you can use the api '
            'key \"special-key\" to test the authorization filters',
            plugins=[FalconPlugin(app)],
        )
    return _spec


@pytest.fixture()
def app_context():
    class HelloResource:
        """Greeting API.
        ---
        x-extension: global metadata
        """
        def on_get(self, req, resp):
            """A greeting endpoint.
            ---
            description: get a greeting
            responses:
                200:
                    description: said hi
            """
            return "hi"

        def on_post(self, req, resp):
            return "hi"

    app = falcon.API()
    hello_resource = HelloResource()
    app.add_route("/hi", hello_resource)
    return app, hello_resource


class TestPathHelpers:

    def test_path_from_resource(self, app_context, spec_factory):
        app, resource = app_context
        spec = spec_factory(app)
        spec.add_path(
            resource=resource, methods=["GET"],
            operations={'get': {'parameters': [], 'responses': {'200': {}}}},
        )
        expected = {
            'description': 'get a greeting',
            'responses': {200: {'description': 'said hi'}},
        }
        assert spec._paths['/hi']['get'] == expected
        assert spec._paths['/hi']['post'] == {}
        assert spec._paths['/hi']['x-extension'] == 'global metadata'


    # def test_path_from_method_view(self, app, spec):
    #     class HelloApi(MethodView):
    #         """Greeting API.
    #         ---
    #         x-extension: global metadata
    #         """
    #         def get(self):
    #             """A greeting endpoint.
    #             ---
    #             description: get a greeting
    #             responses:
    #                 200:
    #                     description: said hi
    #             """
    #             return 'hi'

    #         def post(self):
    #             return 'hi'

    #     method_view = HelloApi.as_view('hi')
    #     app.add_url_rule('/hi', view_func=method_view, methods=('GET', 'POST'))
    #     spec.add_path(view=method_view)
    #     expected = {
    #         'description': 'get a greeting',
    #         'responses': {200: {'description': 'said hi'}},
    #     }
    #     assert spec._paths['/hi']['get'] == expected
    #     assert spec._paths['/hi']['post'] == {}
    #     assert spec._paths['/hi']['x-extension'] == 'global metadata'

    # def test_path_with_multiple_methods(self, app, spec):

    #     @app.route('/hello', methods=['GET', 'POST'])
    #     def hello():
    #         return 'hi'

    #     spec.add_path(
    #         view=hello, operations=dict(
    #             get={'description': 'get a greeting', 'responses': {'200': {}}},
    #             post={'description': 'post a greeting', 'responses': {'200': {}}},
    #         ),
    #     )
    #     get_op = spec._paths['/hello']['get']
    #     post_op = spec._paths['/hello']['post']
    #     assert get_op['description'] == 'get a greeting'
    #     assert post_op['description'] == 'post a greeting'

    # def test_methods_from_rule(self, app, spec):
    #     class HelloApi(MethodView):
    #         """Greeting API.
    #         ---
    #         x-extension: global metadata
    #         """
    #         def get(self):
    #             """A greeting endpoint.
    #             ---
    #             description: get a greeting
    #             responses:
    #                 200:
    #                     description: said hi
    #             """
    #             return 'hi'

    #         def post(self):
    #             return 'hi'

    #         def delete(self):
    #             return 'hi'

    #     method_view = HelloApi.as_view('hi')
    #     app.add_url_rule('/hi', view_func=method_view, methods=('GET', 'POST'))
    #     spec.add_path(view=method_view)
    #     assert 'get' in spec._paths['/hi']
    #     assert 'post' in spec._paths['/hi']
    #     assert 'delete' not in spec._paths['/hi']

    # def test_integration_with_docstring_introspection(self, app, spec):

    #     @app.route('/hello')
    #     def hello():
    #         """A greeting endpoint.

    #         ---
    #         x-extension: value
    #         get:
    #             description: get a greeting
    #             responses:
    #                 200:
    #                     description: a pet to be returned
    #                     schema:
    #                         $ref: #/definitions/Pet

    #         post:
    #             description: post a greeting
    #             responses:
    #                 200:
    #                     description: some data

    #         foo:
    #             description: not a valid operation
    #             responses:
    #                 200:
    #                     description:
    #                         more junk
    #         """
    #         return 'hi'

    #     spec.add_path(view=hello)
    #     get_op = spec._paths['/hello']['get']
    #     post_op = spec._paths['/hello']['post']
    #     extension = spec._paths['/hello']['x-extension']
    #     assert get_op['description'] == 'get a greeting'
    #     assert post_op['description'] == 'post a greeting'
    #     assert 'foo' not in spec._paths['/hello']
    #     assert extension == 'value'

    # def test_path_is_translated_to_swagger_template(self, app, spec):

    #     @app.route('/pet/<pet_id>')
    #     def get_pet(pet_id):
    #         return 'representation of pet {pet_id}'.format(pet_id=pet_id)

    #     spec.add_path(view=get_pet)
    #     assert '/pet/{pet_id}' in spec._paths

    # def test_path_includes_app_root(self, app, spec):

    #     spec.options['basePath'] = '/v1'
    #     app.config['APPLICATION_ROOT'] = '/v1/app/root'

    #     @app.route('/partial/path/pet')
    #     def get_pet():
    #         return 'pet'

    #     spec.add_path(view=get_pet)
    #     assert '/app/root/partial/path/pet' in spec._paths

    # def test_path_with_args_includes_app_root(self, app, spec):

    #     spec.options['basePath'] = '/v1'
    #     app.config['APPLICATION_ROOT'] = '/v1/app/root'

    #     @app.route('/partial/path/pet/{pet_id}')
    #     def get_pet(pet_id):
    #         return 'representation of pet {pet_id}'.format(pet_id=pet_id)

    #     spec.add_path(view=get_pet)
    #     assert '/app/root/partial/path/pet/{pet_id}' in spec._paths

    # def test_path_includes_app_root_with_right_slash(self, app, spec):

    #     spec.options['basePath'] = '/v1'
    #     app.config['APPLICATION_ROOT'] = '/v1/app/root/'

    #     @app.route('/partial/path/pet')
    #     def get_pet():
    #         return 'pet'

    #     spec.add_path(view=get_pet)
    #     assert '/app/root/partial/path/pet' in spec._paths
