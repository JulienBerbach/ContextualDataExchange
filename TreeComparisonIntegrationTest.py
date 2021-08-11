import TreeComparison
import ChopperModule
import json
import DatabaseInterface

print(" +++ Tree comparison of 2 simple trees +++")

# create 2 database objects with ID 0 and 1
Database0 = DatabaseInterface.connection(dbID = 0)
Database1 = DatabaseInterface.connection(dbID = 1)
'''
# flush to start with an empty database
Database0.FlushDB()
Database1.FlushDB()

# load data for Chopper test
MyJSON0 = [{ 'A' : { 'B' : [ 'C' , 'D', {'B' : { 'X' : 'Z' } } ]  }  }]
TopLevelKeys = ChopperModule.processJSON(Database0, MyJSON0)
print("Unit Test : Input JSON0 processed")

MyJSON1 = [{ 'A' : { 'B' : [ 'C' , 'D', 'E', 'F', {'B' : { 'X' : 'Z' } } ]  }  }]
TopLevelKeys = ChopperModule.processJSON(Database1, MyJSON1)
print("Unit Test : Input JSON1 processed")

# read data from database
treeUID0 = ChopperModule.ReadAllTreesFromBase(Database0, 'A', 3)
print(treeUID0)
treeUID1 = ChopperModule.ReadAllTreesFromBase(Database1, 'A', 3)
print('trees from database read done')

# there are several trees that could have been read, we decide to pick the first one
tree0 = ChopperModule.RemoveTreeUIDSuffix(treeUID0[0])
tree1 = ChopperModule.RemoveTreeUIDSuffix(treeUID1[0])
print('tree from database removal of UID done')

# convert to 1D 
treeOneD0 = TreeComparison.Tree1Dtransformation(tree0)
treeOneD1 = TreeComparison.Tree1Dtransformation(tree1)

print('tree0')
print(tree0)
print(treeOneD0)
print('tree1')
print(tree1)
print(treeOneD1)

# do the tree comparison
Matrix = TreeComparison.ComparisonMatrix(treeOneD0, treeOneD1)
print("Tree comparison done")
print(Matrix)
TreeComparison.ComparisonReport(treeOneD0,treeOneD1, xListName = 'tree0', yListName = 'tree1')

TreeComparison.PlotMatchingMatrix(Matrix, XaxisName = 'tree0', YaxisName = 'tree1')
print('comparison plotting done')
'''
############################################################################

print(" +++ Tree comparison of more complicated trees +++")

# the database objects are already created from the test above
# flush to start with an empty database
Database0.FlushDB()
Database1.FlushDB()

# read file
f = open("Tree_output.json", "r")
FileContent = f.read() 
MyJSON0 = json.loads(FileContent)

# load data for Chopper test
TopLevelKeys = ChopperModule.processJSON(Database0, MyJSON0)
print("Unit Test : Input JSON0 processed")


#MyJSON1 = [{ 'A' : { 'B' : [ 'C' , 'D', 'E', 'F', {'B' : { 'X' : 'Z' } } ]  }  }]
#TopLevelKeys = ChopperModule.processJSON(Database1, MyJSON1)
#print("Unit Test : Input JSON1 processed")


# read data from database
treeUID0 = ChopperModule.ReadAllTreesFromBase(Database0, 'A', 3)
print(treeUID0)

'''
treeUID1 = ChopperModule.ReadAllTreesFromBase(Database1, 'A', 3)
print('trees from database read done')

# there are several trees that could have been read, we decide to pick the first one
tree0 = ChopperModule.RemoveTreeUIDSuffix(treeUID0[0])
tree1 = ChopperModule.RemoveTreeUIDSuffix(treeUID1[0])
print('tree from database removal of UID done')

# convert to 1D 
treeOneD0 = TreeComparison.Tree1Dtransformation(tree0)
treeOneD1 = TreeComparison.Tree1Dtransformation(tree1)

print('tree0')
print(tree0)
print(treeOneD0)
print('tree1')
print(tree1)
print(treeOneD1)

# do the tree comparison
Matrix = TreeComparison.ComparisonMatrix(treeOneD0, treeOneD1)
print("Tree comparison done")
print(Matrix)
TreeComparison.ComparisonReport(treeOneD0,treeOneD1, xListName = 'tree0', yListName = 'tree1')

TreeComparison.PlotMatchingMatrix(Matrix, XaxisName = 'tree0', YaxisName = 'tree1')
print('comparison plotting done')'''
