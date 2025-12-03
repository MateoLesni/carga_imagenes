# 🚀 Guía de Despliegue en Streamlit Cloud

## 📋 Pre-requisitos

1. Cuenta de GitHub (gratis)
2. Cuenta de Streamlit Cloud (gratis): https://share.streamlit.io/

## 🔧 Paso 1: Preparar el Repositorio de GitHub

### 1.1 Crear un nuevo repositorio en GitHub

1. Ve a https://github.com/new
2. Nombre del repositorio: `sistema-facturas` (o el que prefieras)
3. **IMPORTANTE**: Márcalo como **Privado** (porque contiene contraseñas)
4. NO inicialices con README (ya tienes archivos)
5. Haz clic en "Create repository"

### 1.2 Subir tu código a GitHub

Abre PowerShell o Git Bash en la carpeta `streamlit_app` y ejecuta:

```bash
# Inicializar git (si no está inicializado)
git initaaaa

# Agregar todos los archivos
git add .

# Crear el primer commit
git commit -m "Initial commit: Sistema de Facturas"

# Conectar con tu repositorio de GitHub
# Reemplaza 'tu-usuario' con tu usuario de GitHub
git remote add origin https://github.com/tu-usuario/sistema-facturas.git

# Subir los archivos
git branch -M main
git push -u origin main
```

## 🌐 Paso 2: Desplegar en Streamlit Cloud

### 2.1 Acceder a Streamlit Cloud

1. Ve a https://share.streamlit.io/
2. Inicia sesión con tu cuenta de GitHub
3. Haz clic en "New app"

### 2.2 Configurar el Deploy

En el formulario de deploy, completa:

- **Repository**: Selecciona `tu-usuario/sistema-facturas`
- **Branch**: `main`
- **Main file path**: `app.py`
- **App URL** (opcional): Elige una URL personalizada

### 2.3 Configuración Avanzada (Opcional)

Haz clic en "Advanced settings" y configura:

- **Python version**: 3.11 o superior
- **Secrets**: NO necesitas configurar secrets por ahora

### 2.4 Deploy

1. Haz clic en "Deploy!"
2. Espera 2-5 minutos mientras se despliega
3. ¡Tu app estará lista!

## 🔒 Paso 3: Seguridad Post-Despliegue

### IMPORTANTE: Cambiar Contraseñas

Una vez desplegada, las contraseñas del archivo `usuarios.json` estarán en texto plano. Considera:

**Opción A: Usar Streamlit Secrets (Recomendado)**

1. En tu app desplegada, ve a "Settings" → "Secrets"
2. Agrega las contraseñas de forma segura

**Opción B: Cambiar las contraseñas en el archivo**

Edita `usuarios.json` con contraseñas seguras antes de hacer push.

## 📊 Almacenamiento de Datos

### ⚠️ IMPORTANTE: Limitaciones

**Tu app guardará datos en el sistema de archivos de Streamlit Cloud, pero:**

1. **Los datos NO son permanentes al 100%**
   - Si la app se reinicia completamente, los datos pueden perderse
   - Streamlit Cloud puede reiniciar la app periódicamente

2. **Solución temporal:**
   - Los datos persisten en la mayoría de los casos
   - Para respaldo, descarga periódicamente:
     - `data/facturas.csv`
     - `data/imagenes.json`
     - Carpeta `imagenes/`

3. **Para producción seria:**
   - Considera migrar a una base de datos (Supabase, PostgreSQL)
   - O usar almacenamiento en la nube (AWS S3, Google Cloud Storage)

## 🔄 Actualizar la App

Cuando hagas cambios en el código:

```bash
# Agregar cambios
git add .

# Crear commit
git commit -m "Descripción de los cambios"

# Subir a GitHub
git push

# Streamlit Cloud detectará los cambios y redesplegará automáticamente
```

## 🆘 Solución de Problemas

### Error: "Module not found"
- Verifica que `requirements.txt` esté en la raíz del repo
- Asegúrate de que todas las dependencias estén listadas

### Error: "Port already in use"
- Reinicia la app desde el dashboard de Streamlit Cloud

### Los datos se perdieron
- Esto puede pasar si la app se reinicia
- Considera implementar respaldos automáticos o migrar a una base de datos

### No puedo ver mi app
- Verifica que el repositorio sea accesible
- Revisa los logs en Streamlit Cloud

## 📱 Acceder a tu App

Una vez desplegada, tu app estará disponible en:
```
https://tu-usuario-sistema-facturas-xxxxx.streamlit.app
```

¡Comparte esta URL con tus usuarios!

## 🔐 Usuarios Configurados

Por defecto, estos son los usuarios creados (cámbialos en producción):

- **PEDIDOS**: Usuario de pedidos (puede asignar MR)
- **PROVEEDORES**: Usuario de proveedores (solo visualiza)
- **Trenes**, **OnceGastro**, etc.: Usuarios de carga

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs en Streamlit Cloud
2. Verifica que todos los archivos estén en GitHub
3. Asegúrate de que `requirements.txt` esté actualizado

---

¡Tu sistema de facturas está listo para usar! 🎉
