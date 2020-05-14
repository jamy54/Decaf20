from parsers.program import Basic
import parsers.message as m
from parsers.expr import Expressions

class WhileStmt(Basic,object):
    def __init__(self, tokens, tokenPosition):
        super(WhileStmt,self).__init__(tokens, tokenPosition)
        self.check_validity()
        self.set_expression()
        self.check_exp_ends()
        self.set_stmt()


    def check_validity(self):
        ntok = self.tokens[self.tokenPosition + 1]
        nntok = self.tokens[self.tokenPosition + 2]
        if ntok.value != "(":
            raise Exception(m.SyntaxErr, ntok)
        if nntok.value == ")":
            raise Exception(m.SyntaxErr, nntok)

    def check_exp_ends(self):
        if self.tokens[self.tokenPostionProcessed + 1].value != ")":
            raise Exception(m.SyntaxErr, self.tokens[self.tokenPostionProcessed + 1])
        self.tokenPostionProcessed += 1

    def set_expression(self):
        expPosition = self.tokenPosition + 2
        exp = Expressions(self.tokens, expPosition)
        self.tokenPostionProcessed = exp.tokenPostionProcessed
        self.exp = exp

    def set_stmt(self):
        import parsers.stmt as st
        stmt = st.Stmt(self.tokens, self.tokenPostionProcessed + 1)
        self.tokenPostionProcessed = stmt.tokenPostionProcessed
        self.stmt = stmt