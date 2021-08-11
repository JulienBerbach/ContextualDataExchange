import DatabaseInterface
import redis

# test of the function InstancesOfNode from module DatabaseInterface
#######################################################################

# create python object for redis database
# database has to be started separately with command ./redis-server in src directory
#r = redis.Redis(host='localhost', port=6379, db=0)

# create a database object with ID 0
Database = DatabaseInterface.connection(dbID = 0)

print(" +++ Unit Test of InstancesofNode +++")
# this program is to test the loading of Redis database with some tuples examples

# flush to start with an empty database
Database.FlushDB()

# load data for process found tuples test

Tuple1 = { 'A' : [ 'B' ,'C', 'D']}
ReturnedTuple1 = Database.ProcessFoundTuples(Tuple1)
Tuple2 = { 'A' : [ 'B' ,'$$_C-1', 'D']}
ReturnedTuple2 = Database.ProcessFoundTuples(Tuple2)
Tuple3 = { '$$_A-1' : [ 'B' ,'$$_C-1', 'D']}
ReturnedTuple3 = Database.ProcessFoundTuples(Tuple3)

ResultA = Database.InstancesOfNode('A')
ResultD = Database.InstancesOfNode('D')

# A has to have 2 instances, D has to have 3 instances
if ResultA != ('A-1', 'A-2'):
    print ("InstancesOfNode returns : " + str(ResultA))

if ResultD != ('D-1', 'D-2', 'D-3'):
    print ("InstancesOfNode returns : " + str(ResultD))  




