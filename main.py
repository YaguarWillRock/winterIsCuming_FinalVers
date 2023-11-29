#main.py jdfr
from firestore_db import Agenda, Contacto
from users import aceptar_invitacion, Usuario, login_user, register_user, email_already_registered
from google.cloud import firestore
import re
from firestore_db import db
import firebase_admin
from firebase_admin import auth, firestore, exceptions
from google.cloud.firestore import FieldFilter
import requests
import json

current_user = Usuario(user_id='id_del_usuario_actual', email='email_del_usuario_actual')
# agenda = Agenda()

def guardar_contacto(agenda, contacto, current_user_email):
    try:
        agenda.agregar_contacto(contacto, current_user_email)
        print(f"Contacto '{contacto.nombre}' guardado exitosamente en ", current_user_email,".")
    except Exception as e:
        print(f"Ocurrió un error al guardar el contacto: {e}")



def mostrar_agenda(agenda, current_user_email):
    print(f"Contactos en la agenda de {current_user_email}: ")
    contactos = (db.collection(current_user_email).where(filter=FieldFilter("user_data", "==", "0")).stream())
    for contacto in contactos:
        #print(f"{contacto.id} => {contacto.to_dict()}")
    #for contacto in agenda.obtener_contactos():
        print(f"Nombre: {contacto.get('nombre')}")
        print(f"Edad: {contacto.get('edad')}")
        print(f"Email: {contacto.get('calle')}")
        print(f"Ciudad: {contacto.get('ciudad')}")
        print(f"Código Postal: {contacto.get('codigo_postal')}")
        print(f"Número Exterior: {contacto.get('numero_exterior')}")
        print(f"Número Interior: {contacto.get('numero_interior')}")
        print(f"Colonia: {contacto.get('colonia')}")
        print(f"Número de Teléfono: {contacto.get('numero')}")
        print(f"Correo Electrónico: {contacto.get('email')}")
        print(f"Página Web: {contacto.get('pagina_web')}")
        print("") 

def mostrar_informacion_contacto(contacto):
    print(f"Nombre: {contacto.nombre}")
    print(f"Edad: {contacto.edad}")
    print(f"Calle: {contacto.calle}")
    print(f"Ciudad: {contacto.ciudad}")
    print(f"Código Postal: {contacto.codigo_postal}")
    print(f"Número Exterior: {contacto.numero_exterior}")
    print(f"Número Interior: {contacto.numero_interior}")
    print(f"Colonia: {contacto.colonia}")
    print(f"Número de Teléfono: {contacto.numero}")
    print(f"Correo Electrónico: {contacto.email}")
    print(f"Página Web: {contacto.pagina_web}")
    print("")

def borrar_contacto(agenda, contacto, current_user_email):
    #agenda.eliminar_contacto(contacto, current_user_email)
    db.collection(current_user_email).document("").delete()
    print(f"Contacto '{contacto.nombre}' ha sido borrado.")

