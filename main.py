import graphviz
from lexer import Lexer


def read_file(filename):
    with open(filename, 'r') as file_object:
        return file_object.read()


def validate_token(token):
    if "'" in token:
        token = token.replace("'", "\"")
    return token


def extract_tokens(rules):
    tokens = []
    for line in rules.strip().splitlines():
        if len(line) > 0:
            tokens = extract_tokens_from_line(line, tokens)
    return tokens

#Eliminar comentarios
def extract_tokens_from_line(line, tokens):
    if '(*' in line:
        line = line[:line.find('(*')].strip()
    if 'rule' not in line:
        if '|' not in line and '{' not in line:
            token = validate_token(line.strip())
            if token != "":
                tokens.append(token)
        # case 2: token and action are specified
        elif '|' not in line and '{' in line:
            token = validate_token(line[:line.find('{')].strip())
            if token != "":
                tokens.append(token)
        # case 3: token and next state are specified
        elif '|' in line and '{' in line:
            token = validate_token(
                line[line.find('|')+1:line.find('{')].strip())
            if token != "":
                tokens.append(token)
    return tokens


def get_child_nodes(parent_position, tree):
    children = []
    for i in range(parent_position - 1, -1, -1):
        if not tree[i].visto and len(children) < 2:
            children.append(i)
    return children


def extract_variables(variables):
    variablesArray = []
    for line in variables.strip().splitlines():
        if len(line) > 0:
            if '(*' in line:
                line = line[:line.find('(*')].strip()
            if len(line) > 0:
                variablesArray.append(line)
    return variablesArray


def is_regex(variableValue):
    if variableValue[0] == '[' and variableValue[-1] == ']':
        return False
    return True


def format_variables(variables):
    # This function takes a list of variables and returns a list of dictionaries containing the name, value and whether or not the value is a regex
    variablesArray = []
    for var in variables:
        equalIndex = var.find('=')
        # get the index of the "=" sign
        varName = var[:equalIndex].strip()
        # get the name of the variable by getting everything before the "=" sign
        varValue = var[equalIndex+1:].strip()
        # get the value of the variable by getting everything after the "=" sign
        varFinalName = var[var.find('let')+3:equalIndex].strip()
        # get the name of the variable by getting everything between "let" and the "=" sign
        isRegex = is_regex(varValue)
        # check if the variable value is a regex
        if isRegex:
            varValue = [varValue]
        variablesArray.append(
            {"varName": varFinalName, "varValue": varValue, "isRegex": isRegex})
        # append the variable to the list of dictionaries
    return variablesArray


def get_values(input_str):
    output = ['(']
    if input_str[0] == '[' and input_str[-1] == ']':
        input_str = input_str[1:-1]
        if "'" in input_str:
            input_str = input_str.replace("'", "")
        if '"' in input_str:
            input_str = input_str.replace('"', "")
        if '-' in input_str:
            input_str = input_str.split('-')

            # validate if case there are 2 ranges like ['A'-'Z''a'-'z']
            if len(input_str) > 2:
                for i in range(len(input_str)):
                    # check if the current element length is 1
                    if len(input_str[i]) != 1:
                        # split the current element and add it to the array
                        input_str[i] = [input_str[i][0], input_str[i][1]]
                        input_str = input_str[:i] + \
                            input_str[i] + input_str[i+1:]

                # loop through the array by pairs and get the values between the ranges and add them to the output array
                for i in range(0, len(input_str), 2):
                    start = input_str[i]
                    end = input_str[i+1]
                    if start.isalpha() and end.isalpha():
                        start = ord(start)
                        end = ord(end)
                        for i in range(start, end+1):
                            if (chr(i).isalpha()):
                                output.append(chr(i))
                                output.append('|')
                    else:
                        start = int(start)
                        end = int(end)
                        for i in range(start, end+1):
                            output.append(str(i))
                            output.append('|')
            elif len(input_str) == 2:
                # ['A'-'Z']
                start = input_str[0]
                end = input_str[1]
                if start.isalpha() and end.isalpha():
                    start = ord(start)
                    end = ord(end)
                    for i in range(start, end+1):
                        if (chr(i).isalpha()):
                            output.append(chr(i))
                            output.append('|')
                else:
                    start = int(start)
                    end = int(end)
                    for i in range(start, end+1):
                        output.append(str(i))
                        output.append('|')

        else:
            # ['A''B''C']
            ignore_index = []
            for i in range(len(input_str)):
                # check if the current element is not in the ignore index array
                if i not in ignore_index:
                    # check if the current element has a backslash
                    if input_str[i] == '\\':
                        # if the current element has a backslash, add the next element to the output array
                        output.append(f"'{input_str[i] + input_str[i+1]}'")
                        output.append('|')

                        # add the next element index to the ignore index array
                        ignore_index.append(i+1)
                    else:
                        # if the current element has not a backslash, add it to the output array
                        output.append(f"'{input_str[i]}'")
                        output.append('|')
    output.pop()
    output.append(')')
    return output


