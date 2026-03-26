import os

print("--- ESCÁNER DE RED ADSO V2.0 ---")

# Esta es una LISTA de Python (va entre corchetes [])
objetivos = ["8.8.8.8", "1.1.1.1", "google.com", "192.168.1.12", "github.com"]

# El bucle 'for' recorre cada objetivo uno por uno
for host in objetivos:
    print(f"\n>>> Verificando: {host}")
    # Lanzamos el ping con solo 2 paquetes para que sea rápido (-c 2)
    respuesta = os.system(f"ping -c 2 {host}")
    
    if respuesta == 0:
        print(f"[+] {host} está ONLINE")
    else:
        print(f"[-] {host} está OFFLINE o no responde")

print("\n--- Escaneo de lista finalizado ---")
