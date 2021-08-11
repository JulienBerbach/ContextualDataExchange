import DatabaseInterface
import redis

# create python object for redis database
# database has to be started separately with command ./redis-server in src directory
#r = redis.Redis(host='localhost', port=6379, db=0)

# create a database object with ID 0
Database = DatabaseInterface.connection(dbID = 0)

print(" +++ Unit Test of ProcessFoundTuples +++")
# this program is to test the loading of Redis database with some tuples examples

# flush to start with an empty database
Database.FlushDB()

# load data for process found tuples test
# and check element existence

Tuple1 = { 'A' : [ 'B' ,'C', 'D']}
ReturnedTuple1 = Database.ProcessFoundTuples(Tuple1)
if ReturnedTuple1 != { '$$_A-1' : [ '$$_B-1' ,'$$_C-1', '$$_D-1']} :
    print('ProcessFoundTuples returns : ' + str(ReturnedTuple1))
A1 = Database.db.hget("A-1", "last")
if A1.decode('UTF-8') != '1' :
    print("A-1 last is unexpected : ")
    print(A1)
B1 = Database.db.hget("B-1", "last")
if B1.decode('UTF-8') != "1" :
    print("B-1 last is unexpected : ")
    print(B1.decode('UTF-8'))
C1 = Database.db.hget("C-1", "last")
if C1.decode('UTF-8') != '1' :
    print("C-1 last is unexpected")
D1 = Database.db.hget("D-1", "last")
if D1.decode('UTF-8') != '1' :
    print("D-1 last is unexpected : ")
    print(D1.decode('UTF-8'))

Tuple2 = { 'A' : [ 'B' ,'$$_C-1', 'D']}
ReturnedTuple2 = Database.ProcessFoundTuples(Tuple2)
if ReturnedTuple2 != { '$$_A-2' : [ '$$_B-2' ,'$$_C-1', '$$_D-2']} :
    print('ProcessFoundTuples returns : ' + str(ReturnedTuple2))
A1 = Database.db.hget("A-1", "last")
if A1.decode('UTF-8') != '2' :
    print("A-1 last is unexpected : ")
    print(A1)
B1 = Database.db.hget("B-1", "last")
if B1.decode('UTF-8') != "2" :
    print("B-1 last is unexpected : ")
    print(B1.decode('UTF-8'))
C1 = Database.db.hget("C-1", "last")
if C1.decode('UTF-8') != '1' :
    print("C-1 last is unexpected")
D1 = Database.db.hget("D-1", "last")
if D1.decode('UTF-8') != '2' :
    print("D-1 last is unexpected : ")
    print(D1.decode('UTF-8'))

Tuple3 = { '$$_A-1' : [ 'B' ,'$$_C-1', 'D']}
ReturnedTuple3 = Database.ProcessFoundTuples(Tuple3)
if ReturnedTuple3 != { '$$_A-1' : [ '$$_B-3' ,'$$_C-1', '$$_D-3']} :
    print('ProcessFoundTuples returns : ' + str(ReturnedTuple3))
A1 = Database.db.hget("A-1", "last")
if A1.decode('UTF-8') != '2' :
    print("A-1 last is unexpected : ")
    print(A1)
B1 = Database.db.hget("B-1", "last")
if B1.decode('UTF-8') != "3" :
    print("B-1 last is unexpected : ")
    print(B1.decode('UTF-8'))
C1 = Database.db.hget("C-1", "last")
if C1.decode('UTF-8') != '1' :
    print("C-1 last is unexpected")
D1 = Database.db.hget("D-1", "last")
if D1.decode('UTF-8') != '3' :
    print("D-1 last is unexpected : ")
    print(D1.decode('UTF-8'))

# check sets of link existence

F_A_1 = Database.db.smembers('f.A-1')
ExpectedResult = {b'D-3', b'B-1', b'D-1', b'C-1', b'B-3'}
if F_A_1 != ExpectedResult :
    print("f.A-1 is unexpected : " + str(F_A_1))

S_C_1 = Database.db.smembers('s.C-1')
ExpectedResult = {b'A-2', b'A-1'}
if S_C_1 != ExpectedResult :
    print("s.C-1 is unexpected : " + str(S_C_1))

# check link entities existence
AB = Database.db.hget("A-1:B-1", "date")
if not AB :
    print("A-1:B-1 not existing")

AC = Database.db.hget("A-2:C-1", "date")
if not AC :
    print("A-2:C-1 not existing")

#---------------------------------------------------------------------
# check several elements addition
#---------------------------------------------------------------------

Tuple4 = { 'X' : [ 'W' ,'P', 'Q'], 'R':'S', 'K':'J' }
ReturnedTuple4 = Database.ProcessFoundTuples(Tuple4)
if ReturnedTuple4 != { '$$_X-1' : [ '$$_W-1' ,'$$_P-1', '$$_Q-1'], '$$_R-1':['$$_S-1'], '$$_K-1':['$$_J-1'] }:
    print('Tuple 4 Error, ProcessFoundTuples returns : ' + str(ReturnedTuple4))

X1 = Database.db.hget("X-1", "last")
if X1.decode('UTF-8') != '1' :
    print("X-1 last is unexpected : ")
    print(X1)
