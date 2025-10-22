import streamlit as st
import matplotlib.pyplot as plt

# ---- Configuração inicial ----
st.set_page_config(page_title="Plano Cartesiano Interativo", layout="wide")
st.title("📈 Plano Cartesiano Interativo")

st.markdown(
    """
    Adicione coordenadas (x, y) para traçar segmentos de reta em tempo real.  
    Ou clique no botão abaixo para desenhar o **Steve do Minecraft** automaticamente!
    """
)

# ---- Sessão de estado ----
if "pontos" not in st.session_state:
    st.session_state.pontos = []

# ---- Função: desenho do Steve ----
def gerar_steve():
    return [
        (-1, 8), (1, 8), (1, 10), (-1, 10), (-1, 8),
        (-1, 8), (-2, 4), (2, 4), (1, 8),
        (-2, 4), (-3, 4), (-3, 0), (-2, 0), (-2, 4),
        (2, 4), (3, 4), (3, 0), (2, 0), (2, 4),
        (-2, 0), (-1, 0), (-1, -4), (0, -4), (0, 0),
        (1, 0), (1, -4), (2, -4), (2, 0)
    ]

# ---- Barra lateral ----
st.sidebar.header("Adicionar coordenadas")
x = st.sidebar.number_input("X", step=0.5)
y = st.sidebar.number_input("Y", step=0.5)

col1, col2 = st.sidebar.columns(2)
if col1.button("➕ Adicionar ponto"):
    st.session_state.pontos.append((x, y))
if col2.button("🗑️ Limpar tudo"):
    st.session_state.pontos = []

# ---- Botão para desenhar o Steve ----
if st.button("🧍‍♂️ Desenhar o Steve do Minecraft"):
    st.session_state.pontos = gerar_steve()

# ---- Exibir lista ----
if st.session_state.pontos:
    st.sidebar.markdown("### Pontos atuais:")
    for i, (px, py) in enumerate(st.session_state.pontos, start=1):
        st.sidebar.write(f"{i}. ({px}, {py})")

# ---- Gráfico ----
fig, ax = plt.subplots(figsize=(6, 6))
ax.set_title("Plano Cartesiano", fontsize=14)
ax.set_xlabel("Eixo X")
ax.set_ylabel("Eixo Y")
ax.axhline(0, color='black', linewidth=1)
ax.axvline(0, color='black', linewidth=1)
ax.grid(True, linestyle='--', alpha=0.6)

if st.session_state.pontos:
    xs, ys = zip(*st.session_state.pontos)
    ax.plot(xs, ys, marker='o', color='dodgerblue', linewidth=2)
    for i, (px, py) in enumerate(st.session_state.pontos, start=1):
        ax.text(px + 0.1, py + 0.1, f"P{i}", fontsize=9, color='darkblue')

st.pyplot(fig)
