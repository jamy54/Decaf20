from parsers.program import Basic
import parsers.message as m

class Caller(Basic,object):
    def __init__(self, tokens, tokenPosition,fromActual=False):
        super(Caller,self).__init__(tokens,tokenPosition)
        self.fromActual = fromActual
        self.exps = []
        self.hasExp = False
        self.identifier = tokens[tokenPosition].value
        self.check_validity()
        self.add_expression()

    def add_expression(self):
        expPosition = self.tokenPosition + 2
        import parsers.expr as ex
        while self.tokens[expPosition].value != ")":
            exp = ex.Expressions(self.tokens, expPosition,self.fromActual)
            self.tokenPostionProcessed = exp.tokenPostionProcessed
            self.exps.append(exp)
            if self.tokens[self.tokenPostionProcessed + 1].value == ")":
                self.tokenPostionProcessed = self.tokenPostionProcessed + 1
                break
            elif self.tokens[self.tokenPostionProcessed + 1].value != ",":
                raise Exception(m.SyntaxErr, self.tokens[self.tokenPostionProcessed + 1])
            expPosition = self.tokenPostionProcessed + 2

        self.hasExp = (len(self.exps)!=0)
        #self.tokenPostionProcessed = expPosition + 1

    def check_validity(self):
        ntok = self.tokens[self.tokenPosition + 1]
        if ntok.value != "(":
            raise Exception(m.SyntaxErr, ntok)
        self.tokenPostionProcessed = self.tokenPosition + 1