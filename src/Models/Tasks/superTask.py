from abc import abstractmethod
from ...Utility.printer import Printer
from .Executers.executerImporter import Executer

##
# @class SuperTask
# @pure
#
# @brief This is an abstract class that must be extended by every Task
class SuperTask():

    def __init__(self):
        pass

    ##
    # @static
    # @return Task's identifier to be used in the input
    #
    # @brief Each concrete implementation of the SuperTask class should contain it's own, unique identifier. \n
    # If no identifier is declared, the SuperTask's id() method is called instead.
    @staticmethod
    def id():
        return "SuperTaskID"

    ##
    # @pure
    #
    # @param self The Task's instance
    # @param value The Task's necessary parameters
    #
    # @brief Executes the Task's code.
    @abstractmethod
    def executeTask(self, value, inheritedResult):
        Printer.getInstance().printMessage("This has been executed on %s" %(self.id()))

    ##
    # @param self The Task's instance
    # @command a str containing the command to be executed
    #
    # @return the result of the command's execution as a string
    # @return None if the execution failed
    #
    # @brief Sends it self and the task line to the Executer, where it will be dealt with.
    def executeCommand(self, command):
        return Executer.getInstance().executeCommand(self, command)