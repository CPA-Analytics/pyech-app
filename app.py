import ast

import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import plotly.io as pio
from pyech import ECH
from dash import html, dcc, Dash, callback_context
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output, State
from dash_bootstrap_templates import load_figure_template
from dash.dash_table import DataTable
from dash.dash_table.Format import Format, Scheme, Trim


stylesheet = dbc.themes.FLATLY
dbc_css = (
    "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.2/dbc.min.css"
)


app = Dash(
    __name__,
    external_stylesheets=[stylesheet, dbc_css],
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    suppress_callback_exceptions=True,
)

server = app.server

template = "flatly"
load_figure_template(template)
pio.templates[template].layout.margin = {"l": 10, "r": 10}


def dbc_dropdown(dropdown: dcc.Dropdown):
    return html.Div(dropdown, className="dash-bootstrap")


NAVBAR = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(
                            html.Img(
                                src="https://github.com/CPA-Analytics/pyech/raw/master/logo.png",
                                height="30px",
                            )
                        ),
                    ],
                    align="center",
                    className="g-0",
                ),
                href="/",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                dbc.Nav(
                    [
                        dbc.NavItem(
                            dbc.NavLink(
                                "Github",
                                href="https://github.com/cpa-analytics/pyech",
                                external_link=True,
                                target="_parent",
                            )
                        ),
                        dbc.NavItem(
                            dbc.NavLink(
                                "PyPI",
                                href="https://pypi.org/project/pyech",
                                external_link=True,
                                target="_parent",
                            )
                        ),
                    ]
                ),
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="light",
)

SURVEY_CHOICE = dbc.Row(
    [
        dbc.Col(
            [
                dbc_dropdown(
                    dcc.Dropdown(
                        id="year",
                        options=[{"label": i, "value": i} for i in range(2007, 2021)],
                        placeholder="Año de encuesta",
                        clearable=False,
                        className="mb-2",
                    )
                ),
            ],
            width=12,
        ),
        dbc.Col(
            [
                dbc_dropdown(
                    dcc.Dropdown(
                        id="weights",
                        options=[
                            {"label": "Anual (pesoano)", "value": "pesoano"},
                            {"label": "Mensual (pesomen)", "value": "pesomen"},
                        ],
                        placeholder="Ponderador",
                    )
                ),
            ],
            width=12,
        ),
    ],
)

SUMMARIZER = html.Div(
    [
        html.Br(),
        dbc.Form(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Label("Seleccionar variable"),
                                dbc_dropdown(
                                    dcc.Dropdown(
                                        id="sumvar",
                                        disabled=True,
                                        placeholder="Variable",
                                    )
                                ),
                            ],
                            md=3,
                            class_name="mb-2",
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Seleccionar agrupadores"),
                                dbc_dropdown(
                                    dcc.Dropdown(
                                        id="by",
                                        multi=True,
                                        disabled=True,
                                        placeholder="Agrupadores",
                                    )
                                ),
                            ],
                            md=3,
                            class_name="mb-2",
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Seleccionar método"),
                                dbc_dropdown(
                                    dcc.Dropdown(
                                        id="aggfunc",
                                        clearable=False,
                                        placeholder="Función",
                                        disabled=True,
                                        options=[
                                            {"label": "Suma", "value": "sum"},
                                            {"label": "Promedio", "value": "mean"},
                                            {
                                                "label": "Recuento",
                                                "value": "count",
                                            },
                                        ],
                                        value="mean",
                                    )
                                ),
                            ],
                            md=2,
                            class_name="mb-2",
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Seleccionar tipo de variable"),
                                dbc_dropdown(
                                    dcc.Dropdown(
                                        id="is-categorical",
                                        placeholder="Tipo",
                                        disabled=True,
                                        clearable=False,
                                        options=[
                                            {"label": "Auto", "value": "None"},
                                            {"label": "Categórica", "value": "True"},
                                            {
                                                "label": "No categórica",
                                                "value": "False",
                                            },
                                        ],
                                        value="None",
                                    )
                                ),
                            ],
                            md=2,
                            class_name="mb-2",
                        ),
                        dbc.Col(
                            [
                                dbc.Label("Seleccionar nivel"),
                                dbc_dropdown(
                                    dcc.Dropdown(
                                        id="household",
                                        placeholder="Nivel",
                                        clearable=False,
                                        options=[
                                            {"label": "Hogares", "value": "True"},
                                            {"label": "Personas", "value": "False"},
                                        ],
                                        disabled=True,
                                        value="False",
                                    )
                                ),
                            ],
                            md=2,
                        ),
                    ]
                )
            ]
        ),
        html.Br(),
    ],
)


