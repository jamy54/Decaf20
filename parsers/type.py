import parsers.message as m

class Type:
    def __init__(self,tok,isvoidallowed=False):
        if not isvoidallowed:
            self.allowedType = ["int","double","bool","string"]
        else:
            self.allowedType = ["int", "double", "bool", "string","void"]
        self.isint = tok.value == self.allowedType[0]
        self.isdouble = tok.value == self.allowedType[1]
        self.isbool = tok.value == self.allowedType[2]
        self.isstring = tok.value == self.allowedType[3]
        self.token = tok
        self.type = tok.value
        if tok.value not in self.allowedType:
            raise Exception(m.SyntaxErr,tok)