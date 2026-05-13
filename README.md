# Generador comandos cisco IOS con Groq

## Descripción

Este proyecto genera configuraciones Cisco IOS usando Python y la API de Groq.

El programa funciona desde consola y permite crear configuraciones para:

- VLAN
- OSPF
- Subnetting
- Access-Lists

Las respuestas se muestran en tiempo real y también se guardan en la carpeta `/configs`.



## Instalación

Instalar dependencias:

```bash
pip install -r requirements.txt
```

## Ejecutar programa

```bash
py cisco_config_gen.py
```

---

## Modelo utilizado

```txt
llama-3.3-70b-versatile
```

---

## Parámetros

- temperature = 0.2
- max_tokens = 800
- stream = True

---

## Validaciones

- VLAN entre 1 y 4094
- Prefijo CIDR entre 1 y 30
- Validación de OSPF
- Validación de ACL

---

## Manejo de errores

El programa detecta:

- API Key faltante
- Error de red
- Error 429
- Datos inválidos

## Integrantes

- Vicente Vega Yañez

---

