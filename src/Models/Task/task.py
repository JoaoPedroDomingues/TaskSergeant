from ..Commands.superProxy import SuperProxy
from ..Assertions.assertionRetriever import AssertionRetriever
from ..Commands.commandRetriever import *
from ...Utility.printer import Printer
import time

##
# @class Task
# @brief Represents a Task - this is the main unit of the program.
#
# This is a Task, which is the main unit of the program. \n
# Composed of the following elements: SuperCommand, SuperAssertion and data
class Task():

    ##
    # @param self
    #
    # Instantiates the data attribute as an empty dict
    def __init__(self):
        self.data = {}
        pass

    ##
    # @param self Task instance
    #
    # @return Command execution result (may be None) - no associated type
    # @return None if no Command is found
    #
    # @brief Calls the class __setup() function. \n
    # If there's a valid Command instance, executes it, followed by the Assertion.
    def execute(self):
        if self.command is None:
            Printer.getInstance().printMessage("No such Command found: %s" %(self.data["categories"]), 1)
            return None

        Printer.getInstance().printMessage("Starting Task -> %s" %(self.data["description"]))

        start_time = time.time() # Starts counting the execution time of the task (command + assertion)

        self.data["commandResult"] = self.command.execute_command(self.data["value"])
        self.data["assertionResult"] = self.assertion.execute_assertion(self.data["commandResult"], self.data["expectedValue"])

        # Stores the task's execution time
        executionTime = time.time() - start_time
        self.data["executionTime"] = executionTime

        Printer.getInstance().printMessage(" vvv Task execution time: %s vvv" %(executionTime))
        Printer.getInstance().processTask(self)

        return self.data["assertionResult"]

    ##
    # @param self Task instance
    #
    # @brief Invokes the necessary procedures in order to execute the Task
    def setup(self):
        self.__setCommand()
        self.__setAssertion()

    ##
    # @param self Task instance
    #
    # @brief Retrieves the Command instance
    def __setCommand(self):
        self.command = retrieveCommand(SuperProxy(), list(self.data["categories"]))

    ##
    # @param self Task instance
    #
    # @brief Retrieves the Assertion instance
    def __setAssertion(self):
        self.assertion = AssertionRetriever.retrieveAssertion(self.data["assertionType"])

    ##
    # @param self Task instance
    #
    # @return The Task formatted as a dict
    #
    # @brief Returns the Task's information as a dict
    def asOutput(self):
        task = dict(self.data)

        task.pop("commandResult", None)

        return task
