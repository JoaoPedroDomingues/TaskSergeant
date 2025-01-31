from .superAssertion import SuperAssertion

##
# @class LesserThanAssertion
#
# @brief This Assertion checks whether the actual value is less than the expected value
class LesserThanAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not self.sameType(actual, expected):
            return False
        return actual < expected

    @staticmethod
    def id():
        return "<"
