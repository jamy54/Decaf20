class SymbolTable():
    def __init__(self):
        self.globals =[]
        self.globalDict = {}
        self.locals = []
        self.localDict = {}
        self.methods = []
        self.methodDict = {}

    def addSymbol(self,type,name,isGlobal,isParameter,funcName):
        s = Symbol(type,name,isGlobal,isParameter,funcName)
        if(s.IsGlobal):
            self.globals.append(s)
            self.globalDict[s.name+s.FuncName] = s
        else:
            self.locals.append(s)
            self.localDict[s.name+s.FuncName] = s

    def addMethodSymbol(self,type,name,formals):
        m = Method(type, name,formals)
        self.methods.append(m)
        self.methodDict[m.name] = m

    def getSymbol(self,name,methodName):
        res = self.globalDict.get(name+methodName)
        if res is None:
            res = self.localDict.get(name + methodName)
        if methodName == 'main' and res is None:
            res = self.globalDict.get(name)
            if res is None:
                res = self.localDict.get(name)
        return res

    def getMethodSymbol(self,name):
        return self.methodDict.get(name)

    def hasMainMethod(self):
        for m in self.methods:
            if m.name.lower() == "main":
                return True
        return False

    def getAllocatedRegister(self,name, methodName):
        return self.getSymbol(name, methodName).allocatedRegister

    def setAllocatedRegister(self,name, methodName,registerName):
        symbl = self.getSymbol(name,methodName)
        symbl.allocatedRegister = registerName

        if not methodName == 'main':
            self.globalDict[name+methodName] = symbl
        else:
            self.localDict[name] = symbl


class Symbol:
    def __init__(self,type,name,isGlobal,isParameter,funcName):
        self.name = name
        self.type = type
        self.IsGlobal = isGlobal
        self.IsParameter = isParameter
        self.FuncName = funcName
        self.allocatedRegister = ""

class Method:
    def __init__(self,type,name,formals):
        self.name = name
        self.type = type
        self.formals = formals