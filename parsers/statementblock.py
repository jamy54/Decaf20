from parsers.program import Basic
from parsers.variabledecl import VariableDecl
import parsers.stmt as st
import parsers.message as m

class StmtBlock(Basic,object):
  def __init__(self,tokens,tokenPosition):
      super(StmtBlock,self).__init__(tokens, tokenPosition)
      self.variableDecls = []
      self.stmts = []

      varTokenPostion = self.tokenPosition+1
      if self.tokens[self.tokenPosition].value == "{":
          while True:
              if self.tokens[varTokenPostion].value == "}":
                  self.tokenPostionProcessed = varTokenPostion
                  break
              nTok = self.tokens[varTokenPostion]
              nnTok = self.tokens[varTokenPostion+1]
              nnnTok = self.tokens[varTokenPostion+2]
              if (nTok.value == "int" or nTok.value == "double" or nTok.value == "string" or nTok.value == "bool") and (nnTok.type.lower() == "T_Identifier".lower()):
                  variableDecl = VariableDecl(self.tokens, varTokenPostion)
                  self.tokenPostionProcessed = variableDecl.tokenPostionProcessed
                  varTokenPostion = self.tokenPostionProcessed + 1
                  self.variableDecls.append(variableDecl)
              else:
                  stmt = st.Stmt(self.tokens, varTokenPostion)
                  self.tokenPostionProcessed = stmt.tokenPostionProcessed
                  varTokenPostion = self.tokenPostionProcessed + 1
                  self.stmts.append(stmt)
      else:
          raise Exception(m.SyntaxErr, self.tokens[self.tokenPosition])