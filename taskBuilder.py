import json
from datetime import datetime
from copy import deepcopy
from src.Models.Assertions.assertionRetriever import AssertionRetriever
from src.Models.Commands.superProxy import SuperProxy
from src.Utility.printer import Printer

Printer(True, True)

allAssertions = []
allCategories = []
tasks = []
rules = []
outputRaw = {"name" : "", "version" : "", "timeout" : 60, "pipeline": [], "categories": []}

# Category Stuff

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
        while key == "":
            key = input("Input key (non-empty string): ")
    value = input("Input value: ").strip()
    Printer.getInstance().printMessage("Value type (string by default or in case of conversion failure):\n1 - String\n2 - Boolean\n3 - Integer\n4 - Float", 4)
    valueType = input("Choose one --> ")

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

def addTask():
    categories = listCategories()

    category = None

    Printer.getInstance().printMessage("\nChoose the task's category by it's index: ", 4)
    while category == None:
        Printer.getInstance().printMessage("\n", 4)

        for count, category in enumerate(categories):
            Printer.getInstance().printMessage("%d - %s" % (count, category), 4)

        index = input("Choose one --> ")
        try:
            category = categories[int(index)]
        except Exception:
            Printer.getInstance().printMessage("Invalid index..!", 3)

    task = {}
    task["category"] = category

    Printer.getInstance().printMessage("\n", 4)
    toList = []
    for command in allCategories:
        if command[0] == category:
            toList.append(command[1])

    for count, command in enumerate(toList):
        Printer.getInstance().printMessage("%s - %s" %(count, command), 4)

    command = input("Insert the Command to be used, using it's index: ")
    try:
        task["command"] = toList[int(command)]
    except Exception:
        Printer.getInstance().printMessage("Something went wrong, exiting Task creation!", 4)
        return

    Printer.getInstance().printMessage("\n", 4)
    repeatable = ""
    repeatable = input("Number of possible repetitions (defaults to 1): ")
    try:
        repeatable = int(repeatable)
        task["repeatable"] = repeatable
    except Exception:
        task["repeatable"] = 1

    Printer.getInstance().printMessage("\n", 4)
    description = ""
    while description == "":
        description = input("Insert the task's description (required): ")
    task["description"] = description

    value = None
    Printer.getInstance().printMessage("\nWhat type of input will the Command need? (enter to skip)\n1 - Single input\n2 - List of inputs\n3 - Composed input (each value has a key)", 4)
    option = input("Choose one --> ")
    if option == "1":
        _, value = createValue()
    elif option == "2":
        value = []
        more = "y"
        while more == "y":
            _, valueAux = createValue()
            value.append(valueAux)
            more = input("Add another value? (y/n): ").lower()
    elif option == "3":
        value = {}
        more = "y"
        while more == "y":
            key, valueAux = createValue(True)
            value[key] = valueAux
            more = input("Add another value? (y/n): ").lower()
    if value is not None:
        task["value"] = value

    Printer.getInstance().printMessage("\n", 4)

    for count, assertion in enumerate(allAssertions):
        Printer.getInstance().printMessage("%s - %s" %(count, assertion), 4)

    index = input("Insert the Assertion to be used, using it's index (enter to skip): ")

    try:
        assertionType = allAssertions[int(index)]
    except Exception:
        assertionType = ""

    if assertionType != "":
        task["assertionType"] = assertionType

        value = None

        Printer.getInstance().printMessage("\nWhat type of input will the Assertion need? (enter to skip)\n1 - Single input\n2 - List of inputs\n3 - Composed input (each value has a key)", 4)
        option = input("Choose one --> ")
        if option == "1":
            _, value = createValue()
        elif option == "2":
            value = []
            more = "y"
            while more == "y":
                _, valueAux = createValue()
                value.append(valueAux)
                more = input("Add another value? (y/n): ").lower()
        elif option == "3":
            value = {}
            more = "y"
            while more == "y":
                key, valueAux = createValue(True)
                value[key] = valueAux
                more = input("Add another value? (y/n): ").lower()
        if value is not None:
            task["expected"] = value

    id = " "
    while(" " in id):
        id = input("Task unique hierarchy identifier without spaces (enter to skip): ")
    if id != "":
        task["id"] = id

    tasks.append(task)

