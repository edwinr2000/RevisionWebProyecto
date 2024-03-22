from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/csv', methods=['POST']) 
def csv():
    file = request.files['file']
    tecnica = request.form['tecnica']
    now = datetime.now()
    file.save(now.strftime("%Y%m%d%H%M%S") + '.csv')
    return jsonify({'message': 'Archivo recibido', 'la técnica fue seleccionada fue:': tecnica})
