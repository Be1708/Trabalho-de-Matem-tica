import streamlit as st
import plotly.graph_objects as go
import ezdxf
import io
import random

st.set_page_config(page_title="Plano Cartesiano Interativo", layout="wide")
st.sidebar.title("Ferramentas")
st.sidebar.markdown("Adicione coordenadas, finalize formas ou carregue um arquivo DXF.")

# Sessão
if "formas" not in st.session_state:
    st.session_state.formas = []
if "pontos" not in st.session_state:
    st.session_state.pontos = []
if "cores" not in st.session_state:
    st.session_state.cores = []

# Coordenadas manuais
x = st.sidebar.number_input("X", step=1.0)
y = st.sidebar.number_input("Y", step=1.0)
if st.sidebar.button("Adicionar ponto"):
    st.session_state.pontos.append((x, y))

if st.sidebar.button("Finalizar forma"):
    if st.session_state.pontos:
        st.session_state.formas.append(st.session_state.pontos.copy())
        st.session_state.cores.append(f"rgb({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)})")
        st.session_state.pontos = []

# Upload DXF
uploaded_file = st.sidebar.file_uploader("Upload DXF", type=["dxf"])
if uploaded_file is not None:
    try:
        # Criar um arquivo temporário para ezdxf.readfile
        with open("temp_file.dxf", "wb") as f:
            f.write(uploaded_file.read())
        doc = ezdxf.readfile("temp_file.dxf")
        msp = doc.modelspace()

        # Ler linhas do DXF
        pontos_dxf = []
        for e in msp:
            if e.dxftype() == "LINE":
                x1, y1, *_ = e.dxf.start
                x2, y2, *_ = e.dxf.end
                pontos_dxf.append(((x1, y1), (x2, y2)))

        if pontos_dxf:
            cor_dxf = f"rgb({random.randint(0,255)},{random.randint(0,255)},{random.randint(0,255)})"
            for (p1, p2) in pontos_dxf:
                st.session_state.formas.append([p1, p2])
                st.session_state.cores.append(cor_dxf)

        st.sidebar.success("Arquivo DXF carregado com sucesso!")

    except Exception as e:
        st.sidebar.error(f"Erro ao ler DXF: {e}")

# --- Criar gráfico ---
fig = go.Figure()

# Eixos estilo plano cartesiano
fig.add_trace(go.Scatter(x=[-20, 20], y=[0,0], mode="lines", line=dict(color="black", width=2), showlegend=False))
fig.add_trace(go.Scatter(x=[0,0], y=[-20, 20], mode="lines", line=dict(color="black", width=2), showlegend=False))

# Desenhar formas
for forma, cor in zip(st.session_state.formas, st.session_state.cores):
    xs, ys = zip(*forma)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color=cor, width=2)))

# Forma atual
if st.session_state.pontos:
    xs, ys = zip(*st.session_state.pontos)
    fig.add_trace(go.Scatter(x=xs, y=ys, mode="lines+markers", line=dict(color="black", dash="dot")))

fig.update_layout(
    width=900, height=700,
    xaxis=dict(title="Eixo X", zeroline=True, showgrid=True, mirror=True, showline=True),
    yaxis=dict(title="Eixo Y", zeroline=True, showgrid=True, mirror=True, showline=True, scaleanchor="x", scaleratio=1),
    plot_bgcolor="white"
)

st.plotly_chart(fig, use_container_width=True)
