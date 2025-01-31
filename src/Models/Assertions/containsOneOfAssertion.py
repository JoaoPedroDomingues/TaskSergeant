from .superAssertion import SuperAssertion
from .containsAssertion import ContainsAssertion

##
# @class ContainsOneOfAssertion
#
# @brief This Assertion receives a list of expected values and checks whether the actual value contains at least one of them
class ContainsOneOfAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        for item in expected:
            if ContainsAssertion().execute_assertion(actual, item):
                return True
        return False

    @staticmethod
    def id():
        return "containsOneOf"
