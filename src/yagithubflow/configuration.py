import six
from miniconfig import ConfiguratorCore
from zope.interface.registry import Components

from . import exc
from . import flow
from . import dottedname


class Configurator(ConfiguratorCore):
    default_flow_factory = flow.Flow

    def __init__(self, *args, **kwds):
        super(Configurator, self).__init__(*args, **kwds)
        self.registry = Components()

    def make_app(self):
        """Create flow application"""
        self.commit()
        factory = self.get_flow_factory()
        return factory(self)

    def get_flow_factory(self):
        """Get flow factory"""
        factory = self.settings['flow_factory']
        factory = dottedname.resolve(factory)

        if factory is None:
            raise exc.FlowPluginResolveError('Plugin not found: {}'.format(dottedname))

        if not callable(factory):
            raise exc.FlowPluginFactoryError(
                'Must be callable object: {}'.format(factory))

        return factory


def bootstrap(root, *config_paths):
    dottedname.resolve(root, raise_exception=True)

    settings = six.moves.ConfigParser()
    settings.read(config_paths)

    configurator = Configurator(settings=settings)
    configurator.include(root)
    return configurator
