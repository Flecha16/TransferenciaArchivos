import tkinter as tk
from tkinter import messagebox, ttk
import os
import csv
import shutil
from datetime import datetime

class Sistema2:
    def __init__(self, root):
        self.root = root
        self.root.title('Consultora de Siniestros')
        self.root.geometry('600x400')

        self.resultados_totales = []
        self.setup_ui()

    def setup_ui(self):
        btn_procesar = tk.Button(self.root, text='Procesar Reclamos', command=self.procesar_reclamos, width=20, height=2)
        btn_procesar.pack(pady=10)

        # Tabla para mostrar los resultados
        self.tabla = ttk.Treeview(self.root, columns=('Poliza', 'Estado', 'Razón'), show='headings')
        self.tabla.heading('Poliza', text='Número de Póliza')
        self.tabla.heading('Estado', text='Estado')
        self.tabla.heading('Razón', text='Razón')
        self.tabla.pack(fill=tk.BOTH, expand=True, pady=10)

    def procesar_reclamos(self):
        carpeta_entrada = './sistema2/entrada'
        carpeta_salida = './sistema2/salida'
        carpeta_respuestas = './sistema1/respuestas'
        carpeta_logs = './sistema2/logs'

        # Verifica si las carpetas existen
        for carpeta in [carpeta_salida, carpeta_respuestas, carpeta_logs]:
            if not os.path.exists(carpeta):
                os.makedirs(carpeta)

        archivos = os.listdir(carpeta_entrada)

        if not archivos:
            messagebox.showinfo('Información', 'No hay archivos para procesar.')
            return

        for archivo in archivos:
            ruta_entrada = os.path.join(carpeta_entrada, archivo)
            ruta_salida = os.path.join(carpeta_salida, 'respuesta_' + archivo)

            resultados = []

            with open(ruta_entrada, mode='r', newline='', encoding='utf-8') as csvfile:
                lector = csv.DictReader(csvfile)
                for fila in lector:
                    numero_poliza = fila['numero_poliza']
                    monto_reclamo = float(fila['monto_reclamo'])
                    fecha_siniestro = fila['fecha_siniestro']
                    descripcion = fila['descripcion']

                    estado, razon = self.validar_reclamo(monto_reclamo, fecha_siniestro, descripcion)

                    resultado = {
                        'numero_poliza': numero_poliza,
                        'estado': estado,
                        'razon': razon
                    }
                    resultados.append(resultado)
                    self.resultados_totales.append(resultado)

            # Generar el archivo de respuesta
            with open(ruta_salida, mode='w', newline='', encoding='utf-8') as csvfile:
                campos = ['numero_poliza', 'estado', 'razon']
                escritor = csv.DictWriter(csvfile, fieldnames=campos)
                escritor.writeheader()
                escritor.writerows(resultados)

            # Simular la devolución moviendo el archivo de respuesta al Sistema 1
            ruta_respuesta = os.path.join(carpeta_respuestas, 'respuesta_' + archivo)
            shutil.move(ruta_salida, ruta_respuesta)

            # Eliminar el archivo de entrada procesado
            os.remove(ruta_entrada)

            # Registrar en el log
            self.registrar_log(archivo, resultados)

        self.actualizar_tabla()
        messagebox.showinfo('Procesamiento completado', 'Los reclamos han sido procesados y las respuestas enviadas al Sistema 1.')

    def validar_reclamo(self, monto, fecha, descripcion):
        # Lógica avanzada de validación
        estado = 'Aprobado'
        razon = 'Reclamo válido'

        # Validar monto
        if monto > 15000:
            estado = 'Rechazado'
            razon = 'Monto excede el límite máximo'

        # Validar fecha (no puede ser futura)
        fecha_siniestro = datetime.strptime(fecha, '%Y-%m-%d')
        if fecha_siniestro > datetime.now():
            estado = 'Rechazado'
            razon = 'Fecha de siniestro es en el futuro'

        # Validar descripción
        if not descripcion or descripcion.strip() == '':
            estado = 'Rechazado'
            razon = 'Descripción vacía'

        return estado, razon

    def actualizar_tabla(self):
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        for resultado in self.resultados_totales:
            self.tabla.insert('', tk.END, values=(resultado['numero_poliza'], resultado['estado'], resultado['razon']))

    def registrar_log(self, archivo, resultados):
        carpeta_logs = './sistema2/logs'
        ruta_log = os.path.join(carpeta_logs, 'procesamiento.log')

        with open(ruta_log, mode='a', encoding='utf-8') as log_file:
            log_file.write(f'Archivo procesado: {archivo}\n')
            for resultado in resultados:
                log_file.write(f"  Póliza: {resultado['numero_poliza']}, Estado: {resultado['estado']}, Razón: {resultado['razon']}\n")
            log_file.write('\n')

if __name__ == '__main__':
    root = tk.Tk()
    app = Sistema2(root)
    root.mainloop()
