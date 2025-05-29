from flask import Flask, render_template, request
import json
import random
import os

app = Flask(__name__)

def cargar_preguntas(ruta):
    with open(ruta, encoding='utf-8') as f:
        return json.load(f)

@app.route('/')
def index():
    # Lista los archivos disponibles automáticamente
    archivos = os.listdir('preguntas')
    años_disponibles = [archivo.replace('.json', '') for archivo in archivos if archivo.endswith('.json')]
    años_disponibles.sort(reverse=True)
    return render_template('index.html', años=años_disponibles)

@app.route('/practicar/<año>')
def practicar(año):
    ruta_json = f'preguntas/{año}.json'
    if not os.path.exists(ruta_json):
        return f"No se encontró el archivo para el año {año}", 404

    preguntas = cargar_preguntas(ruta_json)
    pregunta = random.choice(preguntas)

    return render_template('pregunta.html', pregunta=pregunta, año=año)

@app.route('/respuesta', methods=['POST'])
def respuesta():
    seleccionada = request.form['respuesta']
    correcta = request.form['correcta']
    año = request.form['año']
    enunciado = request.form['enunciado']
    opciones = json.loads(request.form['opciones'])

    return render_template('resultado.html',
                           resultado=(seleccionada == correcta),
                           correcta=correcta,
                           seleccionada=seleccionada,
                           enunciado=enunciado,
                           opciones=opciones,
                           año=año)

if __name__ == '__main__':
    app.run(debug=True)
