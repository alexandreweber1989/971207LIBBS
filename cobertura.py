import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração da página
st.set_page_config(page_title="Dashboard de Vendas", layout="wide")

# Carregar os dados do Excel
@st.cache_data
def load_data():
    file_path = "DADOS GERAIS - PBI.xlsx"
    df = pd.read_excel(file_path, sheet_name="DADOS EM GERAL")
    df["PDV"] = df["PDV"].astype(str)
    return df

data = load_data()

# Dicionário de usuários e senhas
usuarios = {
    "9712 TRAJANO": "9712 TRAJANO",
    "9712 RODOCENTRO": "9712 RODOCENTRO",
    "9712 FCIA RIO": "9712 FCIA RIO",
    "9712 FARMA&FARMA": "9712 FARMA&FARMA",
    "9712 FARMASSIM": "9712 FARMASSIM",
    "9712 FCIA UNIÃO STA TEREZINHA": "9712 FCIA UNIÃO STA TEREZINHA",
    "9712 FERNANDO HIPERFARMA": "9712 FERNANDO HIPERFARMA",
    "9712 LUCAS GONTARZOCENTRO": "9712 LUCAS GONTARZOCENTRO",
    "9712 FCIA HEROOS": "9712 FCIA HEROOS",
    "9712 BONA": "9712 BONA"
}

# Tela de login
st.sidebar.header("Login")
usuario = st.sidebar.text_input("Usuário")
senha = st.sidebar.text_input("Senha", type="password")
login_button = st.sidebar.button("Entrar")

if login_button:
    if usuario in usuarios and usuarios[usuario] == senha:
        st.session_state["logado"] = True
        st.session_state["bandeira"] = usuario
    else:
        st.sidebar.error("Usuário ou senha incorretos")

# Verifica se o usuário está logado
if "logado" in st.session_state and st.session_state["logado"]:
    bandeira_selecionada = st.session_state["bandeira"]
    data_filtrada = data[data["BANDEIRA"] == bandeira_selecionada]
    
    # Seleção de PDV
    pdvs = data_filtrada["PDV"].unique()
    pdv_selecionado = st.sidebar.selectbox("Selecione o PDV", pdvs)

    # Interface do usuário
    st.markdown(f"# Dashboard de Vendas - {bandeira_selecionada}")
    st.markdown("### Acompanhamento de metas e resultados")

    # Calcular totais da bandeira
    total_objetivo = data_filtrada["Cota"].sum()
    total_atendido = data_filtrada["Atendido"].sum()
    total_desvio = total_atendido - total_objetivo

    # Exibir as informações totais da bandeira
    st.markdown("### Totais da Bandeira")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f'<div style="border: 2px solid #00BFFF; border-radius: 10px; padding: 10px; text-align: center;">'
            f'<strong>Objetivo Total</strong><br>R$ {total_objetivo:,.2f}</div>', unsafe_allow_html=True)

    cor_atendido = "#32CD32" if total_atendido >= total_objetivo else "#FFA500"
    cor_desvio = "#32CD32" if total_desvio >= 0 else "#FFA500"

    with col2:
        st.markdown(
            f'<div style="border: 2px solid {cor_atendido}; border-radius: 10px; padding: 10px; text-align: center;">'
            f'<strong>Atendido Total</strong><br>R$ {total_atendido:,.2f}</div>', unsafe_allow_html=True)

    with col3:
        st.markdown(
            f'<div style="border: 2px solid {cor_desvio}; border-radius: 10px; padding: 10px; text-align: center;">'
            f'<strong>Desvio Total</strong><br>R$ {total_desvio:,.2f}</div>', unsafe_allow_html=True)

    # Filtrar dados do PDV
    pdv_data = data_filtrada[data_filtrada["PDV"] == pdv_selecionado]

    # Layout de cards
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Objetivo", f"R$ {pdv_data['Cota'].values[0]:,.2f}", "🎯")
    with col2:
        st.metric("Atendido", f"R$ {pdv_data['Atendido'].values[0]:,.2f}", "📈", delta_color="inverse")
    with col3:
        st.metric("Desvio", f"R$ {pdv_data['Desvio'].values[0]:,.2f}", "⚠️")
    with col4:
        st.metric("Filiais", len(pdvs), "📄")

    # Aba de Vendas por Filial e Totais por Bandeira
    aba = st.tabs(["Vendas por Filial", "Totais por Bandeira"])

    with aba[0]:
        st.markdown("### 🏢 Vendas por Filial")
        data_filtrada_formatada = data_filtrada[["PDV", "Cota", "Atendido", "Desvio", "% Cobertura"]]
        data_filtrada_formatada = data_filtrada_formatada.rename(columns={
            "PDV": "Filial",
            "Cota": "Objetivo",
            "Atendido": "Atendido",
            "Desvio": "Desvio",
            "% Cobertura": "% Atingido"
        })
        data_filtrada_formatada["Objetivo"] = data_filtrada_formatada["Objetivo"].apply(lambda x: f"R$ {x:,.2f}")
        data_filtrada_formatada["Atendido"] = data_filtrada_formatada["Atendido"].apply(lambda x: f"R$ {x:,.2f}")
        data_filtrada_formatada["Desvio"] = data_filtrada_formatada["Desvio"].apply(lambda x: f"R$ {x:,.2f}")
        data_filtrada_formatada["% Atingido"] = data_filtrada_formatada["% Atingido"].apply(lambda x: f"{x * 100:.2f}%")
        st.dataframe(data_filtrada_formatada)

else:
    st.sidebar.warning("Faça login para acessar o dashboard.")