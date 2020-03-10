from app.api import api
def init_app(app, **kwargs):
    """
    Init admin module.
    """
    from . import resource
    api.add_namespace(resource.ns)