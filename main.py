#que debe hacer el laboratorio d?
# 1. leer el archivo de entrada .yal
# 2. Generar una expresion regular del .yal 
# 3. Convertir la expresion regular a un AFD DIRECTO O UN AFN AUN NO SE
# 4. Graficar el automata generado
# 5. Leer el archivo de entrada .txt
# 6. Validar la cadena de entrada con el automata generado
# 7. Imprimir los tokens encontrados
# 8. Implementar reconocimiento de errores
# 9. Si hay errores, imprimirlos

from lexer import Lexer

def main():
    filename = 'slr-1.yal'
    lexer = Lexer(filename)
    # Continúe con el análisis léxico del archivo utilizando la instancia de lexer

if __name__ == '__main__':
    main()