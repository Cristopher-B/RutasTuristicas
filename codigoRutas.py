import heapq
from collections import deque


def validar_contraseña(contraseña):
    tiene_mayuscula = any(c.isupper() for c in contraseña)
    tiene_minuscula = any(c.islower() for c in contraseña)
    tiene_numero = any(c.isdigit() for c in contraseña)
    return tiene_mayuscula and tiene_minuscula and tiene_numero

def registrar_usuario():
    nombre = input("Ingrese su nombre y apellido: ")
    identificacion = input("Ingrese su identificación: ")
    edad = input("Ingrese su edad: ")
    usuario = input("Ingrese su correo: ")
    while True:
        contraseña = input("Ingrese su contraseña segura: ")
        if validar_contraseña(contraseña):
            break
        else:
            print("La contraseña debe tener al menos una mayúscula, una minúscula y un número.")

    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{nombre},{identificacion},{edad},{usuario},{contraseña}\n")
    print("Usuario registrado correctamente.\n")

def iniciar_sesion():
    usuario = input("Correo: ")
    contraseña = input("Contraseña: ")
    if usuario == "politours@admin.com" and contraseña == "Tours2025":
        print("Inicio de sesión como administrador exitoso.\n")
        return usuario
    with open("usuarios.txt", "r") as archivo:
        for linea in archivo:
            datos = linea.strip().split(",")
            if datos[3] == usuario and datos[4] == contraseña:
                print("Inicio de sesión exitoso.\n")
                return usuario.split("@")[0]
    print("Credenciales incorrectas.Intente de nuevo\n")
    return None

def leer_rutas():
    rutas = {}
    try:
        with open("rutas.txt", "r") as archivo:
            for linea in archivo:
                origen, destino, distancia, costo = linea.strip().split(',')
                distancia = float(distancia.replace("km", ""))
                costo = float(costo.replace("$", ""))
                if origen not in rutas:
                    rutas[origen] = {}
                rutas[origen][destino] = {"distancia": distancia, "costo": costo}
        return rutas
    except FileNotFoundError:
        return {}

def guardar_rutas(rutas):
    with open("rutas.txt", "w") as archivo:
        for origen in rutas:
            for destino in rutas[origen]:
                datos = rutas[origen][destino]
                archivo.write(f"{origen},{destino},{datos['distancia']}km,${datos['costo']}\n")

def dijkstra(grafo, inicio, fin):
    heap = [(0, inicio, [])]
    visitados = set()
    while heap:
        (costo, nodo, camino) = heapq.heappop(heap)
        if nodo in visitados:
            continue
        visitados.add(nodo)
        camino = camino + [nodo]
        if nodo == fin:
            return costo, camino
        for vecino in grafo.get(nodo, {}):
            if vecino not in visitados:
                heapq.heappush(heap, (costo + grafo[nodo][vecino]["costo"], vecino, camino))
    return float("inf"), []

def ordenamiento_burbuja(lista):
    for i in range(len(lista)):
        for j in range(0, len(lista)-i-1):
            if lista[j] > lista[j+1]:
                lista[j], lista[j+1] = lista[j+1], lista[j]
    return lista

def busqueda_lineal(lista, elemento):
    for i in range(len(lista)):
        if lista[i].lower() == elemento.lower():
            return i
    return -1

arbol_lugares = {
    "Sierra": {},
    "Costa": {},
    "Oriente": {}
}

def agregar_al_arbol(region, origen, destino, distancia, costo):
    if region in arbol_lugares:
        if origen not in arbol_lugares[region]:
            arbol_lugares[region][origen] = {}
        arbol_lugares[region][origen][destino] = {"distancia": distancia, "costo": costo}

def imprimir_arbol(arbol, nivel=0):
    for zona, subzonas in arbol.items():
        print("  " * nivel + f"- {zona}")
        if isinstance(subzonas, dict):
            imprimir_arbol(subzonas, nivel + 1)
        else:
            print("  " * (nivel + 1) + str(subzonas))

