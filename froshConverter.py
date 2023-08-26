import re
indir = input("Input file directory:")
outdir = input("Output file directory:")

f = open(indir)

loop = "211, 212a, 212b, 213, 214, 221, 222a, 222b, 223, 224, 225A, 225".split(", ")
clam = "311, 312a, 312b, 313, 314, 315A, 315, 321, 322a, 322b, 323, 324, 325A, 325".split(", ")
pecker = "431, 432a, 432b, 433, 434, 435A, 435, 441, 442a, 442b, 443, 444".split(", ")
blackhole = "231, 232a, 232b, 233, 234, 235A, 235, 241, 242a, 242b, 243, 244, 245A, 245".split(", ")

toptionalRooms = clam+pecker+blackhole
catRooms = loop+blackhole

froshList = [line.split('\t') for line in f.readlines()]
for line in froshList:
    line = [True if i == "Yes" else False if i == "No" else i for i in line]
    name, kerb, phone, gender, roomateGender, noFemFloor, catAllergy, toptional, desiredRoomate = line[1:11]
    roomateGender = roomateGender.split(", ")
    wantedRooms = "\""+"\",\"".join(line[12:26])+"\""
    wantedRooms = re.sub(r'"([2-9][1-9]2)"', r'"\g<1>a","\g<1>b"', wantedRooms) #used [2-9] bc 112 is wierd
    bannedRooms = (toptionalRooms if not(toptional) else []) + (loop if (noFemFloor or (gender=="Male")) else []) + (catRooms if catAllergy else [])
    bannedRooms = ("\""+", ".join(bannedRooms)+"\"") if (len(bannedRooms)>0) else ""
    gender = "m" if gender=="Male" else "f" if gender=="Female" else "x" 
    roomateGender = ("m" if "Male" in roomateGender else "")+("f" if "Female" in roomateGender else "")+("x" if "Nonbinary" in roomateGender else "")
    print(noFemFloor)
    with open(outdir, "a") as out:
        frosh = ("frosh(\""+kerb+"\",["+wantedRooms+"], ["+bannedRooms+"],\""+gender+"\",\""+roomateGender+"\""+((",\""+desiredRoomate+"\"") if not(desiredRoomate=="") else "")+")")
        print(frosh)
        out.write(frosh+",\n")