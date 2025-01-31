from .superAssertion import SuperAssertion

##
# @class DefaultAssertion
#
# @brief This Assertion simply returns the actual value - it is the Assertion used by default (when no Assertion is specified)
class DefaultAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        return actual

    @staticmethod
    def id():
        return "none"