def main():
    current_user_id, current_user_email = None, None
    mi_agenda = Agenda(owner_id=current_user_id)
    current_user_id, current_user_email = None, None  

    while True:
        if not current_user_id:
            print("")
            print("No hay ninguna sesión activa")
            print("1. Registrarse")
            print("2. Iniciar sesión ")            
            opcion_inicio = input("Seleccione una opción: ")
            print("*****************************************************")  
            
            while True:


                if opcion_inicio == "1":
                        email = input("Por favor ingrese su email: ")
                        
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                            print("Error: el formato de correo electrónico no es válido.")
                            continue
                        
                        password = input("Por favor ingrese su contraseña: ")
                        
                        if len(password) < 6:
                            print("Error: la contraseña debe tener al menos 6 caracteres.")
                            continue
                        
                        if email_already_registered(email):
                            print("Error: el correo ya está registrado.")
                            continue
                        
                        contact_info = {
                            'nombre': input("Ingrese su nombre completo: "),
                            'edad': input("Ingrese su edad: "),
                            'calle': input("Ingrese su calle: "),
                            'ciudad': input("Ingrese su ciudad: "),
                            'codigo_postal': input("Ingrese su código postal: "),
                            'numero_exterior': input("Ingrese su número exterior: "),
                            'numero_interior': input("Ingrese su número interior: "),
                            'colonia': input("Ingrese su colonia: "),
                            'numero': input("Ingrese su número de teléfono: "),
                            'email': email,
                            'pagina_web': input("Ingrese su página web: ")
                        }
                        current_user_id, current_user_email = register_user(email, password, contact_info)

                        print("*****************************************************")  
                        if current_user_id:
                            print(f"Bienvenido {current_user_email}")
                            print("*****************************************************")  
                        else:
                            print("Error al registrar el usuario. Intente de nuevo.")      

                if opcion_inicio == "2":
                    email = input("Por favor ingrese su email: ")
                    password = input("Por favor ingrese su contraseña: ")
                    current_user_id, current_user_email = login_user(email, password)
                    print("*****************************************************")  

                    if current_user_id:
                        print(f"Bienvenido {current_user_email}")
                        print("*****************************************************")  
                    else:
                        print("Inicio de sesión fallido, intente de nuevo.")
                        continue
                break 
        
        #print("modo admin")
        #agenda = input()
        #current_user.clonar_agenda(agenda)
        print("1. Crear nuevo contacto")
        print("2. Mostrar Agenda")
        print("3. Buscar contacto por nombre")
        print("4. Buscar contacto por teléfono")
        print("5. Borrar contacto")
        #print("6. Compartir mi agenda")
        print("6. Ver agendas de usuarios disponibles")
        print("9. Cerrar sesión")
        #print("7. Responder a una invitación")
        print("0. Salir")
        print("")

        opcion = input("Seleccione una opción: ")
        print("")
        
        if opcion == "1":
            print("Ingrese los datos del nuevo contacto:")

            while True:
                nombre = input("Nombre: ")
                if not nombre.strip():
                    print("El nombre no puede estar vacío.")
                    continue
                elif not all(x.isalpha() or x.isspace() for x in nombre):
                    print("El nombre solo puede contener letras y espacios.")
                    continue
                break

            while True:
                edad = input("Edad: ")
                if not edad.isdigit() or not 0 < int(edad) < 120:
                    print("La edad debe estar entre 1 y 119 años.")
                    continue
                break

            while True:
                calle = input("Calle: ")
                if not calle.strip():
                    print("La calle no puede estar vacía.")
                    continue
                break

            while True:
                ciudad = input("Ciudad: ")
                if not ciudad.strip():
                    print("La ciudad no puede estar vacía.")
                    continue
                break

            while True:
                codigo_postal = input("Código Postal: ")
                if not re.match(r"^\d{5}$", codigo_postal):
                    print("El código postal debe tener 5 dígitos.")
                    continue
                break

            while True:
                numero_exterior = input("Número Exterior: ")
                if not numero_exterior.strip():
                    print("El número exterior no puede estar vacío.")
                    continue
                break

            numero_interior = input("Número Interior (opcional): ")

            while True:
                colonia = input("Colonia: ")
                if not colonia.strip():
                    print("La colonia no puede estar vacía.")
                    continue
                break

            while True:
                numero = input("Número de Teléfono: ")
                if not re.match(r"^\+?[\d\s]{3,}$", numero):
                    print("El número de teléfono es inválido.")
                    continue
                break

            while True:
                email = input("Correo Electrónico: ")
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    print("El correo electrónico no tiene un formato válido.")
                    continue
                break

            while True:
                pagina_web = input("Página Web (opcional): ")
                if pagina_web and not re.match(r"^https?:\/\/.*\..+$", pagina_web):
                    print("La página web tiene un formato inválido.")
                    continue
                break
            
            # nombre = input("Nombre: ")
            # edad = int(input("Edad: ")) 
            # calle = input("Calle: ")
            # ciudad = input("Ciudad: ")
            # codigo_postal = input("Código Postal: ")
            # numero_exterior = input("Número Exterior: ")
            # numero_interior = input("Número Interior: ")
            # colonia = input("Colonia: ")
            # numero = input("Número de Teléfono: ")
            # email = input("Correo Electrónico: ")
            # pagina_web = input("Página Web: ")
            
            # if Contacto.validar_datos(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web):
            #     nuevo_contacto = Contacto(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web)
            #     resultado = guardar_contacto(mi_agenda, nuevo_contacto, current_user_email)
            # else:
            #     print("Los datos del contacto no son válidos.")     
            user_data = "0"       
            edad = int(edad)
            nuevo_contacto = Contacto(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web, user_data)
            guardar_contacto(mi_agenda, nuevo_contacto, current_user_email)

        elif opcion == "2":
            mostrar_agenda(mi_agenda, current_user_email)

        elif opcion == "3":
            nombre = input("Ingrese el nombre a buscar: ")
            contacto_encontrado = mi_agenda.buscar_contacto_por_nombre(nombre, current_user_email)
            if contacto_encontrado:
                mostrar_informacion_contacto(contacto_encontrado)
            else:
                print("Contacto no encontrado.")

        elif opcion == "4":
            numero = input("Ingrese el número de teléfono a buscar: ")
            contacto_encontrado = mi_agenda.buscar_contacto_por_telefono(numero)
            if contacto_encontrado:
                mostrar_informacion_contacto(contacto_encontrado)
            else:
                print("Contacto no encontrado.")                
        elif opcion == "5":
            nombre = input("Ingrese el nombre del contacto a borrar: ")
            contacto_a_borrar = mi_agenda.buscar_contacto_por_nombre(nombre, current_user_email)
            if contacto_a_borrar:
                borrar_contacto(mi_agenda, contacto_a_borrar, current_user_email)
            else:
                print("Contacto no encontrado.")

        elif opcion == "6":
            """print("Enviar una invitación para compartir tu agenda.")
            agenda_id = input("ID de la agenda a compartir: ")
            receptor_email = input("Email del usuario con quien compartir: ")
            nivel_de_acceso = input("Nivel de acceso (lectura/escritura): ")
            enviar_invitacion(agenda_id, current_user.user_id, receptor_email, nivel_de_acceso)"""
            print("Estas son las agendas disponibles: ")
            current_user.visualizar_agendas_disponibles()
            print("¿Quiere hacer un merge de los contactos de una agenda con la suya?: ")
            print("1) Sí")
            print("Otro) No")
            opcion = input("")
            if (opcion=="1"):
                agenda = input("Ingrese el correo de la agenda con la que desea hacer merge:")
                current_user.clonar_agenda(agenda, current_user_email)

        #elif opcion == "7":
        #    print("Responder a invitaciones pendientes.")
        #    invitacion_id = input("ID de la invitación a responder: ")
        #    respuesta = input("Aceptas la invitación? (s/n): ")
        #    if respuesta.lower() == 's':
        #        aceptar_invitacion(current_user, invitacion_id)
        #    else:
        #        print("Invitación declinada o ignorada.")

        elif opcion == "0":
            print("Saliendo...")
            break
        
        elif opcion == "9":
            current_user_id, current_user_email = None, None
            print("Se ha cerrado la sesión.")
    

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()