import sys
import json
import os

# This is a (quite scuffed) utility script

# Receives a .puml file - these may be viewed in websites like https://www.planttext.com/
# Converts it to a Pipeline hierarchy
# THIS DOES NOT GENERATE A COMPLETE VALID INPUT FILE FOR TASK SERGEANT

# An hierarchy is written like this
# fatherID --> childID : result

# The result comes in many forms
# String are written with "" (fatherID --> childID : "this is a string")
# Booleans are lowercase, without "" (fatherID --> childID : true)
# Numbers are writen without "", floats are represented with a . (fatherID --> childID : 123.4)
# Lack of result is represented with an Any (fatherID --> childID : Any)

inputFolder = 'p2pInputs'
outputFolder = 'p2pOutputs'

def __puml2pipeline(inputName):
    results = []

    with open('%s/%s.puml' %(inputFolder, inputName)) as inputFile:
        for line in inputFile:
            if not ("-->" in line and ":" in line):
                continue

            result = {}
            paths = []
            path = {}

            parent = line.split("-->")[0].strip()
            remaining = line.split("-->")[-1]

            child = remaining.split(":")[0].strip()
            key = remaining.split(":")[-1].strip()

            result["id"] = parent

            path["nextSlotId"] = child

            if key == "Any": # No key specified
                pass
            elif key.lower() == "true":
                path["key"] = True
            elif key.lower() == "false":
                path["key"] = False
            elif key.lower() == "none":
                path["key"] = None
            elif key.replace('.','',1).isdigit(): # float
                path["key"] = float(key)
                if key.isdigit():                 # integer
                    path["key"] = int(key)
            else:                                 # string
                path["key"] = key.replace("\"", "")

            paths.append(path)
            
            result["paths"] = paths

            results.append(result)

    final = {}

    final["pipeline"] = results

    output = json.dumps(final, indent=2)

    f = open('%s/%s.json' %(outputFolder, inputName), "w")
    f.write(output)
    f.close()

#################################

def __pipeline2puml(inputName):
    finalResult = ""

    with open('%s/%s.json' %(inputFolder, inputName)) as inputFile:
        info = json.load(inputFile)

        for rule in info["pipeline"]:
            for path in rule["paths"]:
                try:
                    key = path["key"]
                    if type(key) == str:
                        finalResult += "\n%s --> %s : \"%s\"" %(rule["id"], path["nextSlotId"], key)
                    else:
                        finalResult += "\n%s --> %s : %s" %(rule["id"], path["nextSlotId"], key)
                except Exception:
                    finalResult += "\n%s --> %s : Any" %(rule["id"], path["nextSlotId"])
                

    finalResult = "@startuml\n[*] --> Placeholder\n" + finalResult + "\n@enduml"    

    f = open('%s/%s.puml' %(outputFolder, inputName), "w+")
    f.write(finalResult)
    f.close()

#################################

inputName = None

for arg in sys.argv:
    inputName = arg

if inputName is None:
    raise Exception("No file indicated for the execution of this script")

file_name, file_extension = os.path.splitext(inputName)

if(file_extension == ".puml"):
    __puml2pipeline(file_name)
elif(file_extension == ".json"):
    __pipeline2puml(file_name)
else:
    raise Exception("This file extension is not supported")
