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
import re
from yallexer import *
from InfixToPost.infixtopostfix import *
from AFN.afn import *
from Graph.graph import graph

lexer = YalLexer('ex/slr-1.yal')
expresion = lexer.final_expression
expresiongenerada = print("Expresion generada:", expresion)
patron = r'(\w+|\s+\s+)'
expresion_modificada = re.sub(patron, r'\1_', expresion)
print("Expresion modificada:", expresion_modificada)

#alphabet = getAlphabet(expresion)
#print("Alfabeto de la expresion", alphabet)
newexpresion = computableExpresion(expresion_modificada)
print("Expresion computable", newexpresion)
postfixexp = infixaPostfix(newexpresion)
print("Expresion en postfix", postfixexp)

#result = ThompsonAlgorithm(postfixexp)
#nfaDict = result.getDict()
#prueba = graph(postfixexp,result)
#transitions = prueba.createTransitions()
#transitions = prueba.createTransitions()
#prueba.graphic(transitions,"Thompson")
#s0 = result.getInitial()
#sf = result.getFinal()
#states = prueba.getStates()
#dictTrans = result.getDict()