def cliente(usuario):
    rutas = leer_rutas()
    seleccionadas = []
    while True:
        print("\n--- Menú Cliente ---")
        print("1. Ver mapa")
        print("2. Consultar ruta óptima entre dos ciudades")
        print("3. Explorar lugares por zonas")
        print("4. Seleccionar ciudades a visitar")
        print("5. Listar ciudades seleccionadas y costo total")
        print("6. Actualizar ciudad seleccionada")
        print("7. Eliminar ciudad seleccionada")
        print("8. Guardar selección")
        print("9. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            rutas = leer_rutas()
            for origen in rutas:
                for destino in rutas[origen]:
                    datos = rutas[origen][destino]
                    print(f"{origen} -> {destino} | Distancia: {datos['distancia']} km | Costo: ${datos['costo']}")

        elif opcion == "2":
            origen = input("Ciudad de origen: ")
            destino = input("Ciudad de destino: ")
            costo, camino = dijkstra(rutas, origen, destino)
            if camino:
                print(f"Ruta óptima: {' -> '.join(camino)} | Costo total: ${costo}")
            else:
                print("No se encontró una ruta.")

        elif opcion == "3":
            for region in arbol_lugares:
                print(f"\nRegión: {region}")
                for origen in arbol_lugares[region]:
                    for destino in arbol_lugares[region][origen]:
                        datos = arbol_lugares[region][origen][destino]
                        print(f"{origen} -> {destino} | Distancia: {datos['distancia']} km | Costo: ${datos['costo']}")

        elif opcion == "4":
            ciudad = input("Ingrese ciudad turística a visitar: ")
            seleccionadas.append(ciudad)

        elif opcion == "5":
            seleccionadas = ordenamiento_burbuja(seleccionadas)
            print("Ciudades seleccionadas:")
            for ciudad in seleccionadas:
                print(f"- {ciudad}")

        elif opcion == "6":
            ciudad_actual = input("Ciudad a actualizar: ")
            if ciudad_actual in seleccionadas:
                nueva = input("Nueva ciudad: ")
                seleccionadas[seleccionadas.index(ciudad_actual)] = nueva
            else:
                print("Ciudad no encontrada.")

        elif opcion == "7":
            ciudad_eliminar = input("Ciudad a eliminar: ")
            if ciudad_eliminar in seleccionadas:
                seleccionadas.remove(ciudad_eliminar)
            else:
                print("Ciudad no encontrada.")

        elif opcion == "8":
            nombre_archivo = f"rutas-{usuario}.txt"
            with open(nombre_archivo, "w") as f:
                for ciudad in seleccionadas:
                    f.write(f"{ciudad}\n")
            print(f"Selección guardada en {nombre_archivo}")

        elif opcion == "9":
            break

        else:
            print("Opción inválida.")

def administrador():
    rutas = leer_rutas()
    while True:
        print("\n--- Menú Administrador ---")
        print("1. Agregar ruta")
        print("2. Listar rutas ordenadas")
        print("3. Buscar ciudad")
        print("4. Actualizar ruta")
        print("5. Eliminar ruta")
        print("6. Guardar rutas")
        print("7. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            region = input("Región (Costa/Sierra/Oriente): ")
            origen = input("Ciudad origen: ")
            destino = input("Ciudad destino: ")
            distancia = float(input("Distancia (km): "))
            costo = float(input("Costo ($): "))
            if origen not in rutas:
                rutas[origen] = {}
            rutas[origen][destino] = {"distancia": distancia, "costo": costo}
            agregar_al_arbol(region, origen, destino, distancia, costo)

        elif opcion == "2":
            for origen in ordenamiento_burbuja(list(rutas.keys())):
                for destino in rutas[origen]:
                    datos = rutas[origen][destino]
                    print(f"{origen} -> {destino} | Distancia: {datos['distancia']} km | Costo: ${datos['costo']}")

        elif opcion == "3":
            ciudad = input("Ciudad a buscar: ")
            encontrado = False
            for origen in rutas:
                if ciudad.lower() == origen.lower():
                    for destino in rutas[origen]:
                        datos = rutas[origen][destino]
                        print(f"{origen} -> {destino} | Distancia: {datos['distancia']} km | Costo: ${datos['costo']}")
                        encontrado = True
            if not encontrado:
                print("Ciudad no encontrada.")

        elif opcion == "4":
            origen = input("Ciudad origen a actualizar: ")
            destino = input("Ciudad destino: ")
            if origen in rutas and destino in rutas[origen]:
                distancia = float(input("Nueva distancia (km): "))
                costo = float(input("Nuevo costo ($): "))
                rutas[origen][destino] = {"distancia": distancia, "costo": costo}
            else:
                print("Ruta no encontrada.")

        elif opcion == "5":
            origen = input("Ciudad origen: ")
            destino = input("Ciudad destino: ")
            if origen in rutas and destino in rutas[origen]:
                del rutas[origen][destino]
                if not rutas[origen]:
                    del rutas[origen]
                print("Ruta eliminada.")
            else:
                print("Ruta no encontrada.")

        elif opcion == "6":
            guardar_rutas(rutas)
            print("Rutas guardadas.")

        elif opcion == "7":
            break

        else:
            print("Opción inválida.")

def menu_principal():
    while True:
        print("\n--- Sistema de Rutas Turísticas ---")
        print("1. Registrarse")
        print("2. Iniciar sesión como cliente")
        print("3. Iniciar sesión como administrador")
        print("4. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            registrar_usuario()
        elif opcion == "2":
            usuario = iniciar_sesion()
            if usuario and usuario != "politours@admin.com":
                cliente(usuario)
        elif opcion == "3":
            print("Ingrese credenciales de administrador")
            usuario = iniciar_sesion()
            if usuario == "politours@admin.com":
                administrador()
        elif opcion == "4":
            print("Gracias por usar el sistema.")
            break
        else:
            print("Opción inválida.")


menu_principal()
