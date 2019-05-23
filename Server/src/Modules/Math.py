def Add(vars, a, b):
    return a+b

def IAdd(vars, a, b):
    return Add(vars, b, a)

def IAddS(vars, a, b):
    return f"'{IAdd(vars, a, b)}'"

def Sub(vars, a, b):
    return a-b

def ISub(vars, a, b):
    return Sub(vars, b, a)

def Mul(vars, a, b):
    return a * b

def Pow(vars, a, b):
    return a ** b

def IPow(vars, a, b):
    return Pow(vars, b, a)

def Div(vars, a, b):
    return a / b

def IDiv(vars, a, b):
    return Div(vars, b, a)

def Len(vars, item):
    return f"'{len(item)}''"
