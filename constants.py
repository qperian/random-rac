floors = {
    "foo":['144', '145A', '145'], 
    "destiny":["112", "112A", "113", "114", "115A", "115", "123", "124", "125A", "125"], 
    "blackhole":['231', '232a', '232b', '233', '234', '235A', '235', '241', '242a', '242b', '243', '244', '245A', '245'], 
    "loop":['211', '212a', '212b', '213', '214', '221', '222a', '222b', '223', '224', '225A', '225'], 
    "bmf":['331', '332a', '332b', '333', '334', '335A', '335', '341', '342a', '342b', '343', '344', '345A', '345'], 
    "clam":['311', '312a', '312b', '313', '314', '315A', '315', '321', '322a', '322b', '323', '324', '325A', '325'], 
    "pecker":['431', '4 32a', '432b', '433', '434', '435A', '435', '441', '442a', '442b', '443', '444'], 
    "bonfire":['411', '412a', '412b', '413', '414', '415A', '415', '421', '422a', '422b', '423', '424', '425A', '425']
}

#ROOMS: list of all the open rooms
ROOMS = [ 
    #FILL WITH ROOMS -- ROOMS ARE STRING
    "115","125","145","145A","212a","212b","222a","222b","232a","232b","242b","312a","312b","322a","322b","325","342b","332a","332b","422a","422b","412a","412b","432a","432b", "431"
]

#path to input tsv
indir = "" ####CHANGE#####

toptionalFloors = floors["clam"]+floors["pecker"]+floors["blackhole"]
catFloors = floors["loop"]+floors["blackhole"]
femFloors = floors["loop"]

pullIns = [] #### Add rooms taken via pull in process here #####

ROOMS = [rm for rm in ROOMS if rm not in pullIns]


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
    

  