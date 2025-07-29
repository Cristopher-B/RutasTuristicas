import re
import heapq
from collections import deque

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
    padres = {nodo: None for nodo in grafo}
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
                    padres[vecino] = nodo_actual
                    heapq.heappush(cola, (nueva_distancia, vecino))
#Especificar el camino
    camino = []
    nodo_actual = destino
    while nodo_actual is not None:
        camino.append(nodo_actual)
        nodo_actual = padres[nodo_actual]
    camino.reverse()
    return distancias[destino], camino if distancias[destino] != float('inf') else []

def encontrar_ruta(grafo, inicio, destino):
    grafo_dijkstra ={}
    for origen in grafo:
        if origen not in grafo_dijkstra:
            grafo_dijkstra[origen] =[]
        for dest, datos in grafo[origen].items():
            grafo_dijkstra[origen].append((dest, datos['costo']))
            if dest not in grafo_dijkstra:
                grafo_dijkstra[dest] = []
    if inicio not in grafo_dijkstra or destino not in grafo_dijkstra:
        return float('inf'), []
    
    distancia, camino = dijkstra(grafo_dijkstra, inicio, destino)
    return distancia, camino
#BFS
def bfs(grafo, inicio):
    visitados = set()
    cola = deque([inicio])
    resultado = []

    while cola:
        nodo = cola.popleft()
        if nodo not in visitados:
            visitados.add(nodo)
            resultado.append(nodo)
            vecinos = grafo.get(nodo, {})
            for vecino in vecinos.keys():
                if vecino not in visitados:
                for vecino in grafo[nodo]:
                    cola.append(vecino)
    return resultado

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
    destino = input("Ciudad de destino: ")
    distancia = input("Distancia en (km): ")
    costo= input("Precio $: ")

    with open("rutas.txt", "a") as archivo:
        archivo.write(f"{origen},{destino},{distancia},{costo}\n")
    print("Lugar agregado con exito")
def consultar_ciudad():
    rutas = leer_rutas()
    ciudad_buscar = input("Ingrese la ciudad a consultar: ")  
    ciudades = []
    for origen in rutas:
        if origen not in ciudades:
            ciudades.append(origen)
        for destino in rutas[origen]:
            if destino not in ciudades:
                ciudades.append(destino)
    
    ciudades = ordenamiento(ciudades)
    indice = busqueda(ciudades, ciudad_buscar)
    
    if indice != -1:
        print(f"\nCiudad encontrada: {ciudad_buscar}")
        print("Rutas desde esta ciudad:")
        if ciudad_buscar in rutas:
            for destino in rutas[ciudad_buscar]:
                info = rutas[ciudad_buscar][destino]
                print(f"  {destino}  Distancia: {info['distancia']} km  Costo: ${info['costo']}")
    else:
        print("Ciudad no encontrada.")
#Actualizar
def actualizar_ciudad():
    rutas = leer_rutas()
    origen = input("Ciudad de origen a actualizar: ")
    destino = input("Ciudad de destino a actualizar: ")
    
    if origen in rutas and destino in rutas[origen]:
        nueva_distancia = float(input("Nueva distancia (km): "))
        nuevo_costo = float(input("Nuevo costo ($): "))
        
        rutas[origen][destino]["distancia"] = nueva_distancia
        rutas[origen][destino]["costo"] = nuevo_costo
        
        guardar_rutas(rutas)
        print("Ciudad actualizada con exito.")
    else:
        print("Ruta no encontrada.")

def eliminar_ciudad():
    rutas = leer_rutas()
    origen = input("Ciudad de origen a eliminar: ")
    destino = input("Ciudad de destino a eliminar: ")
    
    if origen in rutas and destino in rutas[origen]:
        del rutas[origen][destino]
        if len(rutas[origen]) == 0:
            del rutas[origen]
        
        guardar_rutas(rutas)
        print("Ruta eliminada con exito.")
    else:
        print("Ruta no encontrada.")
#clientes
ciudades_seleccionadas = []

def seleccionar_ciudades():
    global ciudades_seleccionadas
    print("Seleccione al menos 2 ciudades para visitar:")
    
    while len(ciudades_seleccionadas) < 2:
        ciudad = input(f"Ciudad {len(ciudades_seleccionadas) + 1}: ")
        if ciudad not in ciudades_seleccionadas:
            ciudades_seleccionadas.append(ciudad)
            print(f"Ciudad {ciudad} agregada.")
        else:
            print("Ciudad ya seleccionada.")
    
    continuar = input("¿Desea agregar mas ciudades? (s/n): ")
    while continuar.lower() == 's':
        ciudad = input("Nueva ciudad: ")
        if ciudad not in ciudades_seleccionadas:
            ciudades_seleccionadas.append(ciudad)
            print(f"Ciudad {ciudad} agregada.")
        continuar = input("¿Desea agregar mas ciudades? (s/n): ")

def listar_ciudades_seleccionadas():
    global ciudades_seleccionadas
    if not ciudades_seleccionadas:
        print("No hay ciudades seleccionadas.")
        return
    
    ciudades_ordenadas = ordenamiento(ciudades_seleccionadas.copy())
    print("\nCiudades seleccionadas (ordenadas):")
    for i, ciudad in enumerate(ciudades_ordenadas, 1):
        print(f"{i}. {ciudad}")

