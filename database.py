import json
import os
from datetime import datetime

# ---------- EVENTOS ----------
RUTA_ARCHIVO = "data/eventos.json"

def cargar_eventos():
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w") as f:
            json.dump([], f)

    with open(RUTA_ARCHIVO, "r") as f:
        try:
            datos = json.load(f)
            if isinstance(datos, list):
                return datos
            else:
                return []  # si por error hay un dict, lo ignora
        except json.JSONDecodeError:
            return []

def guardar_eventos(eventos):
    with open(RUTA_ARCHIVO, "w") as f:
        json.dump(eventos, f, indent=4)

def agregar_evento(nombre, fecha, hora, prioridad, responsable, categoria, ubicacion, estado):
    eventos = cargar_eventos()
    nuevo_evento = {
        "nombre": nombre,
        "fecha": fecha,
        "hora": hora,
        "prioridad": prioridad,
        "responsable": responsable,
        "categoria": categoria,
        "ubicacion": ubicacion,
        "estado": estado
    }
    eventos.append(nuevo_evento)
    guardar_eventos(eventos)

def filtrar_eventos(prioridad=None, categoria=None, ubicacion=None, responsable=None, estado=None, fecha_inicio=None, fecha_fin=None):
    eventos = cargar_eventos()
    eventos_filtrados = []

    for evento in eventos:
        if prioridad and evento.get("prioridad") != prioridad:
            continue
        if categoria and evento.get("categoria") != categoria:
            continue
        if ubicacion and evento.get("ubicacion") != ubicacion:
            continue
        if responsable and evento.get("responsable") != responsable:
            continue
        if estado and evento.get("estado") != estado:
            continue
        if fecha_inicio and datetime.strptime(evento.get("fecha"), "%Y-%m-%d") < datetime.strptime(fecha_inicio, "%Y-%m-%d"):
            continue
        if fecha_fin and datetime.strptime(evento.get("fecha"), "%Y-%m-%d") > datetime.strptime(fecha_fin, "%Y-%m-%d"):
            continue

        eventos_filtrados.append(evento)

    # Asegúrate de que siempre devuelvas la lista de eventos
    return eventos_filtrados


def modificar_evento(nombre_original, fecha_original, nuevos_datos):
    eventos = cargar_eventos()
    evento_modificado = False

    for evento in eventos:
        if evento["nombre"] == nombre_original and evento["fecha"] == fecha_original:
            evento.update(nuevos_datos)  # Actualiza los datos del evento
            evento_modificado = True
            break

    if evento_modificado:
        guardar_eventos(eventos)
        return True
    else:
        return False

def eliminar_evento(nombre, fecha):
    eventos = cargar_eventos()
    eventos_filtrados = [evento for evento in eventos if not (evento["nombre"] == nombre and evento["fecha"] == fecha)]

    if len(eventos_filtrados) < len(eventos):
        guardar_eventos(eventos_filtrados)
        return True
    else:
        return False
    


# ---------- USUARIOS ----------
RUTA_USUARIOS = "data/usuarios.json"

def cargar_usuarios():
    if not os.path.exists(RUTA_USUARIOS):
        with open(RUTA_USUARIOS, "w") as f:
            json.dump({}, f)

    with open(RUTA_USUARIOS, "r") as f:
        usuarios = json.load(f)

    # Si hay usuarios en formato antiguo (solo contraseña como string), los convertimos
    if isinstance(usuarios, dict):
        for user, value in list(usuarios.items()):
            if isinstance(value, str):  # está en formato viejo
                usuarios[user] = {
                    "contrasena": value,
                    "tema": "light"
                }
        guardar_usuarios(usuarios)

    return usuarios

def guardar_usuarios(usuarios):
    with open(RUTA_USUARIOS, "w") as f:
        json.dump(usuarios, f, indent=4)

def verificar_credenciales(usuario, contrasena):
    usuarios = cargar_usuarios()
    return usuario in usuarios and usuarios[usuario]["contrasena"] == contrasena

def agregar_usuario(usuario, contrasena):
    usuarios = cargar_usuarios()
    if usuario in usuarios:
        return False
    usuarios[usuario] = {
        "contrasena": contrasena,
        "tema": "dark"
    }
    guardar_usuarios(usuarios)
    return True

def obtener_tema_usuario(usuario):
    usuarios = cargar_usuarios()
    if usuario in usuarios:
        return usuarios[usuario].get("tema", "dark")
    return "dark"

def cambiar_tema_usuario(usuario, nuevo_tema):
    usuarios = cargar_usuarios()
    if usuario in usuarios:
        usuarios[usuario]["tema"] = nuevo_tema
        guardar_usuarios(usuarios)
        return True
    return False
