#main.py jdfr
from firestore_db import Agenda, Contacto
from users import aceptar_invitacion, Usuario, login_user, register_user, email_already_registered
from google.cloud import firestore
import re

current_user = Usuario(user_id='id_del_usuario_actual', email='email_del_usuario_actual')
# agenda = Agenda()

def guardar_contacto(agenda, contacto, current_user_email):
    try:
        agenda.agregar_contacto(contacto, current_user_email)
        print(f"Contacto '{contacto.nombre}' guardado exitosamente en ", current_user_email,".")
    except Exception as e:
        print(f"Ocurrió un error al guardar el contacto: {e}")

def mostrar_agenda(agenda):
    print("Contactos en la agenda:")
    for contacto in agenda.obtener_contactos():
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
    agenda.eliminar_contacto(contacto, current_user_email)
    print(f"Contacto '{contacto.nombre}' ha sido borrado.")
def buscarContactoEmail(agenda:Agenda,correo:str,current_user_email:str):
    return agenda.correoContactoExiste(correo,current_user_email)
def main():
    current_user_id, current_user_email = None, None
    mi_agenda = Agenda(owner_id=current_user_id)
    current_user_id, current_user_email = None, None  

    while True:
        if not current_user_id:
            print("")
            print("-------Bienvenido----------")
            print("1. Registrarse")
            print("2. Iniciar sesión ")            
            opcion_inicio = input("Seleccione una opción: ")
            #opcion_inicio="2"
            print("*****************************************************")  
            
            while True:
                if opcion_inicio == "1":
                        email = input("Por favor ingrese su email: ")
                        #email="orojasa@toluca.tecnm.mx"
                        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                            print("Error: el formato de correo electrónico no es válido.")
                            continue
                        
                        password = input("Por favor ingrese su contraseña: ")
                        #password="123456"
                        if len(password) < 6:
                            print("Error: la contraseña debe tener al menos 6 caracteres.")
                            continue
                        
                        if email_already_registered(email):
                            print("Error: el correo ya está registrado.")
                            break
                        current_user_id, current_user_email = register_user(email, password)

                        print("*****************************************************")  
                        if current_user_id:
                            print(f"Bienvenido {current_user_email}")
                            print("*****************************************************")  
                        else:
                            print("Error al registrar el usuario. Intente de nuevo.") 
                        input("Presione una tecla para continuar ..")     

                if opcion_inicio == "2":
                    email = input("Por favor ingrese su email: ")
                    password = input("Por favor ingrese su contraseña: ")
                    #email = "orojasa@toluca.tecnm.mx"
                    #password = "123456"
                    current_user_id, current_user_email = login_user(email, password)#se hace el login, donde se guarda el token y el correo con el que inicia sesión
                    print("*****************************************************")  

                    if current_user_id:
                        print(f"Bienvenido {current_user_email}")
                        print("*****************************************************")
                        input("Presione una tecla para continuar ..")
                    else:
                        print("Inicio de sesión fallido, intente de nuevo.")
                        input("Presione una tecla para continuar ..")
                        continue #inicia una nueva iteración del ciclo que contiene la sentencia
                break 

        print("")
        print("1. Crear nuevo contacto")
        print("2. Mostrar Agenda")
        print("3. Buscar contacto por nombre")
        print("4. Buscar contacto por teléfono")
        print("5. Borrar contacto")
        #print("6. Compartir mi agenda")
        print("6. Ver agendas de usuarios disponibles.")
        print("7. Responder a una invitación")
        print("8. Salir")
        print("")

        opcion = input("Seleccione una opción: ")
        #opcion = "5"
        print("")
        
        if opcion == "1":
            print("Ingrese los datos del nuevo contacto:")
            while True:
                nombre = input("Nombre: ")
                #nombre = "some name"
                if not nombre.strip():
                    print("El nombre no puede estar vacío.")
                    input("Presione una tecla para continuar ..")
                    continue
                elif not all(x.isalpha() or x.isspace() for x in nombre):
                    print("El nombre solo puede contener letras y espacios.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                edad = input("Edad: ")
                #edad="40"
                if not edad.isdigit() or not 0 < int(edad) < 120:
                    print("La edad debe estar entre 1 y 119 años.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                calle = input("Calle: ")
                #calle="calle ejemplo"
                if not calle.strip():
                    print("La calle no puede estar vacía.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                ciudad = input("Ciudad: ")
                #ciudad = "ciudad ejemplo"
                if not ciudad.strip():
                    print("La ciudad no puede estar vacía.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                codigo_postal = input("Código Postal: ")
                #codigo_postal = "12345"
                if not re.match(r"^\d{5}$", codigo_postal):
                    print("El código postal debe tener 5 dígitos.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                numero_exterior = input("Número Exterior: ")
                #numero_exterior= "10"
                if not numero_exterior.strip():
                    print("El número exterior no puede estar vacío.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            numero_interior = input("Número Interior (opcional): ")
            #numero_interior = "1"
            while True:
                colonia = input("Colonia: ")
                #colonia = "Colonia Ejemplo"
                if not colonia.strip():
                    print("La colonia no puede estar vacía.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                numero = input("Número de Teléfono: ")
                #numero = "1234567890"
                if not re.match(r"^\+?[\d\s]{3,}$", numero):
                    print("El número de teléfono es inválido.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                email = input("Correo Electrónico: ")
                #email = "correo@ejemplo.com"
                if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
                    print("El correo electrónico no tiene un formato válido.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            while True:
                pagina_web = input("Página Web (opcional): ")
                #pagina_web="https://demo.bpmn.io/"
                if pagina_web and not re.match(r"^https?:\/\/.*\..+$", pagina_web):
                    print("La página web tiene un formato inválido.")
                    input("Presione una tecla para continuar ..")
                    continue
                break
            edad = int(edad)#parsea la edad a numero
            if buscarContactoEmail(mi_agenda,email,current_user_email):
                    print("El correo de este contacto ya está registrado, cancelando...")
                    input("Presione una tecla para continuar ..")
                    continue
            nuevo_contacto = Contacto(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web)
            guardar_contacto(mi_agenda, nuevo_contacto, current_user_email)

        elif opcion == "2":
            mostrar_agenda(mi_agenda)
            input("Presione una tecla para continuar ..")

        elif opcion == "3":
            nombre = input("Ingrese el nombre a buscar: ")
            contacto_encontrado = mi_agenda.buscar_contacto_por_nombre(nombre, current_user_email)
            if contacto_encontrado:
                mostrar_informacion_contacto(contacto_encontrado)
            else:
                print("Contacto no encontrado.")
            input("Presione una tecla para continuar ..")

        elif opcion == "4":
            numero = input("Ingrese el número de teléfono a buscar: ")
            contacto_encontrado = mi_agenda.buscar_contacto_por_telefono(numero)
            if contacto_encontrado:
                mostrar_informacion_contacto(contacto_encontrado)
            else:
                print("Contacto no encontrado.")
            input("Presione una tecla para continuar ..")               
        elif opcion == "5":
            while True:
                nombre = input("Ingrese el email del contacto a borrar: \nDigite \"2\" para cancelar operación\n>")
                if nombre!="2":
                    contacto_a_borrar = mi_agenda.buscar_contacto_por_correo(nombre, current_user_email)
                    if contacto_a_borrar:
                        while True:
                            confirmacion=input("Contacto encontrado : "+contacto_a_borrar.nombre+","+contacto_a_borrar.email+"\nPor favor, confirme la eliminación (y/n)\n>")
                            if confirmacion =="y" or confirmacion=="n":
                                if confirmacion == "y":
                                    borrar_contacto(mi_agenda, contacto_a_borrar, current_user_email)
                                    print("Usuario eliminado con exito!")
                                    input("Presione una tecla para continuar ..")
                                break
                            else:
                                print("Opción no válida")
                                input("Presione una tecla para continuar ..")
                        break
                    else:
                        print("Contacto no encontrado.")
                        input("Presione una tecla para continuar ..")
                else:
                    break

        elif opcion == "6":
            """print("Enviar una invitación para compartir tu agenda.")
            agenda_id = input("ID de la agenda a compartir: ")
            receptor_email = input("Email del usuario con quien compartir: ")
            nivel_de_acceso = input("Nivel de acceso (lectura/escritura): ")
            enviar_invitacion(agenda_id, current_user.user_id, receptor_email, nivel_de_acceso)"""
            print("Estas son las agendas disponibles: ")
            current_user.visualizar_agendas_disponibles()

        elif opcion == "7":
            print("Responder a invitaciones pendientes.")
            invitacion_id = input("ID de la invitación a responder: ")
            respuesta = input("Aceptas la invitación? (s/n): ")
            if respuesta.lower() == 's':
                aceptar_invitacion(current_user, invitacion_id)
            else:
                print("Invitación declinada o ignorada.")

        elif opcion == "8":
            print("Saliendo...")
            input("Presione una tecla para continuar ..")
            break
        
        elif opcion == "9":
            current_user_id, current_user_email = None, None
            print("Se ha cerrado la sesión.")
    

        else:
            print("Opción no válida. Intente nuevamente.")

if __name__ == "__main__":
    main()