from abc import abstractmethod
from ..superCommand import *  # This warning is a false-positive, please ignore

# This is an abstract class that must be extended by every Command (along with it's abstract method)
class NativeCommand(SuperCommand):

    @abstractmethod
    def execute_command(self, value):
        pass
