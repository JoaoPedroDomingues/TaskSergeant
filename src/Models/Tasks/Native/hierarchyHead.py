from .nativeTask import NativeTask

##
# @class HierarchyHead
#
# @brief This Task does nothing, can be used as the head of a hierarchy
class HierarchyHead(NativeTask):

    @staticmethod
    def id():
        return "hierarchyHead"

    def executeTask(self, value):
        return value