CONTROLS = dbc.Row(
    [
        dbc.Col(
            [
                dbc.Label("Eje X"),
                dbc_dropdown(
                    dcc.Dropdown(
                        id="x-axis",
                        placeholder="Eje X",
                        clearable=True,
                    )
                ),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Color"),
                dbc_dropdown(
                    dcc.Dropdown(
                        id="color",
                        placeholder="Color",
                        clearable=True,
                    )
                ),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Columnas"),
                dbc_dropdown(
                    dcc.Dropdown(
                        id="facet-col",
                        placeholder="Columnas",
                        clearable=True,
                    )
                ),
            ],
            md=3,
        ),
        dbc.Col(
            [
                dbc.Label("Filas"),
                dbc_dropdown(
                    dcc.Dropdown(
                        id="facet-row",
                        placeholder="Filas",
                        clearable=True,
                    )
                ),
            ],
            md=3,
        ),
    ],
)

RESULTS = dbc.Fade(
    dbc.Accordion(
        [
            dbc.AccordionItem(
                [html.Br(), CONTROLS, html.Br(), html.Div(id="chart-div")],
                title="Gráfico interactivo",
            ),
            dbc.AccordionItem(
                [html.Br(), html.Div(id="table-div")], title="Tabla de datos"
            ),
        ],
        flush=True,
    ),
    is_in=False,
    id="results-fade",
    class_name="px-md-5",
)

DICTIONARY = dbc.Fade(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Input(
                    placeholder="Ingresar término de búsqueda",
                    class_name="mb-3",
                    id="dictionary-search",
                ),
                md=6,
            )
        ),
        html.Div(id="dictionary-div"),
    ],
    is_in=False,
    id="dictionary-fade",
)

app.layout = html.Div(
    [
        NAVBAR,
        dbc.Container(
            [
                dbc.Offcanvas(
                    [
                        html.Img(
                            src="https://github.com/CPA-Analytics/pyech/raw/master/logo.png",
                            width="100%",
                            className="mb-3",
                        ),
                        dcc.Markdown(
                            """
                             PyECH es un procesador de la Encuesta Continua de Hogares del INE escrito en Python.
                             Esta app brinda acceso a un subset de la funcionalidad completa de la librería: calcular estadísticos resumen y cruzar variables.
                             """
                        ),
                        html.Br(),
                        html.H5("Seleccionar año de encuesta y ponderador"),
                        SURVEY_CHOICE,
                        html.P("🕑 Cargar cada encuesta puede llevar entre 20 y 40 segundos dependiendo del año.", className="text-muted mt-2"),
                        dcc.Loading(
                            html.Div(id="placeholder-1", hidden=True),
                            type="dot",
                            fullscreen=True,
                            style={"backgroundColor": "rgba(250, 250, 250, 0.5)"},
                        ),
                    ],
                    is_open=True,
                    id="offcanvas",
                    scrollable=True,
                ),
                dbc.Button(
                    ">> Seleccionar encuesta y ponderador",
                    id="open-offcanvas",
                    color="primary",
                    class_name="my-3",
                ),
                #dbc.Toast("📈 Encuesta cargada.", id="toast", color="success", duration=5000, dismissable=True,
                #            is_open=False),
                dcc.Loading(
                    html.Div(id="placeholder-2", hidden=True),
                    type="dot",
                    fullscreen=True,
                    style={"backgroundColor": "rgba(250, 250, 250, 0.5)"},
                ),
                dbc.Tabs(
                    [
                        dbc.Tab(
                            [SUMMARIZER, html.Br(), RESULTS],
                            label="Resumir y cruzar variables",
                        ),
                        dbc.Tab(DICTIONARY, label="Explorar diccionario de variables"),
                    ]
                ),
                html.Br(),
                dcc.Store(id="sum-data"),
            ],
            fluid=True,
        ),
    ],
    className="dbc",
)


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    Input("year", "value"),
    Input("weights", "value"),
    State("offcanvas", "is_open"),
)
def toggle_offcanvas(n, year, weights, is_open):
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id in ["year", "weights"] and year and weights:
        return False
    if n:
        return not is_open
    return is_open


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


