


class CodeGenerator(object):
    def __init__(self, programTree, tokens, data,symbolTable):
        self.data = data
        self.programTree = programTree
        self.tokens = tokens
        self.symbolTable = symbolTable
        self.instructions = []
        self.assCode = ""
        self.levelCounter = 0

        self.registerDict = {}
        self.reset()

        self.generate()

    def generate(self):
        if self.programTree is None:
            return
        for decl in self.programTree.decls:
            if not decl.isVariableDecl:
                self.currentMethodName = decl.functionDecl.identifier
                self.AddEpilogue(decl.functionDecl.identifier)
                self.AllocateRegister(decl.functionDecl.formals,"formals")
                self.GenerateFromBlock(decl.functionDecl.stmtBlock)
                if not self.InReturn:
                    self.AddProLogue(decl.functionDecl.identifier)
                self.reset()

        return self.generateAss()

    def generateAss(self):
        code = ""
        for ins in self.instructions:
            code = code + ins + "\n"
        self.assCode = code
        return code

    def reset(self):
        self.argumentCount = 0
        self.regularCount = 0
        self.frameCounter = 0
        self.hasLastLabel = False
        self.InReturn = False

    def GenerateFromBlock(self, stmtBlock):
        for vd in stmtBlock.variableDecls:
            self.AllocateRegister([vd.variable], "regular")
        for stmt in stmtBlock.stmts:
            self.GenerateFromStmt(stmt)

    def GenerateFromStmt(self, stmt):
        if stmt.stmtType == "block":
            self.GenerateFromBlock(stmt.stmtblock)
        elif stmt.stmtType == "if":
            self.levelCounter+=1
            lebel = "L"+str(self.levelCounter)
            self.GenerateExpr(stmt.ifStmt.exp.value,lebel)
            self.GenerateFromStmt(stmt.ifStmt.ifstmt)
            self.instructions.append(lebel+":")
            if stmt.ifStmt.hasElse:
                self.GenerateFromStmt(stmt.ifStmt.elstmt)
        elif stmt.stmtType == "while":
            pass
        elif stmt.stmtType == "return":
            self.InReturn = True
            if stmt.rStmt.hasExp:
                type,register = self.GenerateExpr(stmt.rStmt.exp.value)
                if stmt.rStmt.exp.value.__class__.__name__ == "Consant":
                    ins = "li"
                else:
                    ins = "move"
                self.instructions.append("{0} {1},{2}".format(ins,"$v0", register))
            self.AddProLogue(self.currentMethodName)
        elif stmt.stmtType == "print":
            for exp in stmt.pStmt.exps:
                type, register = self.GenerateExpr(exp.value)
                if exp.value.__class__.__name__ == "Consant" and (not "$" in register):
                    ins = "li"
                else:
                    ins = "move"
                self.AddInstructions(ins,"$a0",register,"=")
                if type =="string":
                    code = 4
                else:
                    code = 1
                self.AddInstructions("li", "$v0", code, "=")
                self.instructions.append("syscall")
        elif stmt.stmtType == "break":
            pass
        elif stmt.stmtType == "for":
            if stmt.fStmt.hasFirstExp:
                self.GenerateExpr(stmt.fStmt.firstexp.value)

            self.levelCounter += 1
            endlebel = "L" + str(self.levelCounter)
            self.levelCounter += 1
            looplevel = "L" + str(self.levelCounter)
            self.instructions.append(looplevel + ":")
            self.GenerateExpr(stmt.fStmt.middleexp.value, endlebel)
            self.GenerateFromStmt(stmt.fStmt.stmt)
            if stmt.fStmt.hasLastExp:
                self.GenerateExpr(stmt.fStmt.lastexp.value)
            self.instructions.append("b "+looplevel)
            self.instructions.append(endlebel + ":")

        elif stmt.stmtType == "exp":
            self.GenerateExpr(stmt.exp.value)

    def AddEpilogue(self, identifier):
        self.instructions.append(".text")
        if identifier.lower() == "main":
            self.instructions.append(".globl main")
        self.instructions.append(identifier+":")
        self.instructions.append("subu $sp,$sp,32")
        self.instructions.append("sw $ra,20($sp)")
        self.instructions.append("sw $fp,16($sp)")
        self.instructions.append("addiu $fp,$sp,28")

    def AddProLogue(self, identifier):
        #if self.hasLastLabel:
            #self.instructions.append("Last1:")
        self.instructions.append("lw $ra, 20($sp)")
        self.instructions.append("lw $fp, 16($sp)")
        self.instructions.append("addiu $sp, $sp, 32 ")
        if identifier.lower() == "main":
            self.instructions.append("li $v0, 10")
            self.instructions.append("syscall")
        else:
            self.instructions.append("jr $ra")

    def CheckArgumentAndAssignReg(self,leftRegister,value):
        if "$a" in leftRegister:
            rReg = str(self.frameCounter*4) + "($fp)"
            self.frameCounter +=1
            self.AddInstructions("sw",leftRegister,rReg,"=")
            self.regularCount += 1
            leftRegister = "$t"+str(self.regularCount-1)
            self.AddInstructions("lw", leftRegister, rReg, "=")
            self.frameCounter -= 1
            if value.__class__.__name__ == "FieldAccess":
                self.SetRegisterToVar(leftRegister,value)
        return leftRegister

    def storeRegistertoMemory(self):
        for i in range(0,self.regularCount):
            rReg = str(self.frameCounter * 4) + "($fp)"
            self.frameCounter += 1
            self.AddInstructions("sw", "$t"+str(i), rReg, "=")

    def storeRegisterFromMemory(self):
        for i in reversed(range(self.regularCount)):
            self.frameCounter -= 1
            rReg = str(self.frameCounter * 4) + "($fp)"
            self.AddInstructions("lw", "$t" + str(i), rReg, "=")

    def GenerateExpr(self, exp,lebel=""):
        if hasattr(exp, 'lvalue'):
            ltype,leftRegister = self.CheckBaseCondition(exp.lvalue)
            leftRegister = self.CheckArgumentAndAssignReg(leftRegister,exp.lvalue)
            rtype, rightRegister = self.CheckBaseCondition(exp.rvalue)
            rightRegister = self.CheckArgumentAndAssignReg(rightRegister,exp.rvalue)

            if rtype =="string":
                return self.handleString(exp.rvalue.val, leftRegister)
                #return "string",leftRegister
            elif rtype in ["int","bool","double"]:
                self.regularCount += 1
                holdReg = "$t" + str(self.regularCount - 1)
                if "$" in rightRegister:
                    ins = "move"
                else:
                    ins = "li"
                self.instructions.append("{0} {1},{2}".format(ins, holdReg, rightRegister))
                rightRegister = holdReg


            leftInstruction = self.getInstructionByOp(exp.operator,rightRegister)
            self.AddInstructions(leftInstruction,leftRegister,rightRegister,exp.operator,lebel)
            return ltype, leftRegister
        else:
            type,register = self.CheckBaseCondition(exp)
            if type =="string":
                self.regularCount += 1
                lReg = "$t" + str(self.regularCount - 1)
                return self.handleString(register,lReg)
            return type,register


    def handleString(self,val,lregister):
        self.levelCounter += 1
        rightRegister = "$jam" + str(self.levelCounter)
        self.instructions.append(".data")
        self.instructions.append(rightRegister + ":")
        self.instructions.append(".ascii {0}".format(val))
        self.instructions.append(".text")

        self.AddInstructions("la", lregister, rightRegister, "=")
        return "string", lregister

    def AddInstructions(self,instruction, leftReg, rightReg, op,lebel=""):
        from parsers.expr import logicaloperator,arithoperator, relationaloperatr
        if op not in arithoperator and op not in relationaloperatr:
            self.instructions.append("{0} {1},{2}".format(instruction, leftReg, rightReg))
        elif op =="<=":
            self.regularCount += 1
            holdReg1 = "$t" + str(self.regularCount - 1)
            self.instructions.append("{0} {1},{2},{3}".format("slt", holdReg1, leftReg,rightReg))

            self.regularCount += 1
            holdReg2 = "$t" + str(self.regularCount - 1)
            self.instructions.append("{0} {1},{2},{3}".format("seq", holdReg2, leftReg,rightReg))
            self.instructions.append("{0} {1},{2},{3}".format("or", holdReg1, holdReg1,holdReg2))
            self.instructions.append("{0} {1},{2}".format("beqz", holdReg1, lebel))
        else:
            self.instructions.append("{0} {1},{2},{3}".format(instruction,leftReg,leftReg,rightReg))

    def CheckBaseCondition(self,value):
        if value.__class__.__name__ == "ReadInteger":
            return None,None
        elif value.__class__.__name__ == "Consant":
            return value.idtype, value.val
        elif value.__class__.__name__ == "FieldAccess":
            reg = self.GetRegister(value)
            type = self.symbolTable.getSymbol(value.identifier,self.currentMethodName).type
            return type,reg
        elif value.__class__.__name__ == "Caller":
            for exp in value.exps:
                type,register = self.GenerateExpr(exp.value)
                if type == ["int","bool","double","string"][0]:
                    self.argumentCount +=1
                    leftReg = "$a"+str(self.argumentCount-1)
                    if exp.value.__class__.__name__ == "Consant" and (not "$" in register):
                        ins = "li"
                    else:
                        ins = "move"
                    self.instructions.append("{0} {1},{2}".format(ins,leftReg, register))
            self.storeRegistertoMemory()
            self.instructions.append("{0} {1}".format("jal", value.identifier))
            self.storeRegisterFromMemory()
            returnType = self.symbolTable.getMethodSymbol(value.identifier).type
            if returnType == "void":
                return "caller", None
            else:
                return "caller", "$v0"
        else:
            return self.GenerateExpr(value)

    def AllocateRegister(self, variables,type):
        for var in variables:
            #if self.symbolTable.getAllocatedRegister(var.identifier,self.currentMethodName) == "":
            registerName = self.getNextRegister(type)
            self.symbolTable.setAllocatedRegister(var.identifier, self.currentMethodName,registerName)

    def SetRegisterToVar(self, registerName, var):
        self.symbolTable.setAllocatedRegister(var.identifier, self.currentMethodName, registerName)

    def GetRegister(self, variable):
        return self.symbolTable.getAllocatedRegister(variable.identifier, self.currentMethodName)

    def getNextRegister(self,type):
        if type == "formals":
            self.argumentCount +=1
            return "$a{0}".format(self.argumentCount-1)
        elif type == "regular":
            self.regularCount += 1
            return "$t{0}".format(self.regularCount - 1)

    def getInstructionByOp(self, operator,rReg=""):
        if operator == "+":
            return "add"
        if operator == "-":
            return "sub"
        if operator == "=":
            return "move"
        if operator == "*":
            return "mul"
        if operator == "<=":
            return "ble"