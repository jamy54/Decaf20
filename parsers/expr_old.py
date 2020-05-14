from parsers.lvalue import FieldAccess
from parsers.program import Basic
from parsers.constants import Consant
from parsers.caller import Caller
import parsers.message as m

operatorList = ["=","+","-","*","/","%","<","<=",">",">=","==","!=","&&","||","!"]


def check_if_constant(tok):
    if tok.type.lower() == "T_IntConstant".lower() or tok.type.lower() == "T_BoolConstant".lower() or tok.type.lower() == "T_DoubleConstant".lower() or tok.type.lower() == "T_STRINGCONSTANT".lower():
        return True
    return False

class Expressions1(Basic):
    def __init__(self, tokens, tokenPosition):
        super().__init__(tokens, tokenPosition)
        self.operatorList = operatorList
        tok = tokens[tokenPosition]
        ntok = tokens[tokenPosition+1]
        nntok = tokens[tokenPosition + 2]
        if (tok.type.lower() == "T_Identifier".lower() or check_if_constant(tok)) and (ntok.value in self.operatorList):
            self.type= self.get_type(ntok)
            self.exp = Expr(tokens,tokenPosition)
            self.tokenPostionProcessed = self.exp.tokenPostionProcessed
        elif tok.type.lower() == "T_Identifier".lower() and (ntok.value == ";" or ntok.value == "," or ntok.value == ")"):
            self.type= "lvalue"
            self.lValue = FieldAccess(tokens, tokenPosition)
            self.tokenPostionProcessed = tokenPosition
        elif check_if_constant(tok) and ntok.value == ")":
            self.type= "constant"
            self.constant = Consant(tokens[tokenPosition])
            self.tokenPostionProcessed = tokenPosition
        #elif tok.type.lower() == "T_Identifier".lower() and ntok.value == "=" and (nntok.value.lower() == "ReadInteger".lower() or nntok.value.lower() == "ReadLine".lower()):
        elif tok.value.lower() == "ReadInteger".lower() or tok.value.lower() == "ReadLine".lower():
            self.type = tok.value.lower()
            if ntok.value == "(":
                if nntok.value == ")":
                    self.tokenPostionProcessed =tokenPosition + 2
                else:
                    raise Exception(m.SyntaxErr, nntok)
            else:
                raise Exception(m.SyntaxErr, ntok)
        elif tok.type.lower() == "T_Identifier".lower() and ntok.type.lower() == "(".lower():
            self.type= "caller"
            self.caller = Caller(tokens,tokenPosition)
            self.tokenPostionProcessed = self.caller.tokenPostionProcessed
        elif tok.value.lower() == "!".lower() and (ntok.type.lower() == "T_BoolConstant".lower() or ntok.type.lower() == "T_Identifier".lower()):
            self.type= "logicalexpression"
            self.exp = Expressions1(tokens, tokenPosition + 1)
            self.tokenPostionProcessed = tokenPosition+1
        else:
            raise Exception(m.SyntaxErr, tok)

    def get_type(self,tok):
        if tok.type.lower() == "=".lower():
            return "assignment"
        elif tok.type.lower() == "+".lower():
            return "addition"
        elif tok.type.lower() == "-".lower():
            return "subtraction"
        elif tok.type.lower() == "*".lower():
            return "multiply"
        elif tok.type.lower() == "/".lower():
            return "divide"
        elif tok.type.lower() == "%".lower():
            return "mod"
        elif tok.type.lower() == "<".lower():
            return "less"
        elif tok.type.lower() == "<=".lower():
            return "lessequal"
        elif tok.type.lower() == ">".lower():
            return "greater"
        elif tok.type.lower() == ">=".lower():
            return "greaterequal"
        elif tok.type.lower() == "==".lower():
            return "ifequal"
        elif tok.type.lower() == "!=".lower():
            return "noequal"
        elif tok.type.lower() == "&&".lower():
            return "and"
        elif tok.type.lower() == "||".lower():
            return "or"
        elif tok.type.lower() == "!".lower():
            return "not"



class Expr(Basic):
    def __init__(self, tokens, tokenPosition):
        super().__init__(tokens, tokenPosition)
        if check_if_constant(tokens[tokenPosition]):
            self.lvalue = Constants(tokens, tokenPosition)
        else:
            self.lvalue = FieldAccess(tokens, tokenPosition)
        self.operator = tokens[tokenPosition+1].value
        tok = tokens[tokenPosition + 2]
        ntok = tokens[tokenPosition + 3]
        if check_if_constant(tok) and (ntok.value not in operatorList):
            self.rValue = Constants(tokens, tokenPosition + 2)
            self.rType = "constant"
            self.tokenPostionProcessed = tokenPosition + 2
        elif tok.type.lower() == "T_Identifier".lower() and (ntok.value == ";" or ntok.value == ")"):
            self.rtype= "fieldaccess"
            self.rValue = FieldAccess(tokens, tokenPosition + 2)
            self.tokenPostionProcessed = tokenPosition +2
        elif tok.value != ")" and tok.value != ";":
            tokpos = tokenPosition + 2
            hasbracket = False
            incr = 0
            if tok.value == "(":
                tokpos +=1
                hasbracket = True
                incr = 1
            self.rType = "exp"
            self.rValue = Expressions1(tokens, tokpos)
            if hasbracket and self.tokens[self.rValue.tokenPostionProcessed + 1].value != ")":
                raise Exception(m.SyntaxErr, self.tokens[self.rValue.tokenPostionProcessed + 1])
            self.tokenPostionProcessed = self.rValue.tokenPostionProcessed + incr
        else:
            raise Exception(m.SyntaxErr, tok)



class ArithExpr(Basic):
    def __init__(self, tokens, tokenPosition):
        super().__init__(tokens, tokenPosition)
        if check_if_constant(tokens[tokenPosition]):
            self.lvalue = Constants(tokens, tokenPosition)
        else:
            self.lvalue = FieldAccess(tokens, tokenPosition)
        self.operator = tokens[tokenPosition+1].value
        tok = tokens[tokenPosition + 2]
        ntok = tokens[tokenPosition + 3]
        if check_if_constant(tok) and (ntok.value not in operatorList):
            self.constantvalue = tokens[tokenPosition + 2].value
            self.rType = "constant"
            self.tokenPostionProcessed = tokenPosition + 2
        elif tok.type.lower() == "T_Identifier".lower() and (ntok.value == ";" or ntok.value == ")"):
            self.rtype= "fieldaccess"
            self.rValue = FieldAccess(tokens, tokenPosition + 2)
            self.tokenPostionProcessed = tokenPosition +2
        elif tok.value != ")" and tok.value != ";":
            tokpos = tokenPosition + 2
            hasbracket = False
            incr = 0
            if tok.value == "(":
                tokpos +=1
                hasbracket = True
                incr = 1
            self.rType = "exp"
            self.exp = Expressions1(tokens, tokpos)
            if hasbracket and self.tokens[self.exp.tokenPostionProcessed + 1].value != ")":
                raise Exception(m.SyntaxErr, self.tokens[self.exp.tokenPostionProcessed + 1])
            self.tokenPostionProcessed = self.exp.tokenPostionProcessed + incr
        else:
            raise Exception(m.SyntaxErr, tok)

class Constants:
    def __init__(self,tokens,tokenPositon):
        self.type = "constant"
        self.value = tokens[tokenPositon + 2].value
