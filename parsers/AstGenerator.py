from __future__ import print_function

tokens = None

def variable_printer(tabindex,data):
    print_string(tabindex, "Type: {0}".format(data.type.token.value))
    print_string(tabindex, "Identifier: {0}".format(data.identifier),tokens[data.tokenPosition].lineno)

def print_ast(progrmNode,tokens2):
    global tokens
    tokens = tokens2
    print("\nProgram:")
    for decl in progrmNode.decls:
        if decl.isVariableDecl:
            print_string(1,"VarDecl:",tokens[decl.variableDecl.tokenPosition].lineno)
            variable_printer(2,decl.variableDecl.variable)
        else:
            print_string(1,"FnDecl:",tokens[decl.functionDecl.tokenPosition].lineno)
            print_function(2,decl.functionDecl)
    pass


def print_string(number_of_tab, data,lineno=""):
    tabs = ""
    for i in range(0,number_of_tab):
        tabs +="\t"
    print(lineno,tabs,data)

def print_function(tabindex,functionDecl):
    print_string(tabindex, "(return type) Type: {0}".format(functionDecl.type))
    print_string(tabindex, "Identifier: {0}".format(functionDecl.identifier),tokens[functionDecl.tokenPosition].lineno)
    if functionDecl.hasFormals:
        print_formals(tabindex,functionDecl.formals)
    print_string(tabindex, "(body) StmtBlock:")
    print_stmt_block(tabindex+1,functionDecl.stmtBlock)


def print_whileStmt(tabindex, stmt):
    print_string(tabindex, "WhileStmt:")
    print_expression(tabindex+1, stmt.wStmt.exp,"(test) ")
    if len(stmt.wStmt.stmt.stmtblock.stmts) >0:
        print_string(tabindex+1, "(body) StmtBlock:")
        print_stmt_block(tabindex+2, stmt.wStmt.stmt.stmtblock)


def print_ifStmt(tabindex, stmt):
    print_string(tabindex, "IfStmt:")
    print_expression(tabindex+1, stmt.ifStmt.exp, "(test) ")
    if stmt.ifStmt.ifstmt.__class__.__name__ == "StmtBlock":
        print_stmt_block(tabindex + 1, stmt.ifStmt.ifstmt)
    else:
        choose_stmt(tabindex+1, stmt.ifStmt.ifstmt,"(then) ")
    if stmt.ifStmt.hasElse:
        if stmt.ifStmt.elstmt.__class__.__name__ == "StmtBlock":
            print_stmt_block(tabindex + 1, stmt.ifStmt.elstmt)
        else:
            choose_stmt(tabindex + 1, stmt.ifStmt.elstmt, "(else) ")


def print_stmt_block(tabindex,stmtBlock):
    for vardecl in stmtBlock.variableDecls:
        print_string(tabindex, "VarDecl:",tokens[vardecl.variable.tokenPosition].lineno)
        variable_printer(tabindex+1, vardecl.variable)

    for stmt in stmtBlock.stmts:
        choose_stmt(tabindex,stmt)


def print_break(tabindex,lineno, header=""):
    print_string(tabindex,header+"BreakStmt:",lineno)


def print_for(tabindex, forstmt):
    print_string(tabindex, "ForStmt:")
    if forstmt.hasFirstExp:
        print_expression(tabindex+1, forstmt.firstexp, "(init) ")
    else:
        print_string(tabindex+1,"(init) Empty:")
    print_expression(tabindex+1, forstmt.middleexp, "(test) ",tokens[forstmt.middleexp.tokenPosition].lineno)
    if forstmt.hasLastExp:
        print_expression(tabindex+1, forstmt.lastexp, "(step) ",tokens[forstmt.lastexp.tokenPosition].lineno)
    else:
        print_string(tabindex+1,"(step) Empty:")

    if forstmt.stmt.__class__.__name__ == "StmtBlock":
        print_string(tabindex, "(body) StmtBlock:")
        print_stmt_block(tabindex + 1, forstmt.stmt)
    else:
        choose_stmt(tabindex + 1, forstmt.stmt, "(else) ")


