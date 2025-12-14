import streamlit as st
import pandas as pd

# -----------------------------------------------------------------------------
# 1. ESTRUCTURAS DE DATOS Y LÓGICA (BACKEND)
# -----------------------------------------------------------------------------

class Libro:
    """Clase que representa la estructura de un libro."""
    def __init__(self, codigo, titulo, apellido_autor, nombre_autor, area, publicador, tramo):
        self.codigo = codigo
        self.titulo = titulo
        self.apellido_autor = apellido_autor
        self.nombre_autor = nombre_autor
        self.area = area
        self.publicador = publicador
        self.tramo = tramo
        # Estado por defecto según el requerimiento futuro (aunque no se usa en MVP, es buena práctica dejarlo)
        self.estado = "En sala"

    def to_dict(self):
        """Convierte el objeto a diccionario para facilitar visualización en Dataframes."""
        return {
            "Código": self.codigo,
            "Título": self.titulo,
            "Autor (Apellido)": self.apellido_autor,
            "Autor (Nombre)": self.nombre_autor,
            "Área": self.area,
            "Publicador": self.publicador,
            "Tramo": self.tramo,
            "Estado": self.estado
        }

class SistemaBiblioteca:
    """Clase controladora que maneja la lista de libros."""
    def __init__(self):
        # Aquí usamos la estructura de datos: LISTA
        self.libros = []

    def agregar_libro(self, nuevo_libro):
        # Validación: No duplicar códigos
        for libro in self.libros:
            if libro.codigo == nuevo_libro.codigo:
                return False, "Error: Ya existe un libro con ese código."
        self.libros.append(nuevo_libro)
        return True, "Libro guardado exitosamente."

    def buscar_por_codigo(self, codigo):
        # Búsqueda lineal en la lista
        for libro in self.libros:
            if libro.codigo == codigo:
                return libro
        return None

    def eliminar_libro(self, codigo):
        # Recorremos la lista para encontrar y remover
        for i, libro in enumerate(self.libros):
            if libro.codigo == codigo:
                del self.libros[i]
                return True, f"Libro {codigo} eliminado."
        return False, "Libro no encontrado."

    def modificar_libro(self, codigo, nuevos_datos):
        libro = self.buscar_por_codigo(codigo)
        if libro:
            libro.titulo = nuevos_datos['titulo']
            libro.apellido_autor = nuevos_datos['apellido_autor']
            libro.nombre_autor = nuevos_datos['nombre_autor']
            libro.area = nuevos_datos['area']
            libro.publicador = nuevos_datos['publicador']
            libro.tramo = nuevos_datos['tramo']
            return True, "Libro actualizado correctamente."
        return False, "No se pudo actualizar (Código no existe)."

    def obtener_todos(self):
        return [libro.to_dict() for libro in self.libros]

# -----------------------------------------------------------------------------
# 2. INTERFAZ GRÁFICA (STREAMLIT)
# -----------------------------------------------------------------------------

