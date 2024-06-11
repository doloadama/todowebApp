document.addEventListener('DOMContentLoaded', function () {
    let loadButton = document.getElementById('loadButton');
    let rowCountInput = document.getElementById('rowCount');
    let tbody = document.getElementById('tbody');
    let archivedTbody = document.getElementById('archivedTbody');
    let showAddTaskFormButton = document.getElementById('showAddTaskFormButton');
    let addTaskFormContainer = document.getElementById('addTaskFormContainer');
    let addButton = document.getElementById('addButton');
    let offset = 0;

    loadButton.onclick = function () {
        let rowCount = parseInt(rowCountInput.value, 10);
        tbody.innerHTML='';

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
                        <td><input type="checkbox"></td>
                        <td>${task.id_user}</td>
                        <td>${task.id}</td>
                        <td>${task.titre}</td>
                        <td>${task.description}</td>
                        <td>${task.statut}</td>
                        <td>
                            <a href="/modifier/${task.id}"><button>Modifier</button></a>
                            <button onclick="supprimerTache(${task.id})">Supprimer</button>
                        </td>
                    `;
                    tbody.appendChild(row);
                });
                offset += rowCount;
            })
            .catch(error => console.error('Error fetching tasks:', error));
    };

     showAddTaskFormButton.onclick = function () {
        addTaskFormContainer.style.display = 'block'; // Afficher le formulaire d'ajout de tâche
    };

      addButton.onclick = function () {
        document.getElementById('addTaskForm').submit();
        confirm('tache créée avec succés!');
    };

    document.getElementById('addButton').onclick = function () {
        document.getElementById('addTaskForm').submit();
    };

    function loadArchivedTasks() {
        archivedTbody.innerHTML = ''; // Vider le tableau des tâches archivées

        fetch(`/api/archived-tasks`)
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
                    `;
                    archivedTbody.appendChild(row);
                });
            })
            .catch(error => console.error('Error fetching archived tasks:', error));
    }

    loadArchivedTasks(); // Charger les tâches archivées au chargement de la page
});

function supprimerTache(id) {
    if (confirm("Voulez-vous vraiment supprimer cette tâche ?")) {
        fetch(`/supprimer/${id}`, {
            method: 'POST'
        })
        .then(response => {
            if (response.ok) {
                alert('Tâche supprimée avec succès');
                location.reload(); // Recharger la page après la suppression
            } else {
                alert('Erreur lors de la suppression de la tâche');
            }
        })
        .catch(error => console.error('Error:', error));
    }
}
