from parsers.program import Basic
from parsers.ifsttmnt import IfStmt
from parsers.whilestmt import WhileStmt
from parsers.forstmt import ForStmt
from parsers.breakStmt import BreakStmt

from parsers.returnstmt import ReturnStmt
from parsers.printstmt import PrintStmt
from parsers.expr import Expressions
import parsers.message as m

class Stmt(Basic,object):
    def __init__(self, tokens, tokenPosition):
        import parsers.statementblock as stb
        super(Stmt,self).__init__(tokens, tokenPosition)
        if tokens[tokenPosition].value == "{":
            self.stmtblock = stb.StmtBlock(tokens,tokenPosition)
            self.stmtType = "block"
            self.tokenPostionProcessed = self.stmtblock.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_If".lower():
            self.ifStmt = IfStmt(tokens, tokenPosition)
            self.stmtType = "if"
            self.tokenPostionProcessed = self.ifStmt.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_While".lower():
            self.wStmt = WhileStmt(tokens, tokenPosition)
            self.stmtType = "while"
            self.tokenPostionProcessed = self.wStmt.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_For".lower():
            self.fStmt = ForStmt(tokens, tokenPosition)
            self.stmtType = "for"
            self.tokenPostionProcessed = self.fStmt.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_Break".lower():
            self.bStmt = BreakStmt(tokens, tokenPosition)
            self.stmtType = "break"
            self.tokenPostionProcessed = self.bStmt.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_Return".lower():
            self.rStmt = ReturnStmt(tokens, tokenPosition)
            self.stmtType = "return"
            self.tokenPostionProcessed = self.rStmt.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_Print".lower():
            self.pStmt = PrintStmt(tokens, tokenPosition)
            self.stmtType = "print"
            self.tokenPostionProcessed = self.pStmt.tokenPostionProcessed
        elif tokens[tokenPosition].type.lower() == "T_Else".lower():
            raise Exception(m.SyntaxErr, tokens[tokenPosition])
        else:
            self.exp = Expressions(tokens, tokenPosition)
            self.stmtType = "exp"
            self.tokenPostionProcessed = self.exp.tokenPostionProcessed
            if tokens[self.tokenPostionProcessed+1].type.lower() != ";".lower():
                raise Exception(m.SyntaxErr, tokens[self.tokenPostionProcessed+1])
            self.tokenPostionProcessed += 1
