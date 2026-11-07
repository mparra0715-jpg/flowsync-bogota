import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="FlowSync Bogotá", page_icon="🚦", layout="wide")

st.markdown("""
<style>
.block-container {padding-top: 1.5rem; padding-bottom: 2rem;}
[data-testid="stMetric"] {background: #f4f7fb; padding: 14px; border-radius: 12px;}
</style>
""", unsafe_allow_html=True)

st.title("🚦 FlowSync Bogotá")
st.caption("Centro demostrativo de monitoreo y prevención de congestiones fantasma")
st.info("MVP académico: los datos y resultados son simulados. No está conectado a cámaras, GPS, Waze ni tráfico real.")

with st.sidebar:
    st.header("Parámetros de simulación")
    velocidad = st.slider("Velocidad inicial (km/h)", 30, 120, 80, 5)
    densidad = st.slider("Densidad vehicular (%)", 10, 100, 50, 5)
    frenado = st.slider("Intensidad del frenado (%)", 10, 90, 40, 5)
    numero_vehiculos = st.slider("Vehículos en el tramo", 5, 30, 10, 1)
    st.divider()
    st.subheader("Supuestos ambientales")
    consumo_ralenti = st.number_input("Consumo en ralentí (L/h por vehículo)", min_value=0.1, max_value=5.0, value=0.8, step=0.1)
    minutos_reducidos = st.number_input("Minutos de congestión que se supone podrían evitarse", min_value=0.0, max_value=60.0, value=3.0, step=0.5)
    factor_emision = st.number_input("Factor de emisión (kg CO₂/L)", min_value=1.0, max_value=5.0, value=2.3, step=0.1)

if st.button("▶ Ejecutar simulación", type="primary", use_container_width=True):
    st.session_state["run_sim"] = True

if "run_sim" not in st.session_state:
    st.session_state["run_sim"] = False

# Cálculo ilustrativo de severidad y propagación; deberá calibrarse con datos reales.
severidad = min(100, round(0.7 * frenado + 0.3 * densidad))
velocidad_posterior = max(0, round(velocidad * (1 - frenado / 100)))
vehiculos_afectados = min(numero_vehiculos, max(0, round(numero_vehiculos * severidad / 100)))

if severidad >= 65:
    riesgo = "ALTO"
    color_alerta = "🔴"
    mensaje = "Señal de frenado intenso. El escenario simulado presenta alta posibilidad de propagación."
    recomendacion = "Advertir con anticipación, reducir progresivamente la velocidad y conservar distancia de seguridad."
elif severidad >= 40:
    riesgo = "MEDIO"
    color_alerta = "🟠"
    mensaje = "Se identifica una desaceleración que podría transmitirse a los vehículos siguientes."
    recomendacion = "Monitorear el tramo y recomendar una reducción gradual de velocidad."
else:
    riesgo = "BAJO"
    color_alerta = "🟢"
    mensaje = "La desaceleración simulada es moderada. No se identifica un riesgo alto de propagación."
    recomendacion = "Mantener distancia de seguridad y continuar monitoreando el flujo."

st.subheader("Panel de indicadores")
c1, c2, c3, c4 = st.columns(4)
c1.metric("Velocidad inicial", f"{velocidad} km/h")
c2.metric("Velocidad posterior estimada", f"{velocidad_posterior} km/h")
c3.metric("Vehículos potencialmente afectados", f"{vehiculos_afectados} / {numero_vehiculos}")
c4.metric("Nivel de riesgo", riesgo)

left, right = st.columns([1.6, 1])
with left:
    st.subheader("Representación del tramo vial")
    # Representación esquemática: el color no corresponde a mediciones reales.
    rows = []
    for i in range(numero_vehiculos):
        afectado = i < vehiculos_afectados
        estado = "Frenado crítico" if afectado and severidad >= 65 else ("Desaceleración" if afectado else "Flujo normal")
        rows.append({"Vehículo": f"V{i+1}", "Posición": i + 1, "Carril": 1 if i < (numero_vehiculos + 1)//2 else 2, "Estado": estado})
    df = pd.DataFrame(rows)
    palette = {"Flujo normal": "#2387c9", "Desaceleración": "#e6a23c", "Frenado crítico": "#d9534f"}
    fig = px.scatter(
        df, x="Posición", y="Carril", color="Estado", text="Vehículo",
        color_discrete_map=palette, category_orders={"Estado": ["Flujo normal", "Desaceleración", "Frenado crítico"]}
    )
    fig.update_traces(marker=dict(size=22, symbol="square"), textposition="top center")
    fig.update_layout(
        height=300, xaxis_title="Posición relativa de los vehículos →",
        yaxis=dict(tickvals=[1, 2], ticktext=["Carril 1", "Carril 2"], range=[0.5, 2.5]),
        plot_bgcolor="#343a40", paper_bgcolor="rgba(0,0,0,0)",
        font_color="#ffffff", legend_title_text="", margin=dict(l=10, r=10, t=25, b=10)
    )
    fig.update_xaxes(showgrid=False, color="#ffffff")
    fig.update_yaxes(showgrid=True, gridcolor="#777777", color="#ffffff")
    st.plotly_chart(fig, use_container_width=True)
    st.caption("Esquema conceptual de vehículos; no es un mapa ni una medición de una vía real.")

with right:
    st.subheader("Alerta FlowSync")
    st.markdown(f"### {color_alerta} Riesgo {riesgo}")
    st.write(mensaje)
    st.warning(recomendacion) if riesgo == "ALTO" else st.info(recomendacion) if riesgo == "MEDIO" else st.success(recomendacion)

st.divider()
st.subheader("Estimación ambiental y económica")
litros_potenciales = vehiculos_afectados * consumo_ralenti * (minutos_reducidos / 60)
co2_potencial = litros_potenciales * factor_emision
a = st.columns(3)
a[0].metric("Combustible potencialmente ahorrado", f"{litros_potenciales:.3f} L")
a[1].metric("CO₂ potencialmente evitado", f"{co2_potencial:.3f} kg")
a[2].metric("Vehículos incluidos en el cálculo", f"{vehiculos_afectados}")

st.caption(
    "Estas cifras son estimaciones de escenario basadas en los supuestos editables de la barra lateral. "
    "No constituyen ahorros medidos ni prueban que la alerta reduzca efectivamente la congestión. "
    "Para validarlas se requieren datos reales, comparación de escenarios y factores de emisión documentados."
)

with st.expander("Ver datos de la simulación"):
    st.dataframe(df, use_container_width=True, hide_index=True)

st.markdown("---")
st.caption("FlowSync Bogotá · Prototipo académico de prueba · Versión 0.1")
