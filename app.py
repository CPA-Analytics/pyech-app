import streamlit as st
from pyech import ECH


st.set_page_config(page_title="PyECH")

#@st.cache(show_spinner=False)
def load_survey(year, weights):
    survey = ECH()
    survey.load(year=year, weights=weights)
    st.session_state.ech = survey
    return

st.sidebar.image("https://github.com/CPA-Analytics/pyech/raw/master/logo.png")
st.sidebar.markdown("PyECH es un procesador de la Encuesta Continua de Hogares del INE escrito en Python.")
st.sidebar.markdown("Aunque fue diseñado para ser utilizado como librería, esta app incorpora la funcionalidad básica.")
year_select = st.sidebar.selectbox(label="Seleccionar año de encuesta", options=list(range(2006, 2021)), index=13)
weights_text = st.sidebar.text_input("Seleccionar ponderador", value="pesoano")
load_button = st.sidebar.button("Cargar", on_click=load_survey, args=(year_select, weights_text))

if "ech" in st.session_state:
    st.text(f"Encuesta cargada: {st.session_state.ech.data['anio'][0]} | Ponderador: {st.session_state.ech.weights}")
section = st.selectbox("Sección", options=["Resumir variables", "Explorar diccionario", "Sobre PyECH"])
st.markdown("---")

if section == "Explorar diccionario" and "ech" in st.session_state:
    #st.subheader("Explorar diccionario")
    term = st.text_input("Términos de búsqueda", value="ingreso")
    n_elements = st.slider("Cantidad de elementos", min_value=1, value=10)
    st.dataframe(st.session_state.ech.search_dictionary(term=term).head(n_elements).astype(str))

categorical_dict = {"Auto": None, "Categórica": True, "No categórica": False}
function_dict = {"Suma": "sum", "Promedio": "mean", "Recuento": "count"}

if section == "Resumir variables" and "ech" in st.session_state:
    #st.subheader("Resumir variables")
    variable_select = st.selectbox("Seleccionar variable", options=st.session_state.ech.data.columns)
    group_select = st.multiselect("Seleccionar agrupadores", options=st.session_state.ech.data.columns)
    function_select = st.selectbox("Seleccionar agregador", options=["Suma", "Promedio", "Recuento"])
    st.caption("Si la variable es categórica solo se agregará mediante recuento.")
    categorical_select = st.selectbox("Tipo de variable", options=["Auto", "Categórica", "No categórica"], index=0)
    try:
        summ = st.session_state.ech.summarize(variable_select, by=group_select, is_categorical=categorical_dict[categorical_select],
                                aggfunc=function_dict[function_select], variable_labels=True)
        st.dataframe(summ)
        st.download_button("Descargar CSV", mime="text/csv", data=summ.to_csv(encoding="latin1"), file_name="pyech-data.csv")
    except:
        pass

if section == "Sobre PyECH":
    st.markdown("Esta app representa la funcionalidad más básica de PyECH, pero que a priori abraca la mayoría de los análisis fundamentales que se pueden hacer con la Encuesta Continua de Hogares: cruzar variables.")
    st.markdown("El paquete de Python sobre el cual esta app está construida también permite calcular percentiles, convertir variables a precios constantes y dólares, y en general brinda una interfaz flexible para trabajar con la encuesta. [Este notebook en Google Colab](https://colab.research.google.com/github/CPA-Analytics/pyech/blob/master/examples/example.ipynb) recorre la API de PyECH y muestra su funcionalidad")
    st.markdown("---")
    st.markdown("[Github](https://github.com/CPA-Analytics/pyech)")
    st.markdown("[PyPI](https://pypi.org/project/pyech/)")
    st.markdown("[Documentación](https://pyech.readthedocs.io/en/latest/)")
