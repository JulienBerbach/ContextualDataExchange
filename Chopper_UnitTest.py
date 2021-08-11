import ChopperModule
import json
import DatabaseInterface

print(" +++ Unit Test of Chopper +++")
# this program is to test the loading of Redis database with some examples

# create a database object with ID 0
Database = DatabaseInterface.connection(dbID = 0)

# flush to start with an empty database
Database.FlushDB()

# load data for Chopper test
MyJSON = [{ 'A' : { 'B' : [ 'C' , 'D', {'B' : { 'X' : 'Z' } } ]  }  }]
TopLevelKeys = ChopperModule.processJSON(Database, MyJSON)
print("Unit Test : Input JSON processed")

# the function must return a list with one unique top element 'A'
if TopLevelKeys != ['$$_A-1']:
    print("top level key is unexpected, should be $$_A-1")

# check the instance number
if Database.LastInstanceIndex('A') != 1 :
    print("A last index is unexpected : ")
    print(Database.LastInstanceIndex('A'))

if Database.LastInstanceIndex('B') != 2 :
    print("B last index is unexpected : ")
    print(Database.LastInstanceIndex('B'))

if Database.LastInstanceIndex('C') != 1 :
    print("C last is unexpected")

if Database.LastInstanceIndex('X') != 1 :
    print("X last is unexpected : ")

if Database.LastInstanceIndex('D') != 1 :
    print("D last is unexpected : ")

if Database.LastInstanceIndex('Z') != 1 :
    print("Z last is unexpected : ")


if not Database.DateOfElement('X-1:Z-1') :
    print("X-1:Z-1 is not present")

if not Database.DateOfElement('B-1:X-1') :
    print("B-1:X-1 is not present")

if not Database.DateOfElement('B-2:C-1') :
    print("B-2:C-1 is not present")

if not Database.DateOfElement('B-2:D-1') :
    print("B-2:D-1 is not present")

if not Database.DateOfElement('B-2:B-1') :
    print("B-2:B-1 is not present")

if not Database.DateOfElement('A-1:B-2') :
    print("A-1:B-2 is not present")

fB2 = Database.LinkedToElements("B-2")
fB2.symmetric_difference_update(('C-1', 'B-1', 'D-1'))
if len(fB2) != 0 :
    print("unexpected element B-2 points to:" + str(fB2))

sB2 = Database.LinkedFromElements('B-2')
if sB2 != {'A-1'}:
    print("unexpected or missing element pointing to B-2 : " + str(sB2))

#------------------------------------------------------------------------

print(" +++ Unit Test of node search +++")

# test tree finding function with depth 1
TestTopNode = "A-1"
TestDepth = 1
TestNodeToBypass = ""
TestResultJSON = ChopperModule.ReadTreeFromBase(Database, TestTopNode, TestDepth, TestNodeToBypass)
if TestResultJSON != {"A-1":["B-2"]}:
    print("result for node A-1 with depth 1 is unexpected")

# test tree finding function with depth 2
TestTopNode = "A-1"
TestDepth = 2
#TestNodeToBypass stays null
TestResultJSON = ChopperModule.ReadTreeFromBase(Database,TestTopNode, TestDepth, TestNodeToBypass)
TestResultJSON['A-1'][0]['B-2'].sort()
if TestResultJSON != {"A-1": [{ "B-2": ["B-1","C-1","D-1"]}]}:
    print("result for node A-1 with depth 2 is unexpected")
    print(TestResultJSON)

# test tree finding function with depth 3
TestTopNode = "A-1"
TestDepth = 3
# TestNodeToBypass is null
TestResultJSON = ChopperModule.ReadTreeFromBase(Database,TestTopNode, TestDepth, TestNodeToBypass)
ExpectedResult = {'A-1': [{'B-2': ['D-1', 'C-1', {'B-1': ['X-1']}]}]}
if not ChopperModule.my_obj_cmp(ExpectedResult, TestResultJSON):
    print("result for node A with depth 3 is unexpected")
    print(TestResultJSON)

# test tree finding function with depth 3 and 1 node to avoid
TestTopNode = "A-1"
TestDepth = 3
TestNodesToBypass = {'B-2'}
TestResultJSON = ChopperModule.ReadTreeFromBase(Database,TestTopNode, TestDepth, TestNodesToBypass)
ExpectedResult = {'A-1':['D-1', 'C-1', {'B-1':[{'X-1':['Z-1']}]}]}
if not ChopperModule.my_obj_cmp(ExpectedResult, TestResultJSON):
    print("result for node A with depth 3 and 'B-2' to bypass is unexpected")
    print(TestResultJSON)

# test tree finding function with depth 3 and 2 node to avoid
TestTopNode = "A-1"
TestDepth = 3
TestNodesToBypass = {'B-2','C-1'}
TestResultJSON = ChopperModule.ReadTreeFromBase(Database,TestTopNode, TestDepth, TestNodesToBypass)
ExpectedResult = {'A-1':['D-1',{'B-1':[{'X-1':['Z-1']}]}]}
if not ChopperModule.my_obj_cmp(ExpectedResult, TestResultJSON):
    print("result for node A with depth 3 and 'B-2' and 'C-1' to bypass is unexpected")
    print(TestResultJSON)

# test removal of UID suffix
TestResultJSON = {'A-1': [{'B-1': [{'X-1': ['Z-1']}]}, 'D-1']}
ResultWithoutUID = ChopperModule.RemoveTreeUIDSuffix(TestResultJSON)
if not ChopperModule.my_obj_cmp(ResultWithoutUID, {'A': [{'B': [{'X': ['Z']}]}, 'D']} ):
    print('removal UID suffix failed')



# test reading of multiple trees
TestTopNode = "B"
TestDepth = 1
TestNodesToBypass = {}
TestResultJSON = ChopperModule.ReadAllTreesFromBase(Database,TestTopNode, TestDepth, TestNodesToBypass)
ExpectedResult = [{'B-1': ['X-1']}, {'B-2': ['C-1', 'B-1', 'D-1']}]
if not ChopperModule.my_obj_cmp(TestResultJSON, ExpectedResult):
    print ('error in ReadAllTreesFromBase')


#ResultFileName = "TestSearchResult.json"
#f = open(ResultFileName, "w")
#f.write(str(TestResultJSON))
#f.close()

