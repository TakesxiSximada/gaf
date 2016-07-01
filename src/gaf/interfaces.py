from zope.interface import Interface


class IPart(Interface):
    pass


class IDefaultPart(IPart):
    pass


class IReleasePart(IPart):
    pass


class IHotfixPart(IPart):
    pass
