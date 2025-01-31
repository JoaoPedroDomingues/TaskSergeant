from .superAssertion import SuperAssertion
from .containsAssertion import ContainsAssertion

##
# @class ContainsAllAssertion
#
# @brief This Assertion receives a list of expected values and checks whether the actual value contains all of them
class ContainsAllAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        for item in expected:
            if not ContainsAssertion().execute_assertion(actual, item):
                return False
        return True

    @staticmethod
    def id():
        return "containsAll"
