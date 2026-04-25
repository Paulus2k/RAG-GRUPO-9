import streamlit as st
import os
import requests

st.set_page_config(
    page_title="Asistente Académico",
    page_icon="🎓",
    layout="wide"
)

CARPETA_DOCS = "documentos"
BACKEND_URL = "https://unpasteurized-metronomically-konnor.ngrok-free.dev"

with st.sidebar:
    st.markdown("## 🎓 Asistente Académico")
    st.caption("Proyecto RAG — Curso de IA")
    st.divider()

    st.markdown("**📂 Documentos del curso**")
    archivos = os.listdir(CARPETA_DOCS) if os.path.exists(CARPETA_DOCS) else []
    if archivos:
        for archivo in archivos:
            ruta = os.path.join(CARPETA_DOCS, archivo)
            with open(ruta, "rb") as f:
                st.download_button(
                    label=f"📄 {archivo}",
                    data=f,
                    file_name=archivo,
                    mime="application/pdf",
                    use_container_width=True
                )
    else:
        st.caption("Sin documentos cargados aún")

    st.divider()
    if st.button("🗑️ Limpiar conversación", use_container_width=True):
        st.session_state.mensajes = []
        st.rerun()

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

st.title("🎓 Asistente Académico")
st.caption("Responde únicamente con base en el material del curso")
st.divider()

if len(st.session_state.mensajes) == 0:
    st.markdown(
        """
        <div style="text-align:center; padding: 60px 20px; opacity: 0.3;">
            <p style="font-size:48px;">🎓</p>
            <p style="font-size:20px; font-weight:500;">¿En qué te puedo ayudar?</p>
            <p style="font-size:14px;">1. Escribe tu pregunta abajo</p>
            <p style="font-size:14px;">2. El sistema busca en los documentos del curso</p>
            <p style="font-size:14px;">3. Te responde con evidencia real</p>
        </div>
        """,
        unsafe_allow_html=True
    )

for mensaje in st.session_state.mensajes:
    with st.chat_message(mensaje["rol"]):
        st.write(mensaje["contenido"])
        if mensaje["rol"] == "assistant" and "fragmentos" in mensaje:
            if mensaje["fragmentos"]:
                st.divider()
                st.markdown("**📎 Fuentes usadas:**")
                fuentes_html = ""
                for fuente in mensaje["fuentes"]:
                    fuentes_html += f'<span style="background-color:#1a472a; color:#7dcea0; padding:4px 12px; border-radius:20px; font-size:12px; margin-right:6px; display:inline-block; margin-bottom:6px;">📄 {fuente}</span>'
                st.markdown(fuentes_html, unsafe_allow_html=True)

                st.markdown("**🔍 Fragmentos recuperados:**")
                for frag in mensaje["fragmentos"]:
                    st.markdown(
                        f"""
                        <div style="border-left: 3px solid #4a90d9; padding: 10px 16px; margin: 8px 0;
                        background-color: #1a2332; border-radius: 0 8px 8px 0;">
                            <p style="margin:0; font-size:13px; color:#a8c4e0;">"{frag['texto']}"</p>
                            <p style="margin:4px 0 0; font-size:11px; color:#5a7a9a;">— {frag['fuente']}</p>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

pregunta = st.chat_input("Escribe tu pregunta aquí...")

if pregunta:
    with st.chat_message("user"):
        st.write(pregunta)
    st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

    with st.spinner("Buscando en los documentos..."):
        try:
            respuesta = requests.post(
                f"{BACKEND_URL}/ask",
                json={"question": pregunta, "top_k": 3},
                headers={"ngrok-skip-browser-warning": "true"},
                timeout=30
            )
            resultado = respuesta.json()

            fragmentos_raw = resultado.get("fragmentos", [])
            fuentes_raw = resultado.get("fuentes", [])

            fragmentos = []
            for i, frag in enumerate(fragmentos_raw):
                fuente_info = fuentes_raw[i] if i < len(fuentes_raw) else {}
                nombre_fuente = fuente_info.get("archivo") or fuente_info.get("chunk_id", "Documento")
                fragmentos.append({
                    "texto": frag.get("texto", ""),
                    "fuente": nombre_fuente
                })

            fuentes = list(set([f["fuente"] for f in fragmentos]))

            datos = {
                "respuesta": resultado.get("respuesta", "Sin respuesta"),
                "fragmentos": fragmentos,
                "fuentes": fuentes
            }

        except Exception as e:
            st.error(f"Error: {e}")
            datos = {
                "respuesta": "Error conectando con el backend.",
                "fragmentos": [],
                "fuentes": []
            }

    with st.chat_message("assistant"):
        if not datos["fragmentos"]:
            st.warning("⚠️ No tengo evidencia suficiente en los documentos recuperados.")
        else:
            st.write(datos["respuesta"])
            st.divider()

            st.markdown("**📎 Fuentes usadas:**")
            fuentes_html = ""
            for fuente in datos["fuentes"]:
                fuentes_html += f'<span style="background-color:#1a472a; color:#7dcea0; padding:4px 12px; border-radius:20px; font-size:12px; margin-right:6px; display:inline-block; margin-bottom:6px;">📄 {fuente}</span>'
            st.markdown(fuentes_html, unsafe_allow_html=True)

            st.markdown("**🔍 Fragmentos recuperados:**")
            for frag in datos["fragmentos"]:
                st.markdown(
                    f"""
                    <div style="border-left: 3px solid #4a90d9; padding: 10px 16px; margin: 8px 0;
                    background-color: #1a2332; border-radius: 0 8px 8px 0;">
                        <p style="margin:0; font-size:13px; color:#a8c4e0;">"{frag['texto']}"</p>
                        <p style="margin:4px 0 0; font-size:11px; color:#5a7a9a;">— {frag['fuente']}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

    st.session_state.mensajes.append({
        "rol": "assistant",
        "contenido": datos["respuesta"],
        "fragmentos": datos["fragmentos"],
        "fuentes": datos["fuentes"]
    })