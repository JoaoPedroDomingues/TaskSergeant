from .userGeneratedCommand import UserGeneratedCommand, Printer

##
# @class Hello
#
# @brief This Command is a test
class HelloWorld(UserGeneratedCommand):

    @staticmethod
    def id():
        return "helloWorld"

    def execute_command(self, value):
        Printer.getInstance().printMessage("I'm a Command in a Sub Category!")
        return None
