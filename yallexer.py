class YalLexer:
    def __init__(self, filename):
        # Constructor de la clase. Recibe un nombre de archivo (nombre completo y ruta) que contiene las reglas para
        # el lexer YAL.
        # Inicializa las variables de la clase, extrae las reglas del archivo, genera los regex para cada regla y
        # crea el regex final para el lexer.
        self.filename = filename
        self.reglas = {}
        self.tokensitos = {}
        self.operators = set()
        self.extraerReglas()
        self.tokensitossolos()
        self.GenerarRegex()

    def tokensitossolos(self):
        # Genera un diccionario con el nombre de cada regla y su correspondiente regex.
        for reglanombre, regexgenerable in self.reglas.items():
            updateRule = self.replacereglas(regexgenerable)
            expanded_rule = self.handleChars(updateRule)
            self.tokensitos[reglanombre] = expanded_rule

    def extraerReglas(self):
        # Extrae las reglas del archivo y las guarda en un diccionario.
        with open(self.filename, "r") as filename:
            lines = filename.readlines()
            for line in lines:
                if line.startswith("let"):
                    reglanombre, regladesc = self.getRule(line)
                    regexgenerable = self.convertRegex(regladesc)
                    self.reglas[reglanombre] = regexgenerable

    def GenerarRegex(self):
        # Crea el regex final para el lexer YAL a partir de los regex de cada regla.
        self.regex = self.creadorderegex()
        self.final_expression = self.handleChars(self.regex)

    def creadorderegex(self):
        # Crea el regex final con las reglas definidas. 
        regex = ""
        operators = set()
        in_rule_tokens = False
        operator_reglas = {}  

        with open(self.filename, "r") as filename:
            lines = filename.readlines()
            for line in lines:

                start_index = 0
                end_index = len(line) - 1

                while start_index < len(line) and line[start_index] in (" ", "\t"):
                    start_index += 1

                while end_index >= 0 and line[end_index] in (" ", "\t"):
                    end_index -= 1

                line = line[start_index:end_index + 1]


                comment_start1 = "(*"
                comment_end1 = "*)"
                comment_start2 = "{"
                comment_end2 = "}"

                if len(line) >= len(comment_start1) and len(line) >= len(comment_end1) and line[:len(comment_start1)] == comment_start1 and line[-len(comment_end1):] == comment_end1:
                    continue
                if len(line) >= len(comment_start2) and len(line) >= len(comment_end2) and line[:len(comment_start2)] == comment_start2 and line[-len(comment_end2):] == comment_end2:
                    continue

                if line.startswith("rule tokens"):
                    in_rule_tokens = True

                    if 'id' in self.tokensitos:
                        operator_reglas['id'] = self.tokensitos['id']


                    if 'ws' in self.tokensitos:
                        operator_reglas['ws'] = self.tokensitos['ws']


                    if 'digit' in self.tokensitos:
                        operator_reglas['digit'] = self.tokensitos['digit']


                    if 'letter' in self.tokensitos:
                        operator_reglas['letter'] = self.tokensitos['letter']


                    if 'operators' in self.tokensitos:
                        operator_reglas['operators'] = self.tokensitos['operators']

                elif in_rule_tokens:
                    operator_line = line.lstrip()
                    if operator_line.startswith('|'):
                        operator_line = operator_line[1:]
                        while operator_line[0] in (' ', '\t'):
                            operator_line = operator_line[1:]

                    operator = ""
                    for c in operator_line:
                        if c in (' ', '\t'):
                            break
                        operator += c

                    if operator:
                        operators.add(operator)

                    rule_name = ""
                    for c in operator_line[len(operator):]:
                        if c == " ":
                            continue
                        rule_name += c

                    if rule_name.strip() in self.tokensitos:
                        operator_reglas[operator] = self.tokensitos[rule_name.strip()]

                    if operator_line.startswith("let") or operator_line.startswith("rule"):
                        in_rule_tokens = False
                elif not in_rule_tokens:
                    continue

        self.operators = operators

        for operator, regexgenerable in operator_reglas.items():
            regex += regexgenerable + "|"

        return regex[:-1]


    def getRule(self, line):
        # Obtiene el nombre y la descripción de una regla a partir de una línea del archivo.
        partition_index = -1
        for i, c in enumerate(line):
            if c == '=':
                partition_index = i
                break

        reglanombre = self.removeSpaces(line[4: partition_index])
        regladesc = self.removeSpaces(line[partition_index + 1:])


        return reglanombre, regladesc


    def removeSpaces(self, s):
        # Elimina los espacios en blanco al inicio y al final de una cadena, y los apóstrofos (') que la encierran.
        result = ""
        in_single_quotes = False
        in_double_quotes = False
        escape_next = False
        for c in s:
            if c == "\\" and not escape_next:
                escape_next = True
                result += c
                continue

            if escape_next:
                escape_next = False
                result += c
                continue

            if c == "'":
                in_single_quotes = not in_single_quotes
            if c == '"':
                in_double_quotes = not in_double_quotes
            if not c.isspace() or in_single_quotes or in_double_quotes:
                if c != "'":
                    result += c
        return result


    def expandExp(self, expression):
        # Expande una expresión regular que contiene rangos de caracteres, en una cadena con todos los caracteres.
        expanded = []
        i = 0
        while i < len(expression):
            if expression[i] == '\\':
                if expression[i+1] == 't':
                    expanded.append(f'\t')
                elif expression[i+1] == 'n':
                    expanded.append(f'\n')
                else:
                    expanded.append(expression[i:i+2])
                i += 2
            elif i + 2 < len(expression) and expression[i + 1] == '-':
                start_char = expression[i]
                end_char = expression[i + 2]
                if (start_char.isupper() and end_char.isupper()) or (start_char.islower() and end_char.islower()) or (start_char.isdigit() and end_char.isdigit()):
                    for char_code in range(ord(start_char), ord(end_char) + 1):
                        expanded.append(chr(char_code))
                else:
                    expanded.append(expression[i])
                i += 3
            else:
                expanded.append(expression[i])
                i += 1
        return expanded


    def handleChars(self, rule_body):
        # Elimina los caracteres especiales (escapados con una diagonal invertida) en una regla, y maneja las clases
        # de caracteres en el regex.
        result = ""
        i = 0
        while i < len(rule_body):
            if rule_body[i] == '\\':
                if rule_body[i+1] == 't':
                    result += f'\\t'
                elif rule_body[i+1] == 'n':
                    result += f'\\n'
                elif rule_body[i+1] == 's':
                    result += f'\\s'
                else:
                    result += '\\\\' + rule_body[i+1]
                i += 2
            elif rule_body[i] == '[':
                i += 1
                inside_brackets = ""
                while rule_body[i] != ']':
                    inside_brackets += rule_body[i]
                    i += 1
                expanded_exp = self.expandExp(inside_brackets)
                result += '(' + '|'.join(expanded_exp) + ')'
                i += 1
            else:
                result += rule_body[i]
                i += 1
        return result



    def replacereglas(self, regexgenerable):
        # Reemplaza las reglas definidas en la descripción de otra regla por su correspondiente regex, en una regla
        # dada.
        sorted_rule_names = sorted(self.reglas.keys(), key=len, reverse=True)
        for reglanombre in sorted_rule_names:
            regladesc = self.reglas[reglanombre]
            updateRule = ""
            i = 0
            while i < len(regexgenerable):
                found = False
                if regexgenerable[i:].startswith(reglanombre):
                    next_char = regexgenerable[i + len(reglanombre):i + len(reglanombre) + 1]
                    if not next_char or not (next_char.isalnum() or next_char == '_'):
                        found = True
                        if regexgenerable[i + len(reglanombre):].startswith("†"):
                            if regladesc.startswith('(') and regladesc.endswith(')'):
                                updateRule += f"{regladesc}†"
                            else:
                                updateRule += f"({regladesc})†"
                            i += len(reglanombre) + 1
                        else:
                            updateRule += regladesc
                            i += len(reglanombre)
                if not found:
                    updateRule += regexgenerable[i]
                    i += 1
            regexgenerable = updateRule
        return regexgenerable


    def convertRegex(self, regladesc):
        # Convierte la descripción de una regla en una expresión regular.
        regladesc = self.handleChars(regladesc)
        regexgenerable = self.replacereglas(regladesc)

        expanded_rule = ""
        i = 0
        while i < len(regexgenerable):
            if regexgenerable[i] == '\\':
                expanded_rule += regexgenerable[i:i+2]
                i += 2
            elif regexgenerable[i] == '[':
                i += 1
                inside_brackets = ""
                while regexgenerable[i] != ']':
                    inside_brackets += regexgenerable[i]
                    i += 1
                expanded_exp = self.expandExp(inside_brackets)
                expanded_rule += '|'.join(expanded_exp)
                i += 1
            else:
                expanded_rule += regexgenerable[i]
                i += 1

        return expanded_rule


    def getFinalExp(self):
        # Retorna el regex final para el lexer YAL.
        return self.final_expression

    def getIndividualreglas(self):
        # Retorna un diccionario con cada regla y su correspondiente regex.
        return self.tokensitos
    

    def getOperators(self):
        # Retorna el conjunto de los caracteres que se definen como operadores en el archivo de reglas.
        return self.operators