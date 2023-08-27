import re
from constants import floors, frosh

def formatFrosh(indir, toptionalFloors, femFloors, catFloors,rooms):
    froshObjects = []
    f = open(indir) 
    froshList = [line.split('\t') for line in f.readlines()[1:]]
    for line in froshList:
        line = [True if i == "Yes" else False if i == "No" else i for i in line]
        name, kerb, phone, gender, roomateGender, noFemFloor, catAllergy, toptional, desiredRoomate = line[1:10] ###### Change this line if form changes #######
        kerb, desiredRoomate = kerb.lower(), desiredRoomate.lower()
        roomateGender = roomateGender.split(", ")
        wantedRooms = ",".join(line[10:(10+len(rooms))])
        wantedRooms = re.sub(r'([2-9][1-9]2)', r'\g<1>a,\g<1>b', wantedRooms).split(",") #used [2-9] bc 112 is wierd
        bannedRooms = (toptionalFloors if not(toptional) else []) + (femFloors if (noFemFloor or (gender=="Male")) else []) + (catFloors if catAllergy else [])
        gender = "m" if gender=="Male" else "f" if gender=="Female" else "x" 
        roomateGender = ("m" if "Male" in roomateGender else "")+("f" if "Female" in roomateGender else "")+("x" if "Non-binary" in roomateGender else "")
        froshObjects.append(frosh(kerb,wantedRooms,bannedRooms,gender,roomateGender,desiredRoomate))
    for extra in range(1,len(rooms)+1-len(froshObjects)):
        froshObjects.append(frosh("jarthur", [], [], "x", "mfx"))
    
    froshDict = {}
    for f in froshObjects:
        froshDict[f.kerb] = f
        
    return(froshObjects, froshDict)

def formatOut(dict, priority, w, rooms):
    out=""
    currentRoomDict = {floorName: (set(floorRooms) & set(rooms)) for floorName, floorRooms in zip(floors.keys(),floors.values())}
    for floorName, floorRooms in currentRoomDict.items():
        out+=floorName+"\n"
        for room in floorRooms:
            out+=room+"\t"+dict[room][0]+"\t"+str(+dict[room][1])+"\n"
    out+= "priority:\n"+"\n".join(["\t".join(map(str,frosh)) for frosh in priority])
    return(out, w)
    