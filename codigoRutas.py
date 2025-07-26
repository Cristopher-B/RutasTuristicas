import re
import heapq

#Inicio de sesion.

def contrasenia(clave):
    return (
        len(clave) >= 6 and
        re.search(r"[a-z]", clave) and
        re.search(r"[A-Z]", clave) and
        re.search(r"[0-9]", clave)
    )

def registrar_usuario():
    print("=== REGISTRO DE USUARIO ===")
    nombres = input("Nombres y Apellidos: ")
    identificacion = input("Identificacion: ")
    edad = input("Edad: ")
    usuario = input("Correo electronico: ")
    clave = input("Contraseña segura: ")

    if not contrasenia(clave):
        print("La contraseña no es segura. Debe tener al menos una mayuscula, una minuscula y un numero.")
        return

    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario},{clave},{nombres},{identificacion},{edad}\n")
    print("Usuario registrado con exito.")

def iniciar_sesion():
    print("=== INICIO DE SESION ===")
    usuario = input("Correo: ")
    clave = input("Contraseña: ")

    try:
        with open("usuarios.txt", "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if datos[0] == usuario and datos[1] == clave:
                    print("Inicio de sesion exitoso.")
                    return True, usuario
        print("Credenciales incorrectas.")
        return False, None

    except FileNotFoundError: 
        print("Archivo de usuarios no encontrado.")
        return False, None

#Archivo rutas.txt

def leer_rutas():
    rutas = {}
    try:
        with open("rutas.txt", "r") as archivo:
            for linea in archivo:
                origen, destino, distancia, costo = linea.strip().split(",")
                distancia = float(distancia)
                costo = float(costo)
                if origen not in rutas:
                    rutas[origen] = {}
                rutas[origen][destino] = {"distancia": distancia, "costo": costo}
        return rutas
    except FileNotFoundError:
        print("Archivo de rutas no encontrado.")
        return {}
#guardar txt
def guardar_rutas(rutas):
    with open("rutas.txt", "w") as archivo:
        for origen in rutas:
            for destino in rutas[origen]:
                distancia = rutas[origen][destino]["distancia"]
                costo = rutas[origen][destino]["costo"]
                archivo.write(f"{origen},{destino},{distancia},{costo}\n")
    print("Rutas guardadas exitosamente")
# ordenamiento burbuja 
def ordenamiento(lista):
    n = len(lista)
    for i in range(n):
        for j in range (0, n-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista 
#busqueda lineal
def busqueda(lista, elemento):
    for i, item in enumerate(lista):
        if item == elemento:
            return i 
    return -1
#revisar algoritmo dijkstra
def dijkstra(grafo, inicio, destino):
    distancias = {nodo:float('inf') for nodo in grafo}
    distancias[inicio] = 0
    cola =[(0, inicio)]
    while cola: 
        distancia_actual, nodo_actual = heapq.heappop(cola)
        if distancia_actual > distancias[nodo_actual]:
            continue
        if nodo_actual == destino:
            break
        if nodo_actual in grafo:
            for vecino, peso in grafo[nodo_actual]:
                nueva_distancia = distancia_actual + peso
                if nueva_distancia < distancias.get(vecino, float('inf')):
                    distancias[vecino] = nueva_distancia
                    heapq.heappush(cola, (nueva_distancia, vecino))
    return distancias

def encontrar_ruta(grafo, inicio, destino):
    grafo_dijkstra ={}
    for origen in grafo:
        grafo_dijkstra[origen] =[]
        for dest, datos in grafo[origen].items():
            grafo_dijkstra[origen].append((dest, datos['costo']))
    distancias= dijkstra(grafo_dijkstra, inicio)
    if destino in distancias and distancias[destino] != float('inf'):
        return distancias[destino], [inicio, destino]
    else:
        return float ('inf'),[]
        
        
        

def main():
    while True:
        print("\n=== SISTEMA DE RUTAS TURISTICAS ===")
        print("1. Registro.")
        print("2. Inicio de sesion")
        print("3. Salir")
        op = input("Opcion: ")

        if op == "1":
            registrar_usuario()
        elif op == "2":
            ok, usuario = iniciar_sesion()
            if ok:
                if usuario == "admin@poli.com":
                    #Debe ir una funcion de MENU DE ADMINISTRADOR
                else:
                    #Debe ir una funcion de MENU DE USUARIO
        elif op == "3":
            print("Gracias por usar nuestro sistema.")
            break

main()
