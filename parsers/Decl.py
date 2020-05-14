import parsers.message as m
from parsers.program import Basic
from parsers.functiondecl import FunctionDecl
from parsers.variabledecl import VariableDecl

class Decl(Basic,object):
    def __init__(self,tokens,tokenPositon):
        super(Decl,self).__init__(tokens,tokenPositon)
        self.variableDecl = None
        self.functionDecl = None
        self.isVariableDecl = False
        self.process()

    def process(self):
        nTok = self.tokens[self.tokenPosition]
        nnTok = self.tokens[self.tokenPosition+1]
        nnnTok = self.tokens[self.tokenPosition+2]
        if (nTok.value == "int" or nTok.value == "double" or nTok.value == "string" or nTok.value == "bool" or nTok.value == "void"):
            if(nnTok.type.lower() == "T_Identifier".lower()):
                if (nnnTok.value == '('):
                    self.functionDecl = FunctionDecl(self.tokens,self.tokenPosition)
                    self.tokenPostionProcessed = self.functionDecl.tokenPostionProcessed
                else:
                    self.isVariableDecl = True
                    self.variableDecl = VariableDecl(self.tokens,self.tokenPosition)
                    self.tokenPostionProcessed = self.variableDecl.tokenPostionProcessed
            else:
                raise Exception(m.SyntaxErr,nnTok)
        else:
            raise Exception(m.SyntaxErr,nTok)
