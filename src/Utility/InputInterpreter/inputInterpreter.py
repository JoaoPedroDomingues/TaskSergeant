import os
import sys
from .jsonInterpreter import JsonInterpreter
from ..printer import Printer

# If we have other input file types, map their extension to their interpreter here
__interpreters = {
    ".json" : JsonInterpreter,
}

def process_input(inputName):

    _, fileExtension = os.path.splitext(inputName)

    interpreter = __interpreters.get(fileExtension, None)

    if interpreter is None:
        raise Exception("File type not supported!")

    # Shortcut to check if the input file is a full path or not
    # Revise this later...
    if "/" not in inputName:
        inputFile = open("Inputs/" + inputName)
    else:
        inputFile = open(inputName)
        
    Printer.getInstance().printMessage("File imported...")
    data = interpreter.process(inputFile)
    Printer.getInstance().printMessage("File's data parsed...")
    inputFile.close()

    return data