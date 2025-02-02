from .slot import Slot
from ...Utility.printer import Printer
import time

##
# @class Pipeline
# @brief A Pipeline is a container and manager of Slots. \n
# It executes the Slots in order, respecting the hierarchies that may exist.
class Pipeline():

    ##
    # @brief Creates an empty list of slots upon instancing
    def __init__(self):
        self.__slots = []
        pass

    ##
    # @param self Pipeline instance
    #
    # @brief Executes the Slots, one by one. calling an auxiliary function when it detects the beginning of an hierarchy. \n
    # At the end of the execution, calls a function to generate stats.
    def execute(self):
        Printer.getInstance().printMessage("Pipeline execution started!!\n------------------")
        start_time = time.time() # Starts counting execution time

        for slot in self.__slots:
            # The beginning of an hierarchy is detected when the current Slot doesn't have a parent and has an ID non-None
            if not slot.hasParent:
                self.__chainExecution(slot)

        Printer.getInstance().printMessage("Pipeline execution ended!!")
        Printer.getInstance().printPipelineStats("\n--------------------\nPipeline execution time: %s" %(time.time() - start_time))

        return self.asOutput()

    ##
    # @param self Pipeline instance
    # @param slot The Slot to be executed
    #
    # @return None - the return is solely used to exit the function
    #
    # @brief Starts by validating the Slot received. \n
    # If it isn't valid, exits the function, via return. \n
    # If it is valid, executes the Slot and calls itself recursively using the next Slot in the hierarchy.
    def __chainExecution(self, slot):
        if slot is None:
            Printer.getInstance().printMessage("No valid children slot found!")
            return
        if slot.repeatable == 0:
            Printer.getInstance().printMessage("This Slot has no repetitions left!")
            return

        result = slot.execute()
        # Get the next slot in the hierarchy
        nextSlotId = slot.getNextSlotId(result)
        nextSlot = self.__getNextSlotInHierarchy(nextSlotId)
        # Recursive call with the child Slot
        self.__chainExecution(nextSlot)

    ##
    # @param self Pipeline instance
    # @param id The identifier of a Slot
    #
    # @return The Slot instance with the provided identifier
    # @return None if there is no slot with the provided identifier
    #
    # @brief Scrolls through the list of Slots until it finds the first Slot with the same identifier as the one received
    def getSlotWithId(self, id):
        for slot in self.__slots:
            if slot.id == id:
                return slot
        Printer.getInstance().printMessage("No slot with id {%s} was found!!" %(id), 1)
        return None

    ##
    # @param self Pipeline instance
    # @param id The identifier of a Slot
    #
    # @return The Slot instance with the provided identifier
    # @return None if there is no slot with the provided identifier
    # @return None if the provided identifier is None
    # @return None if there are no Slots with the provided identifier that were not executed
    #
    # @brief Scrolls through the list of Slots until it finds the first Slot with the same identifier as the one received. \n
    # Ignores ID's that are None, as they do not belong to any Hierarchy. \n
    # Ignores Slots that have been executed.
    def __getNextSlotInHierarchy(self, id):
        if id is None:
            return None
        for slot in self.__slots:
            if slot.id == id:
                if not slot.repeatable == 0:
                    return slot
        return None

    ##
    # @param self Pipeline instance
    # @param task The instance of a Task to be stored in a Slot
    # @param id The Slot identifier
    #
    # @brief Adds an new instance of Slot to the Pipeline's list of Slots with the received Task instance. \n
    # Rules out Tasks with no Command.
    def addTask(self, task, id, repeatable=1):
        if type(task.command) == type(None):
            Printer.getInstance().printMessage("Task with category path %s has no valid Command associated and will be excluded from the pipeline!" %(task.data["categories"]), 1)
            return
        Printer.getInstance().printMessage("Added Slot with [ID] %s and [DESCRIPTION] %s" %(id, task.data["description"]))
        self.__slots.append(Slot(task, id, repeatable))

    ##
    # @param self Pipeline instance
    # @param parentId The identifier of the parent Slot
    # @param key The key needed to access the child Slot
    # @param childId The identifier of the child Slot
    #
    # @brief Generates the hierarchy between two Slots - one parent and one child.
    def addHierarchy(self, parentId, key, childId):
        parent = self.getSlotWithId(parentId)
        child = self.getSlotWithId(childId)
        if not parent is None:
            parent.addPath(key, childId)
            Printer.getInstance().printMessage("Added hierarchy flow: %25s  -->  %25s  :  %s" %(parentId, childId, key))
        if not child is None:
            child.makeChild()

    ##
    # @param self Pipeline instance
    #
    # @brief Determines the pipeline's global result \n
    # As of now, the global result is OK if there are no failed tasks.
    def globalResult(self):
        for slot in self.__slots:
            if type(slot.result()) == bool and not slot.result():
                return "NOK"
        return "OK"

    ##
    # @brief This method's goal is to show the pipeline's status \n
    # It has no impact whatsoever on how the pipeline works, it just sends a string containing information to the Printer
    def __pipelineStats(self):
        success = failed = executed = others = 0
        notExecuted = []
        total = len(self.__slots)
        for slot in self.__slots:
            if slot.executed():
                executed += 1
                if not type(slot.result()) == bool:
                    others += 1
                elif slot.result():
                    success += 1
                else:
                    failed += 1
            else:
                notExecuted.append(slot.task.data["description"])
        msg = "Pipeline stats:\n\tTotal tasks: %d\n\tExecuted: %d\n\t\tSuccessful: %d\n\t\tFailed: %d\n\t\tOther results: %d\n\tNot Executed:" %(total, executed, success, failed, others)
        for ne in notExecuted:
            msg += "\n\t\t" + ne
        msg += "\n--------------------"
        Printer.getInstance().printPipelineStats(msg)
        return total, executed, success, failed, others

    ##
    # @param self Pipeline instance
    #
    # @return The Pipeline formatted as a dict
    #
    # @brief Returns the Pipeline's information as a dict
    def asOutput(self):

        from datetime import datetime

        result = {}

        total, executed, success, failed, others = self.__pipelineStats()
        result["version"] = None # Defined in the main.py
        result["globalResult"] = self.globalResult()
        result["date"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        result["totalTasks"] = total
        result["tasksExecuted"] = executed
        result["successfulAssertions"] = success
        result["failedAssertions"] = failed
        result["otherResults"] = others

        output = []
        for slot in self.__slots:
            output.append(slot.asOutput())

        result["slots"] = output

        return result