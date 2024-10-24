import tkinter as tk
from tkinter import messagebox, ttk
import csv
import os
import shutil
from datetime import datetime

class Sistema1:
    def __init__(self, root):
        self.root = root
        self.root.title('Sistema de Seguros Globales')
        self.root.geometry('500x400')

        self.reclamos = []
        self.setup_ui()

    def setup_ui(self):
        # Frame para el formulario
        frame_form = tk.Frame(self.root)
        frame_form.pack(pady=10)

        tk.Label(frame_form, text='Número de Póliza:').grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_poliza = tk.Entry(frame_form)
        self.entry_poliza.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_form, text='Monto del Reclamo:').grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_monto = tk.Entry(frame_form)
        self.entry_monto.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame_form, text='Fecha de Siniestro (YYYY-MM-DD):').grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_fecha = tk.Entry(frame_form)
        self.entry_fecha.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame_form, text='Descripción:').grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        self.entry_descripcion = tk.Entry(frame_form)
        self.entry_descripcion.grid(row=3, column=1, padx=5, pady=5)

        btn_agregar = tk.Button(self.root, text='Agregar Reclamo', command=self.agregar_reclamo)
        btn_agregar.pack(pady=5)

        btn_transferir = tk.Button(self.root, text='Transferir Reclamos', command=self.transferir_reclamos)
        btn_transferir.pack(pady=5)

        # Tabla para mostrar los reclamos agregados
        self.tabla = ttk.Treeview(self.root, columns=('Poliza', 'Monto', 'Fecha', 'Descripción'), show='headings')
        self.tabla.heading('Poliza', text='Número de Póliza')
        self.tabla.heading('Monto', text='Monto')
        self.tabla.heading('Fecha', text='Fecha de Siniestro')
        self.tabla.heading('Descripción', text='Descripción')
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)

    def agregar_reclamo(self):
        numero_poliza = self.entry_poliza.get()
        monto_reclamo = self.entry_monto.get()
        fecha_siniestro = self.entry_fecha.get()
        descripcion = self.entry_descripcion.get()

        # Validaciones básicas
        if not numero_poliza or not monto_reclamo or not fecha_siniestro or not descripcion:
            messagebox.showerror('Error', 'Todos los campos son obligatorios.')
            return
        
        if not numero_poliza.isalnum():
            messagebox.showerror('Error', 'El número de póliza solo debe contener letras y números, sin símbolos.')
            return

        if numero_poliza == "0":
            messagebox.showerror('Error', 'El número de póliza no puede ser "0".')
            return

        try:
            monto_reclamo = float(monto_reclamo)
            if monto_reclamo <= 0:
                messagebox.showerror('Error', 'El monto del reclamo debe ser un número mayor a cero.')
                return
        except ValueError:
            messagebox.showerror('Error', 'El monto del reclamo debe ser un número válido.')
            return

        try:
            datetime.strptime(fecha_siniestro, '%Y-%m-%d')
        except ValueError:
            messagebox.showerror('Error', 'La fecha debe estar en formato YYYY-MM-DD.')
            return

        reclamo = {
            'numero_poliza': numero_poliza,
            'monto_reclamo': monto_reclamo,
            'fecha_siniestro': fecha_siniestro,
            'descripcion': descripcion
        }

        self.reclamos.append(reclamo)
        self.actualizar_tabla()
        self.limpiar_campos()

    def limpiar_campos(self):
        self.entry_poliza.delete(0, tk.END)
        self.entry_monto.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)
        self.entry_descripcion.delete(0, tk.END)

    def actualizar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for reclamo in self.reclamos:
            self.tabla.insert('', tk.END, values=(reclamo['numero_poliza'], reclamo['monto_reclamo'], reclamo['fecha_siniestro'], reclamo['descripcion']))

    def transferir_reclamos(self):
        if not self.reclamos:
            messagebox.showinfo('Información', 'No hay reclamos para transferir.')
            return

        # Crear carpeta si no existe
        carpeta_entrada = './sistema2/entrada'
        if not os.path.exists(carpeta_entrada):
            os.makedirs(carpeta_entrada)

        # Generar archivo CSV
        nombre_archivo = f'reclamos_{datetime.now().strftime("%Y%m%d%H%M%S")}.csv'
        ruta_archivo = os.path.join(carpeta_entrada, nombre_archivo)

        with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as csvfile:
            campos = ['numero_poliza', 'monto_reclamo', 'fecha_siniestro', 'descripcion']
            escritor = csv.DictWriter(csvfile, fieldnames=campos)
            escritor.writeheader()
            escritor.writerows(self.reclamos)

        messagebox.showinfo('Transferencia exitosa', 'Los reclamos han sido transferidos al Sistema 2.')

        # Limpiar lista de reclamos y actualizar tabla
        self.reclamos.clear()
        self.actualizar_tabla()

if __name__ == '__main__':
    root = tk.Tk()
    app = Sistema1(root)
    root.mainloop()
