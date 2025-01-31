from .superAssertion import SuperAssertion

##
# @class EqualsAssertion
#
# @brief This Assertion checks whether the actual value equals the expected value
class EqualsAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not self.sameType(actual, expected):
            return False
        return actual == expected

    @staticmethod
    def id():
        return "="
