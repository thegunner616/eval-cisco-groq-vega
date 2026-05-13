import os
from groq import Groq
from groq import RateLimitError
from groq import APIConnectionError
from dotenv import load_dotenv
from datetime import datetime

# =========================
# CARGAR VARIABLES DE ENTORNO
# =========================

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("ERROR: No se encontró GROQ_API_KEY en el archivo .env")
    exit()

# =========================
# CLIENTE GROQ
# =========================

client = Groq(api_key=api_key)

# =========================
# CREAR CARPETA CONFIGS
# =========================

if not os.path.exists("configs"):
    os.makedirs("configs")

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
Eres un experto en Cisco IOS.

Debes responder SOLO configuraciones Cisco IOS válidas.

NO expliques nada.
NO uses markdown.
NO uses bloques ```.

Puedes usar comentarios IOS con !.
"""

# =========================
# GUARDAR CONFIGURACIÓN
# =========================

def guardar_config(tipo, contenido):

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    nombre_archivo = f"configs/escenario_{tipo}_{timestamp}.txt"

    with open(nombre_archivo, "w") as archivo:
        archivo.write(contenido)

    print(f"\n\nConfiguración guardada en: {nombre_archivo}")

# =========================
# GENERAR CONFIGURACIÓN
# =========================

def generar_config(prompt_usuario, tipo):

    try:

        stream = client.chat.completions.create(

            model="llama-3.3-70b-versatile",

            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": prompt_usuario
                }
            ],

            # RESPUESTAS DETERMINÍSTICAS
            temperature=0.2,

            # CONFIGURACIONES LARGAS
            max_tokens=800,

            # STREAMING EN TIEMPO REAL
            stream=True
        )

        respuesta_completa = ""

        print("\n===== CONFIGURACIÓN GENERADA =====\n")

        # STREAMING
        for chunk in stream:

            contenido = chunk.choices[0].delta.content or ""

            print(contenido, end="")

            respuesta_completa += contenido

        guardar_config(tipo, respuesta_completa)

    # RATE LIMIT 429
    except RateLimitError:
        print("\nERROR 429: Límite de solicitudes alcanzado.")
        print("Espere unos segundos e intente nuevamente.")

    # ERROR DE RED
    except APIConnectionError:
        print("\nERROR DE RED: No se pudo conectar con la API de Groq.")

    # OTROS ERRORES
    except Exception as e:
        print(f"\nERROR GENERAL: {e}")

# =========================
# VALIDAR VLAN
# =========================

def validar_vlan(vlan):

    return 1 <= vlan <= 4094

# =========================
# ESCENARIO VLAN
# =========================

def escenario_vlan():

    try:

        print("\n===== CONFIGURACIÓN VLAN =====")

        vlan = int(input("Ingrese VLAN ID (1-4094): "))

        # VALIDACIÓN VLAN
        if not validar_vlan(vlan):
            print("ERROR: VLAN fuera de rango válido (1-4094)")
            return

        nombre = input("Nombre VLAN: ").strip()

        if not nombre:
            print("ERROR: El nombre no puede estar vacío")
            return

        puertos = input("Puertos (ej: fa0/1-fa0/5): ").strip()

        if not puertos:
            print("ERROR: Debe ingresar puertos")
            return

        prompt = f"""
        Genera configuración Cisco IOS para una VLAN.

        VLAN ID: {vlan}
        Nombre VLAN: {nombre}
        Puertos: {puertos}

        Incluye:
        - creación de VLAN
        - nombre VLAN
        - asignación de puertos
        - switchport access
        """

        generar_config(prompt, "vlan")

    except ValueError:
        print("ERROR: VLAN debe ser numérica")

# =========================
# ESCENARIO OSPF
# =========================

def escenario_ospf():

    try:

        print("\n===== CONFIGURACIÓN OSPF =====")

        proceso = int(input("ID proceso OSPF: "))

        # VALIDACIÓN PROCESO
        if proceso < 1:
            print("ERROR: ID OSPF inválido")
            return

        red = input("Red a anunciar (ej: 192.168.1.0 0.0.0.255): ").strip()

        if not red:
            print("ERROR: Debe ingresar red")
            return

        area = int(input("Área OSPF: "))

        # VALIDACIÓN ÁREA
        if area < 0:
            print("ERROR: Área inválida")
            return

        prompt = f"""
        Genera configuración Cisco IOS para OSPF.

        Proceso OSPF: {proceso}
        Red: {red}
        Área: {area}

        Incluye:
        - router ospf
        - network
        - area
        """

        generar_config(prompt, "ospf")

    except ValueError:
        print("ERROR: Debe ingresar valores válidos")

# =========================
# ESCENARIO SUBNETTING
# =========================

def escenario_subnet():

    try:

        print("\n===== CONFIGURACIÓN SUBNETTING =====")

        red = input("Red base: ").strip()

        if not red:
            print("ERROR: Debe ingresar red base")
            return

        prefijo = int(input("Prefijo CIDR (1-30): "))

        # VALIDACIÓN PREFIJO
        if prefijo < 1 or prefijo > 30:
            print("ERROR: Prefijo fuera de rango válido (1-30)")
            return

        subredes = int(input("Cantidad de subredes: "))

        # VALIDACIÓN SUBREDES
        if subredes <= 0:
            print("ERROR: Cantidad de subredes inválida")
            return

        prompt = f"""
        Genera configuración Cisco IOS realizando subnetting.

        Red base: {red}/{prefijo}
        Cantidad de subredes: {subredes}

        Incluye:
        - subnetting
        - máscaras
        - interfaces
        - direcciones IP
        - comandos Cisco IOS válidos
        """

        generar_config(prompt, "subnet")

    except ValueError:
        print("ERROR: Debe ingresar valores numéricos válidos")

# =========================
# ESCENARIO ACL
# =========================

def escenario_acl():

    try:

        print("\n===== CONFIGURACIÓN ACL =====")

        numero_acl = int(input("Número ACL (1-199): "))

        # VALIDACIÓN ACL
        if numero_acl < 1 or numero_acl > 199:
            print("ERROR: Número ACL fuera de rango válido (1-199)")
            return

        accion = input("Acción (permit/deny): ").lower().strip()

        # VALIDACIÓN ACCIÓN
        if accion not in ["permit", "deny"]:
            print("ERROR: Acción inválida")
            return

        origen = input("Red origen (ej: 192.168.1.0): ").strip()

        if not origen:
            print("ERROR: Debe ingresar red origen")
            return

        wildcard = input("Wildcard mask (ej: 0.0.0.255): ").strip()

        if not wildcard:
            print("ERROR: Debe ingresar wildcard mask")
            return

        destino = input("Destino (any o red): ").strip()

        if not destino:
            print("ERROR: Debe ingresar destino")
            return

        prompt = f"""
        Genera configuración Cisco IOS para una Access List.

        Número ACL: {numero_acl}
        Acción: {accion}
        Origen: {origen}
        Wildcard Mask: {wildcard}
        Destino: {destino}

        Devuelve SOLO comandos Cisco IOS válidos.
        """

        generar_config(prompt, "acl")

    except ValueError:
        print("ERROR: Número ACL inválido")

# =========================
# MENÚ PRINCIPAL
# =========================

def menu():

    while True:

        print("\n===== GENERADOR CISCO IOS CON GROQ =====")
        print("1. Configuración VLAN")
        print("2. Configuración OSPF")
        print("3. Subnetting")
        print("4. Access List")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        if opcion == "1":
            escenario_vlan()

        elif opcion == "2":
            escenario_ospf()

        elif opcion == "3":
            escenario_subnet()

        elif opcion == "4":
            escenario_acl()

        elif opcion == "5":
            print("Saliendo...")
            break

        else:
            print("ERROR: Opción inválida")

# =========================
# MAIN
# =========================

if __name__ == "__main__":
    menu()