from parsers.program import Basic
import parsers.message as m
from parsers.expr import Expressions

class PrintStmt(Basic,object):
    def __init__(self, tokens, tokenPosition):
        super(PrintStmt,self).__init__(tokens, tokenPosition)
        self.exps = []
        #tok = tokens[tokenPosition]
        self.check_validity()
        self.add_expression()

    def add_expression(self):
        expPosition = self.tokenPosition + 2
        while self.tokens[expPosition].value != ")":
            exp = Expressions(self.tokens, expPosition,True)
            self.tokenPostionProcessed = exp.tokenPostionProcessed
            self.exps.append(exp)
            if self.tokens[self.tokenPostionProcessed + 1].value == ")":
                expPosition = self.tokenPostionProcessed + 1
                break
            elif self.tokens[self.tokenPostionProcessed + 1].value != ",":
                raise Exception(m.SyntaxErr, self.tokens[self.tokenPostionProcessed + 1])
            expPosition = self.tokenPostionProcessed + 2

        if self.tokens[expPosition + 1].value != ";":
            raise Exception(m.SyntaxErr, self.tokens[expPosition + 1])

        self.tokenPostionProcessed = expPosition + 1

    def check_validity(self):
        ntok = self.tokens[self.tokenPosition + 1]
        nntok = self.tokens[self.tokenPosition + 2]
        nnntok = self.tokens[self.tokenPosition + 3]
        if ntok.value != "(":
            raise Exception(m.SyntaxErr, ntok)
        if nntok.value == ")":
            raise Exception(m.SyntaxErr, nntok)