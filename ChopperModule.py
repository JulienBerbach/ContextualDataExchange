# This module writes and reads from the database

import DatabaseInterface

# this functions adds an entity in the database if it is not existing yet
# expected element is a string like 'A'
# it returns the instance number
def AddFoundKey(element):
    return DatabaseInterface.AddFoundKey(element)

# recursive function that processes a nested JSON generated from a tree 
# the expected input argument is an python list containing dictionaries or simple elements
#  [{ A : B, C : D }, { X : [ D , E ] }, K , { F : { V : W } } ]
# the function returns a list of single entities (already created) that must be linked
#  by the caller
# [ A, C, X, K , F]
def processJSON(local_JSON):

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
                    NewElement = dict(())
                    NewElement[key] = element[key]
                    TuplesAdded = DatabaseInterface.ProcessFoundTuples(NewElement)
                
                # check if the type of the element could be an array [..]
                elif isinstance(element[key], list):
                    # it is a list then we call the function recursively
                    EntitiesBelow = processJSON(element[key])
                    ## here we have to link the entities found below
                    NewElements = {key : []} # create dictionary that will contain the found links
                    for i in EntitiesBelow:
                        NewElements[key].append(i) # append new element 
                    TuplesAdded = DatabaseInterface.ProcessFoundTuples(NewElements)

                # check if the type of element below is a dictionary {..}
                elif isinstance(element[key], dict):
                    # we call the function recursively, the element must be transformed into 
                    # a list (of one element) before continuing
                    listToProcess = []
                    listToProcess.append(element[key])
                    EntitiesBelow = processJSON(listToProcess)
                    ## here we have to link the entities found below
                    NewElements = {key : []} # create dictionary that will contain the found links
                    for i in EntitiesBelow:
                        NewElements[key].append(i) # append new element 
                    TuplesAdded = DatabaseInterface.ProcessFoundTuples(NewElements)

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



# recursive function that replaces nodes with deeper one until no bypass is required
# the inputs are two set, the one of elements to bypass, the working one
def BypassedSet(SetToBypass, WorkingSet):
    for i in WorkingSet.intersection(SetToBypass):
        # this pass consists into removing all bypass elements found
        WorkingSet.remove(i)
        # search for elements linked to i
        LinkedSet = DatabaseInterface.LinkedToElements(i)
        # add new set elements found to working set
        WorkingSet.update(LinkedSet)
    # check if there are still nodes to bypass
    if WorkingSet.intersection(SetToBypass): # this is false is the intersection is empty
        # call for reiterate pass
        NewSet = BypassedSet(SetToBypass, WorkingSet) 
        return NewSet
    else:
        return WorkingSet

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
      



# function that returns a tree in form of a JSON file from database (python dictionary)
# the input is the searched top node (string) with an instance number as suffix, like 'A-1'
# the desired depth in an integer, default is 1
# NodesToBypass is a set of generic nodes, without suffix { "A", "B" }, default empty
# if TopNode does not exist : returns {}
# depth = 0 : returns {}
# depth = 1 : returns something like {  'Q-1' : [ 'A-2' , 'B-4', 'C-1' ]}
# depth = 2 : returns something like { 'Q-1': [ {'A-2' : [ 'A1-1', 'A2-1' ]}, 'B-5' , 'C-1' ]}
# if NodesToBypass = {'A'}, the above is returned like : { 'Q-1' : [ A1', 'A2', 'B' , 'C' ]}
# if NodesToBypass = {'A1'}, the 2 lines above is returned as { 'Q-1' : [ {'A-2': [ A2']}, 'B' , 'C' ]}
def ReadTreeFromBase(TopNode, RequiredDepth = 1 , NodesToBypass = {}):
    
    theJSON = dict()
    print("ReadTreeFromBase")
    print("top node = " + TopNode)
  
    # check if TopNode exists
    if DatabaseInterface.ElementExists(TopNode):
        # read all the elements linked to TopNode
        scanResult = DatabaseInterface.LinkedToElements(TopNode)
       
        # remove nodes to bypass until there are none of these nodes anymore in the set
        if NodesToBypass == {}:
            LinkedSet = scanResult
        else:
            LinkedSet = BypassedSet(NodesToBypass, scanResult)
        CurrentRequiredDepth = RequiredDepth - 1
        if (not LinkedSet): # if the result is empty
            return dict()
        else:
            # now we have found a set to link 
            theJSON[TopNode] = [] # declare     the elements as a list
            for j in LinkedSet:
                # add the element to the list, we construct {A : [A1, A2, A3]}
                theJSON[TopNode].append(j)
            # now we have to go one level deeper for all the elements found at this level
            # only if there is a need to go deeper
            if CurrentRequiredDepth == 0:
                return theJSON
            else:
                # loop the table elements and get the tree below filled
                for j in range(len(theJSON[TopNode])):
                    # in this call, the top node is given by MainNode][j]
                    LowerResult = ReadTreeFromBase(theJSON[TopNode][j], CurrentRequiredDepth, NodesToBypass)
            
                    # if not empty, add the result found below, otherwise do nothing
                    if LowerResult:
                        theJSON[TopNode][j] = LowerResult
                return theJSON

    else:
        return theJSON


# function that returns a list of possible trees in form of dictionaries
# according to all existing instances of a key
# ex: for key "A" it will return a possible tree for "A-1", "A-2", "A-3" etc.
# input argument is the generic key name, without suffix
def ReadAllTreesFromBase(TopNode, RequiredDepth = 1, NodesToBypass = {}):

    if DatabaseInterface.GenericKeyElementExists(TopNode):
        returnedSet = list()
        for i in range (1, 1 + DatabaseInterface.LastInstanceIndex(TopNode)):
            returnedSet.append(ReadTreeFromBase(TopNode + '-' + str(i), RequiredDepth, NodesToBypass))
        return returnedSet
    else:
        return list()

# tooling
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
