from .nativeCommand import NativeCommand

##
# @class RunCommand
#
# @brief This Command retrieves the result of a user-provided command line
class RunCommand(NativeCommand):

    @staticmethod
    def id():
        return "runCommand"

    def execute_command(self, value):
        return self.execute(value)
