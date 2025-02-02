from abc import abstractmethod
from ...Utility.printer import Printer
from .Executers.executerImporter import Executer

##
# @class SuperCommand
# @pure
#
# @brief This is an abstract class that must be extended by every Command
class SuperCommand():

    def __init__(self):
        pass

    ##
    # @static
    # @return Command's identifier to be used in the input
    #
    # @brief Each concrete implementation of the SuperCommand class should contain it's own, unique identifier. \n
    # If no identifier is declared, the SuperCommand's id() method is called instead.
    @staticmethod
    def id():
        return "SuperCommandID"

    ##
    # @pure
    #
    # @param self The Command's instance
    # @param value The Command's necessary parameters
    #
    # @brief Executes the Command's code.
    @abstractmethod
    def execute_task(self, value):
        Printer.getInstance().printMessage("This has been executed on %s" %(self.id()))

    ##
    # @param self The Command's instance
    # @command a str containing the command-line to be executed
    #
    # @return the result of the command-line's execution as a string
    # @return None if the execution failed
    #
    # @brief Sends it self and the command line to the Executer, where it will be dealt with.
    def execute_command(self, command):
        return Executer.getInstance().executeCommand(self, command)