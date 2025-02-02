import json
from datetime import datetime
from copy import deepcopy
from src.Models.Assertions.assertionRetriever import AssertionRetriever
from src.Models.Tasks.superProxy import SuperProxy
from src.Utility.printer import Printer

Printer(True, True)
printer = Printer.getInstance()

allAssertions = []
allCategories = []
tasks = []
rules = []
outputRaw = {"name" : "", "version" : "", "timeout" : 60, "pipeline": [], "categories": []}

# Category Stuff



def listCategories():
    dedupedCategories = []

    for (category, _) in allCategories:
        if category not in dedupedCategories:
            dedupedCategories.append(category)

    return dedupedCategories
    
# Values

def createValue(hasKey=False):
    key = ""
    if hasKey:
        key = printer.getInput("Input key (non-empty string): ", True)
    value = printer.getInput("Input value: ").strip()
    printer.printMessage("Value type (string by default or in case of conversion failure):\n1 - String\n2 - Boolean\n3 - Integer\n4 - Float")
    valueType = printer.getInput("")

    if valueType == "2":
        if(value.lower() == "true"):
            value = True
        elif(value.lower() == "false"):
            value = False
    elif valueType == "3":
        try:
            value = int(value)
        except Exception:
            pass
    elif valueType == "4":
        try:
            value = float(value)
        except Exception:
            pass
    return key, value

# Task Stuff

def __addTaskInput():
    printer.printMessage("\nWhat type of parameter will be needed?")
    printer.printMessage("0 - None")
    printer.printMessage("1 - Single parameter")
    printer.printMessage("2 - List of parameter")
    printer.printMessage("3 - Composed parameter")
    option = printer.getInput("(defaults to None)")

    value = None

    match option:
        case '1':
            _, value = createValue()

        case '2':
            value = []

            _, valueAux = createValue()
            value.append(valueAux)

            while printer.getInput("Add another value? (y/n)").lower() == "y":
                _, valueAux = createValue()
                value.append(valueAux)

        case '3':
            value = {}

            key, valueAux = createValue(True)
            value[key] = valueAux

            while printer.getInput("Add another value? (y/n)").lower() == 'y':
                key, valueAux = createValue(True)
                value[key] = valueAux

    return value

def __selectTaskCategory():
    categories = listCategories()
    printer.printMessage("\nChoose the task's category:")
    for count, category in enumerate(categories):
        printer.printMessage("%d - %s" % (count, category))

    while True:
        try:
            return categories[int(printer.getInput(""))]
        except Exception:
            printer.printMessage("Invalid index..!", 3)

def __selectTaskFromCategory(category):
    printer.printMessage("")
    toList = []
    for cat in allCategories:
        if cat[0] == category:
            toList.append(cat[1])

    for count, task in enumerate(toList):
        printer.printMessage("%s - %s" %(count, task))

    while True:
        try:
            return toList[int(printer.getInput("Pick the Task", True))]
        except Exception:
            printer.printMessage("Invalid index..!", 3)

def __addRepeatable():
    try:
        return int(printer.getInput("Number of possible repetitions (defaults to 1)"))
    except Exception:
        return 1

def addTask():
    newTask = {}
    
    newTask["category"] = __selectTaskCategory()
    newTask["task"] = __selectTaskFromCategory(newTask["category"])
    newTask["repeatable"] = __addRepeatable()
    newTask["description"] = printer.getInput("Insert the task's description (required)", True)

    if (value := __addTaskInput()) is not None:
        newTask["value"] = value

    printer.printMessage("")

    for count, assertion in enumerate(allAssertions):
        printer.printMessage("%s - %s" %(count, assertion))

    try:
        newTask["assertionType"] = allAssertions[int(printer.getInput("Which Assertion should be used? (defaults to None)"))]

        if (value := __addTaskInput()) is not None:
            newTask["expected"] = value

    except Exception:
        pass

    newTask["id"] = "task_{:03d}".format(len(tasks) + 1)

    tasks.append(newTask)

def listTasks():
    printer.printMessage("")

    for count, task in enumerate(tasks):
        printer.printMessage("%d - %s: %s" %(count, task.get("id", None), task["description"]))

def deleteTask():
    printer.printMessage("")
    if(len(tasks) == 0):
        printer.printMessage("No tasks exist yet!",3)
        return

    listTasks()

    try:
        index = int(printer.getInput("Select the index to delete"))
        del tasks[index]
    except Exception:
        pass

# Hierarchy stuff

