#from parser import getToken,find_column,find_type,find_value
from parsers.program import ProgramNode
from parsers.Decl import Decl
import mylexer
import parsers.AstGenerator as ag
import sys

data= ""

def gettoken():
    global data
    fileName = "Samples/t3.decaf"
    #fileName = sys.argv[1]
    f = open(fileName, "r")
    data = f.read()
    d = mylexer.gettoken(data)
    return d


def parseTokens(tokens):
    global data
    tokenLength = len(tokens)
    if tokenLength== 0:
        print("Empty program is syntactically incorrect because it is empty.")
        return
    try:
        progrmNode = ProgramNode()
        tokenposition = 0
        while True:
            if tokenLength <= tokenposition:
                break
            decl = Decl(tokens,tokenposition)
            tokenposition = decl.tokenPostionProcessed +1
            progrmNode.decls.append(decl)
        return progrmNode,data
    except Exception as error:
        import traceback
        print(traceback.format_exc())
        print_error(error.args[1],error.args[0])


def print_error(erroneousToken,errormessage):
    global data
    print("\n*** Error line {0}.".format(erroneousToken.lineno))
    insert_string = get_insert_string(erroneousToken)
    bposition,aposition = get_newline_position(erroneousToken.lexpos)
    data1 = data[bposition:aposition] + insert_string
    print(data1)
    print(errormessage)

def get_newline_position(postion):
    global data
    bcounter = acounter = postion
    for d in data[postion:]:
        if d=='\n':
            break
        acounter = acounter + 1

    for d in data[:postion][::-1]:
        if d=='\n':
            break
        bcounter = bcounter - 1

    return bcounter,acounter

def get_insert_string(token):
    insert_string = "\n"
    position = mylexer.find_column_start(data, token)
    for i in range(0,position-1):
        insert_string += " "
    for j in range(0,len(token.value)):
        insert_string += "^"
    return insert_string

if __name__ == "__main__":
    tokens = gettoken()
    progrmNode = parseTokens(tokens)
    ag.print_ast(progrmNode, tokens)

