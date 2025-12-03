import streamlit as st
import pandas as pd
import os
from datetime import datetime
from PIL import Image
import json
from pathlib import Path
import zipfile
from io import BytesIO

# Configuración de la página
st.set_page_config(
    page_title="Sistema de Facturas",
    page_icon="📄",
    layout="wide"
)

# Directorio base para almacenamiento persistente
# En Streamlit Cloud, usa el directorio actual
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
IMAGENES_DIR = BASE_DIR / "imagenes"

# Crear directorios necesarios
DATA_DIR.mkdir(exist_ok=True)
IMAGENES_DIR.mkdir(exist_ok=True)

# Rutas de archivos
FACTURAS_FILE = str(DATA_DIR / "facturas.csv")
IMAGENES_FILE = str(DATA_DIR / "imagenes.json")
USUARIOS_FILE = str(BASE_DIR / "usuarios.json")
PROVEEDORES_FILE = str(BASE_DIR / "proveedores.json")

# Inicializar archivos si no existen
def inicializar_archivos():
    if not os.path.exists(FACTURAS_FILE):
        df = pd.DataFrame(columns=["id", "fecha", "local", "proveedor", "orden_compra", "fecha_registro", "usuario", "mr_asignado", "numero_mr"])
        df.to_csv(FACTURAS_FILE, index=False)

    if not os.path.exists(IMAGENES_FILE):
        with open(IMAGENES_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)

inicializar_archivos()

