from abc import ABC, abstractmethod

import sys
# Python 3 renamed the unicode type to str, this is to avoid troubles related to that
if sys.version_info[0] >= 3:
    unicode = str

##
# @class SuperAssertion
# @pure
#
# @brief This is an abstract class that must be extended by every Assertion
class SuperAssertion():

    def __init__(self):
        pass

    ##
    # @pure
    #
    # @param self The Assertion's instance
    # @param actual The Task's result
    # @param expected The expected expression
    #
    # @brief Executes the Assertion's code
    @abstractmethod
    def execute_assertion(self, actual, expected):
        pass

    ##
    # @static
    # @return Assertion's identifier to be used in the input
    #
    # @brief Each concrete implementation of the SuperAssertion class should contain it's own, unique identifier. \n
    # If no identifier is declared, the SuperAssertion's id() method is called instead.
    @staticmethod
    def id():
        return "SuperAssertionID"


    ##
    # @param self The Assertion's instance
    # @param actual The Task's result
    # @param expected The expected expression
    #
    # @return bool, True if both are of the same type, False otherwise
    #
    # @brief Determines whether the actual and expected values are of the same type, treating edge cases properly. \n
    # If one of the results is of type unicode and the other is of type str, they are considered to be of the same type.
    def sameType(self, actual, expected):
        if type(expected) == type(actual):
            return True
        if type(expected) == unicode and type(actual) == str:
            return True
        if type(expected) == str and type(actual) == unicode:
            return True
        return False
