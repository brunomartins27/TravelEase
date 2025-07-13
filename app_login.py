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
root.geometry("440x490")
root.configure(bg="#f8fafd")

card = tk.Frame(root, bg="white", bd=0, highlightthickness=0)
card.place(relx=0.5, rely=0.5, anchor="center", width=440, height=490)

shadow = tk.Frame(root, bg="#dde6ed", bd=0)
shadow.place(relx=0.5, rely=0.5, anchor="center", width=455, height=505)

card.lift()

tk.Label(card, text="TravelEase", font=("Helvetica", 22, "bold"), fg="#0066cc", bg="white").pack(pady=(20, 10))

style_label = {"bg": "white", "font": ("Segoe UI", 11)}
style_entry = {
    "bg": "#f6f6fa",
    "relief": "flat",
    "font": ("Segoe UI", 11),
    "highlightthickness": 2,
    "highlightbackground": "#e0e7ef",
    "highlightcolor": "#66bfff",
    "bd": 0,
    "insertbackground": "#0066cc"
}
style_button = {
    "font": ("Segoe UI", 11, "bold"),
    "bd": 0,
    "relief": "flat",
    "activebackground": "#0080ff",
    "activeforeground": "white",
    "cursor": "hand2"
}

tk.Label(card, text="Nombre", **style_label).pack(anchor="w", padx=30)
entry_nombre = tk.Entry(card, **style_entry)
entry_nombre.pack(padx=30, fill="x", pady=(0, 10), ipady=6)
entry_nombre.configure(highlightbackground="#e0e7ef", highlightcolor="#66bfff")

tk.Label(card, text="Email", **style_label).pack(anchor="w", padx=30)
entry_email = tk.Entry(card, **style_entry)
entry_email.pack(padx=30, fill="x", pady=(0, 10), ipady=6)
entry_email.configure(highlightbackground="#e0e7ef", highlightcolor="#66bfff")

tk.Label(card, text="Contraseña", **style_label).pack(anchor="w", padx=30)
entry_contraseña = tk.Entry(card, show="*", **style_entry)
entry_contraseña.pack(padx=30, fill="x", pady=(0, 18), ipady=6)
entry_contraseña.configure(highlightbackground="#e0e7ef", highlightcolor="#66bfff")

def on_enter(e): e.widget.config(highlightbackground="#66bfff")
def on_leave(e): e.widget.config(highlightbackground="#e0e7ef")
for entry in [entry_nombre, entry_email, entry_contraseña]:
    entry.bind("<FocusIn>", on_enter)
    entry.bind("<FocusOut>", on_leave)

btn_registrar = tk.Button(
    card, text="Registrarse", command=registrar,
    bg="#00cc66", fg="white", **style_button
)
btn_registrar.pack(pady=(0, 8), padx=30, fill="x", ipady=6)
btn_registrar.config(activebackground="#22e38d")

btn_login = tk.Button(
    card, text="Iniciar Sesión", command=login,
    bg="#0066cc", fg="white", **style_button
)
btn_login.pack(padx=30, fill="x", ipady=6)
btn_login.config(activebackground="#0099ff")


root.mainloop()
