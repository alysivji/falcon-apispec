import copy
import re
from apispec import BasePlugin, yaml_utils
from apispec.exceptions import APISpecError


class FalconPlugin(BasePlugin):
    """APISpec plugin for Falcon"""

    def __init__(self, app):
        super(FalconPlugin, self).__init__()
        self._app = app

    @staticmethod
    def _generate_resource_uri_mapping(app, resource, suffix):
        routes_to_check = copy.copy(app._router._roots)

        mapping = {}
        for route in routes_to_check:
            uri = route.uri_template
            # Filter by resource so we don't have to parse all routes
            if route.resource == resource:
                mapping[uri] = {}
                if route.method_map:
                    methods = {}
                    for method_name, method_handler in route.method_map.items():
                        # Multiple conditions to ignore the method : falcon responder, or a method that does not
                        # meet the suffix requirements: no suffix provided = ignore suffixed methods, and vice-versa
                        if method_handler.__dict__.get("__module__") == "falcon.responders" or \
                                (suffix is not None and not method_handler.__name__.lower().endswith(suffix)) or \
                                (suffix is None and not method_handler.__name__.lower().endswith(method_name.lower())):
                            continue
                        methods.update({method_name.lower(): method_handler})
                    mapping[uri] = methods

            routes_to_check.extend(route.children)
        return mapping

    def path_helper(self, operations, resource, base_path=None, suffix=None, **kwargs):
        """Path helper that allows passing a Falcon resource instance."""
        resource_uri_mapping = self._generate_resource_uri_mapping(self._app, resource, suffix)

        if not resource_uri_mapping:
            raise APISpecError("Could not find endpoint for resource {0}".format(resource))

        operations.update(yaml_utils.load_operations_from_docstring(resource.__doc__) or {})

        # In case multiple uri were found, keep the only one that has methods
        try:
            path = next(uri for uri, methods in resource_uri_mapping.items() if methods)
        except StopIteration:
            path = next(iter(resource_uri_mapping))

        methods = resource_uri_mapping[path]

        if base_path is not None:
            # make sure base_path accept either with or without leading slash
            # swagger 2 usually come with leading slash but not in openapi 3.x.x
            base_path = '/' + base_path.strip('/')
            path = re.sub(base_path, "", path, 1)

        for method_name, method_handler in methods.items():
            docstring_yaml = yaml_utils.load_yaml_from_docstring(method_handler.__doc__)
            operations[method_name] = docstring_yaml or dict()
        return path
