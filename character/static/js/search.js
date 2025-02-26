// Búsqueda en tiempo real
        document.getElementById('search-character').addEventListener('input', async function(e) {
            const searchTerm = e.target.value;
            try {
                const response = await fetch(`/api/characters/?search=${encodeURIComponent(searchTerm)}`);
                const data = await response.json();
                updateTable(data);
            } catch (error) {
                console.error('Error en la búsqueda:', error);
            }
        });

        // Función para actualizar la tabla
        function updateTable(characters) {
            const tbody = document.getElementById('characters-body');
            tbody.innerHTML = '';

            if (characters.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="6">No se encontraron resultados</td>
                    </tr>`;
                return;
            }

            characters.forEach(character => {
    const row = document.createElement('tr');

    // Crear lista de equipamiento correctamente
    const equipmentList = character.equipment.length > 0
        ? character.equipment.map(equipo => equipo.name.charAt(0).toUpperCase() + equipo.name.slice(1)).join(', ')
        : 'Sin equipamiento';

    row.innerHTML = `
        <td>${character.name}</td>
        <td>${character.race}</td>
        <td>${character.ubication}</td>
        <td>${equipmentList}</td>
        <td>${character.arma_equipada ? character.arma_equipada.name : 'Sin arma'}</td>
        <td>
            <a href="/character/change-ubication/${character.id}/">Cambiar Ubicación</a>
            <a href="/character/equip-weapon/${character.id}/">Equipar Arma</a>
            <a href="/character/detail/${character.id}/">Ver Detalles</a>
            <a href="/character/delete/${character.id}/"
               class="delete-link"
               data-character-name="${character.name}">Eliminar</a>
        </td>`;

    tbody.appendChild(row);
});

        }

        // Confirmación para eliminar
        document.querySelectorAll('.delete-link').forEach(link => {
            link.addEventListener('click', function(e) {
                const characterName = this.dataset.characterName;
                if (!confirm(`¿Estás seguro de querer eliminar a ${characterName}?`)) {
                    e.preventDefault();
                }
            });
        });