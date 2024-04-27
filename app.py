from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from joblib import load

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
    
    # Devolver el promedio de las predicciones como respuesta JSON
    return jsonify({
        'Resultado predicción:': promedio_predicciones_knn
    })


if __name__ == '__main__':
    app.run(debug=True)
