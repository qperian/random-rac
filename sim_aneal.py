from random import choice
import random
from reformat import *
from constants import floors, frosh, ROOMS, indir, toptionalFloors, catFloors, femFloors



froshL, froshDict = formatFrosh(indir, toptionalFloors,femFloors,catFloors, ROOMS)

#curry : func (a, b -> c), a -> func(b -> c)
def curry(f, x):
    return (lambda y : f(x,y))
        
#getWeight : list frosh, func (list frosh, frosh -> number) -> number
# gets the total weight given a function of the weight of each frosh in the current config
def getWeight(l, f):
    return sum(map(curry(f, l), l))

#getTemp : Int, Int -> [0,1] // idealy (0,100)->1, (100,100)-> 0
def getTemp(t, T):
    return max( (T-(6/5 * t)) / T, 0)

#anneal : List Frosh, func (frosh -> number), Int -> List Frosh for
# now, say that we have firm restriction of putting people in banned
# rooms, but soft restriction (i.e. weight penalties) for putting
# people with "incompatable" gendered roommates, since otherwise our
# program won't be able to solve a MM and FF pairs that make good
# roommates but should be in opposite rooms
def anneal(l, f, N):
    currWeight = getWeight(l, f)
    bestWeight = currWeight
    L = []
    for i in range(N):
        temp = getTemp(i, N)
        #print(i, currWeight, bestWeight, temp)
        a, b = (choice(l), choice(l))
        if not(a.room in b.bannedRooms or b.room in a.bannedRooms):
            a.room, b.room = b.room, a.room
            if (currWeight > getWeight(l, f) or (random.uniform(0,1) < temp)):
                currWeight = getWeight(l, f)
                L.append(currWeight)
                if currWeight < bestWeight:
                    bestWeight = currWeight
            else:
                a.room, b.room = b.room, a.room #swap back
    
    assignments = []
    for x in l:
        assignments.append((x.kerb, x.room, x.prefrences_index()))
    return assignments

#method 1: plain old least squares; note it counts ranking a double as 1 slots, 0-indexed ; roommate of "bad" gender counts as 50 extra weight ; desired Roommate drops weight by 5 (should fine tune)
def leastSquares(l, student):
    w = 0
    if student.room in student.bannedRooms:
        return 100000 #break
    if findRoommate(l, student).gender not in student.genderRoommate:
        w += 20
    if findRoommate(l, student).kerb == student.desiredRoommate:
        w -= 10
    w += findRoomPosn(student) ** 2 # try making it hurt these rooms even more
    return w

def findRoomPosn(s):
    n = 0
    twoRooms = set()
    for r in s.prefrences:
        if r == s.room:
            return n
        elif r[2] == "2" and r != "112":
            if s.room == (r[0:3] + diffLetter(r[3])):
                return n
            if r[0:3] not in twoRooms:
                n += 1
                twoRooms.add(r[0:3])
        else:
            n += 1
    return n

def findRoomPosnII(s, R):
    n = 0
    twoRooms = set()
    for r in s.prefrences:
        if r == R:
            return n
        elif r[2] == "2":
            if r[0:3] not in twoRooms:
                n += 1
                twoRooms.add(r[0:3])
        else:
            n += 1
    return n

#jarthur ( a great roommate ) is assumed if no one is given this code
#does depend on room names being "xx[1-5]" with "xx2a" and "xx2b"
#variations -- potentially special case around 5 rooms?
def findRoommate(l, student):
    if student.room[2] != "2" or student.room == "112": #112 is weird
        return frosh("jarthur", [], [], student.gender, "mfx")
    else:
        #print(student.room)
        soughtRoom = student.room[0:3] + diffLetter(student.room[3])
        for f in l:
            if f.room == soughtRoom:
                return f
        return frosh("jarthur", [], [], student.gender, "mfx")

def diffLetter(s):
    if s == "a":
        return "b"
    else:
        return "a"
            
def assignRooms(l, f, T):
    usedRooms = []
    for student in l: #randomly assign rooms -- note! can put people in illegal rooms
        x = choice(listMinus(ROOMS, usedRooms))
        student.room = x
        usedRooms.append(x)
    return anneal(l, f, T)

def listMinus(l1, l2):
    toRet = []
    for i in l1:
        if i not in l2:
            toRet.append(i)
    return toRet

def runAssign():
    res, w = assignRooms(froshL, leastSquares, 40000), getWeight(froshL, leastSquares)
    roomDict = {}
    
    for f in res:
        roomDict[f[1]]=(f[0],f[2])
    priority = sorted(res, key = lambda row: (row[2], random.uniform(1,10)))
    return(roomDict, priority, w)


res, w = formatOut(*runAssign(), ROOMS)
with open("out1_"+str(w)+".tsv", "a") as out:
    out.write(res)

res, w = formatOut(*runAssign(), ROOMS)
with open("out2_"+str(w)+".tsv", "a") as out:
    out.write(res)

res, w = formatOut(*runAssign(), ROOMS)
with open("out3_"+str(w)+".tsv", "a") as out:
    out.write(res)
