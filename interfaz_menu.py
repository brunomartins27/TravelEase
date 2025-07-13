import tkinter as tk
from tkinter import messagebox
from paquete_service import obtener_paquetes_disponibles
from reserva_service import crear_reservas_multiples, obtener_reservas_por_usuario, cancelar_reserva

def mostrar_menu_principal(usuario):
    root = tk.Tk()
    root.title("TravelEase – Menú Principal")
    root.geometry("680x440")
    root.configure(bg="#f8fafd")

    shadow = tk.Frame(root, bg="#dde6ed")
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=640, height=400)
    card = tk.Frame(root, bg="white")
    card.place(relx=0.5, rely=0.5, anchor="center", width=620, height=380)
    card.lift()

    style_label = {"bg": "white", "font": ("Segoe UI", 13)}
    style_listbox = {
        "bg": "#f6f6fa", "bd": 0, "font": ("Segoe UI", 11), "highlightthickness": 1,
        "highlightbackground": "#e0e7ef", "selectbackground": "#b7e6cd", "relief": "flat"
    }
    style_button = {
        "font": ("Segoe UI", 11, "bold"), "bd": 0, "relief": "flat",
        "activebackground": "#0080ff", "activeforeground": "white", "cursor": "hand2"
    }

    tk.Label(card, text=f"Bienvenido, {usuario['nombre']}", font=("Segoe UI", 18, "bold"), fg="#0066cc", bg="white", anchor="center")\
      .grid(row=0, column=0, columnspan=3, pady=(18, 15), sticky="ew")

    tk.Label(card, text="Paquetes Disponibles:", **style_label).grid(row=1, column=0, sticky="w", padx=(22,0))
    lista_paquetes = tk.Listbox(card, selectmode=tk.MULTIPLE, width=32, height=8, **style_listbox)
    lista_paquetes.grid(row=2, column=0, padx=(22,18), pady=5)
    for p in obtener_paquetes_disponibles():
        lista_paquetes.insert(tk.END, f"{p[0]} – {p[1]} — ${p[3]}")

    tk.Button(card, text="Reservar", bg="#00cc66", fg="white",
              command=lambda: procesar_reservas(lista_paquetes, usuario, refrescar_listas),
              **style_button)\
      .grid(row=3, column=0, pady=(8, 4), padx=(22,18), sticky="ew")

    def encerrar_sesion():
        root.destroy()
    tk.Button(card, text="Encerrar sesión", bg="#cccccc", fg="black",
              command=encerrar_sesion, **style_button)\
      .grid(row=4, column=0, pady=(0, 4), padx=(22,18), sticky="ew")

    tk.Label(card, text="Mis Reservas:", **style_label).grid(row=1, column=2, sticky="w", padx=(22,0))
    lista_res = tk.Listbox(card, selectmode=tk.MULTIPLE, width=32, height=8, **style_listbox)
    lista_res.grid(row=2, column=2, padx=(22,18), pady=5)

    tk.Button(card, text="Pagar Reservas", bg="#0066cc", fg="white",
              command=lambda: abrir_metodo_pago(root, lista_res),
              **style_button)\
      .grid(row=3, column=2, pady=(8,4), padx=(18,22), sticky="ew")

    tk.Button(card, text="Eliminar Reservas", bg="#cc3333", fg="white",
              command=lambda: eliminar_seleccion(lista_res, refrescar_listas),
              **style_button)\
      .grid(row=4, column=2, pady=(0,4), padx=(18,22), sticky="ew")

    def refrescar_listas():
        lista_paquetes.delete(0, tk.END)
        for p in obtener_paquetes_disponibles():
            lista_paquetes.insert(tk.END, f"{p[0]} – {p[1]} — ${p[3]}")
        lista_res.delete(0, tk.END)
        for r in obtener_reservas_por_usuario(usuario['id']):
            lista_res.insert(tk.END, f"{r[0]} – {r[1]} — ${r[2]} ({r[3][:10]})")

    refrescar_listas()
    root.mainloop()

def procesar_reservas(lista_paquetes, usuario, refrescar_cb):
    sels = lista_paquetes.curselection()
    if not sels:
        messagebox.showwarning("Atención", "Seleccioná al menos un paquete.")
        return
    reservas = [(usuario['id'], int(lista_paquetes.get(i).split(" – ")[0])) for i in sels]
    crear_reservas_multiples(reservas)
    messagebox.showinfo("Reservas", f"{len(reservas)} reserva(s) creada(s).")
    refrescar_cb()