survey = ECH()


@app.callback(
    Output("sumvar", "disabled"),
    Output("by", "disabled"),
    Output("aggfunc", "disabled"),
    Output("is-categorical", "disabled"),
    Output("household", "disabled"),
    Output("sumvar", "options"),
    Output("by", "options"),
    Output("open-offcanvas", "color"),
    Output("open-offcanvas", "children"),
    Output("placeholder-1", "children"),
    Output("placeholder-2", "children"),
    Output("sumvar", "value"),
    Output("by", "value"),
    Output("dictionary-div", "children"),
    Output("dictionary-fade", "is_in"),
    #Output("toast", "is_open"),
    Input("year", "value"),
    Input("weights", "value"),
)
def set_survey_year_and_weights_and_create_dictionary(year, weights):
    fully_loaded = False
    ctx = callback_context
    trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]
    if trigger_id == "year":
        survey.load(int(year), from_repo=True)
        if weights:
            survey.weights = weights
            fully_loaded = True
    elif trigger_id == "weights" and year:
        survey.weights = weights
        fully_loaded = True
    else:
        pass
    if fully_loaded:
        options = [{"label": survey.metadata.column_labels_and_names[i], "value": i} for i in survey.data.columns]
        dictionary = DataTable(
            data=survey.dictionary.to_dict("records"),
            columns=[{"name": i, "id": i} for i in survey.dictionary.columns],
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_size=50,
            id="dictionary-table",
        )
        return (
            False,
            False,
            False,
            False,
            False,
            options,
            options,
            "primary",
            f">> Año: {survey.data['anio'][0]} | Ponderador: {survey.weights}",
            0,
            0,
            None,
            None,
            dictionary,
            True,
            #True,
        )
    else:
        return (
            True,
            True,
            True,
            True,
            True,
            [],
            [],
            "secondary",
            ">> Seleccionar encuesta y ponderador",
            0,
            0,
            None,
            None,
            None,
            False,
            #False,
        )


@app.callback(
    Output("dictionary-table", "data"),
    Input("dictionary-search", "value"),
    prevent_initial_call=True,
)
def filter_dictionary(term):
    if hasattr(survey, "dictionary"):
        filtered = survey.search_dictionary(term)
        return filtered.to_dict("records")
    else:
        raise PreventUpdate


@app.callback(
    Output("sum-data", "data"),
    Output("results-fade", "is_in"),
    Input("sumvar", "value"),
    Input("by", "value"),
    Input("aggfunc", "value"),
    Input("is-categorical", "value"),
    Input("household", "value"),
    Input("weights", "value"),
)
def summarize(sumvar, by, aggfunc, is_categorical, household_level, weights):
    if sumvar:
        is_categorical = ast.literal_eval(is_categorical)
        household_level = ast.literal_eval(household_level)
        summarized = survey.summarize(
            sumvar,
            by,
            aggfunc=aggfunc,
            is_categorical=is_categorical,
            household_level=household_level,
        )
        summarized = summarized.reset_index()
        records = summarized.to_dict("records")
        return records, True
    else:
        return None, False


