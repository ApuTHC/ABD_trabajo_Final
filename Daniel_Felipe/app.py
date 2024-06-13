from flask import Flask, render_template, jsonify
import json

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/data')
def data():
    # Leer el archivo JSON y devolver los datos
    data = []
    with open('simulated_data.json', 'r') as file:
        for line in file:
            data.append(json.loads(line))

    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True)
