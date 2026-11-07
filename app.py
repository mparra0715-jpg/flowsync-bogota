import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="FlowSync Bogotá",
    page_icon="🚦",
    layout="wide"
)

st.title("🚦 FlowSync Bogotá")
st.subheader("Sistema de simulación y alerta preventiva de tráfico")

st.write(
    "Prototipo de monitoreo conceptual para anticipar "
    "la propagación de frenadas y reducir los trancones fantasma."
)

st.divider()

st.header("1. Configuración del escenario")

col1, col2 = st.columns(2)

with col1:
    frenado = st.slider(
        "Intensidad del frenado (%)", 0, 100, 60
    )

with col2:
    densidad = st.slider(
        "Densidad vehicular (%)", 0, 100, 70
    )

intervencion = st.toggle(
    "Activar alerta preventiva FlowSync",
    value=True
)

if st.button("▶ EJECUTAR SIMULACIÓN", type="primary"):

    severidad = round(frenado * 0.7 + densidad * 0.3)

    velocidad_inicial = 60
    velocidades_sin_alerta = []
    velocidades_con_alerta = []

    velocidad_sin = velocidad_inicial
    velocidad_con = velocidad_inicial

    for tiempo in range(11):

        if tiempo == 0:
            velocidad_sin = velocidad_inicial
            velocidad_con = velocidad_inicial
        else:
            impacto = (severidad / 100) * 22

            # Propagación del frenado sin intervención
            velocidad_sin -= impacto * (
                0.20 + densidad / 250
            )

            # Respuesta con alerta preventiva
            if intervencion:
                velocidad_con -= impacto * (
                    0.08 + densidad / 500
                )
            else:
                velocidad_con = velocidad_sin

        velocidad_sin = max(5, velocidad_sin)
        velocidad_con = max(5, velocidad_con)

        velocidades_sin_alerta.append(
            round(velocidad_sin, 1)
        )

        velocidades_con_alerta.append(
            round(velocidad_con, 1)
        )

    if severidad >= 70:
        riesgo = "ALTO"
    elif severidad >= 40:
        riesgo = "MEDIO"
    else:
        riesgo = "BAJO"

    afectados = round(
        severidad * 0.8 +
        densidad * 0.2
    )

    if intervencion:
        mejora = round(
            velocidades_con_alerta[-1] -
            velocidades_sin_alerta[-1], 1
        )
    else:
        mejora = 0

    st.session_state["resultados"] = {
        "severidad": severidad,
        "riesgo": riesgo,
        "afectados": afectados,
        "mejora": mejora,
        "sin_alerta": velocidades_sin_alerta,
        "con_alerta": velocidades_con_alerta
    }

if "resultados" in st.session_state:

    r = st.session_state["resultados"]

    st.divider()
    st.header("2. Resultados de la simulación")

    a, b, c = st.columns(3)

    a.metric(
        "Índice de congestión",
        f'{r["severidad"]}/100'
    )

    b.metric(
        "Vehículos potencialmente afectados",
        r["afectados"]
    )

    c.metric(
        "Velocidad recuperada",
        f'{r["mejora"]} km/h'
    )

    st.progress(r["severidad"] / 100)

    if r["riesgo"] == "ALTO":
        st.error("RIESGO ALTO: posible propagación de congestión.")
    elif r["riesgo"] == "MEDIO":
        st.warning("RIESGO MEDIO: condiciones de tráfico inestables.")
    else:
        st.success("RIESGO BAJO: circulación relativamente estable.")

    st.divider()
    st.header("3. Evolución del tráfico")

    datos = pd.DataFrame({
        "Momento": list(range(11)),
        "Sin alerta FlowSync": r["sin_alerta"],
        "Con alerta FlowSync": r["con_alerta"]
    }).set_index("Momento")

    st.line_chart(datos)

    st.caption(
        "Velocidad estimada (km/h) durante 10 intervalos "
        "de simulación. Modelo conceptual."
    )

    st.header("4. Interpretación")

    st.write(
        f'La intensidad del frenado fue de {frenado}% '
        f'y la densidad vehicular de {densidad}%.'
    )

    if intervencion:
        st.success(
            "FlowSync activa una estrategia preventiva "
            "de regulación de velocidad. La comparación "
            "muestra el efecto estimado de la intervención."
        )
    else:
        st.info(
            "Simulación sin intervención preventiva. "
            "Se observa el comportamiento estimado "
            "del tráfico sin alertas."
        )

    st.info(
        "IMPORTANTE: Los resultados son ilustrativos. "
        "No representan datos reales de Waze, Google Maps "
        "ni sensores o drones."
    )

st.divider()

st.caption(
    "FlowSync Bogotá | Prototipo académico de movilidad sostenible"
)