def abrir_metodo_pago(root, lista_res):
    sels = lista_res.curselection()
    if not sels:
        messagebox.showwarning("Atención", "Seleccioná al menos una reserva para pagar.")
        return

    ventana_pago = tk.Toplevel(root)
    ventana_pago.title("Método de Pago")
    ventana_pago.geometry("500x340")
    ventana_pago.configure(bg="#f8fafd")

    shadow = tk.Frame(ventana_pago, bg="#dde6ed")
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=440, height=270)
    card = tk.Frame(ventana_pago, bg="white")
    card.place(relx=0.5, rely=0.5, anchor="center", width=420, height=250)
    card.lift()

    style_button = {
        "font": ("Segoe UI", 13, "bold"), "bd": 0, "relief": "flat",
        "activebackground": "#0080ff", "activeforeground": "white", "cursor": "hand2"
    }

    tk.Label(card, text="Elegí el método de pago", font=("Segoe UI", 14, "bold"),
             fg="#0066cc", bg="white").pack(pady=(18, 14))

    tk.Button(card, text="Pago con Tarjeta", bg="#0066cc", fg="white",
              command=lambda: abrir_pago_tarjeta(ventana_pago, lista_res, sels),
              **style_button).pack(pady=(0, 10), padx=34, fill="x", ipady=10)
    
    tk.Button(card, text="Pago por Transferencia", bg="#008fb3", fg="white",
              command=lambda: abrir_pago_transferencia(ventana_pago),
              **style_button).pack(pady=(0, 10), padx=34, fill="x", ipady=10)

def abrir_pago_tarjeta(prev_win, lista_res, sels):
    prev_win.destroy()
    vp = tk.Toplevel()
    vp.title("Pago con Tarjeta")
    vp.geometry("620x600")
    vp.configure(bg="#f8fafd")

    shadow = tk.Frame(vp, bg="#dde6ed")
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=460, height=480)
    card = tk.Frame(vp, bg="white")
    card.place(relx=0.5, rely=0.5, anchor="center", width=620, height=640)
    card.lift()

    style_label = {"bg": "white", "font": ("Segoe UI", 13)}
    style_entry = {
        "bg": "#f6f6fa", "relief": "flat", "font": ("Segoe UI", 14),
        "highlightthickness": 2, "highlightbackground": "#e0e7ef",
        "highlightcolor": "#66bfff", "bd": 0, "insertbackground": "#0066cc"
    }
    style_button = {
        "font": ("Segoe UI", 13, "bold"), "bd": 0, "relief": "flat",
        "activebackground": "#0080ff", "activeforeground": "white", "cursor": "hand2"
    }

    fields_frame = tk.Frame(card, bg="white")
    fields_frame.pack(padx=28, pady=(30, 4), fill="x")

    tk.Label(fields_frame, text="Número de Tarjeta (XXXX-XXXX-XXXX-XXXX):", **style_label, anchor="w").pack(anchor="w")
    entry_num = tk.Entry(fields_frame, **style_entry)
    entry_num.pack(fill="x", pady=(3, 14), ipady=9)
    def format_card_number(event):
        value = entry_num.get().replace("-", "").replace(" ", "")
        value = ''.join(filter(str.isdigit, value))[:16]
        new_value = ''
        for i, char in enumerate(value):
            if i in [4, 8, 12] and i != 0:
                new_value += '-'
            new_value += char
        entry_num.delete(0, tk.END)
        entry_num.insert(0, new_value)
        entry_num.icursor(len(new_value))
    entry_num.bind("<KeyRelease>", format_card_number)

    tk.Label(fields_frame, text="Nombre y Apellido:", **style_label, anchor="w").pack(anchor="w")
    entry_name = tk.Entry(fields_frame, **style_entry)
    entry_name.pack(fill="x", pady=(3, 14), ipady=9)
    def only_letters(event):
        value = entry_name.get()
        new_value = ''.join(filter(lambda x: x.isalpha() or x.isspace(), value))
        if value != new_value:
            entry_name.delete(0, tk.END)
            entry_name.insert(0, new_value)
    entry_name.bind("<KeyRelease>", only_letters)

    tk.Label(fields_frame, text="Vencimiento (MM/AAAA):", **style_label, anchor="w").pack(anchor="w")
    entry_exp = tk.Entry(fields_frame, **style_entry)
    entry_exp.pack(fill="x", pady=(3, 14), ipady=9)
    def format_expiry(event):
        value = ''.join(filter(str.isdigit, entry_exp.get()))[:6]
        if len(value) > 2:
            value = value[:2] + '/' + value[2:]
        entry_exp.delete(0, tk.END)
        entry_exp.insert(0, value)
        entry_exp.icursor(len(value))
    entry_exp.bind("<KeyRelease>", format_expiry)

    tk.Label(fields_frame, text="CVC (3 dígitos):", **style_label, anchor="w").pack(anchor="w")
    entry_cvc = tk.Entry(fields_frame, **style_entry)
    entry_cvc.pack(fill="x", pady=(3, 6), ipady=9)
    def only_3_digits(event):
        value = ''.join(filter(str.isdigit, entry_cvc.get()))[:3]
        entry_cvc.delete(0, tk.END)
        entry_cvc.insert(0, value)
        entry_cvc.icursor(len(value))
    entry_cvc.bind("<KeyRelease>", only_3_digits)

    campos = {
        "num": entry_num,
        "name": entry_name,
        "exp": entry_exp,
        "cvc": entry_cvc
    }

    for entry in campos.values():
        def on_enter(event, widget=entry):
            widget.config(highlightbackground="#66bfff")
        def on_leave(event, widget=entry):
            widget.config(highlightbackground="#e0e7ef")
        entry.bind("<FocusIn>", on_enter)
        entry.bind("<FocusOut>", on_leave)

  
    def procesar_pago():
        import re
        num = campos["num"].get().strip()
        name = campos["name"].get().strip()
        exp = campos["exp"].get().strip()
        cvc = campos["cvc"].get().strip()

        if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{4}", num):
            messagebox.showerror("Error", "Número de tarjeta inválido.")
            return
        if not re.fullmatch(r"[A-Za-z ]+", name):
            messagebox.showerror("Error", "Nombre inválido.")
            return
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{4}", exp):
            messagebox.showerror("Error", "Vencimiento inválido. Usá el formato MM/AAAA.")
            return
        if not re.fullmatch(r"\d{3}", cvc):
            messagebox.showerror("Error", "CVC inválido.")
            return

        reserva_ids = [int(lista_res.get(i).split(" – ")[0]) for i in sels]
        messagebox.showinfo("Pago Exitoso", f"Pago con tarjeta procesado.\nReservas pagadas: {len(reserva_ids)}")
        vp.destroy()

    tk.Button(card, text="Confirmar pago", bg="#0066cc", fg="white", command=procesar_pago, **style_button)\
        .pack(fill="x", padx=28, pady=(10, 22), ipady=10)

