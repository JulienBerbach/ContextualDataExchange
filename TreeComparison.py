import ChopperModule

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

"""def Tree1Dtransformation(tree):

    new1DTree = dict()
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
            new1DTree[newI] = newList
        elif isinstance(tree[i], dict):
            new1DTree[newI] = RemoveTreeUIDSuffix(tree[i])
        elif isinstance(tree[i], str):
            new1DTree[newI] = RemoveUIDSuffix(tree[i])
        else:
            raise Exception('Unknown element type found in dictionary')
    return new1DTree
"""