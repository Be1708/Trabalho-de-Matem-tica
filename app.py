import streamlit as st
import plotly.graph_objects as go
import ezdxf
import io
import random

st.set_page_config(page_title="Plano Cartesiano Interativo", layout="wide")

# --- Barra lateral ---
st.sidebar.title("Ferramentas")
st.sidebar.markdown("Adicione coordenadas, finalize formas ou carregue um arquivo DXF.")

# --- Variáveis de sessão ---
if "formas" not in st.session_state:
    st.session_state.formas = []
if "pontos" not in st.session_state:
    st.session_state.pontos = []
if "cores" not in st.session_state:
    st.session_state.cores = []

# --- Entrada de coordenadas ---
st.sidebar.subheader("Adicionar coordenada manual")
x = st.sidebar.number_input("X", value=0.0, step=1.0)
y = st.sidebar.number_input("Y", value=0.0, step=1.0)
adicionar = st.sidebar.button("Adicionar ponto")
finalizar = st.sidebar.button("Finalizar forma")

# --- Upload de DXF ---
st.sidebar.subheader("Upload de arquivo DXF")
uploaded_file = st.sidebar.file_uploader("Escolha um arquivo DXF", type=["dxf"])

# --- Adiciona ponto manual ---
if adicionar:
    st.session_state.pontos.append((x, y))

# --- Finaliza a forma atual ---
if finalizar and st.session_state.pontos:
    st.session_state.formas.append(st.session_state.pontos.copy())
    st.session_state.cores.append(f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})")
    st.session_state.pontos = []

# --- Lê o DXF (se enviado) ---
if uploaded_file is not None:
    try:
        dxf_data = uploaded_file.read()
        doc = ezdxf.read(stream=io.BytesIO(dxf_data))
        msp = doc.modelspace()

        pontos_dxf = []
        for e in msp:
            if e.dxftype() == "LINE":
                x1, y1, _, _ = e.dxf.start
                x2, y2, _, _ = e.dxf.end
                pontos_dxf.append(((x1, y1), (x2, y2)))

        if pontos_dxf:
            cor_dxf = f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"
            for (p1, p2) in pontos_dxf:
                st.session_state.formas.append([p1, p2])
                st.session_state.cores.append(cor_dxf)
        st.sidebar.success("Arquivo DXF carregado e desenhado com sucesso!")

    except Exception as e:
        st.sidebar.error(f"Erro ao ler o arquivo DXF: {e}")

# --- Cria o gráfico ---
fig = go.Figure()

# Eixos e aparência de plano cartesiano
fig.update_layout(
    xaxis=dict(
        title="Eixo X",
        zeroline=True,
        showgrid=True,
        mirror=True,
        showline=True,
        zerolinewidth=2,
        zerolinecolor="black"
    ),
    yaxis=dict(
        title="Eixo Y",
        zeroline=True,
        showgrid=True,
        mirror=True,
        showline=True,
        zerolinewidth=2,
        zerolinecolor="black",
        scaleanchor="x",
        scaleratio=1
    ),
    plot_bgcolor="white",
    width=900,
    height=700,
    margin=dict(l=20, r=20, t=20, b=20)
)

# Desenha as formas finalizadas
for forma, cor in zip(st.session_state.formas, st.session_state.cores):
    xs, ys = zip(*forma)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color=cor, width=2), name="Forma"))

# Desenha a forma atual (ainda sendo feita)
if st.session_state.pontos:
    xs, ys = zip(*st.session_state.pontos)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color="black", dash="dot"), name="Atual"))

# --- Mostra o gráfico ---
st.plotly_chart(fig, use_container_width=True)
