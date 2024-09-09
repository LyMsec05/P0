### Programa para iniciar la implementacion basica de un lexer y parser en python.
### Por favor escribir el nombre del archivo a parsear (que esté en el workspace). 

import basic

archivo = 'archivo.txt'

def leer_txt(path):
    with open(path, 'r') as file:
        contenido = file.read()
        print(contenido)
        return (contenido)
    

text = leer_txt(archivo)
result, error, ToF_parse = basic.run('<stdin>', text)

if error: 
    print(error.as_string())
else: 
    print(result)
    print(ToF_parse)