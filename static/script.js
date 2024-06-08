document.addEventListener('DOMContentLoaded', function () {
    let loadButton = document.getElementById('loadButton');
    let rowCountInput = document.getElementById('rowCount');
    let tbody = document.getElementById('tbody');
    let offset = 0;


    loadButton.onclick = function () {
        let rowCount = parseInt(rowCountInput.value, 10) || 10; // Default to 10 if no value
        tbody.innerHTML = ''; // Clear the table body

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
    let ajouter = document.getElementById('addButton');
    ajouter.onclick = function () {
        document.getElementById('addTaskForm').submit();
    };
});