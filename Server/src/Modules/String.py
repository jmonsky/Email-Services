
def IAddS(vars, a, b):
    return f"'{b + a}'"

def LenS(vars, item):
    return f"'{len(item)}'"

def DoubleBS(vars, item):
    return f"'{item}'".replace("\\", "\\\\")