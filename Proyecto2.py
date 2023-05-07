import re
import sys

# Función para leer el archivo de entrada y devolver su contenido como una cadena
def leer_archivo(nombre_archivo):
    with open(nombre_archivo, 'r') as archivo:
        return archivo.read()

# Función para dividir la entrada en tokens utilizando expresiones regulares
def dividir_tokens(entrada):
    # Expresión regular para reconocer tokens
    patron = re.compile(r'while|[a-z]|[0-9]|[<>=!]=|[<>=]|[{}();]|\s+')

    # Dividir la entrada en tokens
    tokens = patron.findall(entrada)

    # Eliminar espacios en blanco innecesarios
    tokens = [token.strip() for token in tokens if not token.isspace()]

    return tokens

# Función para validar si un bloque while está bien formado
def validar_while(tokens):
    pila = []

    for token in tokens:
        if token == 'while':
            pila.append(token)
        elif token == '{':
            if not pila or pila[-1] != 'while':  # Asegúrate de que haya elementos en la pila antes de acceder a ellos y verifica que el { vaya después de un while
                return False
            pila.append(token)
        elif token == '=':
            print("Hay un error en la comparación")
            return False
        elif token == '}':
            if len(pila) < 2 or pila[-1] != '{' or pila[-2] != 'while':  # Asegúrate de que haya suficientes elementos en la pila antes de acceder a ellos
                return False
            pila.pop()
            pila.pop()

    return not pila # regresa true si la pila está vacía


# Función para contar las variables y operadores de comparación utilizados en un bloque while
def contar_variables_y_operadores(tokens):
    print(tokens)
    variables = set()
    operadores = set()

    for i, token in enumerate(tokens):
        if token.isalpha() and len(token) == 1:
            variables.add(token)
        elif token in ['<', '>', '==', '>=', '<=', '!=']:
            operadores.add(token)
            

    return len(variables), operadores



def main():
    # Leer el nombre del archivo de entrada desde la línea de comandos o por medio de una ventana de dialogo
    if len(sys.argv) == 2:
        nombre_archivo = sys.argv[1]
    else:
        from tkinter import Tk, filedialog
        root = Tk()
        root.withdraw()
        nombre_archivo = filedialog.askopenfilename()

    # Leer el archivo de entrada
    entrada = leer_archivo(nombre_archivo)

    # Dividir la entrada en tokens
    tokens = dividir_tokens(entrada)

    # Variables para contar los resultados
    num_variables = 0
    num_operadores = 0
    num_whiles = 0



    operadores_globales = set()

    # Recorrer los tokens para buscar bloques while
    i = 0
    while i < len(tokens):
        if tokens[i] == 'while':
            # Contar el número de bloques while
            num_whiles += 1

            # Buscar el bloque de código dentro del while
            j = i + 1
            while j < len(tokens) and tokens[j] != '{':
                j += 1

            if j < len(tokens):
                # Encontramos un bloque while bien formado, validar su sintaxis
                k = j + 1
                pila = ['{']
                while k < len(tokens) and pila:
                    if tokens[k] == '{':
                        pila.append('{')
                    elif tokens[k] == '}':
                        pila.pop()
                    k += 1

            # Extraer el bloque de código dentro del while
            bloque_while = tokens[i:k]

            # Contar variables y operadores en el bloque while actual
            var_count, op_set = contar_variables_y_operadores(bloque_while)
            num_variables += var_count
            operadores_globales.update(op_set)

            # Mover el índice a la posición después del bloque while analizado
            i = k - 1

        # Mover al siguiente token
        i += 1

    # Imprimir los resultados
    print("Número total de variables utilizadas:", num_variables)
    print("Número total de operadores de comparación distintos:", len(operadores_globales))
    print("Número total de whiles encontrados:", num_whiles)


if __name__ == "__main__":
    main()
