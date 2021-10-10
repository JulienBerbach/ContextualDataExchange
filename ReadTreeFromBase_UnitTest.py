import ChopperModule
import DatabaseInterface
import ReadTreeFromBase

# this program is to test the loading of Redis database with some examples

print(" +++ Unit Test of ReadTreeFromBase +++")

# create a database object with ID 0
Database = DatabaseInterface.connection(dbID = 0)

# flush to start with an empty database
Database.FlushDB()

# load data for test
MyJSON = [{ 'A' : { 'B' : [ 'C' , 'D', {'B' : { 'X' : 'Z' } } ]  }  }]
TopLevelKeys = ChopperModule.processJSON(Database, MyJSON)


# test tree finding function with depth 1
TestTopNode = "A-1"
TestDepth = 1
TestNodeToBypass = ""
TestResultJSON = ReadTreeFromBase.ReadTree(Database, TestTopNode, TestDepth, TestNodeToBypass)
if TestResultJSON != {"A-1":["B-2"]}:
    print("result for node A-1 with depth 1 is unexpected")

# test tree finding function with depth 2
TestTopNode = "A-1"
TestDepth = 2
#TestNodeToBypass stays null
TestResultJSON = ReadTreeFromBase.ReadTree(Database,TestTopNode, TestDepth, TestNodeToBypass)
TestResultJSON['A-1'][0]['B-2'].sort()
if TestResultJSON != {"A-1": [{ "B-2": ["B-1","C-1","D-1"]}]}:
    print("result for node A-1 with depth 2 is unexpected")
    print(TestResultJSON)

# test tree finding function with depth 3
TestTopNode = "A-1"
TestDepth = 3
# TestNodeToBypass is null
TestResultJSON = ReadTreeFromBase.ReadTree(Database,TestTopNode, TestDepth, TestNodeToBypass)
ExpectedResult = {'A-1': [{'B-2': ['D-1', 'C-1', {'B-1': ['X-1']}]}]}
if not ChopperModule.my_obj_cmp(ExpectedResult, TestResultJSON):
    print("result for node A with depth 3 is unexpected")
    print(TestResultJSON)

# test tree finding function with depth 3 and 1 node to avoid
TestTopNode = "A-1"
TestDepth = 3
TestNodesToBypass = {'B-2'}
TestResultJSON = ReadTreeFromBase.ReadTree(Database,TestTopNode, TestDepth, TestNodesToBypass)
ExpectedResult = {'A-1':['D-1', 'C-1', {'B-1':[{'X-1':['Z-1']}]}]}
if not ChopperModule.my_obj_cmp(ExpectedResult, TestResultJSON):
    print("result for node A with depth 3 and 'B-2' to bypass is unexpected")
    print(TestResultJSON)

# test tree finding function with depth 3 and 2 node to avoid
TestTopNode = "A-1"
TestDepth = 3
TestNodesToBypass = {'B-2','C-1'}
TestResultJSON = ReadTreeFromBase.ReadTree(Database,TestTopNode, TestDepth, TestNodesToBypass)
ExpectedResult = {'A-1':['D-1',{'B-1':[{'X-1':['Z-1']}]}]}
if not ChopperModule.my_obj_cmp(ExpectedResult, TestResultJSON):
    print("result for node A with depth 3 and 'B-2' and 'C-1' to bypass is unexpected")
    print(TestResultJSON)


# test reading of multiple trees
TestTopNode = "B"
TestDepth = 1
TestNodesToBypass = {}
TestResultJSON = ReadTreeFromBase.ReadAllTrees(Database,TestTopNode, TestDepth, TestNodesToBypass)
ExpectedResult = [{'B-1': ['X-1']}, {'B-2': ['C-1', 'B-1', 'D-1']}]
if not ChopperModule.my_obj_cmp(TestResultJSON, ExpectedResult):
    print ('error in ReadAllTreesFromBase')


#ResultFileName = "TestSearchResult.json"
#f = open(ResultFileName, "w")
#f.write(str(TestResultJSON))
#f.close()

