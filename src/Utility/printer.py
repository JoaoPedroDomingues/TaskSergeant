import sys
if sys.version_info[0] >= 3:
    unicode = str

##
# @class Printer
# @brief Auxiliary class to where the debug output is generated
#
# In order to activate the class's debug funcionality, it must be instantiated with a True flag.
# This class is a Singleton.
class Printer():

    ##
    # @private
    #
    # @brief Printer's own self instance
    __instance = None

    ##
    # @static
    #
    # @throws Exception "No instance of Printer exists yet!"
    #
    # @brief Retrieves the Singleton instance. If it doesn't exist, raises an Exception.
    @staticmethod
    def getInstance():
        if Printer.__instance == None:
            raise Exception("No instance of Printer exists yet, please call the class's constructor to create one!")
        return Printer.__instance

    ##
    # @param self
    # @param resultFlag bool defining whether the class's result debug functionality is active or not
    # @param debugFlag bool defining whether the class's debug functionality is active or not
    #
    # @throws Exception "An instance of Printer already exists!"
    #
    # Instantiates the class's self instance, in case it hasn't been instantiated yet. \n
    # Raises an Exception in case an instance of Printer already exists.
    def __init__(self, resultFlag, debugFlag):
        if not Printer.__instance == None:
            raise Exception("An instance of Printer already exists, please call the class's getInstance() method to get it!")
        else:
            self.__resultFlag = resultFlag
            self.__debugFlag = debugFlag
            Printer.__instance = self

    ##
    # @param self Printer instance
    # @param task Task instance to be processed
    #
    # @brief Calls the __debugger() depending on the resultFlag's state.
    def processTask(self, task):
        if not self.__resultFlag:
            return

        # Printing the categories in order
        categories = ""
        for cat in task.data["categories"]:
            categories += "[" + cat + "]"

        # If the assertion did not retrieve a boolean it is because a DefaultAssertion has been used (which returns the Command's result directly)
        # To remove false negatives (where the Command's result is itself a boolean, which may indicate the Assertion used was not the DefaultAssertion), we also check for the expectedValue being None
        # If either of those happen, the Task ran with a DefaultAssertion
        # The last validation of the first line is triggered when an expectedValue is provided and the DefaultAssertion's result is bool
        # TODO: There are problems with this validation... There are cases where a Result is confused for an Assertion, find a way to treat those
        # It doesn't break the program, but under very specific situations, it may produce confusing results
        # (e.g.: expectedValue = "test", assertionResult = True, assertionType = "somethingThatDoesntExist")
        if not type(task.data["assertionResult"]) is bool or task.data["expectedValue"] is None or task.data["assertionType"] is None:
            print("[RESULT]%s - %s : %s" %(categories, task.data["description"], task.data["assertionResult"]))
        elif task.data["assertionResult"]:
            print("[ASSERTION]%s - %s : OK" %(categories, task.data["description"]))
        else:
            # We print both the actual and expected values and types, to help determine what went wrong
            print("[ASSERTION]%s - %s : NOK" %
                  (categories, task.data["description"]))
            commandResult = task.data["commandResult"]
            if (type(commandResult) == str or type(commandResult) == unicode) and len(commandResult) > 500:
                commandResult = commandResult[0:500] + "\n\t[Result continues for longer ...]"
            print("\tExpected:\n\t\tValue: %s\n\t\tType: %s\n\tActual:\n\t\tValue: %s\n\t\tType: %s\n\tAssertion Type: %s" %(str(task.data["expectedValue"]), type(task.data["expectedValue"]), commandResult, type(task.data["commandResult"]), task.data["assertionType"]))

        print("\n")

    ##
    # @param self Printer instance
    # @param commandId A Command's identifier
    # @param exceptionMessage An exception's message
    #
    # @brief Custom output for subprocess.CalledProcessError exceptions
    def subprocessException(self, commandId, exceptionMessage):
        self.printMessage("An exception occured when executing a command with id '%s'.\nException Message: %s" %(commandId, exceptionMessage), 3)

    ##
    # @param self Printer instance
    # @param message The message to be printed
    # @param level Defines the message type, default is 0 (INFO)
    #
    # @brief Prints a message, along with a message type
    def printMessage(self, message, level=0):
        if not self.__debugFlag:
            return

        if level == 0:
            msgType = "[INFO]"
        elif level == 1:
            msgType = "[WARNING]"
        elif level == 2:
            msgType = "[ERROR]"
        elif level == 3:
            msgType = "[EXCEPTION]"
        elif level == 4:
            msgType = "[PROMPT]"
        else:
            msgType = "[OTHER]"

        for line in message.split('\n'):
            print("%-11s %s" % (msgType, line))

    def getInput(self, message, mandatory=False):
        formattedMessage = "%-11s %s --> " % ("[PROMPT]", message)
        
        value = input(formattedMessage).strip()
        
        if mandatory is False:
            return value
        
        while not value:
            value = input(formattedMessage).strip()

        return value

    def printPipelineStats(self, message):
        if not self.__resultFlag:
            return

        print(message)
