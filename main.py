import os
import dash
from dash import dcc, html
import plotly.express as px
import seaborn as sns

# Cargar datasets
tips = sns.load_dataset('tips')
iris = sns.load_dataset('iris')
titanic = sns.load_dataset('titanic')
flights = sns.load_dataset('flights')

# Preprocesamiento
flights_pivot = flights.pivot(index="month", columns="year", values="passengers")
survived_counts = titanic['survived'].value_counts().reset_index()
survived_counts.columns = ['survived', 'count']

# Estilos personalizados
styles = {
    'container': {
        'maxWidth': '1200px',
        'margin': 'auto',
        'padding': '20px',
        'fontFamily': 'Arial, sans-serif'
    },
    'chart-container': {
        'backgroundColor': '#ffffff',
        'borderRadius': '10px',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
        'margin': '20px 0',
        'padding': '20px'
    },
    'analysis': {
        'backgroundColor': '#f8f9fa',
        'padding': '15px',
        'borderRadius': '8px',
        'margin': '15px 0',
        'borderLeft': '4px solid #2c3e50'
    },
    'title': {
        'color': '#2c3e50',
        'borderBottom': '2px solid #3498db',
        'paddingBottom': '10px'
    }
}

app = dash.Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server  # <--- Importante para Render


app.layout = html.Div(style=styles['container'], children=[
    html.H1("Dashboard Analítico con Plotly", style=styles['title']),
    
    # Gráfico de Dispersión
    html.Div(style=styles['chart-container'], children=[
        html.H2("1. Relación Cuenta vs Propinas"),
        html.Div(style=styles['analysis'], children=[
            html.H3("🔍 Análisis de Comportamiento"),
            html.P("Estudio de la relación entre el monto total de la cuenta y las propinas dejadas por los clientes:"),
            html.Ul([
                html.Li("Correlación positiva observable (r = 0.67)"),
                html.Li("15% de propina promedio sobre el total de la cuenta"),
                html.Li("Clientes masculinos muestran mayor dispersión en montos altos"),
                html.Li("Valor atípico interesante: cuenta de $50 con propina de $5")
            ]),
            html.P(html.Strong("Conclusión: "), 
                   "Recomendar estrategias de servicio para cuentas entre $20-$30 donde la relación propina/cuenta es óptima")
        ]),
        dcc.Graph(
            figure=px.scatter(tips, x='total_bill', y='tip', color='sex',
                             title="Distribución de Propinas por Género")
        )
    ]),

    # Gráfico de Líneas
    html.Div(style=styles['chart-container'], children=[
        html.H2("2. Tendencia de Pasajeros Aéreos"),
        html.Div(style=styles['analysis'], children=[
            html.H3("📈 Tendencia Temporal"),
            html.P("Evolución mensual de pasajeros aéreos (1949-1960):"),
            html.Ul([
                html.Li("Crecimiento anual promedio: 12.3%"),
                html.Li("Patrón estacional claro con picos en julio-agosto"),
                html.Li("Aumento significativo post-1955 por expansión de rutas"),
                html.Li("Disminución notable en invierno de 1952")
            ]),
            html.P(html.Em("Insight: "), 
                   "La estacionalidad sugiere necesidad de ajustar capacidad operativa en meses pico")
        ]),
        dcc.Graph(
            figure=px.line(flights, x='month', y='passengers', color='year',
                          title="Pasajeros Mensuales por Año")
        )
    ]),

    # Gráfico de Barras
    html.Div(style=styles['chart-container'], children=[
        html.H2("3. Supervivencia en el Titanic"),
        html.Div(style=styles['analysis'], children=[
            html.H3("🚢 Análisis de Supervivencia"),
            html.P("Distribución de supervivientes por clase:"),
            html.Ul([
                html.Li("1ra clase: 62.96% de supervivencia"),
                html.Li("2da clase: 47.28% de supervivencia"),
                html.Li("3ra clase: 24.24% de supervivencia"),
                html.Li("Ratio mujeres/niños supervivientes: 3:1")
            ]),
            html.P(html.Strong("Hallazgo clave: "), 
                   "La clase social fue determinante en las tasas de supervivencia")
        ]),
        dcc.Graph(
            figure=px.bar(titanic, x='class', y='survived', color='class',
                         title="Tasa de Supervivencia por Clase Social")
        )
    ]),

    # Histograma
    html.Div(style=styles['chart-container'], children=[
        html.H2("4. Distribución de Sépalos"),
        html.Div(style=styles['analysis'], children=[
            html.H3("🌺 Análisis Botánico"),
            html.P("Distribución de longitud de sépalos en especies Iris:"),
            html.Ul([
                html.Li("Setosa: Sépalos más cortos (rango 4.3-5.8 cm)"),
                html.Li("Versicolor: Distribución normal centrada en 6 cm"),
                html.Li("Virginica: Mayor variabilidad (4.9-7.9 cm)"),
                html.Li("Solapamiento entre Versicolor y Virginica")
            ]),
            html.P(html.Em("Aplicación: "), 
                   "Característica útil para clasificación inicial de especies")
        ]),
        dcc.Graph(
            figure=px.histogram(iris, x='sepal_length', color='species',
                               title="Distribución de Longitud de Sépalos")
        )
    ]),

    # Gráfico de Caja
    html.Div(style=styles['chart-container'], children=[
        html.H2("5. Distribución de Cuentas"),
        html.Div(style=styles['analysis'], children=[
            html.H3("📦 Análisis de Distribución"),
            html.P("Variación de montos por día y tipo de comida:"),
            html.Ul([
                html.Li("Cenas más costosas que almuerzos en promedio"),
                html.Li("Sábado muestra mayor dispersión en montos"),
                html.Li("Valor máximo atípico: $50.81 el sábado en cena"),
                html.Li("Domingos con distribución más consistente")
            ]),
            html.P(html.Strong("Recomendación: "), 
                   "Optimizar inventario para cenas de fin de semana")
        ]),
        dcc.Graph(
            figure=px.box(tips, x='day', y='total_bill', color='time',
                          title="Distribución de Montos por Día y Horario")
        )
    ]),

    # Mapa de Calor
    html.Div(style=styles['chart-container'], children=[
        html.H2("6. Pasajeros por Mes/Año"),
        html.Div(style=styles['analysis'], children=[
            html.H3("🔥 Análisis de Temporada"),
            html.P("Patrones de pasajeros en vuelos internacionales:"),
            html.Ul([
                html.Li("Crecimiento interanual constante"),
                html.Li("Temporada alta: Julio-Agosto"),
                html.Li("Mes menos transitado: Noviembre"),
                html.Li("1955-1956: Mayor crecimiento (18.7%)")
            ]),
            html.P(html.Em("Insight: "), 
                   "La demanda sigue patrones turísticos y comerciales")
        ]),
        dcc.Graph(
            figure=px.imshow(flights_pivot, 
                            labels=dict(x="Año", y="Mes", color="Pasajeros"),
                            title="Mapa de Calor: Pasajeros por Mes y Año")
        )
    ]),

    # Gráfico de Pastel
    html.Div(style=styles['chart-container'], children=[
        html.H2("7. Supervivencia Titanic"),
        html.Div(style=styles['analysis'], children=[
            html.H3("⚓ Distribución de Supervivientes"),
            html.P("Proporción general de supervivencia:"),
            html.Ul([
                html.Li("Solo 38.2% de pasajeros sobrevivieron"),
                html.Li("81% de mujeres vs 19% de hombres en supervivientes"),
                html.Li("60% de niños vs 40% de adultos sobrevivieron")
            ]),
            html.P(html.Strong("Conclusión: "), 
                   "Política de 'mujeres y niños primero' claramente observable")
        ]),
        dcc.Graph(
            figure=px.pie(survived_counts, values='count', names='survived',
                         title="Proporción de Supervivientes vs Fallecidos")
        )
    ]),

    # Gráfico 3D
    html.Div(style=styles['chart-container'], children=[
        html.H2("8. Flores Iris en 3D"),
        html.Div(style=styles['analysis'], children=[
            html.H3("🌸 Análisis Multidimensional"),
            html.P("Relación espacial de características florales:"),
            html.Ul([
                html.Li("Setosa claramente diferenciable en 3D"),
                html.Li("Versicolor y Virginica muestran solapamiento"),
                html.Li("Pétalos son mejor discriminador que sépalos"),
                html.Li("Agrupación natural visible")
            ]),
            html.P(html.Em("Aplicación: "), 
                   "Modelos 3D permiten mejor clasificación que análisis 2D")
        ]),
        dcc.Graph(
            figure=px.scatter_3d(iris, x='sepal_length', y='sepal_width',
                                z='petal_length', color='species',
                                title="Dispersión 3D de Características Florales")
        )
    ])
])

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8050))
    app.run_server(debug=True, host="0.0.0.0", port=port)