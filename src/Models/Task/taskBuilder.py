from .task import Task

##
# @class TaskBuilder
# @brief Builder class for Task.
#
# A Builder class for Task - implemented according to the Builder Pattern
class TaskBuilder():

    ##
    # @param self
    #
    # Resets itself upon instantiation
    def __init__(self):
        self.reset()

    ##
    # @param self TaskBuilder instance
    #
    # @brief Defines it's own Task instance as a new one
    def reset(self):
        self.__categoriesFlag = False
        self.__descriptionFlag = False
        self.__task = Task()

    ##
    # @property task
    # @param self TaskBuilder instance
    #
    # @throws Exception "No categories provided when creating a Task!"
    #
    # @return task The Task instance being built
    #
    # @brief TaskBuilder's Task instance. Upon being retrieved, it resets.
    @property
    def task(self):
        if not self.__categoriesFlag:
            raise Exception("No categories provided when creating a Task!")
        if not self.__descriptionFlag:
            self.addDescription("No description provided...")
        self.__task.setup()
        task = self.__task
        self.reset()
        return task

    ##
    # @param self TaskBuilder instance
    # @param value The input's values for the Task
    #
    # @return self TaskBuilder instance
    #
    # @brief Adds the input's value to the Task's dict, under the key "value"
    def addValue(self, value):
        self.__task.data["value"] = value
        return self

    ##
    # @param self TaskBuilder instance
    # @param categories The input's categories for the Task
    #
    # @return self TaskBuilder instance
    #
    # @brief Adds the input's categories to the Task's dict, under the key "categories"
    def addCategories(self, categories):
        self.__task.data["categories"] = categories
        self.__categoriesFlag = True
        return self

    ##
    # @param self TaskBuilder instance
    # @param expected The input's expected value for the Task
    #
    # @return self TaskBuilder instance
    #
    # @brief Adds the input's description to the Task's dict, under the key "expectedValue"
    def addExpected(self, expected):
        self.__task.data["expectedValue"] = expected
        return self

    ##
    # @param self TaskBuilder instance
    # @param description The input's description for the Task
    #
    # @return self TaskBuilder instance
    #
    # @brief Adds the input's description to the Task's dict, under the key "description"
    def addDescription(self, description):
        self.__task.data["description"] = description
        self.__descriptionFlag = True
        return self

    ##
    # @param self TaskBuilder instance
    # @param assertionType The input's assertionType for the Task
    #
    # @return self TaskBuilder instance
    #
    # @brief Adds the input's assertionType to the Task's dict, under the key "assertionType"
    def addAssertionType(self, assertionType):
        self.__task.data["assertionType"] = assertionType
        return self
