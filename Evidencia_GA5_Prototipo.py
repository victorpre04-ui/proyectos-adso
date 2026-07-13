import tkinter as tk
from tkinter import messagebox

# Función para la pantalla de error que pide la guía
def mostrar_error():
    messagebox.showerror("Error de Sistema", "Datos incorrectos. Intente de nuevo.")

app = tk.Tk()
app.title("Prototipo Espigas s.a ESP")
app.geometry("400x300")
app.configure(bg='#2c3e50') # Color 1: Azul oscuro

# Componentes de la pantalla de Registro
tk.Label(app, text="Registro de Usuario", bg='#2c3e50', fg='white', font=('Arial', 14)).pack(pady=10)

# Campo Cédula (Pide la guía)
tk.Label(app, text="Cédula:", bg='#2c3e50', fg='white').pack()
tk.Entry(app).pack(pady=5)

# Botones con los otros 2 colores de la guía
tk.Button(app, text="Guardar Datos", bg='#27ae60', fg='white').pack(pady=10) # Color 2: Verde
tk.Button(app, text="Simular Error", bg='#e74c3c', fg='white', command=mostrar_error).pack() # Color 3: Rojo

app.mainloop()