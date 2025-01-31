from .superAssertion import SuperAssertion
from .equalsAssertion import EqualsAssertion

##
# @class AndAssertion
#
# @brief This Assertion receives a list of expected values and checks whether the actual value equals all of them
class AndAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not type(expected) is list:
            eq = EqualsAssertion()
            return eq.execute_assertion(actual, expected)

        found = True
        for e in expected:
            if not EqualsAssertion().execute_assertion(actual, e):
                found = False

        return found

    @staticmethod
    def id():
        return "and"
