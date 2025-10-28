import streamlit as st
import plotly.graph_objects as go
import ezdxf
import random
import time

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
        st.session_state.cores.append(f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})")
        st.session_state.pontos = []

# Upload DXF
uploaded_file = st.sidebar.file_uploader("Upload DXF", type=["dxf"])
if uploaded_file is not None:
    try:
        with open("temp_file.dxf", "wb") as f:
            f.write(uploaded_file.read())
        doc = ezdxf.readfile("temp_file.dxf")
        msp = doc.modelspace()

        linhas = []
        min_x = min_y = float("inf")
        max_x = max_y = float("-inf")

        for e in msp:
            tipo = e.dxftype()
            if tipo == "LINE":
                x1, y1, *_ = e.dxf.start
                x2, y2, *_ = e.dxf.end
                linhas.append([(x1, y1), (x2, y2)])
                min_x, max_x = min(min_x, x1, x2), max(max_x, x1, x2)
                min_y, max_y = min(min_y, y1, y2), max(max_y, y1, y2)

            elif tipo in ["LWPOLYLINE", "POLYLINE"]:
                pontos = []
                for v in e:
                    if hasattr(v, "dxf"):
                        x, y = v.dxf.location.x, v.dxf.location.y
                    else:
                        x, y = v[0], v[1]
                    pontos.append((x, y))
                    min_x, max_x = min(min_x, x), max(max_x, x)
                    min_y, max_y = min(min_y, y), max(max_y, y)
                if len(pontos) > 1:
                    linhas.append(pontos)

        if linhas:
            scale = max(max_x - min_x, max_y - min_y) / 18
            if scale == 0:
                scale = 1
            dx = (max_x + min_x) / 2
            dy = (max_y + min_y) / 2
            cor_dxf = f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"

            for pts in linhas:
                pts_scaled = [((px - dx) / scale, (py - dy) / scale) for px, py in pts]
                st.session_state.formas.append(pts_scaled)
                st.session_state.cores.append(cor_dxf)

            st.sidebar.success(f"DXF carregado e {len(linhas)} entidades desenhadas!")
        else:
            st.sidebar.warning("Nenhuma linha ou polilinha encontrada no DXF.")

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

grafico = st.plotly_chart(fig, use_container_width=True)

# --- Botão Cortar ---
if st.sidebar.button("Cortar"):
    if not st.session_state.formas:
        st.sidebar.warning("Não há formas para cortar.")
    else:
        # Percorre cada linha
        for forma in st.session_state.formas:
            for x, y in forma:
                # Desenha a forma original
                fig2 = fig
                # Adiciona ponto vermelho simulando cortadora
                fig2.add_trace(go.Scatter(x=[x], y=[y], mode="markers", marker=dict(color="red", size=12), name="Cortando"))
                grafico.plotly_chart(fig2, use_container_width=True)
                time.sleep(0.05)  # Ajusta velocidade do "corte"
