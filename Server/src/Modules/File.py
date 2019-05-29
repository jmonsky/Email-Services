import base64
import os
from os.path import isfile, join

def Join(vars, path1, path2):
    return join(path1, path2)

def JoinPaths(vars, path1, path2):
    return join(path1, path2)

def GetPath(vars):
    return f"'{os.getcwd()}'"

def SPath(vars):
    return f"'%% Path - {os.getcwd()}'".replace("\\", "\\\\")

def Path(vars):
    return GetPath(vars)

def Navigate(vars, path):
    os.chdir(path)
    return path

def CD(vars, path):
    return Navigate(vars, path)

def RelNavigate(vars, path):
    os.chdir(join(os.getcwd(), path))
    return join(os.getcwd(), path)

def MakeDirectory(vars, name):
    os.mkdir(name)
    return name

def NewDir(vars, name):
    return MakeDirectory(vars, name)

def MakeDir(vars, name):
    return MakeDirectory(vars, name)

def RN(vars, path):
    return RelNavigate(vars, path)

def RawDir(vars):
    return os.listdir()

def DirBody(vars):
    direct = RawDir(vars)
    files = [f for f in direct if isfile(f)]
    directories = [f for f in direct if not isfile(f)]
    for file in files:
        vars["BODY"] += f"%% File - {file}\n"
    for dir in directories:
        vars["BODY"] += f"%% Dir - {dir}\n"

def Directory(vars):
    direct = RawDir(vars)
    files = [f for f in direct if isfile(f)]
    directories = [f for f in direct if not isfile(f)]
    return f"'Files:{files} Directories:{directories}'"

def GetFiles(vars):
    direct = RawDir(vars)
    files = [f for f in direct if isfile(f)]
    return files

def GetDirectories(vars):
    direct = RawDir(vars)
    directories = [f for f in direct if not isfile(f)]
    return directories

def Dir(vars):
    return Directory(vars)

def LS(vars):
    return Directory(vars)

def Rename(vars, old, new):
    os.rename(old, new)
    return new

def RemoveFile(vars, file):
    os.remove(file)
    return file

def RM(vars, file):
    return RemoveFile(vars, file)

def RemoveDirectory(vars, dir):
    os.rmdir(dir)
    return dir

def RmDir(vars, dir):
    return RemoveDirectory(vars, dir)

def Serialize(vars, filename):
    with open(filename, "rb") as file:
        byteList = file.read()
        #intList = [int(byte) for byte in byteList]
        return str(base64.standard_b64encode(byteList))[2:-1]
    return "'Serialization Failed'"

def StandardSerialize(vars, fname):
    return f"'%% Attachment - {fname} - {Serialize(vars, fname)}'"

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
    fname = codes[1][2:].strip(" ")
    if type(newFname) == str:
        fname = newFname
    print(newFname)
    sList = codes[2]
    print(sList)
    return DeSerialize(vars, fname, sList)

def SDS(vars, line, nFname = None):
    return StandardDeSerialize(vars, line, nFname)

def ReadTextFile(vars, filename):
    with open(filename, "r") as file:
        for line in file.readlines():
            Body(vars, line)

if __name__ == "__main__":
    print(SPath(None))