def main():
    st.set_page_config(page_title="Sistema Biblioteca Nacional", page_icon="📚", layout="wide")
    
    st.title("📚 Sistema de Gestión Bibliotecaria")
    st.markdown("---")

    # Inicialización del Estado (Persistencia en memoria durante la sesión)
    if 'sistema' not in st.session_state:
        st.session_state.sistema = SistemaBiblioteca()
        # Datos de prueba para no empezar vacíos
        st.session_state.sistema.agregar_libro(Libro("L001", "Cien Años de Soledad", "García Márquez", "Gabriel", "Literatura", "Sudamericana", "A1"))
        st.session_state.sistema.agregar_libro(Libro("P002", "Python Data Science", "VanderPlas", "Jake", "Tecnología", "O'Reilly", "T5"))

    # Menú Lateral
    menu = ["Inicio", "Registrar Libro", "Consultar Inventario", "Buscar", "Modificar", "Eliminar"]
    choice = st.sidebar.selectbox("Menú de Operaciones", menu)

    # Lógica de Vistas
    if choice == "Inicio":
        st.subheader("Bienvenido al Panel de Control")
        st.info("Utilice el menú lateral para gestionar el inventario de la biblioteca.")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Libros", len(st.session_state.sistema.libros))
        col2.metric("Áreas Registradas", len(set(l.area for l in st.session_state.sistema.libros)))
        col3.metric("Estado del Sistema", "Activo")
        
        

    elif choice == "Registrar Libro":
        st.subheader("📝 Registrar Nuevo Libro")
        with st.form("entry_form"):
            c1, c2 = st.columns(2)
            codigo = c1.text_input("Código del Libro")
            titulo = c2.text_input("Título del Libro")
            
            c3, c4 = st.columns(2)
            nombre_autor = c3.text_input("Nombre del Autor")
            apellido_autor = c4.text_input("Apellido del Autor")
            
            c5, c6 = st.columns(2)
            area = c5.selectbox("Área de Conocimiento", ["General", "Tecnología", "Literatura", "Historia", "Ciencias", "Arte"])
            publicador = c6.text_input("Publicador / Editorial")
            
            tramo = st.text_input("Tramo Asignado (Estantería)")
            
            submitted = st.form_submit_button("Guardar Libro")
            
            if submitted:
                if codigo and titulo:
                    nuevo_libro = Libro(codigo, titulo, apellido_autor, nombre_autor, area, publicador, tramo)
                    exito, mensaje = st.session_state.sistema.agregar_libro(nuevo_libro)
                    if exito:
                        st.success(mensaje)
                    else:
                        st.error(mensaje)
                else:
                    st.warning("El código y el título son obligatorios.")

    elif choice == "Consultar Inventario":
        st.subheader("📋 Inventario Completo")
        datos = st.session_state.sistema.obtener_todos()
        if datos:
            df = pd.DataFrame(datos)
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("No hay libros registrados en el sistema.")

    elif choice == "Buscar":
        st.subheader("🔍 Búsqueda de Libros")
        busqueda = st.text_input("Ingrese el Código del Libro a buscar")
        if st.button("Buscar"):
            libro = st.session_state.sistema.buscar_por_codigo(busqueda)
            if libro:
                st.success("Libro Encontrado")
                st.json(libro.to_dict())
            else:
                st.error("Libro no encontrado con ese código.")

    elif choice == "Modificar":
        st.subheader("✏️ Modificar Libro Existente")
        busqueda_mod = st.text_input("Ingrese Código del libro a modificar")
        buscar_btn = st.button("Cargar Datos")
        
        # Usamos session_state para mantener si ya buscamos el libro
        if buscar_btn or 'libro_temp' in st.session_state:
            libro_encontrado = st.session_state.sistema.buscar_por_codigo(busqueda_mod)
            
            if libro_encontrado:
                st.info(f"Editando: {libro_encontrado.titulo}")
                with st.form("update_form"):
                    n_titulo = st.text_input("Título", value=libro_encontrado.titulo)
                    n_nombre = st.text_input("Nombre Autor", value=libro_encontrado.nombre_autor)
                    n_apellido = st.text_input("Apellido Autor", value=libro_encontrado.apellido_autor)
                    n_area = st.selectbox("Área", ["General", "Tecnología", "Literatura", "Historia", "Ciencias", "Arte"], index=0) # Simplificado index
                    n_pub = st.text_input("Publicador", value=libro_encontrado.publicador)
                    n_tramo = st.text_input("Tramo", value=libro_encontrado.tramo)
                    
                    actualizar = st.form_submit_button("Confirmar Cambios")
                    
                    if actualizar:
                        nuevos_datos = {
                            'titulo': n_titulo, 'nombre_autor': n_nombre, 
                            'apellido_autor': n_apellido, 'area': n_area, 
                            'publicador': n_pub, 'tramo': n_tramo
                        }
                        exito, msg = st.session_state.sistema.modificar_libro(busqueda_mod, nuevos_datos)
                        if exito: 
                            st.success(msg)
                        else:
                            st.error(msg)
            elif buscar_btn: # Solo mostrar error si se presionó buscar y no se encontró
                st.error("Código no encontrado.")

    elif choice == "Eliminar":
        st.subheader("🗑️ Eliminar Libro")
        del_codigo = st.text_input("Código del libro a eliminar")
        if st.button("Eliminar permanentemente"):
            exito, msg = st.session_state.sistema.eliminar_libro(del_codigo)
            if exito:
                st.success(msg)
            else:
                st.error(msg)

if __name__ == '__main__':
    main()