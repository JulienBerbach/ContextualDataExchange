
import matplotlib.pyplot as plt 
import numpy as np


# transforms the tree in a 1D numeric representation
# returns a dictionary with the point names and the value on a line, center is the top node
# child nodes are distributed evenly between nodes left and right of parent node
# the input tree is a dictionary of lists
def NumberOfElements(tree):
    number = 0
    for i in tree:
        number += 1
        if isinstance(tree[i], list):
            for y in tree[i]:
                if isinstance(y,str):
                    number +=1
                elif isinstance(y, dict):
                    number = number + NumberOfElements(y)
                else:
                    raise Exception('Unknown element type found in dictionary')
        elif isinstance(tree[i], dict):
            number = number + NumberOfElements(tree[i])
        elif isinstance(tree[i], str):
            number += 1
        else:
            raise Exception('Unknown element type found in dictionary')
    return number

# the idea is to create a grid with the same number of elemens as the content of the tree
# then the grid is populated from left to right
# the children are put around of the parent, if it's an uneven number, the right side will have one more
# all elements are shifted to the right
# ex: { A : [B, C, D] } translates into ordered list ( B, A, C, D)
# the input is expected to be a python dictionary
# lists shall always be used for nested dictionaries, {A:[{ B : C }]}, not { A:{ B : C }}
def Tree1Dtransformation(tree):

    newI = list()
    for i in tree:
        newI.append(i)
        if isinstance(tree[i], list):
            newList = list()
            # we have to check the number of elements in the list in order to know how to distribute them around i
            elementsLeft = len(tree[i]) // 2
            # now we loop through the list members, y will be the index following these
            inputListIndex = 0
            insersionIndex = 0
            while inputListIndex < elementsLeft:
                # insert element to the left, same position as in the input list
                if isinstance(tree[i][inputListIndex],str):
                    newI.insert(insersionIndex, tree[i][inputListIndex])
                    inputListIndex += 1
                    insersionIndex += 1
                elif isinstance(tree[i][inputListIndex], dict):
                    newList = Tree1Dtransformation(tree[i][inputListIndex])
                    # we need to insert all the elements found below one by one
                    for z in newList:
                        newI.insert(insersionIndex, z)
                        insersionIndex +=1
                    inputListIndex += 1
                else:
                    raise Exception('Unknown element type found')

            while inputListIndex < len(tree[i]):
                # insert element to the right, same position but after the key
                # position to start with is + 1 to account for the key
                if isinstance(tree[i][inputListIndex],str):
                    newI.insert(insersionIndex + 1, tree[i][inputListIndex])
                    inputListIndex += 1
                    insersionIndex += 1
                elif isinstance(tree[i][inputListIndex], dict):
                    newList = Tree1Dtransformation(tree[i][inputListIndex])
                    # we need to insert all the elements found below one by one
                    for z in newList:
                        newI.insert(insersionIndex + 1 , z)
                        insersionIndex +=1
                    inputListIndex += 1
                else:
                    raise Exception('Unknown element type found')

       # elif isinstance(tree[i], dict):
            # marche pas
            #insersionIndex +=1
            #newI.insert(insersionIndex,Tree1Dtransformation(tree[i]))
        elif isinstance(tree[i], str) :
            # the unique element is added to the right
            newI.append(tree[i])
        else:
                    raise Exception('Unknown element type found')

    return newI

# this procedures creates a matrix that can be plotted
# when there is a match there is a 1, otherwise 0
def ComparisonMatrix(xTreeList, yTreeList):
    # create an empty matrix withe zeros, having the dimension of the lists
    arr = np.zeros((len(xTreeList),len(yTreeList)), np.int32)
    # loop on the elements 
    xpoint = 0
    for x in xTreeList:
        ypoint = 0
        for y in yTreeList:
            if x == y:
               arr[xpoint,ypoint] = 1
            ypoint += 1
        xpoint += 1
    return arr


def ComparisonReport(xTreeList, yTreeList, xListName = '', yListName = ''):
    xSet = set(xTreeList)
    ySet = set(yTreeList)
    # print the elements that are new in x in comparison to y
    # this comparison will not see duplicates
    print('new elements in ' + xListName + ' not present in ' + yListName)
    print(xSet.difference(ySet))
    print('new elements in ' + yListName + ' not present in ' + xListName)
    print(ySet.difference(xSet))

    # print the elements that have a different position


# expects a 2D array
def PlotMatchingMatrix(arr, XaxisName = '', YaxisName = ''):
    
    (xLength, yLength) = np.shape(arr)
    XList = list()
    YList = list()

    # plot the elements that have not found a correspondance
    # loop on x elements and check
    for i in range (0,yLength):
        # h is the slice of matching matrix of row i
        h = arr[:,i]
        H = np.where(h == 1)
        # if length is 0, there has been no matching, so we add the point
        if len(H[0]) == 0:
            XList.append(0)
            YList.append(i)

    # loop on y elements and check for missing correspondance
    for i in range (0,xLength):
        # h is the slice of matching matrix of column i
        h = arr[i,:]
        H = np.where(h == 1)
        if len(H[0]) == 0:
            XList.append(i)
            YList.append(0)

    # plot the found points
    xpoints = np.array(XList)
    ypoints = np.array(YList)
    plt.scatter(xpoints, ypoints)
    
    # plot the "ones" of the matrix
    (x,y) = np.nonzero(arr)
    plt.scatter(x,y)
    
    plt.xlabel(XaxisName)
    plt.ylabel(YaxisName)

    plt.show()
    