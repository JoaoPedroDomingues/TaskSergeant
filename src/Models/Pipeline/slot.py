from ...Utility.printer import Printer

##
# @class This class represents a Slot, which is a component of the Pipeline. \n
# It's a container and manager of a single instance of a Task. \n
# It contains information regarding it's relation to other Slots.
class Slot():

    ##
    # @param self Slot instance
    # @param task The Task instance to be stored in the Slot
    # @param id The Slot's identifier
    #
    # @brief Calls __setup() upon instancing
    def __init__(self, task, id, repeatable=1):
        self.__setup()
        self.id = id
        self.task = task
        self.repeatable = repeatable
        self.__repeatableInitial = repeatable

    ##
    # @param self Slot instance
    #
    # @brief Creates an empty dict and sets both flags to False
    def __setup(self):
        self.__paths = {}
        self.hasParent = False
        self.default = None

    ##
    # @param self Slot instance
    #
    # @brief Executes the Slot's Task.
    # Sets the executed flag to True and decrements the repeatable flag
    def execute(self):
        result = self.task.execute()
        self.repeatable -= 1
        return result

    ##
    # @param self Slot instance
    #
    # @brief Sets the hasParent flag to True.
    def makeChild(self):
        self.hasParent = True

    ##
    # @param self Slot instance
    # @param result The key to access the child Slot
    # @param slot The child Slot
    #
    # @brief Maps a child Slot to a key, adding that correspondance to a local dict. \n
    # If we want that a task is followed by another, regardless of it's result, we omit the key \n
    # One slot can only be followed by one slot. If the key is omited and there's another valid slot in __paths, the later one will be chosen \n
    # Practical example: \n
    # "id" : "1", \n
    # "paths" : [ \n
    #   { \n
    #     "key" : false, \n
    #     "nextSlotId" : "2" \n
    #   }, \n
    #   { \n
    #     "nextSlotId" : "3" \n
    #   } \n
    # ] \n
    # If the result of the slot with ID 1 comes out as False, the next slot to be executed will be the one with ID 2 \n
    # Slot with ID 3 will then be ignored (in this hierarchy) \n
    # On the other hand, if it came out as True, the next slot would be the one with ID 3 (True doesn't exist, so it defaults to 3, since it has no key) \n
    def addPath(self, result, slot):
        if self.__paths is None:
            self.__paths = {}

        if result is None:
            self.default = slot
        self.__paths[result] = slot

    ##
    # @param self Slot instance
    # @param result The key to the child Slot
    #
    # @return The child Slot corresponding to the received key.
    # @return None if there are no child Slots with that key and if there is no default Slot defined.
    #
    # @brief Retrieves the child Slot corresponding to the received key.
    def getNextSlotId(self, result):
        try:
            nextSlot = self.__paths.get(result, self.default)
        except Exception as e:
            Printer.getInstance().printMessage(e, 1)
            nextSlot = self.default
        
        # TODO: Check this condition
        # If there is no path for the task result, but there was no expected value,
        # it's because the task consisted in a [RESULT] and not in a [ASSERTION]
        #if nextSlot == None:
        #    if self.task.data.get("expectedValue") is None:
        #        nextSlot = self.__defaultNext

        return nextSlot

    ##
    # @param self Slot instance
    #
    # @return bool value that represents whether the Slot has been executed yet
    def executed(self):
        return self.repeatable != self.__repeatableInitial

    ##
    # @param self Slot instance
    #
    # @brief This method is only used by Pipeline.__pipelineStats(), please read it's documentation for context.
    def result(self):
        return self.task.data.get("assertionResult")

    ##
    # @param self Slot instance
    #
    # @return The Slot formatted as a dict
    #
    # @brief Returns the Slot's information as a dict
    def asOutput(self):
        result = {}

        if(self.id is not None):
            result["id"] = self.id

        result["repeatable"] = self.__repeatableInitial
        result["executed"] = self.__repeatableInitial - self.repeatable

        if self.executed():
            nextSlot = self.getNextSlotId(self.task.data["assertionResult"])
            if(nextSlot is not None):
                result["followedBy"] = nextSlot

        result["task"] = self.task.asOutput()

        return result
