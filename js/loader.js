
async function cargarRepuestos(jsonPath) {
    const tabla = document.getElementById('tablaRepuestos');

    // Alternar visibilidad si ya hay contenido cargado
    if (tabla.innerHTML.trim() !== "") {
        tabla.innerHTML = "";
        return;
    }

    try {
        const response = await fetch(jsonPath);
        const data = await response.json();
        const repuestos = data.repuestos || [];

        if (repuestos.length === 0) {
            tabla.innerHTML = '<p>No hay repuestos disponibles</p>';
            return;
        }

        tabla.innerHTML = `
            <table border="1" style="margin: 0 auto;">
                <tr><th>Repuesto</th><th>Código</th><th>Qty</th><th>UM</th></tr>
                ${repuestos.map(item => `
                    <tr>
                        <td>${item.Descripcion}</td>
                        <td>${item.Articulo}</td>
                        <td>${item.Cantidad}</td>
                        <td>${item.UM}</td>
                    </tr>
                `).join('')}
            </table>
        `;
    } catch (error) {
        console.error('Error loading repuestos:', error);
        tabla.innerHTML = '<p>Error al cargar los repuestos</p>';
    }
}

