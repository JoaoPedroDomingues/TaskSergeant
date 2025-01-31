from .superCommand import SuperCommand
from ...Utility.printer import Printer

##
# @class SuperProxy
#
# @brief The initial layer's Proxy
class SuperProxy():

    ##
    # @brief A dict that maps the current layer's Commands to their respective identifiers
    commands = {}

    ##
    # @brief A dict that maps the current layer's sublayers' Proxies to their respective identifiers
    proxies = {}

    @staticmethod
    def genDict():
        SuperProxy().genProxy()

        result = {}
        for proxy in SuperProxy.proxies:
            result[proxy] = SuperProxy.__genDictAux(SuperProxy.proxies[proxy], "")

        return result


    @staticmethod
    def __genDictAux(current, pathSoFar):
        pathNow = "%s/%s" %(pathSoFar, current.id())

        if pathNow[0] == '/':
            pathNow = pathNow[1:]

        result = {"commands": [], "categories": {}}

        for command in current.commands:
            result["commands"].append(command)

        for proxy in current.proxies:
            nextPath = "%s/%s" %(pathNow, proxy)
            result["categories"][nextPath] = SuperProxy.__genDictAux(current.proxies[proxy], nextPath)

        return result

    # The comments in this method use the SuperProxy class as an example
    def genProxy(self):
        import importlib
        import pkgutil, os.path
        import inspect

        # self.__class__ = <class 'src.Models.Commands.superProxy.SuperProxy'>
        # pkgpath = "{path to your project folder}\TaskSergeant\src\Models\Command"
        pkgpath = os.path.dirname(inspect.getfile(self.__class__))

        # currentFile = "src.Models.Commands.superProxy"
        currentFile = self.__module__.split(".")
        del currentFile[-1]

        # currentPackage = "src.Models.Commands"
        currentPackage = ".".join(currentFile)

        # for each module in the current package
        # name = module name
        # isPkg = boolean indicating if module is a package or not
        for _, name, isPkg in pkgutil.iter_modules([pkgpath]):
            if isPkg: # If it is a package, we are entering a subcategory and will now look for it's Proxy
                for _, subName, subIsPkg in pkgutil.iter_modules([pkgpath+"/"+name]): # For each element in the subcategory
                    if subIsPkg or "Proxy" not in subName:  # We skip packages and files without Proxy in the name
                        continue
                    try:
                        # We import the module using it's full path: "src.Models.Commands.superProxy"
                        module = importlib.import_module("%s.%s.%s" %(currentPackage, name, subName))
                        # class name = module name with first character capitalized
                        className = subName[0].upper() + subName[1:]
                        # We get the class inside the module
                        class_ = getattr(module, className)
                        # Creating an instance of the class
                        instance = class_()
                        # We add to the current Proxy the mapping to the next one
                        self.__class__.proxies[instance.id()] = type(instance)
                        # We call this function on the next Proxy (this runs recursivelly the category tree)
                        type(instance)().genProxy()
                        Printer.getInstance().printMessage("Processed Proxy %s" %(name))
                    except Exception as e:
                        Printer.getInstance().printMessage("Error Processing Proxy %s" %(name), 2)
                        Printer.getInstance().printMessage(e, 2)
            else: # If it is NOT a package, we deal with files, looking for Commands
                if isPkg or "Proxy" in name or "Retriever" in name:  # We skip packages and files with Proxy/Retriever in the name
                    continue
                try:
                    # We import the module using it's full path: "src.Models.Commands.superProxy"
                    module = importlib.import_module("%s.%s" %(currentPackage, name))
                    # class name = module name with first character capitalized
                    className = name[0].upper() + name[1:]
                    # We get the class inside the module
                    class_ = getattr(module, className)
                    # Creating an instance of the class
                    instance = class_()
                    # Skip the SuperCommands
                    if (instance.id() == SuperCommand.id()):
                        continue
                    # We add to the current Proxy the mapping to the Command
                    self.__class__.commands[instance.id()] = type(instance)
                    Printer.getInstance().printMessage("Processed Command %s" %(name))
                except Exception as e:
                    Printer.getInstance().printMessage("Error Processing Command %s" %(name), 2)
                    Printer.getInstance().printMessage(str(e), 2)
