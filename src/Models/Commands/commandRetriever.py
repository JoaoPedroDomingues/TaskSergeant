##
# @param proxy The Proxy that maps the current layer
# @param categories A list that contains the path to the desired Command
#
# @return The Command instance defined by the path
#
# @brief Processes the category list and either calls itself recursively with a new Proxy or returns the Command specified by the path.
def retrieveCommand(proxy, categories):
    (category, subCategories) = __processCategories(categories)

    if subCategories:
        proxy = proxy.proxies.get(category, None) # This may be changed, where we create a default task area that debugs the input

        if proxy is None: # If that default task area happens, this ceases to exist
            return None

        return retrieveCommand(proxy(), subCategories)

    else:
        command = proxy.commands.get(category, None) # This may be changed, where we create a default task area that debugs the input

        if command is None: # If that default task area happens, this ceases to exist
            return None

        return command()

##
# @param categories A list that contains the path to the desired Command
#
# @return A Tuple containing the head and tail of the categories list
#
# @brief Divides the categories list parameter into head and tail, returning both in a Tuple
def __processCategories(categories):
    category = categories[0]
    del categories[0]
    return category, categories
