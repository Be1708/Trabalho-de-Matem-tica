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
uploaded_file = st.sidebar.fil_
