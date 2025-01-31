from .superAssertion import SuperAssertion, Printer

##
# @class ContainsAssertion
#
# @brief This Assertion receives an expected value and checks whether it is contained in the actual value
class ContainsAssertion(SuperAssertion):

    def execute_assertion(self, actual, expected):
        try:
            return str(expected) in str(actual)
        except Exception as message:
            Printer.getInstance().printMessage("ContainsAssertion raised an Exception!! \n\tException message: %s" %(message), 3)
            return False

    @staticmethod
    def id():
        return "contains"
