from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from sklearn.feature_extraction.text import CountVectorizer
from joblib import load
from sklearn.preprocessing import OneHotEncoder


app = Flask(__name__)
CORS(app)

@app.route('/csv', methods=['POST']) 
def csv():
    tecnica = request.form['tecnica']
    tipo_persona = request.form['tipo_persona']
    sexo = request.form['sexo']
    monto = request.form['monto']    
    now = datetime.now()
    return jsonify({'message': 'Se recibieron los datos', 'la técnica fue seleccionada fue:': tecnica, 'Tipo de persona:': tipo_persona, 'Sexo:': sexo, 'Monto:': monto})

def arreglarDatosKNN(datosArregar):
    tecnica = request.form['tecnica']
    Tipo_de_persona = request.form['tipo_persona']
    Sexo = request.form['sexo']
    Nombre_Entidad = request.form['Nombre_Entidad']
    Tipo_de_garantía = request.form['Tipo_de_garantía']
    datos_in = [Tipo_de_persona, Sexo,Nombre_Entidad , Tipo_de_garantía]
    encoder = OneHotEncoder()
    datos = encoder.fit_transform(datos_in)
    


def hacer_prediccion(datos, modelo):
    vectorizador = OneHotEncoder()
    x = vectorizador.fit_transform(datos)
    predicciones = modelo.predict(x)
    return predicciones.tolist()

@app.route('/prediccion', methods=['POST'])
def prediccion():
    # Cargar los modelos
    knn = load('modelo_knn.joblib')
    lineal = load('modelo_Lineal.joblib')
    tree = load('modelo_Tree.joblib')
    arreglarEntrada = arreglarDatosKNN(datosArregar)
    predicciones_knn = hacer_prediccion(arreglarEntrada, knn)
    


    
    # Devolver las predicciones como respuesta JSON

    return jsonify({
        'predicciones_knn': predicciones_knn
        
        
    })