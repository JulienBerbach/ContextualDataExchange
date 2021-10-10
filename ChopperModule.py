# This module writes and reads from the database
# expected "Database" is a database oject from class connection in DatabaseInterface module
#-------------------------------------------------------------------------------------------

# this functions adds an entity in the database if it is not existing yet
# expected element is a string like 'A'
# it returns the instance number
def AddFoundKey(Database, element):
    return Database.AddFoundKey(element)

# this recursive function processes a nested JSON generated from a linux tree command
# the expected input argument is an python list containing dictionaries or simple elements
#  [{ A : B, C : D }, { X : [ D , E ] }, K , { F : { V : W } } ]
# the function returns a list of single entities (already created) that must be linked
#  by the caller
# [ A, C, X, K , F]
def processJSON(Database, local_JSON):

    KeysFoundSoFar = list(())
    # Python list of keys that will be returned to the caller, for possible linking
    # to something on a higher level

    print("localJSON : "+ str(local_JSON))

    # loop on the list elements, in [..]
    for element in local_JSON:

        # check if these elements are python dictionaries { .. }
        if isinstance(element, dict):
        # loop on the keys of the elements in {..}
            for key in element:

                # check if the type of the element is of a simple type
                if (isinstance(element[key], str) or isinstance(element[key], int) or
                    isinstance(element[key], float) or isinstance(element[key], bool)):
                    # a single dictionary element is added
                    NewElement = {key : []} # create dictionary, it will hold only one element
                    NewElement[key].append(element[key])
                    TuplesAdded = Database.ProcessFoundTuples(NewElement)

                # check if the type of the element could be an array [..]
                elif isinstance(element[key], list):
                    # it is a list then we call the function recursively
                    EntitiesBelow = processJSON(Database, element[key])
                    ## here we have to link the entities found below
                    NewElements = {key : []} # create dictionary that will contain the found links
                    for i in EntitiesBelow:
                        NewElements[key].append(i) # append new element
                    TuplesAdded = Database.ProcessFoundTuples(NewElements)

                # check if the type of element below is a dictionary {..}
                elif isinstance(element[key], dict):
                    # we call the function recursively, the element must be transformed into
                    # a list (of one element) before continuing
                    listToProcess = []
                    listToProcess.append(element[key])
                    EntitiesBelow = processJSON(Database, listToProcess)
                    ## here we have to link the entities found below
                    NewElements = {key : []} # create dictionary that will contain the found links
                    for i in EntitiesBelow:
                        NewElements[key].append(i) # append new element
                    TuplesAdded = Database.ProcessFoundTuples(NewElements)

                else:
                    print('ProcessJSON, unknown element type : ' + str(element[key]))

            # append the element that has been returned by the add process
            for key in TuplesAdded:
                KeysFoundSoFar.append(key)

        elif (isinstance(element, str) or isinstance(element, int) or
            isinstance(element, float) or isinstance(element, bool)):
            # add the key to the list that will be returned to the caller, for possible linking
            # nothing below, so no need to process a tuple, just returning the element found above
            KeysFoundSoFar.append(element)

        else:
            print('processJSON, unknow element type : ' + str(element))

    # the result is returned, these are the single elements found in that level
    # the tuples found (composed of element of this level, and what has been returned below
    # have taken care by calling ProcessFoundTuples)
    return (KeysFoundSoFar)


# tooling related to Tree data model
#----------------------------------------------------------------------------------------

# function that simply removes the unicity suffix like "-1"
# the input element is a string
def RemoveUIDSuffix(element):
    y = element.split('-')
    h = y[-1]
    if h.isnumeric():
        return element.rstrip('-' + h)
    else:
        raise Exception('The database element is expected to have at the end a dash and a number')

# function that simply removes the unicity suffix like "-1" on a nested object of dictionaries and lists
# the input variable "tree" is a dictionary
# all basic elements are strings
# the returned variable is of the same type
def RemoveTreeUIDSuffix(tree):
    newTree = dict()
    for i in tree:
        newI = RemoveUIDSuffix(i)
        if isinstance(tree[i], list):
            newList = list()
            for y in tree[i]:
                if isinstance(y,str):
                    newList.append(RemoveUIDSuffix(y))
                elif isinstance(y, dict):
                    newList.append(RemoveTreeUIDSuffix(y))
                else:
                    raise Exception('Unknown element type found in dictionary')
            newTree[newI] = newList
        elif isinstance(tree[i], dict):
            newTree[newI] = RemoveTreeUIDSuffix(tree[i])
        elif isinstance(tree[i], str):
            newTree[newI] = RemoveUIDSuffix(tree[i])
        else:
            raise Exception('Unknown element type found in dictionary')
    return newTree



# generic tooling for tests
#----------------------------------------------------------------------------------------

# sorting of json for making comparion possible - does not work with list in the dict.
def sorting(item):
    if isinstance(item, dict):
        return sorted((key, sorting(values)) for key, values in item.items())
    if isinstance(item, list):
        return sorted(sorting(x) for x in item)
    else:
        return item

# object comparator seems to work fine (tested on a few examples)
# https://stackoverflow.com/questions/25851183/how-to-compare-two-json-objects-with-the-same-elements-in-a-different-order-equa

def my_list_cmp(list1, list2):
    if (list1.__len__() != list2.__len__()):
        return False

    for l in list1:
        found = False
        for m in list2:
            res = my_obj_cmp(l, m)
            if (res):
                found = True
                break
        if (not found):
            return False
    return True


def my_obj_cmp(obj1, obj2):
    if isinstance(obj1, list):
        if (not isinstance(obj2, list)):
            return False
        return my_list_cmp(obj1, obj2)
    elif (isinstance(obj1, dict)):
        if (not isinstance(obj2, dict)):
            return False
        exp = set(obj2.keys()) == set(obj1.keys())
        if (not exp):
            # print(obj1.keys(), obj2.keys())
            return False
        for k in obj1.keys():
            val1 = obj1.get(k)
            val2 = obj2.get(k)
            if isinstance(val1, list):
                if (not my_list_cmp(val1, val2)):
                    return False
            elif isinstance(val1, dict):
                if (not my_obj_cmp(val1, val2)):
                    return False
            else:
                if val2 != val1:
                    return False
    else:
        return obj1 == obj2
    return True