def choose_stmt(tabindex,stmt,header=""):
    if stmt.stmtType == "print":
        print_printStmt(tabindex, stmt)
    elif stmt.stmtType == "return":
        print_returnStmt(tabindex, stmt)
    elif stmt.stmtType == "while":
        print_whileStmt(tabindex, stmt)
    elif stmt.stmtType == "if":
        print_ifStmt(tabindex, stmt)
    elif stmt.stmtType == "exp":
        print_expression(tabindex, stmt.exp,header)
    elif stmt.stmtType == "break":
        print_break(tabindex,tokens[stmt.tokenPosition].lineno,header)
    elif stmt.stmtType == "for":
        print_for(tabindex,stmt.fStmt)
    elif stmt.stmtType == "block":
        print_string(tabindex, "(body) StmtBlock:")
        print_stmt_block(tabindex+1,stmt.stmtblock)

def print_returnStmt(tabindex,stmt):
    print_string(tabindex, "ReturnStmt:",tokens[stmt.rStmt.tokenPosition].lineno)
    if stmt.rStmt.hasExp:
        print_expression(tabindex+1,stmt.rStmt.exp)
    else:
        print_string(tabindex+1,"Empty:")

expression_types = ["ArithmeticExpr","LogicalExpr","RelationalExpr","AssignExpr","EqualityExpr"]

def print_different_expression(tabindex,value):
    if value is None:
        return
    if value.type in expression_types:
        print_expression(tabindex, value)
    elif value.type == "FieldAccess":
        print_fieldAccess(tabindex, value)
    elif value.type == "readinteger":
        print_string(tabindex, "ReadIntegerExpr:",value.tok.lineno)
    elif value.type in ["IntConstant", "BoolConstant", "DoubleConstant", "StringConstant"]:
        print_string(tabindex, "{0}: {1}".format(value.type, value.val),value.token.lineno)

def print_expression(tabindex,exp,expressionHeader="",header=""):
    if exp.type == "constant":
        print_string(tabindex, "(args) {0}: {1}".format(exp.value.type, exp.value.val),exp.value.token.lineno)
    elif exp.type == "fieldaccess":
        print_fieldAccess(tabindex, exp.value,expressionHeader)
    elif exp.type in expression_types:
        obj = get_obj(exp)
        print_string(tabindex, expressionHeader + exp.type + ":",tokens[exp.tokenPosition].lineno)
        print_different_expression(tabindex+1,obj.lvalue)
        print_string(tabindex+1, "Operator: {0}".format(obj.operator),tokens[obj.tokenPosition].lineno)
        print_different_expression(tabindex+1,obj.rvalue)

    elif exp.type == "caller":
        print_string(tabindex, expressionHeader +" Call:",tokens[exp.value.tokenPosition].lineno)
        print_string(tabindex + 1, "Identifier: {0}".format(exp.value.identifier),tokens[exp.value.tokenPosition].lineno)
        if exp.value.hasExp:
            for sExp in exp.value.exps:
                print_expression(tabindex + 1, sExp,"(actuals) ",tokens[sExp.tokenPosition].lineno)

def get_obj(exp):
    if hasattr(exp, 'value'):
        return exp.value
    return exp


def print_fieldAccess(tabindex,fieldaccess,header=""):
    print_string(tabindex, header+" FieldAccess:",tokens[fieldaccess.tokenPosition].lineno)
    print_string(tabindex +1, "Identifier: {0}".format(fieldaccess.identifier),tokens[fieldaccess.tokenPosition].lineno)

def print_printStmt(tabindex,stmt):
    print_string(tabindex, "PrintStmt:")
    for exp in stmt.pStmt.exps:
        print_expression(tabindex +1,exp,"(args)")

def print_formals(tabindex,formals):
    for v in formals:
        print_string(tabindex, "(formals) VarDecl:",tokens[v.tokenPosition].lineno)
        variable_printer(tabindex+1, v)