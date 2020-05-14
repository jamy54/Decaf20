from __future__ import print_function

from myparser import gettoken,parseTokens
import SymaticAnalyzer
from CodeGenerator.CodeGenerator import CodeGenerator
import subprocess


def ExtractLine(data,lineNUmb):
    return data.splitlines()[lineNUmb-1]


def PrepareErrorString(er):
    ErrorString = ""
    for i in range(0,er.StartPos-1):
        ErrorString += " "
    for j in range(0,er.LastPos-er.StartPos):
        ErrorString += "^"
    return ErrorString

def print_error(anlyzer):
    for er in anlyzer.errorList:
        headMsg = "*** Error line {0}.".format(er.lineNumber)
        midgleMsg =  ExtractLine(data,er.lineNumber)
        errorString = PrepareErrorString(er)
        lastMsg = "*** {0}".format(er.Message)

        print()
        print(headMsg)
        print(midgleMsg)
        print(errorString)
        print(lastMsg)
        print()

    if not anlyzer.symbolTable.hasMainMethod():
        print()
        print("*** Error.")
        print("*** Linker: function 'main' not defined")
        print()
        return True
    return False or len(anlyzer.errorList) != 0


def RunAssembly(assCode):
    f = open("output.s", "w")
    f.write(assCode)
    f.close()
    out = subprocess.Popen(['./spim', '-file', 'output.s'],stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    stdout, stderr = out.communicate()
    print(stdout)
    #print(stderr)



if __name__ == "__main__":
    tokens = gettoken()
    progrmNode,data = parseTokens(tokens)
    anlyzer = SymaticAnalyzer.Analyzer(progrmNode,tokens,data)
    error = print_error(anlyzer)

    if not error:
        assemblyCode = CodeGenerator(progrmNode,tokens,data,anlyzer.symbolTable)
        #print(assemblyCode.assCode)
        RunAssembly(assemblyCode.assCode)
