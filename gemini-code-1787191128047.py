import pandas as pd
import plotly.express as px
import streamlit as st

# Configuración de la página
st.set_page_config(
    page_title="ClaroVenta - Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Datos de muestra iniciales (Simulador)
INITIAL_DATA = [
    {
        "Producto": "Café Premium",
        "Unidades": 142,
        "Precio": 18.00,
        "Costo": 9.36,
    },
    {"Producto": "Té Verde", "Unidades": 98, "Precio": 12.00, "Costo": 7.08},
    {
        "Producto": "Galletas artesanales",
        "Unidades": 89,
        "Precio": 6.50,
        "Costo": 4.61,
    },
    {
        "Producto": "Jabón natural",
        "Unidades": 56,
        "Precio": 8.50,
        "Costo": 7.50,
    },
    {
        "Producto": "Miel artesanal",
        "Unidades": 67,
        "Precio": 15.00,
        "Costo": 7.20,
    },
]

# Inicializar datos en la sesión
if "df_sales" not in st.session_state:
    st.session_state.df_sales = pd.DataFrame(INITIAL_DATA)


def calculate_metrics(df):
    """Calcula utilidades y márgenes de ganancia."""
    df["Ingresos"] = df["Unidades"] * df["Precio"]
    df["Costos_Totales"] = df["Unidades"] * df["Costo"]
    df["Utilidad"] = df["Ingresos"] - df["Costos_Totales"]
    df["Margen_%"] = (
        (df["Utilidad"] / df["Ingresos"]) * 100
    ).fillna(0).round(1)

    # Definir estado según el margen
    def check_status(margin):
        if margin >= 30:
            return "Bien"
        elif margin >= 15:
            return "Atención"
        else:
            return "Crítico"

    df["Estado"] = df["Margen_%"].apply(check_status)
    return df


# --- SIDEBAR: Navegación y Carga de Datos ---
with st.sidebar:
    st.title("📈 ClaroVenta")
    st.caption("Hecho para pequeños negocios")
    st.divider()

    menu = st.radio("Navegación", ["Dashboard Resumen", "Cargar / Editar Datos"])

    st.divider()
    st.caption("Usuario: **Juan Pérez**")

# --- LÓGICA PRINCIPAL ---
df = calculate_metrics(st.session_state.df_sales.copy())

if menu == "Cargar / Editar Datos":
    st.title("📥 Carga y Gestión de Ventas")
    st.write(
        "Sube un archivo CSV con tus ventas o edita la tabla directamente."
    )

    tab1, tab2 = st.tabs(["📤 Subir CSV", "✏️ Editar Tabla Manualmente"])

    with tab1:
        uploaded_file = st.file_uploader("Elige un archivo CSV", type=["csv"])
        if uploaded_file is not None:
            try:
                new_df = pd.read_csv(uploaded_file)
                st.session_state.df_sales = new_df
                st.success("¡Datos cargados correctamente!")
                st.rerun()
            except Exception as e:
                st.error(f"Error al procesar el archivo CSV: {e}")

    with tab2:
        edited_df = st.data_editor(
            st.session_state.df_sales,
            num_rows="dynamic",
            use_container_width=True,
        )
        if st.button("Guardar Cambios", type="primary"):
            st.session_state.df_sales = edited_df
            st.success("¡Tabla actualizada con éxito!")
            st.rerun()

elif menu == "Dashboard Resumen":
    st.title("📊 Resumen de tu negocio")
    st.caption("Análisis automático de tus márgenes y utilidades")

    # Métricas principales
    total_utilidad = df["Utilidad"].sum()
    total_ingresos = df["Ingresos"].sum()
    margen_promedio = (
        (total_utilidad / total_ingresos) * 100 if total_ingresos > 0 else 0
    )
    prod_bien = (df["Estado"] == "Bien").sum()
    prod_atencion = (df["Estado"] != "Bien").sum()

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Utilidad Total", f"${total_utilidad:,.2f}", "+12% vs mes ant.")
    col2.metric("Margen Promedio", f"{margen_promedio:.1f}%")
    col3.metric("Productos Saludables", f"{prod_bien}", f"de {len(df)} total")
    col4.metric(
        "Requieren Atención",
        f"{prod_atencion}",
        delta_color="inverse",
    )

    st.divider()

    # Sección de Alertas y Recomendaciones
    col_rec, col_table = st.columns([1, 1.5])

    with col_rec:
        st.subheader("💡 Recomendaciones Prioritarias")

        criticos = df[df["Estado"] == "Crítico"]
        atencion = df[df["Estado"] == "Atención"]

        if not criticos.empty:
            for _, row in criticos.iterrows():
                st.error(
                    f"**Alta Prioridad: {row['Producto']}**\n\n"
                    f"El margen es solo del **{row['Margen_%']}%**. "
                    f"Considera aumentar el precio o renegociar el costo de ${row['Costo']:.2f} con tu proveedor."
                )

        if not atencion.empty:
            for _, row in atencion.iterrows():
                st.warning(
                    f"**Atención: {row['Producto']}**\n\n"
                    f"Margen del **{row['Margen_%']}%**. "
                    "Prueba promociones o combos para impulsar las ventas."
                )

        if criticos.empty and atencion.empty:
            st.success(
                "🎉 ¡Excelente! Todos tus productos muestran un margen saludable superior al 30%."
            )

    with col_table:
        st.subheader("📦 Estado de Productos")
        st.dataframe(
            df[["Producto", "Unidades", "Precio", "Margen_%", "Estado"]],
            use_container_width=True,
            hide_index=True,
        )

    st.divider()

    # Gráficos interactivos con Plotly
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        st.subheader("💰 Utilidad por Producto")
        fig_bar = px.bar(
            df,
            x="Producto",
            y="Utilidad",
            color="Estado",
            color_discrete_map={
                "Bien": "#059669",
                "Atención": "#D97706",
                "Crítico": "#DC2626",
            },
            text_auto=".2s",
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_chart2:
        st.subheader("📈 Distribución del Margen de Ganancia (%)")
        fig_pie = px.pie(
            df,
            names="Producto",
            values="Utilidad",
            hole=0.4,
        )
        st.plotly_chart(fig_pie, use_container_width=True)