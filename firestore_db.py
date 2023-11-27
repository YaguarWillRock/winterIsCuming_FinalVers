#firestore_db.py jdfr
import firebase_admin
from firebase_admin import credentials, firestore
import warnings
import re


cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

"""class Usuario:
    def __init__(self, user_id, email):
        self.user_id = user_id
        self.email = email
        self.agendas_compartidas = [] 

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'agendas_compartidas': self.agendas_compartidas,
        }"""

class Direccion:
    def __init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia):
        self.calle = calle
        self.ciudad = ciudad
        self.codigo_postal = codigo_postal
        self.numero_exterior = numero_exterior
        self.numero_interior = numero_interior
        self.colonia = colonia

    def to_dict(self):
        return vars(self)

class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def to_dict(self):
        return vars(self)

class Telefono:
    def __init__(self, numero):
        self.numero = numero

    def to_dict(self):
        return vars(self)

class CorreoElectronico:
    def __init__(self, email, pagina_web):
        self.email = email
        self.pagina_web = pagina_web

    def to_dict(self):
        return vars(self)

class Contacto(Persona, Direccion, Telefono, CorreoElectronico):
    def __init__(self, nombre,edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web, doc_id=None):
        Persona.__init__(self, nombre, edad)
        Direccion.__init__(self, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia)
        Telefono.__init__(self, numero)
        CorreoElectronico.__init__(self, email, pagina_web)
        self.doc_id = doc_id 
        
    @staticmethod
    def validar_datos(nombre, edad, calle, ciudad, codigo_postal, numero_exterior, numero_interior, colonia, numero, email, pagina_web):
        errores = []
        
        if not nombre.strip():
            errores.append("El nombre no puede estar vacío.")
        elif not all(x.isalpha() or x.isspace() for x in nombre):
            errores.append("El nombre solo puede contener letras y espacios.")
        
        try:
            edad = int(edad)
            if not 0 < edad < 120:
                errores.append("La edad debe estar entre 1 y 119 años.")
        except ValueError:
            errores.append("La edad debe ser un número.")
        
        if not calle.strip():
            errores.append("La calle no puede estar vacía.")
        
        if not ciudad.strip():
            errores.append("La ciudad no puede estar vacía.")
        
        if not re.match(r"^\d{5}$", codigo_postal):
            errores.append("El código postal debe tener 5 dígitos.")
        
        if not numero_exterior.strip():
            errores.append("El número exterior no puede estar vacío.")
        
        if not colonia.strip():
            errores.append("La colonia no puede estar vacía.")
        
        if not re.match(r"^\+?[\d\s]{3,}$", numero):
            errores.append("El número de teléfono es inválido.")
        
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            errores.append("El correo electrónico no tiene un formato válido.")
        
        if pagina_web and not re.match(r"^https?:\/\/.*\..+$", pagina_web):
            errores.append("La página web tiene un formato inválido.")
        
        if errores:
            return False, "Errores de validación: " + "; ".join(errores)
        return True, "Todos los datos son válidos."

    def to_dict(self):
        data = {}
        for base_class in self.__class__.__bases__:
            data.update(base_class.to_dict(self))
        return data

    def merge(self, otro_contacto):
        if otro_contacto.timestamp > self.timestamp:
            for attr, value in vars(otro_contacto).items():
                setattr(self, attr, value)

    @staticmethod
    def from_dict(source):
        contacto = Contacto(
            nombre=source['nombre'],
            edad=source['edad'],
            calle=source['calle'],
            ciudad=source['ciudad'],
            codigo_postal=source['codigo_postal'],
            numero_exterior=source['numero_exterior'],
            numero_interior=source['numero_interior'],
            colonia=source['colonia'],
            numero=source['numero'],
            email=source['email'],
            pagina_web=source['pagina_web']
        )
        return contacto

class Agenda:
    def __init__(self, owner_id):
        self.owner_id = owner_id
        self.lista_de_contactos = []
        self.usuarios_con_acceso = {}  
        #self.lista_de_contactos = []

    def agregar_contacto(self, contacto, current_user_email):
        self.lista_de_contactos.append(contacto)#agrega el contacto a la lista_de_contactos
        if contacto.doc_id is None:#esto es para ver si es que el documento existe
            new_doc_ref = db.collection(current_user_email).document("AGENDA").collection("CONTACTOS").document()#crea una nueva colección si no existe, si existe accede a la colección
            new_doc_ref.set(contacto.to_dict())#le dice a firebase que se crea un documento con id automatica
            contacto.doc_id = new_doc_ref.id #le asigna el id obtenido al documento (todo inutil por que en la siguiente linea seguro se pierde)
        else:
            db.collection(current_user_email).document(contacto.doc_id).set(contacto.to_dict())#este actualiza el documento de la nube, quzá deba ir arriba

    def cargar_contactos(self, current_user_email):
        self.lista_de_contactos = []
        contactos_ref = db.collection(current_user_email).document("AGENDA").collection("CONTACTOS")
        docs = contactos_ref.stream()
        for doc in docs:
            contacto = Contacto.from_dict(doc.to_dict())
            self.lista_de_contactos.append(contacto)

    def obtener_contactos(self):
        return self.lista_de_contactos

    def eliminar_contacto(self, contacto, current_user_email):
        if contacto.doc_id:
            db.collection(current_user_email).document("AGENDA").collection("CONTACTOS").document(contacto.doc_id).delete()
            self.cargar_contactos(current_user_email)

    def buscar_contacto_por_telefono(self, numero):
        for contacto in self.lista_de_contactos:
            if contacto.numero == numero:
                return contacto
        return None
    
    def correoContactoExiste(self, correo:str,current_user_email:str):
        warnings.filterwarnings("ignore", category=UserWarning, module='google.cloud.firestore')
        try:
            contactos_ref = db.collection(current_user_email).document("AGENDA").collection("CONTACTOS")
            query = contactos_ref.where('email', '==', correo).limit(1)
            results = query.stream()
            for result in results:
                return True
            return False
        except Exception as e:
            return False

        
    def buscar_contacto_por_correo(self, correo, current_user_email):
        warnings.filterwarnings("ignore", category=UserWarning, module='google.cloud.firestore')
        try:
            contactos_ref = db.collection(current_user_email).document("AGENDA").collection("CONTACTOS")
            query = contactos_ref.where('email', '==', correo).limit(1)
            results = query.stream()
            for result in results:
                contact_result = Contacto.from_dict(result.to_dict())
                contact_result.doc_id = str(result.id)
                return contact_result
            return None
        except Exception as e:
            print(f"Error al buscar contacto: {e}")
            return None
    def buscar_contacto_por_nombre(self, nombre, current_user_email):
        warnings.filterwarnings("ignore", category=UserWarning, module='google.cloud.firestore')
        try:
            contactos_ref = db.collection(current_user_email)
            query = contactos_ref.where('nombre', '==', nombre).limit(1)
            results = query.stream()
            for result in results:
                return Contacto.from_dict(result.to_dict())
            return None
        except Exception as e:
            print(f"Error al buscar contacto: {e}")
            return None
        
    def merge_contactos(self, otro_contacto):
        for contacto in self.lista_de_contactos:
            if contacto.nombre == otro_contacto.nombre and contacto.numero == otro_contacto.numero:
                contacto.merge(otro_contacto)
                return contacto
        self.agregar_contacto(otro_contacto)
        return otro_contacto
    
    def compartir_agenda(self, user_id, nivel_de_acceso):
        self.usuarios_con_acceso[user_id] = nivel_de_acceso