@app.callback(
    Output("x-axis", "value"),
    Output("color", "value"),
    Output("facet-col", "value"),
    Output("facet-row", "value"),
    Input("sum-data", "data"),
    Input("x-axis", "value"),
    Input("color", "value"),
    Input("facet-col", "value"),
    Input("facet-row", "value"),
    Input("sumvar", "value"),
)
def validate_chart_values(data, x_axis, color, facet_col, facet_row, sumvar):
    if not data:
        raise PreventUpdate
    data = pd.DataFrame.from_records(data, coerce_float=True, index="index")
    values = [
        x if x in data.columns else None for x in [x_axis, color, facet_col, facet_row]
    ]
    if "Recuento" in data.columns:
        values[0] = sumvar
    return values


@app.callback(
    Output("x-axis", "options"),
    Output("color", "options"),
    Output("facet-col", "options"),
    Output("facet-row", "options"),
    Input("by", "value"),
    Input("sum-data", "data"),
    Input("sumvar", "value"),
)
def set_chart_controls_options(by, data, sumvar):
    if not data:
        raise PreventUpdate
    data = pd.DataFrame.from_records(data, coerce_float=True, index="index")
    if by:
        options = [{"label": survey.metadata.column_labels_and_names[i], "value": i} for i in by]
    else:
        options = []
    if "Recuento" in data.columns:
        return [{"label": survey.metadata.column_labels_and_names[sumvar], "value": sumvar}], options, options, options
    else:
        return options, options, options, options


@app.callback(
    Output("table-div", "children"),
    Output("chart-div", "children"),
    Input("sum-data", "data"),
    Input("sumvar", "value"),
    Input("x-axis", "value"),
    Input("color", "value"),
    Input("facet-col", "value"),
    Input("facet-row", "value"),
    State("weights", "value"),
    State("year", "value"),
)
def create_table_and_chart(
    data, sumvar, x_axis, color, facet_col, facet_row, weights, year
):
    if not data:
        raise PreventUpdate
    if sumvar:
        data = pd.DataFrame.from_records(data, coerce_float=True, index="index")
        name_sumvar = survey.metadata.column_names_to_labels[sumvar]
        if "Recuento" in data.columns:
            plot = px.bar(
                data,
                x=x_axis,
                y="Recuento",
                color=color,
                facet_col=facet_col,
                facet_row=facet_row,
                barmode="group",
                color_discrete_sequence=px.colors.qualitative.Prism,
                color_continuous_scale=px.colors.sequential.thermal,
                template=template,
                title=f"{name_sumvar} ({year}, {weights})",
            )
        else:
            plot = px.bar(
                data,
                x=x_axis,
                y=sumvar,
                color=color,
                facet_col=facet_col,
                facet_row=facet_row,
                barmode="group",
                color_discrete_sequence=px.colors.qualitative.Prism,
                color_continuous_scale=px.colors.sequential.thermal,
                template=template,
                title=f"{name_sumvar} ({year}, {weights})",
            )
        dtypes = ["text" if i == "object" else "numeric" for i in data.dtypes]
        column_formats = [
            {
                "name": survey.metadata.column_names_to_labels[i],
                "id": i,
                "type": d,
                "format": Format(precision=4, scheme=Scheme.fixed, trim=Trim.yes).group(
                    True
                ),
            }
            if i != "Recuento"
            else {
                "name": "Recuento",
                "id": "Recuento",
                "type": "numeric",
                "format": Format(precision=4, scheme=Scheme.fixed, trim=Trim.yes).group(
                    True
                ),
            }
            for i, d in zip(data.columns, dtypes)
        ]
        table = DataTable(
            id="dash-table",
            data=data.to_dict("records"),
            columns=column_formats,
            sort_action="native",
            filter_action="native",
            page_action="native",
            page_size=50,
            export_format="csv",
        )
        return table, dcc.Graph(figure=plot, id="chart")
    else:
        return None, None


if __name__ == "__main__":
    app.run_server(debug=True, host="0.0.0.0", port=8080)
