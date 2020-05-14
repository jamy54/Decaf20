from parsers.expr import Expressions
from parsers.program import Basic
import parsers.message as m

class ReturnStmt(Basic,object):
    def __init__(self, tokens, tokenPosition):
        super(ReturnStmt,self).__init__(tokens, tokenPosition)
        self.hasExp = False
        self.find_expression()

    def find_expression(self):
        if self.tokens[self.tokenPosition + 1].value == ";":
            self.tokenPostionProcessed = self.tokenPosition + 1
            return
        else:
            tokPos = self.tokenPosition+1
            hasbrcket = False
            inc = 1
            if self.tokens[tokPos].value == "(":
                tokPos +=1
                hasbrcket = True
            exp = Expressions(self.tokens, tokPos,True)
            self.exp = exp
            self.hasExp = True
            self.tokenPostionProcessed = exp.tokenPostionProcessed

            if hasbrcket and self.tokens[exp.tokenPostionProcessed+1].value != ")":
                raise Exception(m.SyntaxErr, self.tokens[self.tokenPostionProcessed + 1])
            elif hasbrcket and self.tokens[exp.tokenPostionProcessed+1].value == ")":
                self.tokenPostionProcessed += 1
                inc = 2
            if self.tokens[exp.tokenPostionProcessed + inc].value != ";":
                raise Exception(m.SyntaxErr,self.tokens[self.tokenPostionProcessed + 1])

            self.tokenPostionProcessed += 1