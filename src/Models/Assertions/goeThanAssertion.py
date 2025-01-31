from .superAssertion import SuperAssertion

##
# @class GoEThanAssertion
#
# @brief This Assertion checks whether the actual value is greater than or equals the expected value
class GoeThanAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not self.sameType(actual, expected):
            return False
        return actual >= expected

    @staticmethod
    def id():
        return ">="
