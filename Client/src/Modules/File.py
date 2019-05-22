import base64
def Serialize(vars, filename):
    with open(filename, "rb") as file:
        byteList = file.read()
        #intList = [int(byte) for byte in byteList]
        return str(base64.standard_b64encode(byteList))[2:-1]
    return "'Serialization Failed'"

def StandardSerialize(vars, fname):
    return f"'%% {fname} - {Serialize(vars, fname)}'"

def SS(vars, fname):
    return StandardSerialize(vars, fname)

def DeSerialize(vars, filename, serializedList):
    byteList = bytes(base64.standard_b64decode(serializedList))
    with open(filename, "wb") as file:
        file.write(byteList)
    return f"'{filename}'"

def StandardDeSerialize(vars, line, newFname = None):
    codes = line.split(" - ")
    print(len(codes))
    fname = codes[0][2:].strip(" ")
    if type(newFname) == str:
        fname = newFname
    print(newFname)
    sList = codes[1]
    print(sList)
    return DeSerialize(vars, fname, sList)

def SDS(vars, line, nFname = None):
    return StandardDeSerialize(vars, line, nFname)

def ReadTextFile(vars, filename):
    with open(filename, "r") as file:
        for line in file.readlines():
            Body(vars, line)

if False:
    import RDP
    RDP.SS(None)
    l = SS(None, "./monitor-1.png")
    print(l)
    print("REINCODING")
    SDS(None, l, "./newMonitor.png")
