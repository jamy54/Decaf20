class FieldAccess:
    def __init__(self, tokens, tokenPosition,fromActual = False):
        self.tokenPosition = tokenPosition
        self.identifier = tokens[tokenPosition].value
        self.type = "FieldAccess"
        self.fromActual = fromActual