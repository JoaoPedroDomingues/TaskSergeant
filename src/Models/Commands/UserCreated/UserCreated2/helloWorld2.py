from .userGenerated2Command import UserGenerated2Command, Printer

##
# @class Hello
#
# @brief This Command is a test
class HelloWorld2(UserGenerated2Command):

    @staticmethod
    def id():
        return "helloWorld2"

    def execute_command(self, value):
        Printer.getInstance().printMessage("Is this working?")
        return None
