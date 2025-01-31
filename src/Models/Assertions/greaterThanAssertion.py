from .superAssertion import SuperAssertion

##
# @class GreaterThanAssertion
#
# @brief This Assertion checks whether the actual value is greater than the expected value
class GreaterThanAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not self.sameType(actual, expected):
            return False
        return actual > expected

    @staticmethod
    def id():
        return ">"
