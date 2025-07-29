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

#Estrucura de ARBOL
def lugares_turisticos(arbol, nivel=0):
    for lugares in arbol:
        print("  "* nivel + "- " + lugares)
        if isinstance(arbol[lugares], dict):
            lugares_turisticos(arbol[lugares], nivel + 1)

arbol_Lugares={
    "Insular":{
        "Galápagos":{},
    },
    "Costa":{
        "Esmeraldas":{},
        "Manta":{},
        "Montañita":{},
        "Salinas":{},
        "Puerto López":{},
    },
    "Sierra":{
        "Baños":{},
        "Cuenca":{},
        "Otavalo":{},
        "Quito":{},
        "Riobamba":{},
    },
    "Oriente":{
        "Archidona":{},
        "Misahuallí":{},
        "Lago Agrio":{},
        "Puyo":{},
        "Tena":{},
    }
}
        
def agregar_lugar():
    origen = input("Ciudad de origen: ")
    destino = input("Ciudad de destini: ")
    distancia = input("Distancia en (km): ")
    costo= input("Precio $: ")

    with open("rutas.txt", "a") as archivo:
        archivo.write(f"{origen},{destino},{distancia},{costo}\n")
    print("Lugar agregado con exito.")

#Menu del admin
def administrador():
    while True:
        print("\n ### MENÚ DE ADMINISTRADOR ###")
        print("1. Agregar ciudad turistico.")
        print("2. Ver lista de ciudades turisticos.")
        print("3. Consultar una ciudad turistica.")
        print("4. Actualizar ciudades turisticos.")
        print("5. Eliminar ciudades turisticos.")
        print("6. Guardar ciudades turisticos en archivo .txt.")
        print("7. Salir.")
        opcion = input("Seleccione una opción: ")
        if opcion == "1":
            agregar_lugar()
        elif opcion == "2":
            rutas = leer_rutas()
            for origen in rutas:
                for destino in rutas[origen]:
                    informacion = rutas[origen][destino]
                    print(f"{origen} -> {destino} | Distancia: {informacion["distancia"]} km | Costo: ${informacion["costo"]}")
        elif opcion == "3":
        elif opcion == "4":
        elif opcion == "5":
        elif opcion == "6":
            guardar_rutas()
        elif opcion == "7":
            break          

#Menu del cliente       
def cliente(user):
    rutas = leer_rutas()
    while True:
         print(f"\n### MENÚ CLIENTE ({user}) ###")
         print("1. Ver mapa de ciudades turísticos conectados.")
         print("2. Calcular ruta mas corta.")
         print("3. Explorar ciudades.")
         print("4. Seleccionar ciudades a visitar.")
         print("5. Ver lista de ciudades turísticos.")
         print("6. Actualizar ciudades escogidos.")
         print("7. Eliminar ciudades escogidas.")
         print("8. Guardar la selección en archivo .txt.")
         print("9. Salir.")        
         opcion = input("Opción: ")
         if opcion == "1":
            for origen in rutas:
                for destino in rutas[origen]:
                    info = rutas[origen][destino]
                    print(f"{origen} -> {destino} | Distancia: {info['distancia']} km | Costo: ${info['costo']}")
         elif opcion == "2":
            origen = input("Ciudad origen: ")
            destino = input("Ciudad destino: ")
            costo, camino = dijkstra(rutas, origen, destino)
            if camino:
                print("Ruta:", " -> ".join(camino))
                print("Costo total:", costo)
            else:
                print("Ruta no encontrada. Intente de nuevo.")
         elif opcion == "3":
            lugares_turisticos(arbol_Lugares)
         elif opcion == "4":
         elif opcion == "5":
         elif opcion == "6":
         elif opcion == "7":
         elif opcion == "8":
         elif opcion == "9":
            break
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
                    administrador()
                else:
                    cliente(usuario)
        elif op == "3":
            print("Gracias por usar nuestro sistema.")
            break

main()
