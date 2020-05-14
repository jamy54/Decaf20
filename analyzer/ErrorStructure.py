
class Error:
    def __init__(self,message="",lN=0,SP=0,LP=0):
        self.Message = message
        self.StartPos = SP
        self.LastPos = LP
        self.length = LP-SP
        self.lineNumber = lN
        self.tokens = []

    def getLength(self):
        self.setLength()
        return  self.length

    def setLength(self):
        self.length = self.LastPos - self.StartPos