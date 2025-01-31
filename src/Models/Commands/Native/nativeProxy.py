from ..superProxy import SuperProxy

class NativeProxy(SuperProxy):

    @staticmethod
    def id():
        return "Native"

    commands = {}

    proxies = {}
