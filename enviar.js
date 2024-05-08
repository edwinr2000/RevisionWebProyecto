function enviarDatos() {
    var tipo_persona = document.getElementById('tipo_persona').value;
    var sexo = document.getElementById('sexo').value;
    var nombre_entidad = document.getElementById('nombre_entidad').value;
    var Tipo_de_garantia = document.getElementById('tipo_garantia').value;
    var tecnicafiltro = 'KNN'
    //var file = fileInput.files[0];
    var formData = new FormData();
    //formData.append('file', file);
    formData.append('tipo_persona', tipo_persona);
    formData.append('sexo', sexo);
    formData.append('nombre_entidad',nombre_entidad)
    formData.append('tipo_garantia',Tipo_de_garantia)
    formData.append('tecnicafiltro',tecnicafiltro)

    fetch('http://localhost:5000/prediccion', {
        method: 'POST',
        body: formData
    })
        .then(function(response) {
            return response.json();
        })
        .then(function(data) {
            console.log(data);
        })
        .catch(function(error) {
            console.error(error);
        });
}