def actualizar_ciudades_seleccionadas():
    global ciudades_seleccionadas
    if not ciudades_seleccionadas:
        print("No hay ciudades seleccionadas.")
        return
    
    listar_ciudades_seleccionadas()
    try:
        indice = int(input("Indice de la ciudad a actualizar: ")) - 1
        if 0 <= indice < len(ciudades_seleccionadas):
            nueva_ciudad = input("Nueva ciudad: ")
            ciudades_seleccionadas[indice] = nueva_ciudad
            print("Ciudad actualizada con exito.")
        else:
            print("Indice invalido.")
    except ValueError:
        print("Por favor ingrese un numero valido.")

def eliminar_ciudades_seleccionadas():
    global ciudades_seleccionadas
    if not ciudades_seleccionadas:
        print("No hay ciudades seleccionadas.")
        return
    
    listar_ciudades_seleccionadas()
    try:
        indice = int(input("Indice de la ciudad a eliminar: ")) - 1
        if 0 <= indice < len(ciudades_seleccionadas):
            ciudad_eliminada = ciudades_seleccionadas.pop(indice)
            print(f"Ciudad {ciudad_eliminada} eliminada con exito.")
        else:
            print("Indice invalido.")
    except ValueError:
        print("Por favor ingrese un numero valido.")

def guardar_seleccion_cliente(usuario):
    global ciudades_seleccionadas
    if not ciudades_seleccionadas:
        print("No hay ciudades seleccionadas para guardar.")
        return
    
    nombre_archivo = f"rutas-{usuario.split('@')[0]}.txt"
    with open(nombre_archivo, "w") as archivo:
        for ciudad in ciudades_seleccionadas:
            archivo.write(f"{ciudad}\n")
    print(f"Seleccion guardada en {nombre_archivo}")


#Menu del admin
def administrador():
    while True:
        print("\n ---- MENU DE ADMINISTRADOR ----")
        print("1. Agregar ciudad turistico.")
        print("2. Ver lista de ciudades turisticos.")
        print("3. Consultar una ciudad turistica.")
        print("4. Actualizar ciudades turisticos.")
        print("5. Eliminar ciudades turisticos.")
        print("6. Guardar ciudades turisticos en archivo .txt.")
        print("7. Salir.")
        opcion = input("Seleccione una opcion: ")
        if opcion == "1":
            agregar_lugar()
        elif opcion == "2":
            rutas = leer_rutas()
            for origen in rutas:
                for destino in rutas[origen]:
                    informacion = rutas[origen][destino]
                    print(f"{origen}  {destino}  Distancia: {informacion['distancia']} km  Costo: ${informacion['costo']}")
            listas_rutas = ordenamiento(listas_rutas)
            for ruta in listas_rutas:
                print(ruta)
        elif opcion == "3":
            consultar_ciudad()
        elif opcion == "4":
            actualizar_ciudad()
        elif opcion == "5":
            eliminar_ciudad()
        elif opcion == "6":
            rutas = leer_rutas()
            guardar_rutas(rutas)
        elif opcion == "7":
            break           
#Menu del cliente       
def cliente(user):
    rutas = leer_rutas()
    while True:
         print(f"\n---- MENU CLIENTE ({user}) ----")
         print("1. Ver mapa de ciudades turisticos conectados.")
         print("2. Calcular ruta mas corta.")
         print("3. Explorar ciudades.")
         print("4. Seleccionar ciudades a visitar.")
         print("5. Ver lista de ciudades turisticos seleccionados.")
         print("6. Actualizar ciudades escogidos.")
         print("7. Eliminar ciudades escogidas.")
         print("8. Guardar la seleccion en archivo .txt.")
         print("9. Explorar rutas cercanas. ")
         print("10. Salir.")        
         opcion = input("Opcion: ")
         if opcion == "1":
            for origen in rutas:
                for destino in rutas[origen]:
                    info = rutas[origen][destino]
                    print(f"{origen} {destino}  Distancia: {info['distancia']} km  Costo: ${info['costo']}")
         elif opcion == "2":
            origen = input("Ciudad origen: ")
            destino = input("Ciudad destino: ")
            costo, camino = encontrar_ruta(rutas, origen, destino)
            if camino:
                print("Ruta:", " -> ".join(camino))
                print("Costo total:", costo)
            else:
                print("Ruta no encontrada. Intente de nuevo.")
         elif opcion == "3":
            lugares_turisticos(arbol_Lugares)
         elif opcion == "4":
             seleccionar_ciudades()
         elif opcion == "5":
             actualizar_ciudades_seleccionadas()
         elif opcion == "6":
             actualizar_ciudades_seleccionadas()
         elif opcion == "7":
             eliminar_ciudades_seleccionadas()
         elif opcion == "8":
             guardar_seleccion_cliente(user)
         elif opcion == "9": 
             ciudad_inicio = input("Ciudad de inicio para BFS: ")
             alcanzables = bfs(rutas, ciudad_inicio)
             print(f"Ciudades alcanzables desde {ciudad_inicio}:")
             for ciudad in alcanzables:
                print(f" - {ciudad}")
         elif opcion == "10":
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
