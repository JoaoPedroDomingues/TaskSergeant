from src.Models.Assertions.assertionRetriever import AssertionRetriever
from src.Models.Commands.superProxy import SuperProxy
from src.Utility.printer import Printer

# This is an utility script
# This script generates 2 files to be placed in the info/ folder
# They'll be used by the taskBuilder to show the available Assertions and Commands

Printer(True, True)
Printer.getInstance().printMessage("A Printer instance has been created...")

Printer.getInstance().printMessage("Registering Assertions...")

f = open("info/assertions.txt", "w")
f.write(AssertionRetriever.genDict())
f.close()

Printer.getInstance().printMessage("Assertions registered!")
Printer.getInstance().printMessage("Registering Commands...")

f = open("info/commands.txt", "w")
f.write(SuperProxy.genDict())
f.close()

Printer.getInstance().printMessage("Commands registered!")