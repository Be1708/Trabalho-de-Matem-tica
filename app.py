import streamlit as st
import plotly.graph_objects as go
import random

st.set_page_config(page_title="Plano Cartesiano Interativo", layout="wide")
st.title("📐 Plano Cartesiano Interativo")

st.markdown("""
Adicione pontos e desenhe segmentos de reta livremente no **plano cartesiano**.  
Agora com aparência de um plano de verdade (eixos cruzando no 0,0).
""")

# ----- Estado inicial -----
if "formas" not in st.session_state:
    st.session_state.formas = []  # Lista de (pontos, cor)
if "forma_atual" not in st.session_state:
    st.session_state.forma_atual = []  # Pontos do desenho atual

# ----- Funções -----
def cor_aleatoria():
    cores = [
        "#FF6B6B", "#6BCB77", "#4D96FF", "#FFD93D",
        "#C77DFF", "#FF9F1C", "#00C9A7", "#845EC2",
        "#F9F871", "#FF5C8D", "#3EC1D3", "#FF914D"
    ]
    return random.choice(cores)

def gerar_steve():
    return [
        (-1, 8), (1, 8), (1, 10), (-1, 10), (-1, 8),
        (-1.5, 8), (1.5, 8), (1.5, 4), (-1.5, 4), (-1.5, 8),
        (-1.5, 7.8), (-2.5, 7.8), (-2.5, 4.2), (-1.5, 4.2), (-1.5, 7.8),
        (1.5, 7.8), (2.5, 7.8), (2.5, 4.2), (1.5, 4.2), (1.5, 7.8),
        (-1.0, 4), (-1.0, 0), (0, 0), (0, 4), (-1.0, 4),
        (0, 4), (0, 0), (1.0, 0), (1.0, 4), (0, 4)
    ]

# ----- Interface lateral -----
st.sidebar.header("Adicionar Coordenadas")
x = st.sidebar.number_input("X", step=0.5)
y = st.sidebar.number_input("Y", step=0.5)

col1, col2 = st.sidebar.columns(2)
if col1.button("➕ Adicionar ponto"):
    st.session_state.forma_atual.append((x, y))

if col2.button("🗑️ Limpar tudo"):
    st.session_state.formas = []
    st.session_state.forma_atual = []

if st.button("✅ Finalizar forma"):
    if st.session_state.forma_atual:
        cor = cor_aleatoria()
        st.session_state.formas.append({"pontos": st.session_state.forma_atual, "cor": cor})
        st.session_state.forma_atual = []

if st.button("🧍‍♂️ Desenhar Steve do Minecraft"):
    cor = cor_aleatoria()
    st.session_state.formas.append({"pontos": gerar_steve(), "cor": cor})

st.sidebar.markdown("### Pontos atuais:")
for i, (px, py) in enumerate(st.session_state.forma_atual, 1):
    st.sidebar.write(f"{i}. ({px}, {py})")

st.sidebar.markdown("### Formas finalizadas:")
st.sidebar.write(f"{len(st.session_state.formas)} desenho(s) salvos")

# ----- Criar gráfico com visual de plano cartesiano -----
fig = go.Figure()

# Eixos X e Y centrais
fig.add_trace(go.Scatter(
    x=[-20, 20], y=[0, 0],
    mode="lines", line=dict(color="black", width=2),
    showlegend=False
))
fig.add_trace(go.Scatter(
    x=[0, 0], y=[-20, 20],
    mode="lines", line=dict(color="black", width=2),
    showlegend=False
))

# Formas finalizadas
for i, forma in enumerate(st.session_state.formas, start=1):
    xs, ys = zip(*forma["pontos"])
    fig.add_trace(go.Scatter(
        x=xs,
        y=ys,
        mode="lines+markers",
        name=f"Forma {i}",
        line=dict(width=3, color=forma["cor"]),
        marker=dict(size=6, color=forma["cor"])
    ))

# Forma atual
if st.session_state.forma_atual:
    xs, ys = zip(*st.session_state.forma_atual)
    fig.add_trace(go.Scatter(
        x=xs, y=ys,
        mode="lines+markers",
        name="Forma atual",
        line=dict(width=2, dash="dash", color="#888"),
        marker=dict(size=6, color="#555")
    ))

# ----- Layout do plano cartesiano -----
fig.update_layout(
    width=700, height=700,
    template="simple_white",
    showlegend=True,
    xaxis=dict(
        title="Eixo X",
        zeroline=False,
        showgrid=True,
        gridcolor="#DDD",
        range=[-10, 10],
        ticks="outside",
        tick0=0,
        dtick=1
    ),
    yaxis=dict(
        title="Eixo Y",
        zeroline=False,
        showgrid=True,
        gridcolor="#DDD",
        range=[-10, 10],
        ticks="outside",
        tick0=0,
        dtick=1
    ),
    plot_bgcolor="white",
)

# Travar proporção e permitir zoom livre
fig.update_xaxes(scaleanchor="y", scaleratio=1)
st.plotly_chart(fig, use_container_width=True)
