from .superAssertion import SuperAssertion
from .equalsAssertion import EqualsAssertion

##
# @class OrAssertion
#
# @brief This Assertion receives a list of expected values and checks whether the actual value equals at least one of them
class OrAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not type(expected) is list:
            eq = EqualsAssertion()
            return eq.execute_assertion(actual, expected)

        found = False
        for e in expected:
            if EqualsAssertion().execute_assertion(actual, e):
                found = True

        return found

    @staticmethod
    def id():
        return "or"
