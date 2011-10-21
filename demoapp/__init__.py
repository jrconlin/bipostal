import os

from pyramid.config import Configurator

from mozsvc.config import Config

from demoapp.resources import Root


def main(global_config, **settings):
    config_file = global_config['__file__']
    config_file = os.path.abspath(
                    os.path.normpath(
                    os.path.expandvars(
                        os.path.expanduser(
                        config_file))))

    settings['config'] = config = Config(config_file)

    # Put values from the config file into the pyramid settings dict.
    for section in config.sections():
        if ":" in section:
            setting_prefix = section.replace(":", ".")
            for name, value in config.get_map(section).iteritems():
                settings[setting_prefix + "." + name] = value

    config = Configurator(root_factory=Root, settings=settings)

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
