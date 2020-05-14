from parsers.program import Basic
from parsers.type import Type
import parsers.message as m

class Variable(Basic,object):
  def __init__(self,tokens, tokenPositon,isvoidallowed=False):
      super(Variable,self).__init__(tokens, tokenPositon)
      self.type = Type(tokens[tokenPositon],isvoidallowed)
      if tokens[tokenPositon+1].type.lower() == "T_Identifier".lower():
          self.identifier = tokens[tokenPositon+1].value
      else:
          raise Exception(m.SyntaxErr,tokens[tokenPositon+1])