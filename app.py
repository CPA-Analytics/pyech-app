import streamlit as st
from pyech import ECH

st.set_page_config(page_title="PyECH")

hide_streamlit_style = """
<style>
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.css-12oz5g7 {padding-top: 2rem;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

categorical_dict = {"Auto": None, "Categórica": True, "No categórica": False}
function_dict = {"Suma": "sum", "Promedio": "mean", "Recuento": "count"}
weights_dict = {"Anual": "pesoano", "Semestral": "pesosem", "Trimestral": "pesotri", "Mensual": "pesomen"}


def load_survey(year):
    survey = ECH()
    survey.load(year=year)
    st.session_state.ech = survey
    return


def set_weights(weights):
    st.session_state.ech.weights = weights
    return


st.sidebar.image("https://github.com/CPA-Analytics/pyech/raw/master/logo.png")
st.sidebar.markdown("PyECH es un procesador de la Encuesta Continua de Hogares del INE escrito en Python.")
st.sidebar.markdown("Esta webapp representa la funcionalidad más básica de PyECH, pero que a priori abraca la mayoría de los análisis fundamentales que se pueden hacer con la Encuesta Continua de Hogares: cruzar variables.")
st.sidebar.markdown("El paquete de Python sobre el cual esta app está construida también permite calcular percentiles, convertir variables a precios constantes y dólares, y en general brinda una interfaz flexible para trabajar con la encuesta. [Este notebook en Google Colab](https://colab.research.google.com/github/CPA-Analytics/pyech/blob/master/examples/example.ipynb) recorre la API de PyECH y muestra su funcionalidad")
st.sidebar.markdown("---")
st.sidebar.markdown("""
                    * [Github](https://github.com/CPA-Analytics/pyech)
                    * [PyPI](https://pypi.org/project/pyech/)
                    * [Documentación](https://pyech.readthedocs.io/en/latest/)
                    """)
st.title("PyECH")
st.caption("Procesamiento de la ECH del INE en Python.")
section = st.selectbox("Sección", options=["Carga", "Resumir variables", "Explorar diccionario"], index=0)
if "ech" in st.session_state:
    st.markdown(f"**Encuesta cargada**: {st.session_state.ech.data['anio'][0]} | **Ponderador**: {st.session_state.ech.weights}")
st.markdown("---")

if section == "Carga":
    year_select = st.selectbox(label="Seleccionar año de encuesta", options=list(range(2006, 2021)), index=13)
    survey_load_button = st.button("Aceptar", on_click=load_survey, args=(year_select,), key=0)
    if "ech" in st.session_state:
        weights_select = st.selectbox("Seleccionar ponderador", options=weights_dict.keys(),
                                        index=0)
        st.caption("No todos los ponderadores están presentes en todas las encuestas.")
        weights_set_button = st.button("Aceptar", on_click=set_weights, args=(weights_dict[weights_select],), key=1)


elif section != "Carga" and "ech" in st.session_state and st.session_state.ech.weights not in st.session_state.ech.data.columns:
    st.markdown(f"El ponderador {st.session_state.ech.weights} no está disponible en la ECH {st.session_state.ech.data['anio'][0]}. Seleccionar otro.")

elif section == "Explorar diccionario" and "ech" in st.session_state:
    col1, col2 = st.columns(2)
    term = col1.text_input("Términos de búsqueda", value="ingreso")
    n_elements = col2.slider("Cantidad de elementos", min_value=1, value=10)
    st.dataframe(st.session_state.ech.search_dictionary(term=term).head(n_elements).astype(str))

elif section == "Resumir variables" and "ech" in st.session_state:
    col1, col2 = st.columns(2)
    variable_select = col1.selectbox("Seleccionar variable", options=st.session_state.ech.data.columns)
    group_select = col2.multiselect("Seleccionar agrupadores", options=st.session_state.ech.data.columns)
    function_select = col1.selectbox("Seleccionar operación", options=["Suma", "Promedio", "Recuento"])
    col1.caption("Si la variable es categórica solo se agregará mediante recuento.")
    categorical_select = col2.selectbox("Definir tipo de variable", options=["Auto", "Categórica", "No categórica"], index=0)
    try:
        summ = st.session_state.ech.summarize(variable_select, by=group_select, is_categorical=categorical_dict[categorical_select],
                                aggfunc=function_dict[function_select], variable_labels=True)
        st.dataframe(summ)
        st.download_button("Descargar CSV", mime="text/csv", data=summ.to_csv(encoding="latin1"), file_name="pyech-data.csv")
    except:
        pass

else:
    st.markdown("Una encuesta tiene que ser cargada en la sección de _Carga_ para poder resumir variables o explorar el diccionario.")