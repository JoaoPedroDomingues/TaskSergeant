from .defaultAssertion import DefaultAssertion
from .superAssertion import SuperAssertion

##
# @class AssertionRetriever
#
# @brief Class dedicated to retriving the Assertion instance represented in the input by it's identifier


class AssertionRetriever():

    ##
    # @brief A dict that maps the Assertions to their respective identifiers
    __assertions = {
    }

    ##
    # @static
    # @param category The Assertion's identifier
    #
    # @return The Assertion instance defined by the id.
    #
    # @brief Returns the Assertion specified by the id. \n
    # Returs a DefaultAssertion instance if there's no Assertion with the indicated identifier.
    @staticmethod
    def retrieveAssertion(category):
        if not AssertionRetriever.__assertions:  # Empty dicts in Python evaluate to False
            AssertionRetriever.genAssertions()

        assertion = AssertionRetriever.__assertions.get(category, DefaultAssertion)

        return assertion()

    @staticmethod
    def genDict():
        AssertionRetriever.genAssertions()
        result = []
        for key in AssertionRetriever.__assertions:
            result.append(key)

        return result

    @staticmethod
    def genAssertions():
        import importlib
        import pkgutil, os.path

        pkgpath = os.path.dirname(__file__)

        for _, name, _ in pkgutil.iter_modules([pkgpath]):
            try:
                # We import the module using it's full path: "src.Models.Tasks.superProxy"
                module = importlib.import_module("%s.%s" %(__package__, name))
                # class name = module name with first character capitalized
                className = name[0].upper() + name[1:]
                # We get the class inside the module
                class_ = getattr(module, className)
                # Creating an instance of the class
                instance = class_()
                # Skip the SuperTasks
                if (instance.id() == SuperAssertion.id()):
                    continue
                # We add to the current Proxy the mapping to the Task
                AssertionRetriever.__assertions[instance.id()] = type(instance)
            except Exception:
                pass
