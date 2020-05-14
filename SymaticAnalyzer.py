from analyzer.SymbolTableGenerator import SymbolTableGenerateor
from analyzer.ErrorStructure import Error
from parsers.expr import operatorList,logicaloperator,relationaloperatr,arithoperator,equalityoperator
import mylexer

class Analyzer(object):
    def __init__(self,programTree, tokens,data):
        stGen = SymbolTableGenerateor(programTree, tokens)
        stGen.generateSymbolTable()

        self.data = data
        self.programTree = programTree
        self.tokens = tokens
        self.symbolTable = stGen.symbolTable
        self.errorList = []
        self.Analyze()

    def Analyze(self):
        if self.programTree is None:
            return
        for decl in self.programTree.decls:
            if not decl.isVariableDecl:
                self.findErrorFromBlock(decl.functionDecl.stmtBlock,decl.functionDecl.identifier,"function",decl.functionDecl.type)

    def findErrorFromStmt(self,stmt,methodName,caller,methodType):
        if stmt.stmtType == "block":
            self.findErrorFromBlock(stmt.stmtblock, methodName, caller, methodType)
        elif stmt.stmtType == "if":
            type, error = self.HandleExprError(stmt.ifStmt.exp, methodName)
            if type != "bool" and type != "error":
                mssage = "Test expression must have boolean type"
                tok = self.tokens[stmt.ifStmt.exp.tokenPosition]
                ltok = self.tokens[stmt.ifStmt.exp.tokenPostionProcessed]
                startPos = mylexer.find_column_start(self.data, tok)
                lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                error = Error(mssage, tok.lineno, startPos, lastPos)
                self.errorList.append(error)
            if stmt.ifStmt.ifstmt.stmtType == "block":
                self.findErrorFromBlock(stmt.ifStmt.ifstmt.stmtblock, methodName, "if", methodType)
            if stmt.ifStmt.hasElse and stmt.ifStmt.elstmt.stmtType == "block":
                self.findErrorFromBlock(stmt.ifStmt.elstmt.stmtblock, methodName, "else", methodType)
            elif stmt.ifStmt.hasElse and stmt.ifStmt.elstmt.__class__.__name__ == "Stmt":
                self.findErrorFromStmt(stmt.ifStmt.elstmt, methodName, "else", methodType)
        elif stmt.stmtType == "while":
            self.HandleExprError(stmt.wStmt.exp, methodName)
            if stmt.wStmt.stmt.stmtType == "block":
                self.findErrorFromBlock(stmt.wStmt.stmt.stmtblock, methodName, "while", methodType)
        elif stmt.stmtType == "return":
            if stmt.rStmt.hasExp:
                type, error = self.HandleExprError(stmt.rStmt.exp, methodName)
                if type != methodType and type != "error":
                    msg = "Incompatible return: {0} given, {1} expected".format(type, methodType)
                    tok = self.tokens[stmt.rStmt.tokenPosition + 1]
                    ltok = self.tokens[stmt.rStmt.tokenPostionProcessed - 1]
                    startPos = mylexer.find_column_start(self.data, tok)
                    lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                    error = Error(msg, tok.lineno, startPos, lastPos)
                    self.errorList.append(error)

        elif stmt.stmtType == "print":
            for i in range(0, len(stmt.pStmt.exps)):
                exp = stmt.pStmt.exps[i]
                type, error = self.HandleExprError(exp, methodName)
                if type == "double":
                    mssage = "Incompatible argument {0}: double given, int/bool/string expected".format(i+1)
                    tok = self.tokens[exp.tokenPosition]
                    ltok = self.tokens[exp.tokenPostionProcessed]
                    startPos = mylexer.find_column_start(self.data, tok)
                    lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                    error = Error(mssage, tok.lineno, startPos, lastPos)
                    self.errorList.append(error)

        elif stmt.stmtType == "break":
            if not (caller == "while" or caller == "for"):
                msg = "break is only allowed inside a loop"
                tok = self.tokens[stmt.bStmt.tokenPosition]
                startPos = mylexer.find_column_start(self.data, tok)
                lastPos = startPos + len("break")
                error = Error(msg, tok.lineno, startPos, lastPos)
                self.errorList.append(error)
        elif stmt.stmtType == "for":
            if stmt.fStmt.hasFirstExp:
                self.HandleExprError(stmt.fStmt.firstexp, methodName)
            type,error = self.HandleExprError(stmt.fStmt.middleexp, methodName)
            if type != "bool" and type !="error":
                mssage = "Test expression must have boolean type"
                tok = self.tokens[stmt.fStmt.middleexp.tokenPosition]
                ltok = self.tokens[stmt.fStmt.middleexp.tokenPostionProcessed]
                startPos = mylexer.find_column_start(self.data, tok)
                lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                error = Error(mssage, tok.lineno, startPos, lastPos)
                self.errorList.append(error)
            if stmt.fStmt.hasLastExp:
                self.HandleExprError(stmt.fStmt.lastexp, methodName)
            if stmt.fStmt.stmt.stmtType == "block":
                self.findErrorFromBlock(stmt.fStmt.stmt.stmtblock, methodName, "for", methodType)
        elif stmt.stmtType == "exp":
            self.HandleExprError(stmt.exp, methodName)


    def findErrorFromBlock(self,stmtBlock,methodName,caller,methodType):
        for stmt in stmtBlock.stmts:
            self.findErrorFromStmt(stmt,methodName,caller,methodType)


    def HandleForConExprError(self, exp, methodName):
        type, error = self.findError(exp.value, methodName)
        if type == "error":
            error.Message = "Test expression must have boolean type"
            error.StartPos = self.tokens[exp.tokenPosition].lexpos
            error.LastPos = self.tokens[exp.tokenPostionProcessed].lexpos
            self.errorList.append(error)

    def HandleExprError(self, exp, methodName):
        type, error = self.findError(exp.value,methodName)
        if type =="error":
            self.errorList.append(error)
        return type,error

    def findError(self, exp,methodName):
        if exp.__class__.__name__ == "FieldAccess" or exp.__class__.__name__ == "Consant" or exp.__class__.__name__ == "Caller" or exp.__class__.__name__ == "ReadInteger":
            return self.getValueType(exp, methodName)
        typeLeft,error = self.getValueType(exp.lvalue,methodName)
        if typeLeft == "error":
            return typeLeft,error
        if typeLeft is None and (exp.operator not in logicaloperator and exp.operator !="-"):
            return self.handleNoDeclError(exp.lvalue)

        typeRight, error = self.getValueType(exp.rvalue, methodName)
        if typeRight == "error":
            return typeRight, error
        if typeRight is None:
            return self.handleNoDeclError(exp.rvalue)

        if exp.operator == "=":
            return self.checkAssignmentArithmeticExp(exp,typeLeft,typeRight)
        elif exp.operator in arithoperator:
            return self.checkAssignmentArithmeticExp(exp,typeLeft,typeRight)
        elif exp.operator in relationaloperatr:
            return self.checkRelationalExpr(exp,typeLeft,typeRight)
        elif exp.operator in logicaloperator:
            return self.checkLogicalExpr(exp, typeLeft, typeRight)
        elif exp.operator in equalityoperator:
            return self.checkEqualityExpr(exp,typeLeft,typeRight)

    def getValueType(self,value,methodName):
        if value is None:
            return None,None
        type = ""
        error = None
        if value.__class__.__name__ == "Expression":
            type, error = self.findError(value, methodName)
        elif value.__class__.__name__ == "ReadInteger":
            type,error = "int",None
        elif value.__class__.__name__ == "Consant":
            type = value.idtype
        elif value.__class__.__name__ == "FieldAccess":
            obj= self.symbolTable.getSymbol(value.identifier, methodName)
            if obj is not None:
                type = obj.type
            else:
                msg = "No declaration found for variable '{0}'".format(value.identifier)
                type = "error"
                tok = self.tokens[value.tokenPosition]
                ltok = self.tokens[value.tokenPosition]
                startPos = mylexer.find_column_start(self.data, tok)
                lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                error = Error(msg, tok.lineno, startPos, lastPos)
        elif value.__class__.__name__ == "Caller":
            obj= self.symbolTable.getMethodSymbol(value.identifier)
            if obj is not None:
                type = obj.type
                if len(value.exps) != len(obj.formals):
                    msg = "Function '{0}' expects {1} arguments but {2} given".format(value.identifier,len(obj.formals), len(value.exps))
                    type = "error"
                    tok = self.tokens[value.tokenPosition]
                    ltok = self.tokens[value.tokenPosition]
                    startPos = mylexer.find_column_start(self.data, tok)
                    lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                    error = Error(msg, tok.lineno, startPos, lastPos)
                else:
                    for i in range(0,len(obj.formals)):
                        typeexp, error = self.findError(value.exps[i].value, methodName)
                        if typeexp == "error":
                            break
                        elif typeexp != obj.formals[i].type.type:
                            msg = "Incompatible argument {0}: {1} given, {2} expected".format(i+1,typeexp,obj.formals[i].type.type)
                            type = "error"
                            tok = self.tokens[value.exps[i].tokenPosition]
                            ltok = self.tokens[value.exps[i].tokenPostionProcessed]
                            startPos = mylexer.find_column_start(self.data, tok)
                            lastPos = mylexer.find_column_start(self.data, ltok) + len(ltok.value)
                            error = Error(msg, tok.lineno, startPos,lastPos)
                            break
        return type, error

    def checkAssignmentArithmeticExp(self, exp,typeLeft,typeRight):
        if self.satisfyAssignmentArithmeticExp(typeLeft,typeRight):
            return self.HandleError(typeLeft,typeRight,exp)
        return typeRight, None

    def checkEqualityExpr(self, exp, typeLeft, typeRight):
        if self.satisfyAssignmentArithmeticExp(typeLeft,typeRight):
            return self.HandleError(typeLeft,typeRight,exp)
        return "bool", None

    def checkLogicalExpr(self, exp, typeLeft, typeRight):
        if self.satisfyLogicalEqualityExpr(typeLeft,typeRight):
            return self.HandleError(typeLeft,typeRight,exp)
        return typeRight, None

    def checkRelationalExpr(self, exp, typeLeft, typeRight):
        if self.satisfyRelationalExpr(typeLeft,typeRight):
            return self.HandleError(typeLeft,typeRight,exp)
        return "bool", None

    def satisfyAssignmentArithmeticExp(self, typeLeft, typeRight):
        if typeRight != typeLeft and typeLeft is not None:# or not (typeRight in ["int", "double"] and typeLeft in ["int", "double"]):
            return True
        elif typeLeft is None and typeRight not in ["int","double"]:
            return True
        return False

    def satisfyLogicalEqualityExpr(self, typeLeft, typeRight):
        if (typeLeft is not None and typeLeft !="bool") or typeRight !="bool":
            return True
        return False

    def satisfyRelationalExpr(self, typeLeft, typeRight):
        if typeRight != typeLeft or typeLeft=="bool" or typeRight =="bool":
            return True
        return False

    def HandleError(self, typeLeft, typeRight, exp):
        operand = "operands"
        if typeLeft is None:
            typeLeft = ""
            operand = "operand"
        msg = "Incompatible {3}: {0} {2} {1}".format(typeLeft, typeRight, exp.operator,operand)
        tok = self.tokens[exp.operatorPosition]
        startPos = mylexer.find_column_start(self.data, tok)
        lastPos = startPos + len(tok.value)
        return "error", Error(msg, tok.lineno, startPos, lastPos)

    def handleNoDeclError(self, value,txt = "variable"):
        msg = "No declaration found for {0} {1}".format(txt,value.identifier)
        tok = self.tokens[value.tokenPosition]
        startPos = mylexer.find_column_start(self.data, tok)
        lastPos = startPos + len(tok.value)
        return "error", Error(msg, tok.lineno, startPos, lastPos)