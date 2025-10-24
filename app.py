import streamlit as st
import plotly.graph_objects as go
import ezdxf
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

if st.sidebar.button
