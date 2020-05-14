from parsers.program import Basic
from parsers.variable import Variable
import parsers.message as m

class VariableDecl(Basic,object):
    def __init__(self,tokens,tokenPositon):
        super(VariableDecl,self).__init__(tokens, tokenPositon)
        self.variable = Variable(self.tokens, self.tokenPosition)
        if tokens[tokenPositon +2].value == ";":
            self.semicolon = ";"
            self.tokenPostionProcessed = tokenPositon +2
        else:
            raise Exception(m.SyntaxErr,tokens[tokenPositon+2])