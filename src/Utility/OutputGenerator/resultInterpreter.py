from ..printer import Printer
from ...Models.Tasks.Native.runCommand import RunCommand
from datetime import datetime

import json

def generate_output(pipeline):
    
    result = json.dumps(pipeline, indent=2)+"\n"

    filename = __generate_filename(pipeline["name"], pipeline["version"])
    Printer.getInstance().printMessage("Generating output file in ./Outputs/%s.json" %(filename), 1)

    try:
        RunCommand().execute_task("if not exist Outputs mkdir Outputs")

        f = open("./Outputs/%s.json" %(filename), "w+")
        f.write(result)
        f.close()
        Printer.getInstance().printMessage("Output file generated at ./Outputs/%s.json" %(filename))
    except:
        Printer.getInstance().printMessage("Failed to generate %s.json" %(filename), 2)


def __generate_filename(name: str, datetime_str: str) -> str:

    # Use 'output' if name is empty
    name = name.strip().lower().replace(" ", "_").replace("-", "_") if name.strip() else "output"
    
    # Convert datetime_str to desired format or use current time
    try:
        dt = datetime.strptime(datetime_str, "%d/%m/%Y %H:%M:%S")
    except (ValueError, TypeError):
        dt = datetime.now()
    
    formatted_dt = dt.strftime("%Y%m%d_%H%M%S")
    
    return f"{name}_{formatted_dt}"