def listTasks():
    Printer.getInstance().printMessage("\n", 4)

    for count, task in enumerate(tasks):
        Printer.getInstance().printMessage("%d - %s: %s" %(count, task.get("id", None), task["description"]), 4)

def deleteTask():
    Printer.getInstance().printMessage("\n", 4)
    if(len(tasks) == 0):
        Printer.getInstance().printMessage("No tasks exist yet!",3)
        return

    listTasks()

    try:
        index = int(input("Select the index to delete"))
        del tasks[index]
    except Exception:
        pass

# Hierarchy stuff

def createRule():
    Printer.getInstance().printMessage("", 4)
    tasksWithId = []
    for task in tasks:
        if task.get("id", None) is not None:
            tasksWithId.append(task)

    if tasksWithId == []:
        Printer.getInstance().printMessage("No tasks eligible for an hierarchy (they need an id)!!", 3)
        return

    for count, task in enumerate(tasksWithId):
        Printer.getInstance().printMessage("%d - %s: %s" % (count, task["id"], task["description"]), 4)

    parent = None
    try:
        parent = tasksWithId[int(input("Select the parent task by index: "))]["id"]
    except Exception:
        Printer.getInstance().printMessage("Invalid index!!! Exiting...", 3)
        return

    child = None
    try:
        child = tasksWithId[int(input("Select the child task by index: "))]["id"]
    except Exception:
        Printer.getInstance().printMessage("Invalid index!!! Exiting...", 3)
        return

    addRule = input("Add a rule? (y/n) ").lower()

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
        Printer.getInstance().printMessage("%s - %s --> %s : %s" % (count, parent, child, key), 4)

def deleteRules():
    Printer.getInstance().printMessage("", 4)

    if(len(rules) == 0):
        Printer.getInstance().printMessage("No rules created yet...", 3)
        return

    Printer.getInstance().printMessage("Select an hierarchy rule by it's index: ", 4)
    listRules()
    try:
        index = int(input("Choose one --> "))
        del rules[index]
    except Exception:
        Printer.getInstance().printMessage("Some error has occured, going back to menu", 3)

# Pipeline stuff

def addPipelineStuff():
    Printer.getInstance().printMessage("", 4)
    outputRaw["name"] = input("Insert the name for this input: ")

    timeout = None
    while type(timeout) != float:
        try:
            timeout = float(input("Insert the timeout (in seconds) for the task executions: "))
        except Exception:
            timeout = None
            
    outputRaw["timeout"] = timeout
    outputRaw["version"] = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

# Generate File

def generateFile(fileName=""):

    output = outputRaw

    for category in listCategories():
        __addCategoryAux(output, category.split("/"))

    for task in tasks:
        __addTask(output, task["category"].split("/"), task)

    output["pipeline"] = rules

    if fileName == "":
        fileName = input("File name (no extension needed): ")

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
        if subCategory == "commands":
            for command in category[subCategory]:
                allCategories.append((name, command))
            continue
        else:
            __addCategories(category[subCategory], subCategory)

proxyInformation = SuperProxy.genDict()
for category in proxyInformation:
    __addCategories(proxyInformation[category], category)

#####################

def sneakyDecoy():
    Printer.getInstance().printMessage("Bye!")

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

    for index, (msg, _) in enumerate(options):
        Printer.getInstance().printMessage("%s - %s" %(index, msg), 4)

    option = input("Choose one --> ")

    try:
        options[int(option)][1]()
    except Exception:
        Printer.getInstance().printMessage("Invalid option!", 3)

    generateFile("autosaved")