# Funciones de usuarios
def cargar_usuarios():
    if os.path.exists(USUARIOS_FILE):
        with open(USUARIOS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("usuarios", [])
    return []

def cargar_proveedores():
    if os.path.exists(PROVEEDORES_FILE):
        with open(PROVEEDORES_FILE, "r", encoding="utf-8") as f:
            proveedores = f.read().splitlines()
            return [p.strip() for p in proveedores if p.strip() and p.strip() != "Proveedores"]
    return []

def validar_login(username, password):
    usuarios = cargar_usuarios()
    for user in usuarios:
        if user["username"] == username and user["password"] == password:
            return user
    return None

def obtener_locales_usuario(username):
    usuarios = cargar_usuarios()
    for user in usuarios:
        if user["username"] == username:
            return user.get("locales", [])
    return []

# Funciones auxiliares
def cargar_facturas():
    if os.path.exists(FACTURAS_FILE):
        df = pd.read_csv(FACTURAS_FILE)
        # Asegurar que las columnas MR existan
        if "mr_asignado" not in df.columns:
            df["mr_asignado"] = False
        if "numero_mr" not in df.columns:
            df["numero_mr"] = ""
        return df
    return pd.DataFrame(columns=["id", "fecha", "local", "proveedor", "orden_compra", "fecha_registro", "usuario", "mr_asignado", "numero_mr"])

def guardar_factura(fecha, local, proveedor, orden_compra, username):
    df = cargar_facturas()
    nuevo_id = len(df) + 1 if len(df) > 0 else 1
    nueva_fila = pd.DataFrame([{
        "id": nuevo_id,
        "fecha": fecha,
        "local": local,
        "proveedor": proveedor,
        "orden_compra": orden_compra,
        "fecha_registro": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "usuario": username,
        "mr_asignado": False,
        "numero_mr": ""
    }])
    df = pd.concat([df, nueva_fila], ignore_index=True)
    df.to_csv(FACTURAS_FILE, index=False)
    return nuevo_id

def asignar_mr(factura_id, numero_mr):
    df = cargar_facturas()
    df.loc[df["id"] == factura_id, "mr_asignado"] = True
    df.loc[df["id"] == factura_id, "numero_mr"] = numero_mr
    df.to_csv(FACTURAS_FILE, index=False)

def cargar_imagenes_index():
    with open(IMAGENES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def guardar_imagen(factura_id, uploaded_file):
    filename = f"factura_{factura_id}_{len(os.listdir(IMAGENES_DIR))}_{uploaded_file.name}"
    filepath = IMAGENES_DIR / filename

    with open(filepath, "wb") as f:
        f.write(uploaded_file.getbuffer())

    index = cargar_imagenes_index()
    if str(factura_id) not in index:
        index[str(factura_id)] = []
    index[str(factura_id)].append(filename)

    with open(IMAGENES_FILE, "w", encoding="utf-8") as f:
        json.dump(index, f, indent=2)

    return filename

def obtener_imagenes_factura(factura_id):
    index = cargar_imagenes_index()
    return index.get(str(factura_id), [])

# Inicializar session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = None
if "user_locales" not in st.session_state:
    st.session_state.user_locales = []
if "user_rol" not in st.session_state:
    st.session_state.user_rol = None

# PANTALLA DE LOGIN
if not st.session_state.logged_in:
    st.title("🔐 Iniciar Sesión")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.write("")
        st.write("")

        with st.form("login_form"):
            username = st.text_input("Usuario", placeholder="Ingresa tu usuario")
            password = st.text_input("Contraseña", type="password", placeholder="Ingresa tu contraseña")
            submit = st.form_submit_button("🔓 Ingresar", use_container_width=True)

            if submit:
                if username and password:
                    user = validar_login(username, password)
                    if user:
                        st.session_state.logged_in = True
                        st.session_state.username = username
                        st.session_state.user_locales = user.get("locales", [])
                        st.session_state.user_rol = user.get("rol", None)
                        st.rerun()
                    else:
                        st.error("❌ Usuario o contraseña incorrectos")
                else:
                    st.error("❌ Por favor, completa todos los campos")

# PANTALLA PRINCIPAL (DESPUÉS DEL LOGIN)
else:
    # Header con usuario y logout
    col1, col2 = st.columns([4, 1])
    with col1:
        st.title("📄 Sistema de Gestión de Facturas")
    with col2:
        st.write(f"👤 **{st.session_state.username}**")
        if st.button("🚪 Cerrar Sesión"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.session_state.user_locales = []
            st.session_state.user_rol = None
            st.rerun()

    # Menú lateral - Ocultar "Cargar Datos" si es rol PEDIDOS o PROVEEDORES
    if st.session_state.user_rol in ["pedidos", "proveedores"]:
        menu_options = ["Visualizar Facturas"]
        menu = "Visualizar Facturas"
    else:
        menu = st.sidebar.selectbox(
            "Selecciona una opción",
            ["Cargar Datos", "Visualizar Facturas"]
        )

    # Sidebar info
    st.sidebar.divider()
    st.sidebar.info(f"**Usuario:** {st.session_state.username}")
    if st.session_state.user_rol == "pedidos":
        st.sidebar.info(f"**Rol:** Pedidos")
    elif st.session_state.user_rol == "proveedores":
        st.sidebar.info(f"**Rol:** Proveedores")
    st.sidebar.info(f"**Locales asignados:** {len(st.session_state.user_locales)}")

    # Botón de descarga de datos (solo para PEDIDOS)
    if st.session_state.user_rol == "pedidos":
        st.sidebar.divider()
        st.sidebar.subheader("💾 Respaldo de Datos")

        df_backup = cargar_facturas()
        csv_data = df_backup.to_csv(index=False).encode('utf-8')

        st.sidebar.download_button(
            label="📥 Descargar CSV",
            data=csv_data,
            file_name=f"facturas_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv",
            help="Descarga todas las facturas en formato CSV"
        )

        # Descargar índice de imágenes
        with open(IMAGENES_FILE, "r", encoding="utf-8") as f:
            imagenes_data = f.read()

        st.sidebar.download_button(
            label="📥 Descargar Índice Imágenes",
            data=imagenes_data,
            file_name=f"imagenes_index_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json",
            help="Descarga el índice de imágenes"
        )

        # Botón para descargar todas las imágenes en ZIP
        if st.sidebar.button("📦 Generar ZIP de Imágenes", help="Genera un archivo ZIP con todas las imágenes"):
            try:
                # Crear ZIP en memoria
                zip_buffer = BytesIO()
                with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
                    # Agregar todas las imágenes
                    imagenes_list = os.listdir(IMAGENES_DIR)
                    if imagenes_list:
                        for img_name in imagenes_list:
                            img_path = IMAGENES_DIR / img_name
                            if os.path.exists(img_path):
                                zip_file.write(img_path, arcname=img_name)

                zip_buffer.seek(0)

                # Botón de descarga del ZIP
                st.sidebar.download_button(
                    label="⬇️ Descargar ZIP",
                    data=zip_buffer.getvalue(),
                    file_name=f"imagenes_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.zip",
                    mime="application/zip",
                    help=f"ZIP generado con {len(imagenes_list)} imagen(es)"
                )
                st.sidebar.success(f"✅ ZIP generado con {len(imagenes_list)} imagen(es)")
            except Exception as e:
                st.sidebar.error(f"❌ Error al generar ZIP: {str(e)}")

    # PÁGINA 1: CARGAR DATOS (Solo visible para usuarios no-PEDIDOS)
    if menu == "Cargar Datos":
        st.header("📤 Cargar Nueva Factura")

        proveedores = cargar_proveedores()

        with st.form("form_factura"):
            col1, col2 = st.columns(2)

            with col1:
                fecha = st.date_input("Fecha de la factura")

                if st.session_state.user_locales:
                    local = st.selectbox("Local", options=st.session_state.user_locales)
                else:
                    st.warning("No tienes locales asignados. Contacta al administrador.")
                    local = None

            with col2:
                if proveedores:
                    proveedor = st.selectbox("Proveedor", options=proveedores)
                else:
                    proveedor = st.text_input("Proveedor")

                orden_compra = st.text_input("Orden de Compra")

            imagenes = st.file_uploader(
                "Subir imágenes de la factura",
                type=["jpg", "jpeg", "png", "pdf"],
                accept_multiple_files=True
            )

            submitted = st.form_submit_button("💾 Guardar Factura")

            if submitted:
                if not local or not proveedor or not orden_compra:
                    st.error("Por favor, completa todos los campos obligatorios.")
                elif not imagenes:
                    st.error("Por favor, sube al menos una imagen de la factura.")
                else:
                    factura_id = guardar_factura(
                        str(fecha),
                        local,
                        proveedor,
                        orden_compra,
                        st.session_state.username
                    )

                    imagenes_guardadas = []
                    for img in imagenes:
                        filename = guardar_imagen(factura_id, img)
                        imagenes_guardadas.append(filename)

                    st.success(f"✅ Factura #{factura_id} guardada correctamente con {len(imagenes_guardadas)} imagen(es).")
                    st.balloons()

    # PÁGINA 2: VISUALIZAR FACTURAS
    elif menu == "Visualizar Facturas":
        st.header("👀 Visualizar Facturas")

        df = cargar_facturas()

        # Filtrar facturas por locales del usuario
        if not df.empty:
            df_usuario = df[df["local"].isin(st.session_state.user_locales)]
        else:
            df_usuario = df

        if df_usuario.empty:
            st.info("No hay facturas registradas para tus locales asignados.")
        else:
            # Mostrar estadísticas si es rol PEDIDOS o PROVEEDORES
            if st.session_state.user_rol in ["pedidos", "proveedores"]:
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total de Facturas", len(df_usuario))
                with col2:
                    facturas_con_mr = len(df_usuario[df_usuario["mr_asignado"] == True])
                    st.metric("Facturas con MR", facturas_con_mr)
                with col3:
                    facturas_sin_mr = len(df_usuario[df_usuario["mr_asignado"] == False])
                    st.metric("Facturas sin MR", facturas_sin_mr)
                st.divider()

            # Filtros
            col1, col2, col3 = st.columns(3)
            with col1:
                filtro_local = st.selectbox("Filtrar por Local", options=["Todos"] + st.session_state.user_locales)
            with col2:
                filtro_proveedor = st.text_input("Filtrar por Proveedor")
            with col3:
                if st.session_state.user_rol in ["pedidos", "proveedores"]:
                    filtro_mr = st.selectbox("Filtrar por Estado MR", options=["Todos", "Con MR", "Sin MR"])
                else:
                    filtro_orden = st.text_input("Filtrar por Orden de Compra")

            # Aplicar filtros
            df_filtrado = df_usuario.copy()

            if filtro_local != "Todos":
                df_filtrado = df_filtrado[df_filtrado["local"] == filtro_local]

            if filtro_proveedor:
                df_filtrado = df_filtrado[df_filtrado["proveedor"].str.contains(filtro_proveedor, case=False, na=False)]

            if st.session_state.user_rol in ["pedidos", "proveedores"]:
                if filtro_mr == "Con MR":
                    df_filtrado = df_filtrado[df_filtrado["mr_asignado"] == True]
                elif filtro_mr == "Sin MR":
                    df_filtrado = df_filtrado[df_filtrado["mr_asignado"] == False]
            else:
                if filtro_orden:
                    df_filtrado = df_filtrado[df_filtrado["orden_compra"].str.contains(filtro_orden, case=False, na=False)]

            st.write(f"**Facturas mostradas:** {len(df_filtrado)}")
            st.divider()

            # Mostrar facturas
            for idx, row in df_filtrado.iterrows():
                # Construir título completo con toda la información
                mr_indicator = "✅" if row.get("mr_asignado", False) else "⏳"
                # Formatear número MR como texto (sin .0)
                numero_mr_display = str(row.get('numero_mr', '')).replace('.0', '') if pd.notna(row.get('numero_mr', '')) and row.get('numero_mr', '') != '' else 'N/A'
                mr_info = f"MR: {numero_mr_display}" if row.get("mr_asignado", False) else "Sin MR"
                usuario_info = f"| Usuario: {row['usuario']}" if "usuario" in row and pd.notna(row["usuario"]) else ""

                titulo = f"{mr_indicator} Factura #{int(row['id'])} | Local: {row['local']} | Proveedor: {row['proveedor']} | OC: {row['orden_compra']} | Fecha: {row['fecha']} | {mr_info} {usuario_info}"

                with st.expander(titulo):
                    # Sistema de MR para usuario PEDIDOS (PROVEEDORES solo ve, no puede asignar)
                    if st.session_state.user_rol in ["pedidos", "proveedores"]:
                        if row.get("mr_asignado", False):
                            st.success(f"✅ **MR Asignado:** {numero_mr_display}")
                        else:
                            st.warning("⏳ **Sin MR asignado**")

                            # Solo PEDIDOS puede asignar MR
                            if st.session_state.user_rol == "pedidos":
                                # Formulario para asignar MR
                                with st.form(key=f"form_mr_{int(row['id'])}"):
                                    numero_mr_input = st.text_input(
                                        "Número de MR",
                                        placeholder="Ingresa el número de MR",
                                        key=f"mr_input_{int(row['id'])}"
                                    )
                                    submit_mr = st.form_submit_button("✅ Asignar MR")

                                    if submit_mr:
                                        if numero_mr_input.strip():
                                            asignar_mr(int(row['id']), numero_mr_input.strip())
                                            st.success("✅ MR asignado correctamente")
                                            st.rerun()
                                        else:
                                            st.error("❌ Por favor, ingresa un número de MR válido")

                        st.divider()

                    # Mostrar imágenes
                    imagenes = obtener_imagenes_factura(int(row['id']))

                    if imagenes:
                        st.write(f"**Imágenes adjuntas:** {len(imagenes)}")

                        cols = st.columns(3)
                        for i, img_name in enumerate(imagenes):
                            img_path = IMAGENES_DIR / img_name
                            if os.path.exists(img_path):
                                with cols[i % 3]:
                                    try:
                                        img = Image.open(img_path)
                                        st.image(img, caption=img_name, use_container_width=True)

                                        with open(img_path, "rb") as f:
                                            st.download_button(
                                                label=f"⬇️ Descargar",
                                                data=f,
                                                file_name=img_name,
                                                mime="image/jpeg",
                                                key=f"download_{row['id']}_{i}"
                                            )
                                    except:
                                        st.error(f"No se pudo cargar: {img_name}")
                    else:
                        st.warning("No hay imágenes adjuntas para esta factura.")

# DEBUG: Mostrar ubicación de archivos en el sidebar (solo para verificación)
with st.sidebar:
    with st.expander("🔍 Debug Info"):
        st.write(f"**Archivo CSV:** `{FACTURAS_FILE}`")
        st.write(f"**Total registros:** {len(cargar_facturas())}")
        if os.path.exists(FACTURAS_FILE):
            st.success("✅ CSV existe")
        else:
            st.error("❌ CSV no existe")
