from .superAssertion import SuperAssertion

##
# @class DifferentAssertion
#
# @brief This Assertion checks whether the actual value is different from the expected value
class DifferentAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        if not self.sameType(actual, expected):
            return True
        return actual != expected

    @staticmethod
    def id():
        return "!="