def createRule():
    printer.printMessage("")
    tasksWithId = []
    for task in tasks:
        if task.get("id", None) is not None:
            tasksWithId.append(task)

    if tasksWithId == []:
        printer.printMessage("No tasks eligible for an hierarchy (they need an id)!!", 3)
        return

    for count, task in enumerate(tasksWithId):
        printer.printMessage("%d - %s: %s" % (count, task["id"], task["description"]))

    parent = None
    try:
        parent = tasksWithId[int(printer.getInput("Select the parent task by index: "))]["id"]
    except Exception:
        printer.printMessage("Invalid index!!! Exiting...", 3)
        return

    child = None
    try:
        child = tasksWithId[int(printer.getInput("Select the child task by index: "))]["id"]
    except Exception:
        printer.printMessage("Invalid index!!! Exiting...", 3)
        return

    addRule = printer.getInput("Add a rule? (y/n) ").lower()

    value = None
    if(addRule == "y"):
        _, value = createValue()

    if value is None:
        rules.append({"id": parent, "paths": [{"nextSlotId": child}]})
    else:
        rules.append({"id": parent, "paths": [{"key": value, "nextSlotId": child}]})

def listRules():
    for count, rule in enumerate(rules):
        parent = rule["id"]
        child = rule["paths"][0]["nextSlotId"]
        key = rule["paths"][0].get("nextSlotId", "{Any value}")
        printer.printMessage("%s - %s%s : %s" % (count, parent, child, key))

def deleteRules():
    if(len(rules) == 0):
        printer.printMessage("\nNo rules created yet...", 3)
        return

    printer.printMessage("\nSelect an hierarchy rule by it's index: ")
    listRules()
    try:
        index = int(printer.getInput(""))
        del rules[index]
    except Exception:
        printer.printMessage("Some error has occured, going back to menu", 3)

# Pipeline stuff

def addPipelineStuff():
    printer.printMessage("")
    outputRaw["name"] = printer.getInput("Insert the name for this TaskSergeant Input")

    timeout = None
    while type(timeout) != float:
        try:
            timeout = float(printer.getInput("Insert the timeout (in seconds) for the task executions"))
        except Exception:
            timeout = None
            
    outputRaw["timeout"] = timeout

# Generate File

def __addTask(elem, cats, task):
    if len(cats) > 0:
        cat = cats[0]
        del cats[0]
        for catAux in elem["categories"]:
            if catAux["name"] == cat:
                __addTask(catAux, cats, task)
                return
    task2 = deepcopy(task)
    task2.pop("category", None)
    elem["tasks"].append(task2)

def __addCategoryAux(elem, cats):
    if len(cats) == 0:
        return

    cat = cats[0]
    del cats[0]

    for elemAux in elem["categories"]:
        if elemAux["name"] == cat:
            __addCategoryAux(elemAux, cats)
            return

    nextElem = {"name": cat, "categories": [], "tasks": []}

    __addCategoryAux(nextElem, cats)
    elem["categories"].append(nextElem)

def generateFile(fileName=""):
    output = outputRaw
    output["version"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    for category in listCategories():
        __addCategoryAux(output, category.split("/"))

    for task in tasks:
        __addTask(output, task["category"].split("/"), task)

    output["pipeline"] = rules

    if fileName == "":
        fileName = printer.getInput("File name (no extension needed): ")

    result = json.dumps(output, indent=2)

    f = open("Inputs/%s.json" % (fileName), "w")
    f.write(result)
    f.close()

    outputRaw["pipeline"] = []
    outputRaw["categories"] = []

#####################

allAssertions = AssertionRetriever.genDict()

def __addCategories(category, name):
    for subCategory in category:
        if subCategory == "tasks":
            for task in category[subCategory]:
                allCategories.append((name, task))
            continue
        else:
            __addCategories(category[subCategory], subCategory)

proxyInformation = SuperProxy.genDict()
for category in proxyInformation:
    __addCategories(proxyInformation[category], category)

#####################

def sneakyDecoy():
    printer.printMessage("Bye!")

def menuOptions():
    message = [("Exit", sneakyDecoy), ("Add Task", addTask)]

    if len(tasks) > 0:
        message.append(("List Added Tasks", listTasks))
        message.append(("Delete Task", deleteTask))

    if len(tasks) > 1:
        message.append(("Create hierarchy rule", createRule))
        message.append(("Delete hierarchy rule", deleteRules))

    message.append(("Add Input File Metadata", addPipelineStuff))
    message.append(("Save Input File", generateFile))

    return message
    

option = ""

while option != "0":
    options = menuOptions()

    printer.printMessage("")
    for index, (msg, _) in enumerate(options):
        printer.printMessage("%s - %s" %(index, msg))

    option = printer.getInput("")

    try:
        options[int(option)][1]()
    except Exception:
        printer.printMessage("Something went wrong!", 3)

    generateFile("autosaved")
