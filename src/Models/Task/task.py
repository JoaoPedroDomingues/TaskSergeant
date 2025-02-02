from ..Tasks.superProxy import SuperProxy
from ..Assertions.assertionRetriever import AssertionRetriever
from ..Tasks.taskRetriever import *
from ...Utility.printer import Printer
import time

##
# @class Task
# @brief Represents a Task - this is the main unit of the program.
#
# This is a Task, which is the main unit of the program. \n
# Composed of the following elements: SuperTask, SuperAssertion and data
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
    # @return Task execution result (may be None) - no associated type
    # @return None if no Task is found
    #
    # @brief Calls the class __setup() function. \n
    # If there's a valid Task instance, executes it, followed by the Assertion.
    def execute(self):
        if self.task is None:
            Printer.getInstance().printMessage("No such Task found: %s" %(self.data["categories"]), 1)
            return None

        Printer.getInstance().printMessage("Starting Task -> %s" %(self.data["description"]))

        start_time = time.time() # Starts counting the execution time of the task (task + assertion)

        self.data["taskResult"] = self.task.execute_task(self.data["value"])
        self.data["assertionResult"] = self.assertion.execute_assertion(self.data["taskResult"], self.data["expectedValue"])

        # Stores the task's execution time
        executionTime = time.time() - start_time
        self.data["executionTime"] = executionTime

        Printer.getInstance().printMessage(f"Task execution time: {executionTime * 1000:.3f} ms")

        Printer.getInstance().processTask(self)

        return self.data["assertionResult"]

    ##
    # @param self Task instance
    #
    # @brief Invokes the necessary procedures in order to execute the Task
    def setup(self):
        self.__setTask()
        self.__setAssertion()

    ##
    # @param self Task instance
    #
    # @brief Retrieves the Task instance
    def __setTask(self):
        self.task = retrieveTask(SuperProxy(), list(self.data["categories"]))

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

        task.pop("taskResult", None)

        return task
