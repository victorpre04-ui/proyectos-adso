import os
from datetime import datetime

print("--- ESCÁNER PROFESIONAL ADSO 3.0 ---")

objetivos = ["8.8.8.8", "1.1.1.1", "google.com","192.168.1.1", "github.com"]
# Creamos (o abrimos) un archivo llamado reporte.txt
with open("reporte_escaneo.txt", "a") as archivo:
    archivo.write(f"\n--- Escaneo del {datetime.now()} ---\n")
    
    for host in objetivos:
        respuesta = os.system(f"ping -c 1 {host}")
        
        if respuesta == 0:
            resultado = f"[+] {host} está ONLINE"
        else:
            resultado = f"[-] {host} está OFFLINE"
        
        print(resultado)
        archivo.write(resultado + "\n")

print("\n--- Resultados guardados en reporte_escaneo.txt ---")
