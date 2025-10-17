$(document).ready(function() {
    // Función genérica para manejar la subida de formularios de modales
    function handleModalFormSubmit(formId, url, modalId, selectId, successMessage, errorMessage) {
        var form = $(formId);

        function clearErrors() {
            form.find('.invalid-feedback').remove();
            form.find('.is-invalid').removeClass('is-invalid');
        }

        function showErrors(errors) {
            clearErrors();
            for (var field in errors) {
                var input = form.find('[name=' + field + ']');
                input.addClass('is-invalid');
                input.after('<div class="invalid-feedback">' + errors[field] + '</div>');
            }
        }

        form.submit(function(e) {
            e.preventDefault();
            var data = {};
            form.serializeArray().forEach(function(item) {
                data[item.name] = item.value;
            });

            var submitBtn = form.find('button[type=submit]');
            var originalText = submitBtn.html();
            submitBtn.html('<i class="bi bi-hourglass"></i> Creando...');
            submitBtn.prop('disabled', true);
            clearErrors();

            $.ajax({
                url: url,
                method: 'POST',
                headers: {
                    'X-CSRFToken': $('input[name=csrfmiddlewaretoken]').val()
                },
                contentType: 'application/json',
                data: JSON.stringify(data),
                success: function(response) {
                    if (response.success) {
                        $(selectId).append($('<option>', { value: response.id, text: response.nombre }));
                        $(selectId).val(response.id);
                        $(modalId).modal('hide');
                        form[0].reset();
                    } else {
                        showErrors(response.errors);
                    }
                },
                error: function(xhr) {
                    alert(errorMessage + '. ' + xhr.responseText);
                },
                complete: function() {
                    submitBtn.html(originalText);
                    submitBtn.prop('disabled', false);
                }
            });
        });

        // Limpiar errores cuando el modal se cierra
        $(modalId).on('hidden.bs.modal', function () {
            clearErrors();
            form[0].reset();
        });
    }

    // Implementación para Categoría
    handleModalFormSubmit(
        '#crearCategoriaForm',
        '/inventario/ajax/crear-categoria/',
        '#crearCategoriaModal',
        '#id_categoria',
        'Categoría creada exitosamente',
        'Error al crear la categoría'
    );

    // Implementación para Proveedor
    handleModalFormSubmit(
        '#crearProveedorForm',
        '/inventario/ajax/crear-proveedor/',
        '#crearProveedorModal',
        '#id_proveedor',
        'Proveedor creado exitosamente',
        'Error al crear el proveedor'
    );
});
