import six
import zope.dottedname.resolve

from .exc import DottednameResolveError


def resolve(dottedname, raise_exception=False):
    if not isinstance(dottedname, (str, six.text_type)):
        return dottedname

    try:
        return zope.dottedname.resolve.resolve(dottedname)
    except ImportError:
        if raise_exception:
            raise DottednameResolveError('Cannot resolve name: {}'.format(dottedname))
        else:
            return None
