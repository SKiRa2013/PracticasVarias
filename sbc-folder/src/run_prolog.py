from pyswip import Prolog
import os, sys

prolog = Prolog()

def get_prolog_file(prolog_file: str):
    os.system("cls" if os.name == "nt" else "clear")
    prolog_file = f"{os.path.abspath(os.path.dirname(__file__))}/{prolog_file}"

    try:
        prolog.consult(prolog_file)
    except Exception as e:
        print(f"Hubo un error al cargar el archivo {prolog_file}: {e}")
        return


def prolog_fibo(prolog_query: str):
    get_prolog_file("fibo.pl")

    fib_pos = "NotFiboPos"
    
    while not isinstance(fib_pos, int):        
        try:
            list(prolog.query("fibonacci(0, F)")) # consulta de prueba
            
            fib_pos = int(input("Ingrese la posición del fibonacci a revisar: \n"))
            
            if fib_pos < 1:
                fib_pos = int("OutOfBoundFiboPos")
            
        except ValueError:
            fib_pos = "NotFiboPos"
            os.system("cls" if os.name == "nt" else "clear")
            
        except Exception as e:
            print(f"Error al ejecutar Prolog: {e}")
      
    if prolog_query == "fibonacci":
        msg_resultado = f"El fibonacci en la posición {fib_pos} es"
   
    elif prolog_query == "fibonacci_list":
        msg_resultado = f"Los fibonacci hasta la posición {fib_pos} son"
   
    else:
        print("QUERY INCORRECTO, ERROR")
        raise TypeError("IncorrectQueryType") 
    
    query_result = {
        "fibonacci": "F",
        "fibonacci_list": "Lista"
    }
        
    for result in prolog.query(f"{prolog_query}({fib_pos-1}, {query_result[prolog_query]})"):
        print(f"{msg_resultado} {result[query_result[prolog_query]]}\n")
        
    input("Presiona ENTER para continuar...")


def prolog_cumples(prolog_query: str):
    get_prolog_file("cumples.pl")
    
    if prolog_query == "obtener_cumples":
        list(prolog.query(f"{prolog_query}"))
        
        print("")
        input("Presiona ENTER para continuar...")
        
        return
    
    if prolog_query == "buscar_cumple":
        persona = input("Ingrese el nombre de la persona a buscarle el cumpleaños (Formato: nombre apellido):\n").split(" ")
        print("")
        
        if len(persona) != 2:
            print("FORMATO INCORRECTO, ERROR")
            raise TypeError("IncorrectQueryArgument")
        
        list(prolog.query(f"{prolog_query}({persona[0]}, {persona[1]})"))
        
        print("")
        input("Presiona ENTER para continuar...")
        
        return    
    
    print("QUERY INCORRECTO, ERROR")
    raise TypeError("IncorrectQueryType")    
     
        
def prolog_repite(prolog_query: str):
    get_prolog_file("repita.pl")
    
    if prolog_query == "escriba":
        list(prolog.query(f"{prolog_query}"))
        
        print("")
        input("Presiona ENTER para continuar...")
        
        return
    
    print("QUERY INCORRECTO, ERROR")
    raise TypeError("IncorrectQueryType")


def prolog_factorial(prolog_query: str):
    get_prolog_file("factorial.pl")
    
    if prolog_query == "factorial":
        fact_number = -1
        
        while fact_number == -1:
            try:
                fact_number = int(input("Ingrese un número al que aplicarle factorial:\n"))
                
                print("")
                
                for result in prolog.query(f"{prolog_query}({fact_number}, Fact)"):
                    print(f"{fact_number}! = {result['Fact']}")
                    
                print("")    
                input("Presiona ENTER para continuar...")
                return
                
            except ValueError:
                os.system("cls" if os.name == "nt" else "clear")
                fact_number = -1
                
    print("QUERY INCORRECTO, ERROR")
    raise TypeError("IncorrectQueryType")
            
       
def prolog_tablamulti(prolog_query: str):
    get_prolog_file("tablamulti.pl")
    
    if prolog_query == "multi_list":
        while True:
            try:
                mult_number = int(input("Ingrese un número al que revisarle la tabla de multiplicar:\n"))
                
                print("")
                
                list(prolog.query(f"{prolog_query}({mult_number})"))
                    
                print("")    
                input("Presiona ENTER para continuar...")
                return
                
            except ValueError:
                os.system("cls" if os.name == "nt" else "clear")
            
    print("QUERY INCORRECTO, ERROR")
    raise TypeError("IncorrectQueryType")


def prolog_potencia(prolog_query: str):
    get_prolog_file("potencia.pl")

    if prolog_query == "potencia":
        while True:
            try:
                pow_base = int(input("Ingrese la base del número a potenciar (!= 0):\n"))
                
                if pow_base == 0:
                    raise ValueError("BaseIsZero")
                
                print("")
                
                pow_exp = int(input("Ingrese el exponente de la potencia (>= 0):\n"))
                
                if pow_exp < 0:
                    raise ValueError("NegativeExp")
                
                print("")
                
                for result in prolog.query(f"{prolog_query}({pow_base}, {pow_exp}, Power)"):
                    print(f"{pow_base} ^ {pow_exp} = {result['Power']}")
                
                print("")
                input("Presiona ENTER para continuar...")
                return
            
            except ValueError:
                os.system("cls" if os.name == "nt" else "clear")
        
    print("QUERY INCORRECTO, ERROR")
    raise TypeError("IncorrectQueryType")
        
        
            
if __name__ == "__main__":
    
    prolog_programs = [prolog_fibo, prolog_fibo, prolog_cumples, prolog_cumples,
                       prolog_repite, prolog_factorial, prolog_tablamulti, prolog_potencia]
    
    prolog_queries = ["fibonacci", "fibonacci_list", "obtener_cumples", "buscar_cumple",
                      "escriba", "factorial", "multi_list", "potencia"]
    
    while True:
        os.system("cls" if os.name == "nt" else "clear")
    
        print("MENÚ PROLOG\n")
        print("1. Fibonacci (número único en posición)")
        print("2. Fibonacci (lista de todos los fibonaccis hasta posición)")
        print("3. Fecha de nacimiento de personas (lista completa)")
        print("4. Fecha de nacimiento de personas (persona específica)")
        print("5. Escritura recursiva por caracteres")
        print("6. Factorial")
        print("7. Tabla de multiplicación")
        print("8. Potencia")
        print("\n0. Salir\n\n")

        try:
            opt = int(input("> "))
            
            if opt < 1:
                raise IndexError("OutOfBounds")
            
            prolog_programs[opt-1](prolog_queries[opt-1])
                    
        except (ValueError, IndexError):
            if opt == 0:
                break
            
            opt = -1         
                
    sys.exit(0)
