#firebase_adminsdk.py jdfr
import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("keys.json")
firebase_admin.initialize_app(cred)
