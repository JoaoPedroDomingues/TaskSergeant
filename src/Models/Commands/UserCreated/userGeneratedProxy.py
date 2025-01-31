from ..superProxy import SuperProxy

class UserGeneratedProxy(SuperProxy):

    @staticmethod
    def id():
        return "UserGenerated"

    commands = {}

    proxies = {}
