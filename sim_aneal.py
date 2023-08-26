from random import choice
import random


#frosh
class frosh:
    def __init__(self, kerb, roomWants, bannedRooms, gender, genderRoommate, desiredRoommate=""):
        self.prefrences = roomWants #list string
        self.bannedRooms = bannedRooms #list string
        self.kerb = kerb #string
        self.room = "0" #string
        self.desiredRoommate = desiredRoommate #string
        self.gender = gender #char
        self.genderRoommate = genderRoommate #string
    def prefrences_index(self):
        if self.kerb == "jarthur":
            return 0
        return self.prefrences.index(self.room)


froshL = [
    #FILL WITH FROSH
    #A FROSH LOOKS LIKE:
    # frosh("kerb", ["list", "of", "rooms"], ["list", "of", "rooms"], 'g', "mfx", "optional_kerb"), where 'g' is one of 'm','f','x'
    # Backfill with the "jarthur" frosh s.t. the # of frosh = the # of rooms
    frosh("a", ["103", "102a", "102b", "101"], [], 'm', 'mfx'),
    frosh("b", ["101", "102a", "102b", "103"], [], 'f', 'mfx'),
    frosh("c", ["103", "101"], ["102a", "102b"], 'm', 'm'),
    frosh("d", ["102a", "102b", "103", "101"], [], 'f', 'mfx')
]

froshDict = {}
for f in froshL:
    froshDict[f.kerb] = f


    
#ROOMS: list of all the open rooms
ROOMS = [
    #FILL WITH ROOMS -- ROOMS ARE STRING
    "125","145","212a","212b","222a","222b","145A","232a","232b","242a","242b","312a","312b","322a","322b","342a","342b","332a","332b","422a","422b","412a","412b","432a","432b"
]

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
                     
    
print(assignRooms(froshL, leastSquares, 40000), getWeight(froshL, leastSquares))
print(assignRooms(froshL, leastSquares, 40000), getWeight(froshL, leastSquares))
print(assignRooms(froshL, leastSquares, 40000), getWeight(froshL, leastSquares))