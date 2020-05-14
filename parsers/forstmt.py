from parsers.program import Basic
import parsers.message as m
from parsers.expr import Expressions

class ForStmt(Basic,object):
    def __init__(self, tokens, tokenPosition):
        super(ForStmt,self).__init__(tokens, tokenPosition)
        self.hasFirstExp = False
        self.hasLastExp = False
        self.check_lef_par()
        self.check_first_exp()
        self.check_middle_exp()
        self.check_last_exp()
        self.set_stmt()

    def check_lef_par(self):
        ntok = self.tokens[self.tokenPosition + 1]
        if ntok.value != "(":
            raise Exception(m.SyntaxErr, ntok)
        self.tokenPostionProcessed = self.tokenPosition + 1

    def check_first_exp(self):
        ntok = self.tokens[self.tokenPostionProcessed + 1]
        if ntok.value != ";":
            firstexp = Expressions(self.tokens, self.tokenPostionProcessed + 1)
            self.firstexp = firstexp
            self.hasFirstExp = True
            self.tokenPostionProcessed = firstexp.tokenPostionProcessed

        self.tokenPostionProcessed += 1

    def check_middle_exp(self):
        ntok = self.tokens[self.tokenPostionProcessed + 1]
        if ntok.value != ";":
            middleexp = Expressions(self.tokens, self.tokenPostionProcessed + 1)
            self.middleexp = middleexp
            self.tokenPostionProcessed = middleexp.tokenPostionProcessed
        else:
            raise Exception(m.SyntaxErr, ntok)
        self.tokenPostionProcessed += 1

    def check_last_exp(self):
        ntok = self.tokens[self.tokenPostionProcessed + 1]
        if ntok.value != ")":
            lastexp = Expressions(self.tokens, self.tokenPostionProcessed + 1)
            self.lastexp = lastexp
            self.hasLastExp = True
            self.tokenPostionProcessed = lastexp.tokenPostionProcessed
        self.tokenPostionProcessed += 1

    def set_stmt(self):
        import parsers.stmt as st
        stmt = st.Stmt(self.tokens, self.tokenPostionProcessed + 1)
        self.tokenPostionProcessed = stmt.tokenPostionProcessed
        self.stmt = stmt