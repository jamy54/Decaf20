from parsers.variable import Variable
from parsers.statementblock import StmtBlock
import parsers.message as m

class FunctionDecl(Variable,object):
  def __init__(self,tokens,tokenPositon):
      super(FunctionDecl,self).__init__(tokens,tokenPositon,True)
      self.formals = []
      self.hasFormals = False
      self.processFormals(self.tokenPosition + 3)
      self.stmtBlock = StmtBlock(tokens,self.tokenPostionProcessed+1)
      self.tokenPostionProcessed = self.stmtBlock.tokenPostionProcessed
      self.type = tokens[tokenPositon].value
      self.identifier = tokens[tokenPositon+1].value

  def processFormals(self,tokPosToProcess):
      variableList = []
      if self.tokens[tokPosToProcess].value == ")":
          self.tokenPostionProcessed =  tokPosToProcess
          return variableList
      variableList.append(Variable(self.tokens,tokPosToProcess))

      while self.tokens[tokPosToProcess+2].value == ",":
          tokPosToProcess += 3
          variableList.append(Variable(self.tokens, tokPosToProcess))

      if self.tokens[tokPosToProcess + 2].value != ")":
          raise Exception(m.SyntaxErr,self.tokens[tokPosToProcess + 2])

      self.formals = variableList
      self.hasFormals = len(variableList) != 0
      self.tokenPostionProcessed += (tokPosToProcess+2)