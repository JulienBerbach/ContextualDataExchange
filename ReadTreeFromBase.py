
# recursive function that replaces nodes with deeper one until no bypass is required
# the inputs are two set, the one of elements to bypass, the working one
def BypassedSet(Database, SetToBypass, WorkingSet):
    for i in WorkingSet.intersection(SetToBypass):
        # this pass consists into removing all bypass elements found
        WorkingSet.remove(i)
        # search for elements linked to i
        LinkedSet = Database.LinkedToElements(i)
        # add new set elements found to working set
        WorkingSet.update(LinkedSet)
    # check if there are still nodes to bypass
    if WorkingSet.intersection(SetToBypass): # this is false is the intersection is empty
        # call for reiterate pass
        NewSet = BypassedSet(Database, SetToBypass, WorkingSet)
        return NewSet
    else:
        return WorkingSet


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
def ReadTree(Database, TopNode, RequiredDepth = 1 , NodesToBypass = {}):

    theJSON = dict()
    print("ReadTreeFromBase")
    print("top node = " + TopNode)

    # check if TopNode exists
    if Database.ElementExists(TopNode):
        # read all the elements linked to TopNode
        scanResult = Database.LinkedToElements(TopNode)

        # remove nodes to bypass until there are none of these nodes anymore in the set
        if NodesToBypass == {}:
            LinkedSet = scanResult
        else:
            LinkedSet = BypassedSet(Database, NodesToBypass, scanResult)
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
                    LowerResult = ReadTree(Database, theJSON[TopNode][j], CurrentRequiredDepth, NodesToBypass)

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
def ReadAllTrees(Database, TopNode, RequiredDepth = 1, NodesToBypass = {}):

    if Database.GenericKeyElementExists(TopNode):
        returnedSet = list()
        for i in range (1, 1 + Database.LastInstanceIndex(TopNode)):
            returnedSet.append(ReadTree(Database, TopNode + '-' + str(i), RequiredDepth, NodesToBypass))
        return returnedSet
    else:
        return list()
