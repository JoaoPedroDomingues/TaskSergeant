import subprocess
from ....Utility.printer import Printer

##
# @class Executer
#
# @brief This class is responsible for the execution of commands, resorting to the subprocess module \n
# It deals with Exceptions and outputs debug messages that are visible if the debug is active \n
# This class is aimed at version of Python 3.x \n
# This class is a Singleton. \n
# In order to import this class, read the script executerImporter.py
class Executer():

    ##
    # @private
    #
    # @brief Executer's own self instance
    __instance = None

    ##
    # @static
    #
    # @throws Exception "No instance of Executer exists yet!"
    #
    # @brief Retrieves the Singleton instance. If it doesn't exist, raises an Exception.
    @staticmethod
    def getInstance():
        if Executer.__instance == None:
            raise Exception("No instance of Executer exists yet!")
        return Executer.__instance

    ##
    # @param self
    # @param timeout The timeout, in seconds, for the subprocess calls
    #
    # @throws Exception "An instance of Executer already exists!"
    #
    # Instantiates the class's self instance, in case it hasn't been instantiated yet. \n
    # Raises an Exception in case an instance of Executer already exists.
    def __init__(self, timeout):
        if not Executer.__instance == None:
            raise Exception("An instance of Executer already exists!")
        else:
            self.__timeout = timeout
            Executer.__instance = self

    ##
    # @param self Executer instance
    # @param caller Task instance that called this function
    # @param command The command that is be executed
    #
    # @return The result of the subprocess call, as a string
    # @return None, if the subprocess call fails/raises an exception
    #
    # @brief Executes the received command, resorting to the subprocess module. \n
    # Exceptions thrown by the subprocess call are treated here, where a debug message is requested. \n
    # Further procedures upon an Exception happening are to be treated at a Task-level, 
    # by validating whether or not the return value of this function is None.
    def executeCommand(self, caller, command):
        result = None
        Printer.getInstance().printMessage("Running command -> %s" %(command))
        try:
            result = subprocess.check_output(command, shell=True, timeout=self.__timeout).decode("utf-8")
        except subprocess.CalledProcessError as message:
            Printer.getInstance().subprocessException(caller.id(), message)
        except subprocess.TimeoutExpired as message:
            Printer.getInstance().subprocessException(caller.id(), message)

        return result