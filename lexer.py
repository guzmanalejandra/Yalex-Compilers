import re


class Lexer():
    def __init__(self):
        # Lista para almacenar los tokens
        self.tokens = []

    def getTokens(self, archivo):
        # Abrir el archivo YALex.txt
        with open(archivo, 'r') as f:
            # Leer todas las líneas del archivo
            lines = f.readlines()

        # Expresión regular para extraer el nombre y la expresión regular de cada token
        token_regex = r"let\s+([a-zA-Z0-9]+)\s+=\s+(.*)$"

        # Recorrer todas las líneas del archivo
        for line in lines:
            # Buscar las líneas que contienen definiciones de tokens
            match = re.match(token_regex, line.strip())
            if match:
                # Extraer el nombre y la expresión regular del token
                name = match.group(1)
                regex = match.group(2)
                # Agregar el token a la lista de tokens
                self.tokens.append((name, regex))
