// --- Inicio ---

MOSTRAR "--- TechCovers ---"

// --- Cliente ---

// --- Consultar catálogo ---

MOSTRAR catálogo de productos

// --- Crear reserva ---

SI el usuario quiere reservar ENTONCES

    PEDIR cantidad

    COMPROBAR stock disponible

    SI hay stock suficiente ENTONCES

        CREAR reserva
        ACTUALIZAR stock

        MOSTRAR "Reserva creada correctamente"

    SINO

        MOSTRAR "No hay stock suficiente"

    FIN SI

// --- Modificar reserva ---

SINO SI el usuario quiere modificar una reserva ENTONCES

    PEDIR nueva cantidad

    COMPROBAR stock disponible

    SI hay stock suficiente ENTONCES

        ACTUALIZAR reserva
        ACTUALIZAR stock

        MOSTRAR "Reserva modificada correctamente"

    SINO

        MOSTRAR "No hay stock suficiente"

    FIN SI

// --- Eliminar reserva ---

SINO SI el usuario quiere eliminar una reserva ENTONCES

    ELIMINAR reserva
    DEVOLVER unidades al stock

    MOSTRAR "Reserva eliminada correctamente"

FIN SI

// --- Administrador ---

SI el usuario es administrador ENTONCES

    // --- Crear producto ---

    SI quiere añadir un producto ENTONCES

        PEDIR datos del producto
        GUARDAR producto

    // --- Modificar producto ---

    SINO SI quiere modificar un producto ENTONCES

        ACTUALIZAR datos del producto

    // --- Eliminar producto ---

    SINO SI quiere eliminar un producto ENTONCES

        ELIMINAR producto

    FIN SI

FIN SI

FIN