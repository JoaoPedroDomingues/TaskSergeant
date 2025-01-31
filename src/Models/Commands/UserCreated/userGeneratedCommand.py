from abc import abstractmethod
from ..superCommand import *

# This is an abstract class that must be extended by every Command (along with it's abstract method)
class UserGeneratedCommand(SuperCommand):

    @abstractmethod
    def execute_command(self, value):
        pass
