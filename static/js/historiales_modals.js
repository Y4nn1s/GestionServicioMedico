$(document).ready(function() {
    // --- Lógica para Crear Alergia --- //
    $('#crearAlergiaForm').submit(function(e) {
        e.preventDefault();
        const nombreAlergia = $('#nueva_alergia_nombre').val().trim();
        if (!nombreAlergia) return;

        $.ajax({
            url: '/historiales/ajax/crear-alergia/',
            method: 'POST',
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            contentType: 'application/json',
            data: JSON.stringify({ nombre: nombreAlergia }),
            success: function(response) {
                if (response.success) {
                    // Crear el nuevo checkbox
                    const newCheckbox = `
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="alergias" value="${response.id}" id="id_alergias_${response.id}" checked>
                            <label class="form-check-label" for="id_alergias_${response.id}">${response.nombre}</label>
                        </div>`;
                    // Añadirlo al contenedor
                    $('#id_alergias_container').append(newCheckbox);
                    // Cerrar modal y limpiar
                    $('#crearAlergiaModal').modal('hide');
                    $('#nueva_alergia_nombre').val('');
                } else {
                    alert(`Error: ${response.errors}`);
                }
            },
            error: function() {
                alert('Ocurrió un error al crear la alergia.');
            }
        });
    });

    // --- Lógica para Crear Enfermedad --- //
    $('#crearEnfermedadForm').submit(function(e) {
        e.preventDefault();
        const nombreEnfermedad = $('#nueva_enfermedad_nombre').val().trim();
        if (!nombreEnfermedad) return;

        $.ajax({
            url: '/historiales/ajax/crear-enfermedad/',
            method: 'POST',
            headers: { 'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val() },
            contentType: 'application/json',
            data: JSON.stringify({ nombre: nombreEnfermedad }),
            success: function(response) {
                if (response.success) {
                    // Crear el nuevo checkbox
                    const newCheckbox = `
                        <div class="form-check">
                            <input class="form-check-input" type="checkbox" name="enfermedades_preexistentes" value="${response.id}" id="id_enfermedades_preexistentes_${response.id}" checked>
                            <label class="form-check-label" for="id_enfermedades_preexistentes_${response.id}">${response.nombre}</label>
                        </div>`;
                    // Añadirlo al contenedor
                    $('#id_enfermedades_preexistentes_container').append(newCheckbox);
                    // Cerrar modal y limpiar
                    $('#crearEnfermedadModal').modal('hide');
                    $('#nueva_enfermedad_nombre').val('');
                } else {
                    alert(`Error: ${response.errors}`);
                }
            },
            error: function() {
                alert('Ocurrió un error al crear la enfermedad.');
            }
        });
    });
});