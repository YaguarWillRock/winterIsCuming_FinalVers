
#users.py jdfr
from firebase_admin import auth, firestore, exceptions
from firestore_db import db
import requests
import json

class Usuario:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.agendas_compartidas = []  

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'agendas_compartidas': self.agendas_compartidas,
        }
        
    def visualizar_agendas_disponibles(self):
        colecciones = [coleccion.id for coleccion in db.collections()]
        print('Colecciones en la base de datos:')
        for nombre_coleccion in colecciones:
            print(nombre_coleccion)

def verify_user(token):
    decoded_token = auth.verify_id_token(token)
    uid = decoded_token.get('uid')
    return uid  

def enviar_invitacion(agenda_id, emisor_user_id, receptor_email, nivel_de_acceso):
    receptor_user_id = buscar_usuario_por_email(receptor_email)
    if receptor_user_id:
        db.collection('invitaciones').add({
            'agenda_id': agenda_id,
            'emisor_user_id': emisor_user_id,
            'receptor_user_id': receptor_user_id,
            'nivel_de_acceso': nivel_de_acceso,
            'estado': 'pendiente'
        })
        print(f"Invitación enviada a {receptor_email}")
    else:
        print("Usuario no encontrado.")

def buscar_usuario_por_email(email):
    usuarios_ref = db.collection('usuarios')
    query = usuarios_ref.where('email', '==', email).limit(1)
    results = query.stream()
    for result in results:
        return result.id 
    return None  

def aceptar_invitacion(usuario, invitacion_id):
    invitacion_ref = db.collection('invitaciones').document(invitacion_id)
    invitacion = invitacion_ref.get()
    if invitacion.exists:
        invitacion_data = invitacion.to_dict()
        usuario.agendas_compartidas.append(invitacion_data['agenda_id'])
        invitacion_ref.update({'estado': 'aceptada'})
        agenda_ref = db.collection('agendas').document(invitacion_data['agenda_id'])
        agenda_ref.update({
            'usuarios_compartidos': firestore.ArrayUnion([usuario.user_id])
        })
        print("Invitación aceptada.")
    else:
        print("La invitación no existe o ya fue procesada.")
        
def login_user(email, password):
    api_key = 'AIzaSyAfbXWM4PF78u7JkdfXpoBSjy3jKbXEErc'#clave de seguridad dada por firebase
    url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={api_key}"#endpoint de firebase para acceder a la base
    headers = {#talves esto es para marcar que se trabajará con json
        "Content-Type": "application/json"
    }
    data = {#aqui se construye el json
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    #headers=headres, no tiene sentido, data=json.dombs, tampoco xd
    response = requests.post(url, headers=headers, data=json.dumps(data))#se consume una API de firebase donde se mandan las credenciales
    if response.status_code == 200:#codigo 200 web = ok, 400 = bad request (credenciales incorrectas)
        user_data = response.json()#json que retorna el post
        return user_data['localId'], user_data['email']#se regresan 2 variables, una contiene un token y otra el email con el que se inicia sesión
    else:
        print(f"Error de autenticación: {response.json()['error']['message']}")
        return None, None
    
def register_user(email, password, contact_info):
    try:
        auth.get_user_by_email(email)
        print("El correo ya está registrado.")
        return None, None
    except exceptions.NotFoundError:
        user = auth.create_user(
            email=email,
            password=password
        )
        print(f"Usuario registrado con UID: {user.uid}")

        coleccion = db.collection(email)
        documentos = coleccion.limit(1).get()

        if documentos:
            print(f'La agenda de "{email}" ya existe.')
        else:
            print(f'La agenda de "{email}" no existe, se creará.')

            campos_documento = {
                'nombre': contact_info['nombre'],
                'edad': contact_info['edad'],
                'calle': contact_info['calle'],
                'ciudad': contact_info['ciudad'],
                'codigo_postal': contact_info['codigo_postal'],
                'numero_exterior': contact_info['numero_exterior'],
                'numero_interior': contact_info['numero_interior'],
                'colonia': contact_info['colonia'],
                'numero': contact_info['numero'],
                'email': contact_info['email'],
                'pagina_web': contact_info['pagina_web']
            }
            settings = {
                'escritura': '0'
            }
            coleccion.add(campos_documento)
            coleccion.add(settings)
        return user.uid, email
    except auth.AuthError as e:
        print(f"Error al registrar el usuario: {e}")
        return None, None
    except auth.EmailAlreadyExistsError:
        print("Error: el correo ya está registrado.")
        return None, None
    except auth.InvalidArgumentError:
        print("Error: el correo proporcionado no tiene un formato válido.")
        return None, None
    except Exception as e:
        print(f"Error durante el registro: {e}")
        return None, None
    
def email_already_registered(email):
    try:
        auth.get_user_by_email(email)
        return True
    except auth.UserNotFoundError:
        return False
    except auth.AuthError as e:
        print(f"Error al verificar el email: {e}")
        return False