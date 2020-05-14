from analyzer.SymbolTable import SymbolTable

class SymbolTableGenerateor(object):
    def __init__(self,programTree, tokens):
        self.programTree = programTree
        self.tokens = tokens
        self.symbolTable = SymbolTable()

    def generateSymbolTable(self):
        for decl in self.programTree.decls:
            if decl.isVariableDecl:
                self.ExtractSymbolFromVariable(decl.variableDecl.variable,False)
            else:
                self.ExtractSymbolFromMethod(decl.functionDecl)

    def ExtractSymbolFromVariable(self,varIable,isParameter,funcName=""):
        type = varIable.type.type
        name = varIable.identifier
        isGlobal = funcName.lower() == "main" or funcName == ""
        isParameter = isParameter
        funcName = funcName
        self.symbolTable.addSymbol(type, name, isGlobal, isParameter, funcName)

    def ExtractSymbolFromStmt(self, stmt, methodName):
        if stmt.stmtType == "block":
            self.ExtractSymbolFromBlock(stmt.stmtblock, methodName)
        elif stmt.stmtType == "if":
            if stmt.ifStmt.ifstmt.stmtType == "block":
                self.ExtractSymbolFromBlock(stmt.ifStmt.ifstmt.stmtblock, methodName)
            if stmt.ifStmt.hasElse and stmt.ifStmt.elstmt.stmtType == "block":
                self.ExtractSymbolFromBlock(stmt.ifStmt.elstmt.stmtblock, methodName)
            elif stmt.ifStmt.hasElse and stmt.ifStmt.elstmt.__class__.__name__ == "Stmt":
                self.ExtractSymbolFromStmt(stmt.ifStmt.elstmt, methodName)
        elif stmt.stmtType == "while":
            if stmt.wStmt.stmt.stmtType == "block":
                self.ExtractSymbolFromBlock(stmt.wStmt.stmt.stmtblock, methodName)
        elif stmt.stmtType == "for":
            if stmt.fStmt.stmt.stmtType == "block":
                self.ExtractSymbolFromBlock(stmt.fStmt.stmt.stmtblock, methodName)

    def ExtractSymbolFromBlock(self, stmtBlock, methodName):
        for varDecl in stmtBlock.variableDecls:
            self.ExtractSymbolFromVariable(varDecl.variable, False,methodName)
        for stmt in stmtBlock.stmts:
            self.ExtractSymbolFromStmt(stmt, methodName)


    def ExtractSymbolFromMethod(self,funcDecl):
        if funcDecl.hasFormals:
            for variable in funcDecl.formals:
                self.ExtractSymbolFromVariable(variable,True,funcDecl.identifier)
        self.symbolTable.addMethodSymbol(funcDecl.type, funcDecl.identifier, funcDecl.formals)
        self.ExtractSymbolFromBlock(funcDecl.stmtBlock,funcDecl.identifier)