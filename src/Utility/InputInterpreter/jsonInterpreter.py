import json

class JsonInterpreter():

    @staticmethod
    def process(inputFile):
        return json.loads(inputFile.read())
