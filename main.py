from src.Models.Task.taskBuilder import TaskBuilder
from src.Models.Pipeline.pipeline import Pipeline
from src.Utility.printer import Printer
from src.Utility.InputInterpreter.inputInterpreter import processInput
from src.Utility.OutputGenerator.resultInterpreter import generate_output
import sys
import os
from src.Models.Tasks.Executers.executerImporter import Executer
from src.Models.Tasks.superProxy import SuperProxy
from copy import deepcopy

# ------------------------------------------------------------------------------


def __genTask(taskInfo, path, pipeline):
    if taskInfo.get("task") is None:
        return
    newPath = list(path)
    newPath.append(taskInfo.get("task"))

    builder = TaskBuilder()

    task = builder.addValue(taskInfo.get("value")) \
        .addAssertionType(taskInfo.get("assertionType")) \
        .addDescription(taskInfo.get("description")) \
        .addExpected(taskInfo.get("expected")) \
        .addCategories(newPath) \
        .task

    ids = taskInfo.get("id")

    if type(ids) == list:
        for id in ids:
            # We use deepcopy here, because the same instance would reproduce fake results
            pipeline.addTask(deepcopy(task), id, taskInfo.get("repeatable", 1))
    else:
        pipeline.addTask(task, ids, taskInfo.get("repeatable", 1))


def __processData(input, path, pipeline):
    name = input.get("name")
    newPath = list(path)

    if not name is None:
        newPath.append(name)

    if not input.get("categories") is None:
        for category in input.get("categories"):
            __processData(category, newPath, pipeline)

    if not input.get("tasks") is None:
        for task in input.get("tasks"):
            __genTask(task, newPath, pipeline)


def __setupPipelineHierarchy(input, pipeline):
    if input.get("pipeline") is None:
        return
    for parent in input.get("pipeline"):
        if parent.get("paths") is None:
            continue
        for child in parent.get("paths"):
            pipeline.addHierarchy(parent.get("id"), child.get("key"), child.get("nextSlotId"))

# ------------------------------------------------------------------------------

# In the final version the program should receive 2 arguments:
# - Input file
#   - Task description
#   - Pipeline description
# - Debug flag

# Example execution command:
# python -d filename.json

debugFlag = False
resultFlag = False
inputFile = ""

# Process arguments
if len(sys.argv) > 1:
    for arg in sys.argv:
        if arg == "-d": # -d flag for full log
            debugFlag = True
            resultFlag = True
        elif arg == "-r": # -r flag for result-only log
            resultFlag = True
        elif arg != "main.py":
            inputFile = arg

# Create Printer instance
Printer(resultFlag, debugFlag)
Printer.getInstance().printMessage("A Printer instance has been created...")

if inputFile == "":
    try:
        files = os.listdir("Inputs")
        for count, assertion in enumerate(files):
            print("%s - %s" %(count, assertion))
        inputFile = files[int(Printer.getInstance().getInput("Choose a file"))]
    except FileNotFoundError:
        Printer.getInstance().printMessage("Error: Folder not found!", 2)   
    except PermissionError:
        Printer.getInstance().printMessage("Error: Permission denied!", 2)
    except:
        Printer.getInstance().printMessage("Something went wrong!", 2)

# Relocate the Working Directory at run time
try:
    os.chdir(os.path.dirname(__file__))
    Printer.getInstance().printMessage("Current Working Directory has been changed to " + os.getcwd())
except Exception:
    pass

# Generate the system's mapping of the available Tasks and Assertions
SuperProxy().genProxy()

# Parse input file to dict
model = processInput(inputFile)

version = model.get("version", "-")
name = model.get("name", "-")
model.pop("name", None) # Remove the name here so it won't be processed later on
Printer.getInstance().printMessage("Input name: %s" %(name))
Printer.getInstance().printMessage("Input version: %s" %(version))

# Create singleton instances
Executer(model.get("timeout"))
Printer.getInstance().printMessage("An Executer instance has been created...")

pipeline = Pipeline()

__processData(model, [], pipeline)

__setupPipelineHierarchy(model, pipeline)

result = pipeline.execute()

result["name"] = name
result["version"] = version

generate_output(result)