def abrir_pago_transferencia(prev_win):
    prev_win.destroy()
    vt = tk.Toplevel()
    vt.title("Pago por Transferencia")
    vt.geometry("420x220")
    vt.configure(bg="#f8fafd")

    shadow = tk.Frame(vt, bg="#dde6ed")
    shadow.place(relx=0.5, rely=0.5, anchor="center", width=340, height=150)
    card = tk.Frame(vt, bg="white")
    card.place(relx=0.5, rely=0.5, anchor="center", width=320, height=130)
    card.lift()

    style_label = {"bg": "white", "font": ("Segoe UI", 12)}
    style_entry = {
        "bg": "#f6f6fa", "relief": "flat", "font": ("Segoe UI", 12),
        "highlightthickness": 2, "highlightbackground": "#e0e7ef",
        "highlightcolor": "#66bfff", "bd": 0, "justify": "center"
    }
    style_button = {
        "font": ("Segoe UI", 11, "bold"), "bd": 0, "relief": "flat",
        "activebackground": "#0080ff", "activeforeground": "white", "cursor": "hand2"
    }

    tk.Label(card, text="Transferí a:", **style_label).pack(pady=(10,5))
    alias = tk.Entry(card, **style_entry)
    alias.insert(0, "TravelEase.Arg")
    alias.config(state="readonly")
    alias.pack(pady=5, padx=25, fill="x", ipady=5)

    def confirmar_pago():
        messagebox.showinfo("Transferencia", "Transferencia confirmada.")
        vt.destroy()

    tk.Button(card, text="Confirmar pago", bg="#008fb3", fg="white", command=confirmar_pago, **style_button)\
        .pack(pady=(18, 28), padx=38, fill="x", ipady=16)


def eliminar_seleccion(listbox, refrescar_cb):
    sels = listbox.curselection()
    if not sels:
        messagebox.showwarning("Atención", "Seleccioná reservas para eliminar.")
        return
    for idx in reversed(sels):
        res_id = int(listbox.get(idx).split(" – ")[0])
        cancelar_reserva(res_id)
    messagebox.showinfo("Eliminado", f"{len(sels)} reserva(s) eliminada(s).")
    refrescar_cb()
