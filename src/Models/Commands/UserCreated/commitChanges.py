from .userGeneratedCommand import UserGeneratedCommand, Printer

##
# @class Hello
#
# @brief This Command is a test
class CommitChanges(UserGeneratedCommand):

    @staticmethod
    def id():
        return "commitChanges"

    def execute_task(self, value):
        printer = Printer.getInstance()

        self.execute_command("cd %s" %(value))

        self.execute_command("git add .")
        printer.printMessage(self.execute_command("git status"))

        if printer.getInput("Want to proceed with the commit? (y/n)").lower() == 'y':
            self.execute_command("git commit -m \"%s\"" %(printer.getInput("Commit message")))
            self.execute_command("git push origin main")
            return True
        
        return False
