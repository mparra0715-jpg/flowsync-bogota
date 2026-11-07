import streamlit as st

st.set_page_config(
    page_title="FlowSync Bogotá",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 FlowSync Bogotá")
st.subheader("Simulador inteligente de tráfico urbano")

st.write(
    "Simula cómo una frenada repentina puede generar "
    "un trancón fantasma y cómo una alerta preventiva "
    "puede ayudar a reducir su propagación."
)

st.divider()

col1, col2 = st.columns(2)

with col1:
    frenado = st.slider(
        "Intensidad del frenado (%)",
        0, 100, 60
    )

with col2:
    densidad = st.slider(
        "Densidad vehicular (%)",
        0, 100, 70
    )

if st.button("▶ Ejecutar simulación", type="primary"):

    severidad = round(
        frenado * 0.7 + densidad * 0.3
    )

    if severidad >= 70:
        riesgo = "ALTO"
        recomendacion = (
            "Activar alerta preventiva. "
            "Reducir progresivamente la velocidad "
            "y aumentar la distancia de seguridad."
        )
    elif severidad >= 40:
        riesgo = "MEDIO"
        recomendacion = (
            "Advertir a los conductores y "
            "recomendar velocidad preventiva."
        )
    else:
        riesgo = "BAJO"
        recomendacion = (
            "Mantener velocidad estable y "
            "monitorear las condiciones del tráfico."
        )

    afectados = round(severidad * 2)
    velocidad = max(10, round(60 - severidad * 0.4))

    st.divider()
    st.header("Resultados de la simulación")

    a, b, c = st.columns(3)

    a.metric("Índice de congestión", f"{severidad}/100")
    b.metric("Vehículos potencialmente afectados",
             afectados)
    c.metric("Velocidad preventiva sugerida",
             f"{velocidad} km/h")

    st.progress(severidad / 100)

    st.subheader(f"Nivel de riesgo: {riesgo}")

    if riesgo == "ALTO":
        st.error(recomendacion)
    elif riesgo == "MEDIO":
        st.warning(recomendacion)
    else:
        st.success(recomendacion)

    st.info(
        "Simulación conceptual: los resultados son "
        "estimaciones ilustrativas, no mediciones reales "
        "de Waze, Google Maps o drones."
    )

st.divider()

st.caption(
    "FlowSync Bogotá | Prototipo académico de movilidad sostenible"
)
