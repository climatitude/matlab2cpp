Declare = "int %(name)s ;"
Int = "%(value)s"
Var = "%(name)s"

def Assign(node):
    node[0].suggest("int")
    return "%(0)s = %(1)s ;"
