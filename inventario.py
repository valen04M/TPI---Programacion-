"""
TPI Programacion 1 - Sistema de Control de Inventario (ferreteria)

Programa con menu interactivo persistente. El inventario vive unicamente en
una lista de diccionarios llamada `inventario`, que se crea dentro de main()
y se pasa como parametro a cada funcion (sin variables globales).

Cada herramienta es un diccionario con exactamente dos claves:
    {'herramienta': 'Martillo', 'cantidad': 10}
La clave 'cantidad' guarda el stock (unidades disponibles).

Para ejecutar:  python inventario.py
"""


# ---------------------------------------------------------------------------
# Funciones auxiliares de validacion
# ---------------------------------------------------------------------------

def leer_entero(mensaje):
    """Pide un dato por teclado y lo convierte a entero.

    Si el texto no se puede convertir (por ejemplo 'abc' o '3.5'), int()
    produce un ValueError. Se captura aca solo para relanzarlo con raise y
    un mensaje claro; quien llamo a esta funcion decide que hacer con el.
    """
    try:
        return int(input(mensaje))
    except ValueError:
        raise ValueError('Debe ingresar un numero entero (sin letras ni decimales).')


def validar_nombre(nombre):
    """Devuelve el nombre sin espacios al inicio/final. Si queda vacio, lanza ValueError."""
    nombre = nombre.strip()
    if nombre == '':
        raise ValueError('El nombre no puede estar vacio.')
    return nombre


def buscar_herramienta(inventario, nombre):
    """Busca una herramienta por nombre, ignorando mayusculas y espacios extremos.

    Devuelve el diccionario de la herramienta (el mismo que esta dentro de
    inventario, no una copia) o None si no existe.
    """
    nombre_buscado = nombre.strip().lower()
    for producto in inventario:
        if producto['herramienta'].strip().lower() == nombre_buscado:
            return producto
    return None


def validar_nombre_nuevo(inventario, nombre):
    """Valida un nombre para una herramienta nueva: no vacio y no duplicado.

    Devuelve el nombre limpio (con strip(), respetando las mayusculas escritas).
    """
    nombre = validar_nombre(nombre)
    if buscar_herramienta(inventario, nombre) is not None:
        raise ValueError(f"La herramienta '{nombre}' ya existe en el inventario.")
    return nombre


def validar_stock_inicial(stock):
    """El stock inicial debe ser un entero mayor o igual que 0."""
    if stock < 0:
        raise ValueError('El stock inicial no puede ser negativo.')
    return stock


def validar_unidades(unidades):
    """Las unidades de un movimiento deben ser un entero mayor que 0."""
    if unidades <= 0:
        raise ValueError('Las unidades deben ser un numero mayor que 0.')
    return unidades


# ---------------------------------------------------------------------------
# Funciones de las opciones del menu
# ---------------------------------------------------------------------------

def mostrar_menu():
    """Imprime el menu con las siete opciones."""
    print()
    print('===== CONTROL DE INVENTARIO - FERRETERIA =====')
    print('1. Cargar herramientas')
    print('2. Mostrar inventario')
    print('3. Consultar stock')
    print('4. Reporte de agotados')
    print('5. Alta de nuevo producto')
    print('6. Actualizar stock (venta / ingreso)')
    print('7. Salir')


def cargar_herramientas(inventario):
    """Opcion 1: carga multiple de herramientas con su stock inicial.

    Aca los errores se capturan dentro de la funcion y se reintenta el dato
    con un bucle, conservando lo que ya fue valido.
    """
    cantidad_a_cargar = 0
    while cantidad_a_cargar <= 0:
        try:
            cantidad_a_cargar = leer_entero('Cuantas herramientas distintas va a cargar? ')
            if cantidad_a_cargar <= 0:
                raise ValueError('La cantidad de herramientas debe ser mayor que 0.')
        except ValueError as e:
            print(f'Error: {e}')

    for numero in range(cantidad_a_cargar):
        nombre = None
        while nombre is None:
            try:
                nombre = validar_nombre_nuevo(
                    inventario, input(f'Nombre de la herramienta {numero + 1}: '))
            except ValueError as e:
                print(f'Error: {e}')

        stock = None
        while stock is None:
            try:
                stock = validar_stock_inicial(leer_entero(f"Stock inicial de '{nombre}': "))
            except ValueError as e:
                print(f'Error: {e}')

        # Recien ahora, con nombre y stock validos, se agrega al inventario.
        inventario.append({'herramienta': nombre, 'cantidad': stock})
        print(f"'{nombre}' cargada con {stock} unidades.")


