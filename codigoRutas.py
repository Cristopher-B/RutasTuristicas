import re

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
    identificacion = input("Identificación: ")
    edad = input("Edad: ")
    usuario = input("Correo electrónico: ")
    clave = input("Contraseña segura: ")

    if not contrasenia(clave):
        print("La contraseña no es segura. Debe tener al menos una mayúscula, una minúscula y un número.")
        return

    with open("usuarios.txt", "a") as archivo:
        archivo.write(f"{usuario},{clave},{nombres},{identificacion},{edad}\n")
    print("Usuario registrado con éxito.")

def iniciar_sesion():
    print("=== INICIO DE SESIÓN ===")
    usuario = input("Correo: ")
    clave = input("Contraseña: ")

    try:
        with open("usuarios.txt", "r") as archivo:
            for linea in archivo:
                datos = linea.strip().split(",")
                if datos[0] == usuario and datos[1] == clave:
                    print("Inicio de sesión exitoso.")
                    return True, usuario
        print("Credenciales incorrectas.")
        return False, None
    #para cuando no existe el archivo.
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

#Mod principal
def main():
    while True:
        print("\n=== SISTEMA DE RUTAS TURÍSTICAS ===")
        print("1. Registro.")
        print("2. Inicio de sesión")
        print("3. Salir")
        op = input("Opción: ")

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
