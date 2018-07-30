import copy

from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError
import falcon


class FalconPlugin(BasePlugin):
    """APISpec plugin for Falcon"""

    def __init__(self, app):
        super(FalconPlugin, self).__init__()
        self._app = app

    @staticmethod
    def _generate_resource_uri_mapping(app):
        routes_to_check = copy.copy(app._router._roots)

        mapping = {}
        for route in routes_to_check:
            uri = route.uri_template
            resource = route.resource
            mapping[resource] = uri
            routes_to_check.extend(route.children)

        return mapping

    def path_helper(self, operations, resource, **kwargs):
        """Path helper that allows passing a Falcon resource instance."""
        resource_uri_mapping = self._generate_resource_uri_mapping(self._app)

        if resource not in resource_uri_mapping:
            raise APISpecError("Could not find endpoint for resource {0}".format(resource))

        operations.update(yaml_utils.load_operations_from_docstring(resource.__doc__) or {})
        path = resource_uri_mapping[resource]

        for method in falcon.constants.HTTP_METHODS:
            http_verb = method.lower()
            method_name = "on_" + http_verb
            if hasattr(resource, method_name):
                method = getattr(resource, method_name)
                docstring_yaml = yaml_utils.load_yaml_from_docstring(method.__doc__)
                operations[http_verb] = docstring_yaml or dict()

        return path