def get_rules(text):
    rulesIndex = text.find('rule')
    return text[rulesIndex:]


def get_variables(text):
    rulesIndex = text.find('rule')
    return text[:rulesIndex]


def flatten_array(array):
    new_array = []
    for Lexer in array:
        if type(Lexer) == list:
            new_array += flatten_array(Lexer)
        else:
            new_array.append(Lexer)
    return new_array


def clean_variables(variables):
    newVariables = []
    for variable in variables:
        if variable["isRegex"]:
            if "''" in variable["varValue"][0]:
                variable["varValue"][0] = variable["varValue"][0].replace(
                    "''", "','")
            if "[" in variable["varValue"][0]:
                variable["varValue"][0] = variable["varValue"][0].replace(
                    "[", "(")
            if "]" in variable["varValue"][0]:
                variable["varValue"][0] = variable["varValue"][0].replace(
                    "]", ")")
            variable["varValue"][0] = variable["varValue"][0].strip(
                "[]").split(',')
        newVariables.append(variable)

    for variable in newVariables:
        if variable["isRegex"]:
            originalValue = variable["varValue"][0]
            newValue = []
            for value in originalValue:
                newValue.append(value)
                if value != originalValue[-1]:
                    newValue.append('|')
            variable["varValue"] = newValue

    for variable in newVariables:
        if variable["isRegex"]:
            if variable["varName"] != 'delim':
                for i in range(len(variable["varValue"])):
                    variable["varValue"][i] = variable["varValue"][i].replace(
                        "'", "")

    for variable in newVariables:
        if variable["isRegex"] and variable["varName"] == "number":
            print(variable["varValue"])
            Lexers = []
            for Lexer in variable["varValue"]:
                if '+' in Lexer:
                    Lexer = Lexer.replace('+', '"+"')
                if '-' in Lexer:
                    Lexer = Lexer.replace('-', '"-"')
                Lexers.append(Lexer)
            if Lexers != []:
                variable["varValue"] = Lexers
    print(newVariables)
    return newVariables


def separate_regex_tokens(variables, productions):
    # print(productions)
    variables = clean_variables(variables)

    for var in variables:
        key = var["varName"]
        value = var["varValue"]
        if key != 'delim' and var["isRegex"]:
            i = 0
            while i < len(value):
                string = value[i]
                tokens = ['(']
                j = 0
                while j < len(string):
                    for word in productions:
                        if string.startswith(word, j):
                            tokens.append(string[j:j+len(word)])
                            j += len(word)
                            break
                    else:
                        tokens.append(string[j])
                        j += 1
                tokens.append(')')
                value[i] = tokens
                i += 1
    return variables


def change_variables_output(variables):

    for var in variables:
        if not var["isRegex"]:
            input_str = var["varValue"]
            output = get_values(input_str)
            var["varValue"] = output
        # var["varValue"] = var["varValue"][1:-1]

    return variables


def change_variables_regex_output(variables, productions):
    return separate_regex_tokens(variables, productions)


def get_value_by_key(variables, key):
    for var in variables:
        if var["varName"] == key:
            return flatten_array(var["varValue"])
    return None


def get_substitutions(variables, tokens, producciones):
    nt = []
    for t in tokens:
        nt.append(t)
        nt.append('|')
    nt.pop()
    tokens = nt
    tokens = ['('] + tokens + [')']
    while True:
        subs = False
        for tokenIndex in range(len(tokens)):
            if tokens[tokenIndex] in producciones:
                value = get_value_by_key(variables, tokens[tokenIndex])
                if type(value) is list:
                    tokens[tokenIndex] = value[0]
                    if len(value) > 1:
                        for i in range(1, len(value)):
                            tokens.insert(tokenIndex+i, value[i])
                    subs = True
                else:
                    tokens[tokenIndex] = value
                    subs = True
        if not subs:
            break
    return tokens


def concatenate_substitutions(substitutions):
    subs = []
    for Lexer in substitutions:
        subs.append(Lexer)
        subs.append('~')
    subs.pop()
    return subs


