class Consant:
    def __init__(self, tok):
        self.val = tok.value
        self.type = self.set_constant(tok)
        self.idtype = self.set_id_constant(tok)
        self.token = tok

    def set_constant(self,tok):
        if tok.type.lower() == "T_IntConstant".lower():
            return "IntConstant"
        elif tok.type.lower() == "T_BoolConstant".lower():
            return "BoolConstant"
        elif tok.type.lower() == "T_DoubleConstant".lower():
            datas= self.val.split(".")
            if datas[1] == "0":
                self.val = datas[0]
            return "DoubleConstant"
        elif tok.type.lower() == "T_STRINGCONSTANT".lower():
            return "StringConstant"

    def set_id_constant(self,tok):
        if tok.type.lower() == "T_IntConstant".lower():
            return "int"
        elif tok.type.lower() == "T_BoolConstant".lower():
            return "bool"
        elif tok.type.lower() == "T_DoubleConstant".lower():
            return "double"
        elif tok.type.lower() == "T_STRINGCONSTANT".lower():
            return "string"