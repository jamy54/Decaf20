from parsers.lvalue import FieldAccess
from parsers.program import Basic
from parsers.constants import Consant
from parsers.caller import Caller
import parsers.message as m
import copy

operatorList = ["=","+","-","*","/","%","<","<=",">",">=","==","!=","&&","||","!"]
arithoperator = ["+","-","*","/","%"]
logicaloperator = ["&&","||","!"]
relationaloperatr = ["<","<=",">",">="]
equalityoperator = ["==","!="]
level = {"=":1,"+":6,"-":6,"*":7,"/":7,"%":7,"<":5,"<=":5,">":5,">=":5,"==":4,"!=":4,"&&":3,"||":2,"!":8}

def check_if_constant(tok):
    if tok.type.lower() == "T_IntConstant".lower() or tok.type.lower() == "T_BoolConstant".lower() or tok.type.lower() == "T_DoubleConstant".lower() or tok.type.lower() == "T_STRINGCONSTANT".lower():
        return True
    return False

def check_end_expression(tok):
    if (tok.value == ")" or tok.value == "," or tok.value == ";"):
        return True
    return False


class ReadInteger:
    def __init__(self,tok):
        self.type = "readinteger"
        self.tok = tok


class Expressions(Basic,object):
    def __init__(self, tokens, tokenPosition,fromActual = False):
        super(Expressions,self).__init__(tokens, tokenPosition)
        self.operatorList = operatorList
        self.bracktresolver = 1
        tok = tokens[tokenPosition]
        ntok = tokens[tokenPosition + 1]
        nntok = tokens[tokenPosition + 2]

        if check_if_constant(tok) and check_end_expression(ntok):
            self.type= "constant"
            self.value = Consant(tokens[tokenPosition])
            self.tokenPostionProcessed = tokenPosition
        elif tok.type.lower() == "T_Identifier".lower() and check_end_expression(ntok):
            self.type= "fieldaccess"
            self.value = FieldAccess(tokens, tokenPosition,fromActual)
            self.tokenPostionProcessed = tokenPosition
        elif tok.type.lower() == "T_Identifier".lower() and ntok.value == "=":
            #self.type = "AssignExpr"
            self.value = self.get_assign_exp(tokens, tokenPosition,"AssignExpr")
            self.type = self.get_type(self.value.operator)
        elif (tok.type.lower() == "T_Identifier".lower() or check_if_constant(tok)) and ntok.value in arithoperator:
            #self.type = "ArithmeticExpr"
            self.value = self.get_expression(tokens,tokenPosition,"ArithmeticExpr")
            self.type = self.get_type(self.value.operator)
        elif ((tok.type.lower() == "T_Identifier".lower() or check_if_constant(tok) )and ntok.value in logicaloperator) or (tok.value in logicaloperator and (ntok.type.lower() == "T_Identifier".lower() or check_if_constant(ntok))):
            #self.type = "LogicalExpr"
            self.value = self.get_expression(tokens,tokenPosition,"LogicalExpr")
            self.type = self.get_type(self.value.operator)
        elif (tok.type.lower() == "T_Identifier".lower() and ntok.value in relationaloperatr):
            #self.type = "RelationalExpr"
            self.value = self.get_expression(tokens, tokenPosition, "RelationalExpr")
            self.type = self.get_type(self.value.operator)
        elif (tok.type.lower() == "T_Identifier".lower() and ntok.value in equalityoperator):
            #self.type = "EqualityExpr"
            self.value = self.get_expression(tokens, tokenPosition, "EqualityExpr")
            self.type = self.get_type(self.value.operator)
        elif (tok.type.lower() == "T_Identifier".lower() and tok.value.lower() in ["readinteger","readline"]) and ntok.type.lower() == "(".lower():
            self.value = ReadInteger(tokens[tokenPosition])
            self.tokenPostionProcessed = tokenPosition + 2
        elif tok.type.lower() == "T_Identifier".lower() and ntok.type.lower() == "(".lower():
            self.type= "caller"
            self.value = Caller(tokens,tokenPosition,fromActual)
            self.tokenPostionProcessed = self.value.tokenPostionProcessed
        #elif ntok.value in operatorList:
            #self.value = self.get_expression(tokens, tokenPosition, "ArithmeticExpr")
            #self.type = self.get_type(self.value.operator)
        else:
            raise Exception(m.SyntaxErr, tokens[tokenPosition])

    def get_assign_exp(self,tokens,tokenposition,type):
        aex = Expression(type,tokenposition)
        aex.operator = "="
        aex.operatorPosition = tokenposition+1
        aex.lvalue = self.get_constant_identifier(tokens, tokenposition)
        aex.type = "AssignExpr"

        if tokens[tokenposition + 2].value.lower() == "ReadInteger".lower() or tokens[tokenposition + 2].value.lower() == "ReadLine".lower():
            aex.rvalue = ReadInteger(tokens[tokenposition + 2])
            if tokens[tokenposition + 3].value == "(":
                if tokens[tokenposition + 4].value == ")":
                    self.tokenPostionProcessed = tokenposition + 4
                    return aex
                else:
                    raise Exception(m.SyntaxErr, tokens[tokenposition + 4])
            else:
                raise Exception(m.SyntaxErr, tokens[tokenposition + 3])
        elif (tokens[tokenposition + 2].type.lower() == "T_Identifier".lower() or  check_if_constant(tokens[tokenposition + 2])) and check_end_expression(tokens[tokenposition + 3]):
            aex.rvalue = self.get_constant_identifier(tokens,tokenposition + 2)
            self.tokenPostionProcessed = tokenposition + 2
            return aex

        elif tokens[tokenposition + 2].type.lower() == "T_Identifier".lower() and tokens[tokenposition + 3].type.lower() == "(".lower():
            #self.type = "caller"
            aex.rvalue = Caller(tokens, tokenposition +2)
            self.tokenPostionProcessed = aex.rvalue.tokenPostionProcessed
            return aex

        arExp = self.get_expression(tokens,tokenposition+2,type)
        #temp = copy.deepcopy(arExp)
        aex.rvalue = arExp
        return aex

    def get_expression(self,tokens, tokenpositon,type):
        initial = True
        aex = None
        while True:
            if tokens[tokenpositon].value == ")" and self.bracktresolver == 1 and (not initial):
                #self.tokenPostionProcessed = tokenpositon
                break
            elif tokens[tokenpositon].value == "," or tokens[tokenpositon].value == ";" and (not initial):
                #self.tokenPostionProcessed = tokenpositon
                break
            initial = False
            if aex is None:
                aex = self.get_recursive_expression(tokens,tokenpositon,type)
            else:
                temp = Expression(type,tokenpositon)
                #aex.lvalue = None
                temp.lvalue = aex
                aex = None
                aex = temp
                aex.operator = tokens[tokenpositon].value
                aex.operatorPosition = tokenpositon
                aex.type = self.get_type(aex.operator)
                if (tokens[tokenpositon+1].value == "(" or self.has_higher_precdence(tokens[tokenpositon+2],tokens[tokenpositon])):  # and (not check_end_expression(nnntok)):
                    aex.rvalue = self.get_recursive_expression(tokens, tokenpositon + 1, type)
                else:
                    aex.rvalue = self.get_constant_identifier(tokens, tokenpositon + 1)
                    self.tokenPostionProcessed = tokenpositon + 1
            tokenpositon = self.tokenPostionProcessed+1
        return aex

    def get_type(self,operator):
        if operator in logicaloperator:
            return "LogicalExpr"
        elif operator in arithoperator:
            return "ArithmeticExpr"
        elif operator in relationaloperatr:
            return "RelationalExpr"
        elif operator in equalityoperator:
            return "EqualityExpr"
        elif operator == "=":
            return "AssignExpr"

    def has_higher_precdence(self,ntok,tok):
        if check_end_expression(ntok):
            return False
        if ntok.value not in operatorList:
            raise Exception(m.SyntaxErr,ntok)
        if tok.value not in operatorList:
            raise Exception(m.SyntaxErr,tok)
        if level[ntok.value]>level[tok.value]:
            return True
        return False

    def get_recursive_expression(self,tokens,tokenpositon,type):
        if tokens[tokenpositon].value == "(":
            tokenpositon +=1
            self.bracktresolver +=1

        aex = Expression(type,tokenpositon)
        inc = 0
        if tokens[tokenpositon].value not in operatorList:
            aex.lvalue = self.get_constant_identifier(tokens,tokenpositon)
        else:
            tokenpositon -=1

        tok = tokens[tokenpositon]
        ntok = tokens[tokenpositon + 1]
        nntok = tokens[tokenpositon + 2]
        nnntok = tokens[tokenpositon + 3]

        aex.operator = ntok.value
        aex.operatorPosition = tokenpositon+1
        if aex.operator not in operatorList:
            raise Exception(m.SyntaxErr, ntok)
        aex.type = self.get_type(aex.operator)

        if tokens[tokenpositon + 2].value.lower() == "ReadInteger".lower() or tokens[tokenpositon + 2].value.lower() == "ReadLine".lower():
            aex.rvalue = ReadInteger(tokens[tokenpositon + 2])
            if tokens[tokenpositon + 3].value == "(":
                if tokens[tokenpositon + 4].value == ")":
                    self.tokenPostionProcessed = tokenpositon + 4
                    return aex
                else:
                    raise Exception(m.SyntaxErr, tokens[tokenpositon + 4])
            else:
                raise Exception(m.SyntaxErr, tokens[tokenpositon + 3])


        if tokens[tokenpositon +2].type.lower() == "T_Identifier".lower() and tokens[tokenpositon + 3].type.lower() == "(".lower():
            #self.type = "caller"
            aex.rvalue = Caller(tokens, tokenpositon+2)
            self.tokenPostionProcessed = aex.rvalue.tokenPostionProcessed
            #return aex

        elif (nntok.value == "(" or self.has_higher_precdence(nnntok, ntok)):# and (not check_end_expression(nnntok)):
            aex.rvalue = self.get_recursive_expression(tokens, tokenpositon + 2,type)
        else:
            aex.rvalue = self.get_constant_identifier(tokens, tokenpositon + 2)
            if nnntok.value == ")" and self.bracktresolver>1:
                self.bracktresolver -=1
                inc = 1

        if tokenpositon +2 > self.tokenPostionProcessed:
            self.tokenPostionProcessed = tokenpositon + 2 + inc
        return aex


    def get_constant_identifier(self,tokens,tokenpositon):
        if check_if_constant(tokens[tokenpositon]):
            return Consant(tokens[tokenpositon])
        elif tokens[tokenpositon].type.lower() == "T_Identifier".lower():
            return FieldAccess(tokens, tokenpositon)
        else:
            raise Exception(m.SyntaxErr, tokens[tokenpositon])


class Expression:
    def __init__(self,type,tokenPositon):
        self.tokenPosition = tokenPositon
        self.type = type
        self.lvalue = None
        self.rvalue = None
        self.operator = None
        self.operatorPosition = 0
