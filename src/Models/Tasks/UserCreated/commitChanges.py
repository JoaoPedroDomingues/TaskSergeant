from .userGeneratedTask import UserGeneratedTask, Printer

##
# @class Hello
#
# @brief This Task is a test
class CommitChanges(UserGeneratedTask):

    @staticmethod
    def id():
        return "commitChanges"

    def executeTask(self, value):
        printer = Printer.getInstance()

        self.executeCommand("cd %s" %(value))

        self.executeCommand("git add .")
        printer.printMessage(self.executeCommand("git status"))

        if printer.getInput("Want to proceed with the commit? (y/n)").lower() == 'y':
            self.executeCommand("git commit -m \"%s\"" %(printer.getInput("Commit message")))
            self.executeCommand("git push origin main")
            return True
        
        return False
