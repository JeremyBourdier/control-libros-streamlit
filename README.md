# 📚 Sistema de Gestión Bibliotecaria (MVP)

Prototipo de software desarrollado para la **Biblioteca Pública Nacional**. Este sistema permite la gestión digital del inventario de libros, simplificando los procesos manuales actuales y preparando el terreno para futuras integraciones con tecnologías de automatización (RFID).

Este MVP (Producto Mínimo Viable) se centra en la gestión de entradas, salidas y modificaciones de libros utilizando **estructuras de datos en memoria (Listas)** y una interfaz web interactiva construida con **Streamlit**.

---

## 🚀 Funcionalidades Principales

El sistema cumple con los siguientes criterios de evaluación:

-   **Registro de Libros:** Almacenamiento de Código, Título, Autor (Nombre/Apellido), Área, Publicador y Tramo.
-   **Validación:** Control para evitar códigos duplicados.
-   **Consultas:** Visualización del inventario completo en formato de tabla interactiva.
-   **Búsqueda:** Localización rápida de libros mediante su Código único.
-   **Modificación:** Edición de metadatos de libros existentes.
-   **Eliminación:** Borrado de libros del inventario.
-   **Persistencia de Sesión:** Los datos se mantienen mientras la aplicación está en ejecución.

---

## 🛠️ Tecnologías Utilizadas

-   **Lenguaje:** Python 3.10+
-   **Frontend:** [Streamlit](https://streamlit.io/)
-   **Manejo de Datos:** Estructuras nativas de Python (Listas y Clases) + Pandas (para visualización).

---

## 📦 Estructura del Proyecto

```text
📁 biblioteca_proyecto/
│
├── biblioteca_app.py      # Código fuente principal (Lógica + Interfaz)
├── requirements.txt       # Dependencias del proyecto
└── README.md              # Documentación

Instalación y Configuración
Sigue estos pasos para ejecutar el proyecto en tu entorno local.

1. Clonar o Descargar
Descarga los archivos del proyecto en tu carpeta de preferencia.

2. Crear Entorno Virtual
Es recomendable usar un entorno virtual para aislar las dependencias.



# Windows
python -m venv venv

# macOS / Linux
python3 -m venv venv
3. Activar el Entorno
Una vez creado, actívalo:

# Windows
.\venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
(Verás que tu terminal muestra (venv) al inicio).

4. Instalar Dependencias
Instala las librerías necesarias (Streamlit y Pandas) usando el archivo de requerimientos:



pip install -r requirements.txt
▶️ Ejecución
Para iniciar la aplicación web, ejecuta el siguiente comando dentro de tu entorno virtual:


streamlit run biblioteca_app.py
El navegador se abrirá automáticamente en http://localhost:8501.