document.addEventListener('DOMContentLoaded', function () {
    const rutInput = document.getElementById('rut'); // Selecciona el input RUT

    rutInput.addEventListener('input', function (e) {
        let rutValue = e.target.value.replace(/\D/g, ''); // Elimina caracteres no numéricos

        // Limita la longitud máxima del RUT (sin el dígito verificador)
        if (rutValue.length > 8) { // Permitimos 8 dígitos + 1 dígito verificador
            rutValue = rutValue.slice(0, 9);
        }

        // Formateo del RUT
        if (rutValue.length > 0) {
            let dv = rutValue.length === 9 ? rutValue.charAt(8) : ''; // Obtiene el dígito verificador
            let rutSinDv = rutValue.slice(0, 8); // RUT sin el dígito verificador

            // Formateo con puntos
            let formattedRut = rutSinDv.replace(/\B(?=(\d{3})+(?!\d))/g, '.');

            // Si hay un dígito verificador, se añade
            if (dv) {
                formattedRut += '-' + dv;
            }

            e.target.value = formattedRut; // Establece el valor formateado
        }

        // Limpia el RUT antes de enviar el formulario
        document.querySelector('form').addEventListener('submit', function () {
            let cleanRut = rutInput.value.replace(/\D/g, ''); // Elimina caracteres no numéricos
            rutInput.value = cleanRut; // Establece el valor limpio antes de enviar
        });
    });
});
