function enviarDatos() {
    var fileInput = document.getElementById('file');
    var tecnica = document.getElementById('tecnica').value;
    var file = fileInput.files[0];
    var formData = new FormData();
    formData.append('file', file);
    formData.append('tecnica', tecnica);

    fetch('http://localhost:5000/csv', {
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