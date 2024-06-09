document.addEventListener('DOMContentLoaded', function () {
    let loadButton = document.getElementById('loadButton');
    let rowCountInput = document.getElementById('rowCount');
    let tbody = document.getElementById('tbody');
    let offset = 0;


    loadButton.onclick = function () {
         let rowCount = parseInt(rowCountInput.value, 10);
         tbody.innerHTML = '' //Vider le tableau à chaque appuie sur charger

            if (isNaN(rowCount) || rowCount < 1 || rowCount > 10) {
                alert("Saisir un nombre compris entre 1 et 10");
                return;
            }

        fetch(`/api/tasks?limit=${rowCount}&offset=${offset}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(task => {
                    let row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${task.id_user}</td>
                        <td>${task.id}</td>
                        <td>${task.titre}</td>
                        <td>${task.description}</td>
                        <td>${task.statut}</td>
                        <td><a href="/modifier/${task.id}">Edit</a></td>
                    `;
                    tbody.appendChild(row);
                });
                offset += rowCount;
            })
            .catch(error => console.error('Error fetching tasks:', error));
    };
    document.addEventListener('DOMContentLoaded', function () {
});
    let ajouter = document.getElementById('addButton');
    ajouter.onclick = function () {
        window.location.href = 'templates/ajouter.html'
    };

});



