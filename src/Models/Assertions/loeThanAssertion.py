from .superAssertion import SuperAssertion

##
# @class LoEThanAssertion
#
# @brief This Assertion checks whether the actual value is less than or equals the expected value
class LoeThanAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not self.sameType(actual, expected):
            return False
        return actual <= expected

    @staticmethod
    def id():
        return "<="
