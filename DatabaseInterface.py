# interface facade for redis
# in Redis key, value, key:value will be entities: A, B for single element, or A:B for a tuple
# entities will be modeled as hashes
# information about what are the tuples keys in Redis will be in sets, under the name f:A for when A is first
# or s.A for all the keys where A is second

import redis
import time

class connection:

    def __init__(self, dbID):
        # create python object for redis database
        # in Redis, object can be created with dbID from 0 to 20
        # database has to be started separately with command ./redis-server in src directory
        self.db = redis.Redis(host='localhost', port=6379, db=dbID)

    # erases the full database
    def FlushDB(self):
        self.db.flushdb()

    def ElementExists(self, elementUID):
        return self.db.hexists(elementUID, 'date')

    def GenericKeyElementExists(self, element):
        return self.db.hexists(element + '-1', 'date')

    # get the highest index of an instance or the element (= the last one created)
    # the input is the GENERIC element
    # the returned index is an integer
    def LastInstanceIndex(self, element):
        Index = self.db.hget(element + '-1', "last")
        return int(Index.decode('UTF-8'))

    # input is the unique identifier of the instance
    def DateOfElement(self, elementUID):
        return  self.db.hget(elementUID, "date")

    # input is the unique identifier of the instance
    # returns the set of element where this element is linked to : element -> ?
    def LinkedToElements(self, elementUID):
        bytes_f = self.db.smembers("f." + elementUID)
        fB2 = set()
        for i in bytes_f:
            fB2.add(i.decode('UTF-8'))
        return fB2

    # input is the unique identifier of the instance
    # returns the set of element that point to this element : ? -> element
    def LinkedFromElements(self, elementUID):
        bytes_s = self.db.smembers("s." + elementUID)
        sB2 = set()
        for i in bytes_s:
            sB2.add(i.decode('UTF-8'))
        return sB2

    # this functions adds an entity in a hash table if it is not existing yet
    # expected element is a string 'A'
    # it returns the instance number
    def AddFoundKey(self, SimpleElement):

        # check if this element "A" already exists in the database
        # the first element to be existing is "A-1", it contains the field "last" which is the number of the
        # last created
        newElementFirst = SimpleElement + '-1'
        CurrentTime = time.time()

        if self.db.hexists(newElementFirst, 'date'):
            #retrive the index of the last of these
            lastIndex = int(self.db.hget(newElementFirst, 'last'))
            # increment the index and create a new element A-2 with this index
            lastIndex = lastIndex + 1
            newElement = SimpleElement + '-' + str(lastIndex)
            self.db.hset(newElement, 'date', CurrentTime)
            # increment the "last" field of "A-1"
            self.db.hincrby(newElementFirst, 'last', 1)
            return lastIndex
        else:
            # create the new element "A-1", index 'last' = 1
            self.db.hset(newElementFirst, 'date', CurrentTime)
            self.db.hset(newElementFirst, 'last', 1)
            return 1

    # this function adds the list of keys, values and couples key:value to the entitiy list,
    # and the tuple to the tuple list (one hash table for all)
    # only if not existing yet
    # inputs must be 1 or several simple elements like this: {'A': ['B', 'C','D'] }
    # - no nesting
    # - if B is not a string (hence probably a number), it is not added to entity list
    # - if an element has the prefix "$$_", the suffix is treated as an already existing
    # database element
    #
    # the function returns an analogous dictionary with the tuple names given in the database
    # the indication that these are database names is given by prefix $$_
    # Example { '$$_A-1' : ['$$_B-1', '$$_C-2', '$$_D-1']}
    # this is done in order for the caller to repeat the same element in a further call

    def ProcessFoundTuples(self, SimpleTuples):

        PrefixForUID = '$$_'
        #print('ProcessFoundTuples - Simple Tuples : ' + str(SimpleTuples))
        CurrentTime = time.time()
        returnedDict = dict()


        # loop on the keys
        counter = 0
        for i in SimpleTuples:

            # list for returned B elements
            returnedList = list()
            # add key 'A' to entity list, provided it's not a unique database name
            if str(i)[0:3] != PrefixForUID:
                # add element to database and get the instance number
                AIndex = self.AddFoundKey(i)
                # preparation for f.A
                FirstName = str(i) + '-' + str(AIndex)
                # preparation of the output of this function
                A_UID = '$$_' + FirstName
            else:
                # remove the prefix for f.A preparation
                FirstName = i[3:]
                # the same is returned as output
                A_UID = i

            #print('ProcessFoundTuples element: ' + str(i))

            # add values 'B' to entity list only in case it is a string
            # and it is not a UID
            for y in SimpleTuples[i]:
                if type(y) is str:
                    if y[0:3] != PrefixForUID:
                        Bindex = self.AddFoundKey(y)
                        SecondName = y + '-' + str(Bindex)
                        B_UID = '$$_' + SecondName
                    else:
                        # remove the UID prefix in the seconde name
                        SecondName = y[3:]
                        B_UID = y
                else:
                    SecondName = str(y)
                    B_UID = y

                #print('ProcessFoundTuples element: ' + str(y))

                # add 'f.A' in index map
                # check if the UID prefix is used
                FFirstName = 'f.' + FirstName
                self.db.sadd(FFirstName, SecondName)

                # add 's.B' in index map if B is a string, hence an entitiy
                if type(y) is str:
                    SSecondName = 's.' + SecondName
                    self.db.sadd(SSecondName, FirstName)

                # add tuple to tuple list
                TupleName = FirstName + ':' + SecondName
                if not self.db.hexists(TupleName, 'date'):
                    self.db.hset(TupleName, 'date', CurrentTime)

                returnedList.append(B_UID)

            returnedDict[A_UID] = returnedList

            counter = counter + 1

        return returnedDict


    # function that searches for linked to that node
    # the returned value is a set
    def LinkedNodes(self, Node):
        Response = {}
        if self.db.hexists(Node, 'date'):
            F_A = "f." + Node
            ResponseBytes = self.db.smembers(F_A)
            Response = set()
            for i in ResponseBytes:
                Response.add(i.decode('UTF-8'))
        return Response

    # function that returns the UIDs of all instances of a node in a set
    # the node designation is the generic one, not the unique one
    # the input node is a string
    def InstancesOfNode(self, Node):
        Response = {}
        if self.GenericKeyElementExists(Node):
            Response = set()
            for i in range(self.LastInstanceIndex(Node)):
                Response.add(Node + '-' + str(i + 1))
        return Response