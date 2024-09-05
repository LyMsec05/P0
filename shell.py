#PRIMERO: CREAR UN LEXER
# 1. El lexer revisara caracter por caracter y 
# divide el texto en una lista que lo llamamos tokens.
# 2. El token es un objeto simple que tiene un tipo y opcionalmente un valor.
import basic

while True:
    text = input('codigo-> ')
    result, error, parsed = basic.run('<stdin>', text)

    if error: print(error.as_string())
    else: 
        print(result)
        print(parsed)
    