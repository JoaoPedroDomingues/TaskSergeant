from ..superProxy import SuperProxy

class UserGeneratedProxy(SuperProxy):

    @staticmethod
    def id():
        return "UserGenerated"

    tasks = {}

    proxies = {}
