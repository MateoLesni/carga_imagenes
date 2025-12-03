# Sistema de Gestión de Facturas

Aplicación web desarrollada con Streamlit para gestionar facturas y sus imágenes asociadas.

## Características

- Carga de facturas con datos: fecha, local, proveedor y orden de compra
- Subida de múltiples imágenes por factura (JPG, PNG, PDF)
- Visualización de facturas con filtros por local, proveedor y orden de compra
- Vista de imágenes en miniatura con opción de descarga
- Almacenamiento local en CSV y JSON

## Instalación

1. Asegúrate de tener Python 3.8 o superior instalado

2. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Ejecución

Ejecuta la aplicación con:
```bash
streamlit run app.py
```

La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`

## Uso

### Cargar Datos
1. Selecciona "Cargar Datos" en el menú lateral
2. Completa los campos: fecha, local, proveedor y orden de compra
3. Sube una o varias imágenes de la factura
4. Haz clic en "Guardar Factura"

### Visualizar Facturas
1. Selecciona "Visualizar Facturas" en el menú lateral
2. Usa los filtros para buscar facturas específicas
3. Haz clic en cada factura para expandir y ver sus detalles e imágenes
4. Descarga las imágenes individuales si es necesario

## Estructura de Archivos

```
streamlit_app/
├── app.py                 # Aplicación principal
├── requirements.txt       # Dependencias
├── data/                  # Carpeta de datos (se crea automáticamente)
│   ├── facturas.csv      # Base de datos de facturas
│   └── imagenes.json     # Índice de imágenes
└── imagenes/             # Carpeta de imágenes (se crea automáticamente)
```

## Datos Almacenados

- **facturas.csv**: Contiene id, fecha, local, proveedor, orden_compra y fecha_registro
- **imagenes.json**: Mapea cada ID de factura con sus archivos de imagen
- **imagenes/**: Carpeta con todas las imágenes subidas
