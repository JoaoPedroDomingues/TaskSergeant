from abc import abstractmethod
from ..superTask import *

# This is an abstract class that must be extended by every Task (along with it's abstract method)
class UserGeneratedTask(SuperTask):

    @abstractmethod
    def execute_task(self, value):
        pass
