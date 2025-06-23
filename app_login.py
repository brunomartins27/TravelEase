import tkinter as tk
from tkinter import messagebox
from usuario_service import registrar_usuario, autenticar_usuario
from paquete_service import cargar_paquetes_iniciales
from interfaz_menu import mostrar_menu_principal

cargar_paquetes_iniciales()

def registrar():
    nombre = entry_nombre.get().strip()
    email = entry_email.get().strip()
    contraseña = entry_contraseña.get().strip()
    if not nombre or not email or not contraseña:
        messagebox.showwarning("Campos vacíos", "Completá Nombre, Email y Contraseña.")
        return
    ok, msg = registrar_usuario(nombre, email, contraseña)
    if ok:
        messagebox.showinfo("Registro exitoso", msg)
        entry_nombre.delete(0, tk.END)
        entry_email.delete(0, tk.END)
        entry_contraseña.delete(0, tk.END)
    else:
        messagebox.showerror("Error", msg)

def login():
    email = entry_email.get().strip()
    contraseña = entry_contraseña.get().strip()
    if not email or not contraseña:
        messagebox.showwarning("Campos vacíos", "Ingresá Email y Contraseña para iniciar sesión.")
        return
    ok, data = autenticar_usuario(email, contraseña)
    if ok:
        root.destroy()
        mostrar_menu_principal(data)
    else:
        messagebox.showerror("Error", data)

root = tk.Tk()
root.title("TravelEase – Login / Registro")
root.geometry("400x350")
root.configure(bg="white")

tk.Label(root, text="TravelEase", font=("Helvetica", 20, "bold"), fg="#0066cc", bg="white").pack(pady=15)
tk.Label(root, text="Nombre", bg="white").pack(anchor="w", padx=50)
entry_nombre = tk.Entry(root, bg="white", relief="solid", bd=1)
entry_nombre.pack(padx=50, fill="x", pady=(0,10))
tk.Label(root, text="Email", bg="white").pack(anchor="w", padx=50)
entry_email = tk.Entry(root, bg="white", relief="solid", bd=1)
entry_email.pack(padx=50, fill="x", pady=(0,10))
tk.Label(root, text="Contraseña", bg="white").pack(anchor="w", padx=50)
entry_contraseña = tk.Entry(root, show="*", bg="white", relief="solid", bd=1)
entry_contraseña.pack(padx=50, fill="x", pady=(0,20))

tk.Button(root, text="Registrarse", command=registrar, bg="#00cc66", fg="white", width=20).pack(pady=(0,10))
tk.Button(root, text="Iniciar Sesión", command=login, bg="#0066cc", fg="white", width=20).pack()

root.mainloop()
