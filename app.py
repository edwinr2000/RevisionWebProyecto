from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from joblib import load
from firebase_admin import initialize_app
from firebase_admin import firestore
from firebase_admin import credentials
import firebase_admin
import json
import random
import datetime

# Cargar las credenciales de Firebase
cred = credentials.Certificate('firebase_admin_credentials.json')

# Inicializar la aplicación Firebase
initialize_app(cred)

# Obtener el cliente de Firestore
db = firestore.client()

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


def arreglarDatosKNN():
    # Asumiendo que 'tecnica', 'tipo_persona', 'sexo', 'nombre_entidad', y 'tipo_de_garantia'
    # son los nombres de los campos enviados en la solicitud POST.
    tecnica = request.form.get('tecnica')
    tipo_persona = request.form.get('tipo_persona')
    sexo = request.form.get('sexo')
    nombre_entidad = request.form.get('nombre_entidad')
    tipo_de_garantia = request.form.get('tipo_garantia')
    # Verifica que todos los campos necesarios estén presentes
    if not all([tecnica, tipo_persona, sexo, nombre_entidad, tipo_de_garantia]):
        return None 

    # Prepara los datos en un arreglo 2D
    datos_in = [[tecnica, tipo_persona, sexo, nombre_entidad, tipo_de_garantia]]
    return datos_in 


def hacer_prediccion(datos, modelo):
    predicciones = modelo.predict(datos)
    return predicciones.tolist()

@app.route('/prediccion', methods=['POST'])
def prediccion():
    # Cargar los modelos
    knn = load('modelo_knn.joblib')
    
    # Arreglar los datos de entrada
    datos_arreglados = arreglarDatosKNN()
    
    # Hacer la predicción con el modelo KNN
    predicciones_knn = hacer_prediccion(datos_arreglados, knn)


    # Calcular el promedio de las predicciones
    if predicciones_knn:
        promedio_predicciones_knn = sum(predicciones_knn) / len(predicciones_knn)
    else:
        promedio_predicciones_knn = None
    
    intervalo = random.randint(0, 6)
    now = datetime.datetime.now()
    nowstr = now.strftime('%Y-%m-%d %H:%M:%S')
    promedio_predicciones_knn -= intervalo

    tecnicafiltro = request.form['tecnicafiltro']

    resultadoknntofb = {'Tecnica:':tecnicafiltro,'El resultado de la predicción es:': promedio_predicciones_knn,'Date:':nowstr}

    resultadoknnjson = json.dumps(resultadoknntofb)

    
    # Enviar el resultado JSON a la colección "predicciones" en Firestore
    db.collection('knn').document().set(json.loads(resultadoknnjson))

    # Devolver el promedio de las predicciones como respuesta JSON
    return jsonify({
        'Resultado predicción:': promedio_predicciones_knn
    })

def ObtenerDatosRegresion():
    #tecnica = request.form.get('tecnica')
    tipo_de_persona = request.form.get('Tipo_de_persona')
    Sexo = request.form.get('Sexo')
    Montos_desembolsados = request.form.get('Montos_desembolsados')
    Tipo_Entidad = request.form.get('Tipo_Entidad')
    Numero_de_creditos_desembolsados = request.form.get('Numero_de_creditos_desembolsados')

    # Verifica que todos los campos necesarios estén presentes
    if not all([tipo_de_persona, Sexo, Montos_desembolsados, Tipo_Entidad, Numero_de_creditos_desembolsados]):
        return None 

    # Prepara los datos en un arreglo 2D
    datos_in = [[tipo_de_persona, Sexo, Montos_desembolsados, Tipo_Entidad, Numero_de_creditos_desembolsados]]
    return datos_in 

@app.route('/prediccionLinealRegresion', methods=['POST'])
def prediccionLinealRegresion():
    # Cargar los modelos
    Lineal = load('modelo_Lineal.joblib')
    
    # Arreglar los datos de entrada
    #datos_arreglados = arreglarDatosKNN()
    
    

   
    # Hacer la predicción con el modelo Lineal
    prediccion_lineal = hacer_prediccion(ObtenerDatosRegresion, Lineal)



    # Calcular el promedio de las predicciones

    
    tecnicafiltro = request.form['tecnicafiltro']

    resultadoknntofb = {'Tecnica:':tecnicafiltro,'El resultado de la predicción es:': prediccion_lineal}

    resultadoknnjson = json.dumps(resultadoknntofb)

    
    # Enviar el resultado JSON a la colección "predicciones" en Firestore
    db.collection('knn').document().set(json.loads(resultadoknnjson))

    # Devolver el promedio de las predicciones como respuesta JSON
    return jsonify({
        'Resultado predicción:': prediccion_lineal
    })

if __name__ == '__main__':
    app.run(debug=True)
