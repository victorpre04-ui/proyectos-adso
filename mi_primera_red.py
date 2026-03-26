# Mi primer script de seguridad en Python
import os

print("--- BIENVENIDO AL MONITOR DE RED DE VICTOR ---")
ip = input("Introduce una dirección IP para probar conexion (ejemplo: 8.8.8.8): ")

print(f"Verificando estado de {ip}...")
respuesta = os.system(f"ping -c 4 {ip}")

if respuesta == 0:
   print(f"\n[ÉXITO] La IP {ip} esta activa.")
else:
   print(f"\n[ALERTA] no se pudo contactar con {ip}.")