def fix_substitutions(substitutions):

    substitutions = concatenate_substitutions(substitutions)

    operators = ['+', '*', '?', '|', '(', ')']

    for index, Lexer in enumerate(substitutions):
        if Lexer == '~' and 0 < index < len(substitutions) - 1:
            prev_char = substitutions[index - 1]
            next_char = substitutions[index + 1]
            if (prev_char not in operators and next_char not in operators) or \
                (prev_char in ['*', '+', '?'] and next_char not in operators) or \
                    (prev_char in ['*', '+', '?', ')'] and next_char == '('):
                substitutions[index] = '~'
            else:
                substitutions[index] = ''
    for index, Lexer in enumerate(substitutions):
        if Lexer == '':
            # delete the Lexer
            del substitutions[index]

    for index, Lexer in enumerate(substitutions):
        if Lexer == '~' and 0 < index < len(substitutions) - 1:
            prev = substitutions[index - 1]
            nextt = substitutions[index + 1]
            if prev == '~':
                substitutions[index] = ''
                substitutions[index-1] = ''
            elif nextt == '~':
                substitutions[index] = ''
                substitutions[index+1] = ''

    return substitutions

# Funcion para parsear la expresion regular a notacion postfix
# param - expresion regular
# basado en el algoritmo de Shunting-yard
def parseRegexToPostfix(regex):
    outputQueue = []
    operatorStack = []
    operatorPrecedence = {"*": 3, "~": 2, "|": 1, "+": 3, "(": 0, ")": 0}

    for char in regex:
        if char == "(":
            operatorStack.append(char)
        elif char == ")":
            while operatorStack[-1] != "(":
                outputQueue.append(operatorStack.pop())
            operatorStack.pop()
        elif char in operatorPrecedence:
            while (
                operatorStack
                and operatorPrecedence[char] <= operatorPrecedence[operatorStack[-1]]
            ):
                outputQueue.append(operatorStack.pop())
            operatorStack.append(char)
        else:
            outputQueue.append(char)

    while operatorStack:
        outputQueue.append(operatorStack.pop())

    return outputQueue


def three_graph(postfix):
    f = graphviz.Digraph(name="arbolS")
    f.attr(rankdir='TB')
    arbol = []

    unary = ['*', '+', '?']
    binary = ['|', '~']
    for indice, valor in enumerate(postfix):
        arbol.append(Lexer(valor, indice))

    for nodo in arbol:
        f.node(str(nodo.id), label=str(nodo.value),
               shape="plaintext", style='filled', fillcolor='white')

    for position, leaf in enumerate(arbol):
        if leaf.value in unary:
            f.edge(str(leaf.id), str(arbol[get_child_nodes(
                position, arbol)[0]].id), arrowhead='vee')
            arbol[get_child_nodes(position, arbol)[0]].visto = True
        elif leaf.value in binary:
            f.edge(str(leaf.id), str(arbol[get_child_nodes(
                position, arbol)[1]].id), arrowhead='vee')
            f.edge(str(leaf.id), str(arbol[get_child_nodes(
                position, arbol)[0]].id), arrowhead='vee')
            arbol[get_child_nodes(position, arbol)[1]].visto = True
            arbol[get_child_nodes(position, arbol)[0]].visto = True

    f.render("ResultadoArbol", format="png", view="True")


def try_file(i):
    complete_text = read_file(f'tests/slr-{i}.yal')
    rules = get_rules(complete_text)
    tokens = extract_tokens(rules)
    operators = ['+', '*', '?', '|', '(', ')']
    for i in range(len(tokens)):
        if tokens[i] in operators:
            tokens[i] = "'" + tokens[i] + "'"

    print("Tokens: \n", tokens)

    variables_sections = get_variables(complete_text)
    variables_declarations = extract_variables(variables_sections)
    formated_variables = format_variables(variables_declarations)
    updated_variables = change_variables_output(formated_variables)
    for variable in updated_variables:
        print(variable["varName"], variable["varValue"])
        


    producciones = [x["varName"] for x in updated_variables]
    producciones.reverse()
    updated_variables = change_variables_regex_output(
        updated_variables, producciones)
    substitutions = get_substitutions(updated_variables, tokens, producciones)
    substitutions = fix_substitutions(substitutions)

    print("Regex final:\n")
    print(''.join(substitutions))
    postfix = parseRegexToPostfix(substitutions)

    three_graph(postfix)
    print("Postfix: \n")
    print(''.join(postfix))



try_file(2)
