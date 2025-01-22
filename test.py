import firebase_admin
from firebase_admin import credentials, auth, db
import requests

# Inicializar Firebase con las credenciales
def initialize_firebase():
    cred = credentials.Certificate('testpython-673c0-firebase-adminsdk-b93r7-ed88edb4da.json')
    firebase_admin.initialize_app(cred, {"databaseURL": "https://testpython-673c0-default-rtdb.firebaseio.com/"})
    print("Firebase inicializado.")

# Función para registrar un nuevo usuario en Firebase Authentication
def sign_up(email, password, display_name):
    try:
        user = auth.create_user(
            email=email,
            password=password,
            display_name=display_name
        )
        print(f"\n¡Usuario registrado exitosamente!")
        print(f"Usuario creado: {user.uid}")
        print(f"Nombre: {user.display_name}")
        print(f"Email: {user.email}")
        
        # Agregar el usuario a la base de datos Realtime
        ref = db.reference(f'users/{user.uid}')
        ref.set({
            'email': email,
            'display_name': display_name
        })
        print("Usuario agregado a la base de datos.")
    except Exception as e:
        print(f"Error: {e}")

# Función para iniciar sesión
def sign_in(email, password, api_key):
    url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }
    
    try:
        # Hacer la solicitud POST a la API de Firebase Authentication
        response = requests.post(f"{url}?key={api_key}", json=payload)
        response_data = response.json()
        
        # Verificar si el inicio de sesión fue exitoso
        if response.status_code == 200:
            print(f"\nBienvenido al juego!")
        else:
            print(f"Error: {response_data['error']['message']}")
    except Exception as e:
        print(f"Error en el inicio de sesión: {e}")

# Función principal para el flujo interactivo
def main():
    print("Bienvenido, por favor ingresa tus datos.")
    
    # Solicitar el correo y contraseña
    email = input("Introduce tu correo electrónico: ")
    password = input("Introduce tu contraseña: ")
    
    # Verificar si el usuario existe en Firebase Authentication
    try:
        user = auth.get_user_by_email(email)
        print(f"Usuario encontrado: {user.display_name}")
        
        # Si el usuario existe, iniciar sesión
        api_key = "AIzaSyBN0ttX9ElGFnmaO0y2HLZEv1HAjnd8cgc" # Reemplazar con tu clave API de Firebase
        sign_in(email, password, api_key)
    
    except auth.UserNotFoundError:
        # Si el usuario no existe, solicitar los datos para registrarlo
        print("Usuario no encontrado.")
        display_name = input("Introduce tu nombre de usuario: ")
        
        # Registrar nuevo usuario
        sign_up(email, password, display_name)

# Ejecutar el flujo principal
if __name__ == "__main__":
    initialize_firebase()  # Inicializar Firebase
    main()  # Ejecutar el flujo de inicio de sesión y registro
