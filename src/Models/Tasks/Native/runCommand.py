from .nativeTask import NativeTask

##
# @class RunCommand
#
# @brief This Task retrieves the result of a user-provided command line
class RunCommand(NativeTask):

    @staticmethod
    def id():
        return "runCommand"

    def execute_task(self, value):
        return self.executeCommand(value)
