from abc import abstractmethod
from ..superTask import *  # This warning is a false-positive, please ignore

# This is an abstract class that must be extended by every Task (along with it's abstract method)
class NativeTask(SuperTask):

    @abstractmethod
    def executeTask(self, value):
        pass