def mostrar_inventario(inventario):
    """Opcion 2: lista todas las herramientas con su stock."""
    if len(inventario) == 0:
        print('Todavia no hay herramientas cargadas.')
    else:
        print('--- Inventario actual ---')
        for producto in inventario:
            print(f"- {producto['herramienta']}: {producto['cantidad']} unidades")


def consultar_stock(inventario):
    """Opcion 3: muestra el stock de una herramienta buscada por nombre."""
    if len(inventario) == 0:
        print('Todavia no hay herramientas cargadas.')
        return

    nombre = validar_nombre(input('Nombre de la herramienta a consultar: '))
    producto = buscar_herramienta(inventario, nombre)
    if producto is None:
        print(f"La herramienta '{nombre}' no se encuentra en el catalogo.")
    else:
        print(f"Stock de '{producto['herramienta']}': {producto['cantidad']} unidades.")


def reporte_agotados(inventario):
    """Opcion 4: lista solo las herramientas con stock igual a cero."""
    if len(inventario) == 0:
        print('Todavia no hay herramientas cargadas.')
        return

    hay_agotados = False
    for producto in inventario:
        if producto['cantidad'] == 0:
            if not hay_agotados:
                print('--- Herramientas agotadas ---')
                hay_agotados = True
            print(f"- {producto['herramienta']}")

    if not hay_agotados:
        print('Ninguna herramienta tiene stock cero.')


def alta_producto(inventario):
    """Opcion 5: agrega una herramienta nueva al final del inventario.

    Los errores NO se capturan aca: salen de la funcion y los recibe el
    except de main(), que muestra el motivo y vuelve al menu.
    """
    nombre = validar_nombre_nuevo(inventario, input('Nombre de la nueva herramienta: '))
    stock = validar_stock_inicial(leer_entero('Stock inicial: '))
    inventario.append({'herramienta': nombre, 'cantidad': stock})
    print(f"'{nombre}' agregada con {stock} unidades.")


def actualizar_stock(inventario):
    """Opcion 6: registra una venta (resta) o un ingreso (suma) de unidades.

    Sigue estrictamente el orden del enunciado y no modifica el stock hasta
    que todas las validaciones pasaron.
    """
    # 1. Sin herramientas cargadas
    if len(inventario) == 0:
        print('Todavia no hay herramientas cargadas.')
        return

    # 2. Nombre valido (si esta vacio lanza ValueError)
    nombre = validar_nombre(input('Nombre de la herramienta: '))

    # 3. La herramienta debe existir
    producto = buscar_herramienta(inventario, nombre)
    if producto is None:
        print(f"La herramienta '{nombre}' no existe en el inventario.")
        return

    # 4. Tipo de movimiento (se compara como texto, sin int())
    print('Tipo de movimiento:')
    print('1. Venta')
    print('2. Ingreso')
    tipo = input('Elija el tipo (1/2 o venta/ingreso): ').strip().lower()
    if tipo != '1' and tipo != 'venta' and tipo != '2' and tipo != 'ingreso':
        print('Tipo de movimiento invalido: solo se acepta venta o ingreso.')
        return

    # 5. Unidades: entero mayor que 0
    unidades = validar_unidades(leer_entero('Unidades del movimiento: '))

    # 6 y 7. Venta (con control de stock suficiente) o ingreso
    if tipo == '1' or tipo == 'venta':
        if unidades > producto['cantidad']:
            raise ValueError(
                f"Stock insuficiente: hay {producto['cantidad']} unidades y se quieren vender {unidades}.")
        producto['cantidad'] -= unidades
        print(f"Venta registrada. Stock de '{producto['herramienta']}': {producto['cantidad']}.")
    else:
        producto['cantidad'] += unidades
        print(f"Ingreso registrado. Stock de '{producto['herramienta']}': {producto['cantidad']}.")


# ---------------------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------------------

def main():
    """Crea el inventario y repite el menu hasta que se elige la opcion 7."""
    inventario = []
    opcion = 0
    while opcion != 7:
        mostrar_menu()
        try:
            opcion = leer_entero('Seleccione una opcion: ')
            if opcion == 1:
                cargar_herramientas(inventario)
            elif opcion == 2:
                mostrar_inventario(inventario)
            elif opcion == 3:
                consultar_stock(inventario)
            elif opcion == 4:
                reporte_agotados(inventario)
            elif opcion == 5:
                alta_producto(inventario)
            elif opcion == 6:
                actualizar_stock(inventario)
            elif opcion != 7:
                raise ValueError('Opcion fuera de rango (1 a 7).')
        except ValueError as e:
            print(f'Error: {e}')
    print('Sistema finalizado. Hasta luego!')


main()
