"""
Reserved translation rules

The module will always check if the specific "<class>_<name>" name
exists before finding the generic "<class>" name.
"""

# List of function names that should be handled by reserved.py:
reserved = [
"eye", "flipud", "length", "max", "min", "size", "transpose",
"zeros", "round", "return", "rand", "floor", "pi", "conv_to",
]

# Common attribute

#  def Assignees(node):
#      node.parent["backend"] = "reserved"
#      return "", ", ", ""

def Declare(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")

def Var(node):
    raise ValueError("Variable name '%s' is reserved."%node["name"]\
            +"\nPlease rename variable.")


def Var_pi(node):
    return "datum::pi"

def Var_return(node):
    if node.func["backend"] == "func_returns":
        return "%(name)s"
    return "%(name)s " + str(node.func[0])

def Get_size(node):

    type = node[0].type()
    if len(node) > 1:

        node.type("int")
        arg2 = node[1]["value"]
        var = node[0]
        if arg2 == "1":
            return var+".n_rows"
        if arg2 == "2":
            return var+".n_cols"
        if arg2 == "3":
            return var+".n_slice"

    elif type in ("ivec", "fvec", "irowvec", "frowvec"):
        node.type("int")
        return node[0]+".n_elem"

    elif type in ("fmat", "imat"):
        node.type("ivec")
#          node.replace("int", node[0]+".n_rows", node[0]+".n_cols")

        return "{%(0)s.n_rows, %(0)s.n_cols}"

    elif type == "TYPE":
        return "size(%(0)s)"

    name = node["name"]
    node.error(
            "'size(%s)'\t\t illigal type (%s)" \
                    % (name, type))

    return "<error:size(%(0)s)>"

def Assigns_size(node):

    if len(node[0])==2:

        for n in node[0]:
            n.suggest("int")

        if len(node[1]) == 0:
            val = str(node[1])
        else:
            val = str(node[1][0])

        return "%s = %s.n_rows ;\n%s = %s.n_cols ;" % \
                (node[0][0], val, node[0][1], val)

    if len(node[0])==3:

        for n in node[0]:
            n.suggest("int")

        if len(node[1]) == 0:
            val = str(node[1])
        else:
            val = str(node[1][0])
        rows, cols, slices = map(str, node[0])
        return  rows+" = "+val+".n_rows ;\n"+\
                cols+" = "+val+".n_cols ;\n"+\
                slices+" = "+val+".n_slice ;"

    raise NotImplementedError

def Get_length(node):
    node.type("int")
    return "%(0)s.n_elem"


def Get_min(node):

    if len(node) == 1:

        typ = node[0].type()
        if typ in ("imat", "fmat"):
            node.type("ivec")
        elif typ in ("ivec", "fvec", "irow", "frow"):
            node.type("int")

        return "arma::min(%(0)s)"

    if len(node) == 2:
        if node[0].type() in ("int", "float") and\
                node[1].type() in ("int", "float"):
            return "(%(0)s<%(1)s?%(0)s:%(1)s)"
        return "arma::min(%(0)s, %(1)s)"

    if len(node) == 3:

        if node[2].type() == "int":

            val = node[2]["value"]
            if val == "1":
                node.type("irowvec")
            elif val == "2":
                node.type("ivec")
            else:
                raise NotImplementedError

            return "arma::min(%(0)s, %(2)s-1)"

def Assigns_min(node):
    m_val = node[0][0]["name"]
    m_ind = node[0][1]["name"]
    type = node[1].type()

    return m_val + " = %(1)s.min("+m_ind+") ;\n"



def Get_max(node):

    if len(node) == 1:

        typ = node[0].type()
        if typ in ("imat", "fmat"):
            node.type("ivec")
        elif typ in ("ivec", "fvec", "irowvec", "frowvec"):
            node.type("int")

        return "arma::max(%(0)s)"

    if len(node) == 2:
        if node[0].type() in ("int", "float") and\
                node[1].type() in ("int", "float"):
            return "(%(0)s<%(1)s?%(1)s:%(0)s)"
        return "arma::max(%(0)s, %(1)s)"

    if len(node) == 3:

        if node[2].type() == "int":

            val = node[2]["value"]
            if val == "1":
                node.type("irowvec")
            elif val == "2":
                node.type("ivec")
            else:
                raise NotImplementedError

            return "arma::max(%(0)s, %(2)s-1)"

    raise NotImplementedError

def Assigns_max(node):
    m_val = node[0][0]["name"]
    m_ind = node[0][1]["name"]
    type = node[1].type()

    return m_val + " = %(1)s.min("+m_ind+") ;\n"

Var_eye = "1"
def Get_eye(node):

    if len(node) == 1:
        type = node[0].type()
        if type in ("float", "int"):
            return "arma::eye<mat>(%(0)s, %(0)s)"
        return "arma::eye<mat>(%(0)s(0), %(0)s(1))"

    if len(node) == 2:
        return "arma::eye<mat>(%(0)s, %(1)s)"

    raise NotImplementedError

def Get_transpose(node):
    type = node.type()
    if type == "fvec":      node.type("frowvec")
    elif type == "ivec":    node.type("irowvec")
    elif type == "frowvec": node.type("fvec")
    elif type == "irowvec": node.type("ivec")

    return "arma::trans(%(0)s)"


def Get_flipud(node):
    return "arma::flipud(%(0)s)"


def Get_zeros(node):

    if len(node) == 1:
        node.type("fvec")
        return "arma::zeros<fvec>(%(0)s)"
    if len(node) == 2:
        node.type("fmat")
        return "arma::zeros<fmat>(%(0)s, %(1)s)"
    if len(node) == 3:
        return "arma::zeros<fcube>(%(0)s, %(1)s, %(2)s)"

    raise NotImplementedError

def Get_round(node):

    assert len(node)<3

    if len(node) == 2:
        decimals = str(node[1])
    else:
        decimals = "0"

    type = node[0].type()
    if type == "int":
        return "%(0)s"

    if type == "float":
        node.include("math")
        if decimals == "0":
            return "std::round(%(0)s)"
        return "std::round(%(0)s*std::pow(10, %(1)s))*std::pow(10, -%(1)s)"

    if decimals == "0":
        return "arma::round(%(0)s)"
    return "arma::round(%(0)s*std::pow(10, %(1)s))*std::pow(10, -%(1)s)"

def Var_rand(node):
    node.type("float")
    return "arma::randu(1)"

def Get_rand(node):

    type = node[0].type()
    if type == "TYPE":
        for c in node: c.suggest("int")
        return "arma::randu<TYPE>(", ", ", ")"

    if len(node) == 1:
        node.type("fvec")
        return "arma::randu<fvec>(%(0)s)"

    elif len(node) == 2:
        node.type("fmat")
        return "arma::randu<fmat>(%(0)s, %(1)s)"
    else:
        raise NotImplementedError

def Get_floor(node):

    type = node[0].type()
    if type == "float":     node.type("int")
    elif type == "fvec":    node.type("ivec")
    elif type == "frowvec": node.type("irowvec")
    elif type == "fmat":    node.type("imat")

    return "arma::floor(%(0)s)"


def Get_conv_to(node):
    return "conv_to<%(type)s>::from(%(0)s)"

