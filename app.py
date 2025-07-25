from flask import Flask, render_template, request, redirect, send_file
import csv
import pandas as pd
import os

app = Flask(__name__)

CSV_FILE = 'mantenimientos.csv'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/guardar', methods=['POST'])
def guardar():
    nombre = request.form['nombre']
    tipo = request.form['tipo']
    descripcion = request.form['descripcion']

    if not (nombre and tipo and descripcion):
        return "Todos los campos son obligatorios", 400

    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([nombre, tipo, descripcion])

    return redirect('/ver')

@app.route('/ver')
def ver():
    data = []
    if os.path.exists(CSV_FILE):
        with open(CSV_FILE, newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            data = list(reader)
    return render_template('ver.html', data=data)

@app.route('/exportar')
def exportar():
    if not os.path.exists(CSV_FILE):
        return "No hay datos para exportar", 404

    df = pd.read_csv(CSV_FILE, names=["Máquina", "Tipo", "Descripción"])
    excel_file = "mantenimientos.xlsx"
    df.to_excel(excel_file, index=False)
    return send_file(excel_file, as_attachment=True)

@app.route('/oee', methods=['GET', 'POST'])
def oee():
    resultado = None
    if request.method == 'POST':
        try:
            td = float(request.form['td'])
            to = float(request.form['to'])
            pb = int(request.form['pb'])
            pt = int(request.form['pt'])

            disponibilidad = to / td
            rendimiento = pt / (to * 60)
            calidad = pb / pt
            oee_valor = disponibilidad * rendimiento * calidad * 100
            resultado = round(oee_valor, 2)
        except Exception as e:
            resultado = f"Error: {e}"
    return render_template('oee.html', resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True)
