from pyramid.config import Configurator

from mozsvc.config import load_into_settings

from demoapp.resources import Root
from demoapp.storage import configure_from_settings


def main(global_config, **settings):
    config_file = global_config['__file__']
    load_into_settings(config_file, settings)

    config = Configurator(root_factory=Root, settings=settings)

    config.registry['storage'] = configure_from_settings(
        'storage', settings['config'].get_map('storage'))

    # adds authorization
    # option 1: auth via repoze.who
    #config.include("pyramid_whoauth")
    # option 2: auth based on IP address
    #config.include("pyramid_ipauth")
    # option 3: multiple stacked auth modules
    config.include("pyramid_multiauth")

    # adds cornice
    config.include("cornice")

    # adds Mozilla default views
    config.include("mozsvc")

    # adds application-specific views
    config.add_route("whoami", "/whoami")
    config.scan("demoapp.views")

    return config.make_wsgi_app()
