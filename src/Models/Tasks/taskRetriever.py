##
# @param proxy The Proxy that maps the current layer
# @param categories A list that contains the path to the desired Task
#
# @return The Task instance defined by the path
#
# @brief Processes the category list and either calls itself recursively with a new Proxy or returns the Task specified by the path.
def retrieveTask(proxy, categories):
    (category, subCategories) = __processCategories(categories)

    if subCategories:
        proxy = proxy.proxies.get(category, None) # This may be changed, where we create a default task area that debugs the input

        if proxy is None: # If that default task area happens, this ceases to exist
            return None

        return retrieveTask(proxy(), subCategories)

    else:
        task = proxy.tasks.get(category, None) # This may be changed, where we create a default task area that debugs the input

        if task is None: # If that default task area happens, this ceases to exist
            return None

        return task()

##
# @param categories A list that contains the path to the desired Task
#
# @return A Tuple containing the head and tail of the categories list
#
# @brief Divides the categories list parameter into head and tail, returning both in a Tuple
def __processCategories(categories):
    category = categories[0]
    del categories[0]
    return category, categories
