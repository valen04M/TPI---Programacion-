# Sistema de Control de Inventario - Ferreteria

Trabajo Practico Integrador de **Programacion 1** (Tecnicatura Universitaria en Programacion a Distancia).

**Alumno:** Valentino Mangini

## Descripcion

Programa en Python con menu interactivo persistente para controlar el inventario de una ferreteria. Cada operacion actualiza el stock en el momento; los datos viven en memoria mientras el programa esta en ejecucion.

El inventario es una lista de diccionarios llamada `inventario`, creada dentro de `main()` y pasada como parametro a cada funcion (sin variables globales). Cada herramienta tiene las claves `'herramienta'` y `'cantidad'` (stock).

## Menu

1. Cargar herramientas (carga multiple con stock inicial)
2. Mostrar inventario
3. Consultar stock
4. Reporte de agotados
5. Alta de nuevo producto
6. Actualizar stock (venta / ingreso)
7. Salir

## Como ejecutarlo

Requiere Python 3. Desde la carpeta del proyecto:

```
python inventario.py
```

Archivo que se ejecuta para iniciar el programa: `inventario.py` (es el unico archivo `.py`).

## Video demostrativo

Link al video (con permisos publicos de visualizacion): https://youtu.be/WP9YJLIIDNs

## Documentacion

Informe de diseño y fundamentacion en PDF: `Informe_Inventario.pdf` (subido en la raiz del repositorio).
