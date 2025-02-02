##
# @brief The only function of this class is to import the right Executer according to the Python version that is running the script
# If there is the need to import an Executer, we do it through this script, via 'from [...]Executers.executerImporter import Executer'
import sys
if(sys.version_info >= (3,0)):
    from .executer import Executer
else:
    from .executerOld import Executer