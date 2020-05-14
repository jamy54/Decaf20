from parsers.expr import Expressions
from parsers.program import Basic
import parsers.message as m

class BreakStmt(Basic,object):
    def __init__(self, tokens, tokenPosition):
        super(BreakStmt,self).__init__(tokens, tokenPosition)
        self.find_expression()
        self.tokenPostionProcessed = self.tokenPosition + 1

    def find_expression(self):
        if self.tokens[self.tokenPosition + 1].value == ";":
            return
        else:
            raise Exception(m.SyntaxErr, self.tokens[self.tokenPosition])
