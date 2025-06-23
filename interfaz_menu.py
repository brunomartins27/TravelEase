import tkinter as tk
from tkinter import messagebox
from paquete_service import obtener_paquetes_disponibles
from reserva_service import crear_reservas_multiples, obtener_reservas_por_usuario, cancelar_reserva

def mostrar_menu_principal(usuario):
    root = tk.Tk()
    root.title("TravelEase – Menú Principal")
    root.geometry("600x520")
    root.configure(bg="white")

    frame = tk.Frame(root, bg="white", padx=20, pady=20)
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text=f"Bienvenido, {usuario['nombre']}", font=("Helvetica", 16), bg="white")\
      .grid(row=0, column=0, columnspan=3, pady=10)

    tk.Label(frame, text="Paquetes Disponibles:", bg="white").grid(row=1, column=0, sticky="w")
    lista_paquetes = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=30, height=8)
    lista_paquetes.grid(row=2, column=0, pady=5)
    for p in obtener_paquetes_disponibles():
        lista_paquetes.insert(tk.END, f"{p[0]} – {p[1]} — ${p[3]}")

    tk.Button(frame, text="Reservar Seleccionados", bg="#009966", fg="white", width=20,
              command=lambda: procesar_reservas(lista_paquetes, usuario, refrescar_listas))\
      .grid(row=3, column=0, pady=10)

    tk.Label(frame, text="Mis Reservas:", bg="white").grid(row=1, column=2, sticky="w")
    lista_res = tk.Listbox(frame, selectmode=tk.MULTIPLE, width=30, height=8)
    lista_res.grid(row=2, column=2, pady=5)

    def refrescar_listas():
        lista_paquetes.delete(0, tk.END)
        for p in obtener_paquetes_disponibles():
            lista_paquetes.insert(tk.END, f"{p[0]} – {p[1]} — ${p[3]}")
        lista_res.delete(0, tk.END)
        for r in obtener_reservas_por_usuario(usuario['id']):
            lista_res.insert(tk.END, f"{r[0]} – {r[1]} — ${r[2]} ({r[3][:10]})")

    refrescar_listas()
    tk.Button(frame, text="Pagar Reservas Seleccionadas", bg="#0066cc", fg="white", width=20,
              command=lambda: abrir_metodo_pago(root, lista_res))\
      .grid(row=3, column=2, pady=10)

    tk.Button(frame, text="Eliminar Reservas", bg="#cc3333", fg="white", width=20,
              command=lambda: eliminar_seleccion(lista_res, refrescar_listas))\
      .grid(row=4, column=2, pady=5)

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
    ventana_pago.geometry("300x140")
    ventana_pago.configure(bg="white")

    tk.Button(ventana_pago, text="Pago con Tarjeta", bg="#0066cc", fg="white", width=20,
              command=lambda: abrir_pago_tarjeta(ventana_pago, lista_res, sels)).pack(pady=5)
    tk.Button(ventana_pago, text="Pago por Transferencia", bg="#008fb3", fg="white", width=20,
              command=lambda: abrir_pago_transferencia(ventana_pago)).pack(pady=5)

def abrir_pago_tarjeta(prev_win, lista_res, sels):
    prev_win.destroy()
    vp = tk.Toplevel()
    vp.title("Pago con Tarjeta")
    vp.geometry("400x300")
    vp.configure(bg="white")

    campos = {}
    labels = [
        ("Número de Tarjeta (XXXX-XXXX-XXXX-XXXX):", "num"),
        ("Nombre en Tarjeta:", "name"),
        ("Vencimiento (MM/AA):", "exp"),
        ("CVC (3 dígitos):", "cvc")
    ]
    for i, (text, key) in enumerate(labels):
        tk.Label(vp, text=text, bg="white").grid(row=i, column=0, sticky="e", padx=10, pady=5)
        e = tk.Entry(vp, bg="white", relief="solid", bd=1, width=25)
        e.grid(row=i, column=1, pady=5)
        campos[key] = e

    def procesar_pago():
        num = campos["num"].get().strip()
        name = campos["name"].get().strip()
        exp = campos["exp"].get().strip()
        cvc = campos["cvc"].get().strip()
        import re
        # Validaciones básicas
        if not re.fullmatch(r"\d{4}-\d{4}-\d{4}-\d{4}", num):
            messagebox.showerror("Error", "Número de tarjeta inválido.")
            return
        if not re.fullmatch(r"[A-Za-z ]+", name):
            messagebox.showerror("Error", "Nombre inválido.")
            return
        if not re.fullmatch(r"(0[1-9]|1[0-2])/\d{2}", exp):
            messagebox.showerror("Error", "Vencimiento inválido.")
            return
        if not re.fullmatch(r"\d{3}", cvc):
            messagebox.showerror("Error", "CVC inválido.")
            return
        # Confirmar pago y eliminar reservas de la lista
        reserva_ids = [int(lista_res.get(i).split(" – ")[0]) for i in sels]
        messagebox.showinfo("Pago Exitoso", f"Pago con tarjeta procesado.\nReservas pagadas: {len(reserva_ids)}")
        vp.destroy()

    tk.Button(vp, text="Pagar", bg="#0066cc", fg="white", command=procesar_pago).grid(row=len(labels), column=0, columnspan=2, pady=20)

def abrir_pago_transferencia(prev_win):
    prev_win.destroy()
    vt = tk.Toplevel()
    vt.title("Pago por Transferencia")
    vt.geometry("350x200")
    vt.configure(bg="white")

    tk.Label(vt, text="Transferí a:", bg="white").pack(pady=(20,5))
    alias = tk.Entry(vt, bg="#f0f0f0", justify="center", relief="solid", bd=1, width=25)
    alias.insert(0, "TravelEase.Arg")
    alias.config(state="readonly")
    alias.pack(pady=5, padx=20)

    def confirmar_pago():
        # Aquí podrías marcar reservas como pagadas
        messagebox.showinfo("Transferencia", "Transferencia confirmada.")
        vt.destroy()

    tk.Button(vt, text="Confirmar pago", bg="#008fb3", fg="white", command=confirmar_pago).pack(pady=20)

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
