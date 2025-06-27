import streamlit as st

st.set_page_config(
    page_title="Calculadora de Taxas Equivalentes",
    page_icon="💰",
    layout="centered"
)

# --- Funções de Cálculo ---
def anual_para_mensal(taxa_anual):
    """Converte uma taxa anual para mensal."""
    # A taxa precisa ser em decimal para o cálculo
    taxa_anual_decimal = taxa_anual / 100
    taxa_mensal_decimal = (1 + taxa_anual_decimal)**(1/12) - 1
    return taxa_mensal_decimal * 100 # Retorna em porcentagem

def mensal_para_anual(taxa_mensal):
    """Converte uma taxa mensal para anual."""
    # A taxa precisa ser em decimal para o cálculo
    taxa_mensal_decimal = taxa_mensal / 100
    taxa_anual_decimal = (1 + taxa_mensal_decimal)**12 - 1
    return taxa_anual_decimal * 100 # Retorna em porcentagem

def anual_para_diaria(taxa_anual, dias_no_ano=365):
    """Converte uma taxa anual para diária."""
    # A taxa precisa ser em decimal para o cálculo
    taxa_anual_decimal = taxa_anual / 100
    taxa_diaria_decimal = (1 + taxa_anual_decimal)**(1/dias_no_ano) - 1
    return taxa_diaria_decimal * 100 # Retorna em porcentagem

def mensal_para_diaria(taxa_mensal, dias_no_mes=30):
    """Converte uma taxa mensal para diária."""
    # A taxa precisa ser em decimal para o cálculo
    taxa_mensal_decimal = taxa_mensal / 100
    taxa_diaria_decimal = (1 + taxa_mensal_decimal)**(1/dias_no_mes) - 1
    return taxa_diaria_decimal * 100 # Retorna em porcentagem

# --- Interface Streamlit ---
st.title("💰 Calculadora de Taxas Equivalentes")

# Opção de seleção para o tipo de conversão
tipo_conversao = st.selectbox(
    "Selecione o tipo de conversão:",
    [
        "ANUAL para MENSAL",
        "ANUAL para DIÁRIA",
        "MENSAL para ANUAL",
        "MENSAL para DIÁRIA"
    ]
)

st.markdown("---")

if tipo_conversao == "ANUAL para MENSAL":
    st.header("Anual para Mensal")
    taxa_anual = st.number_input("Digite a taxa ANUAL (%):", min_value=0.0, format="%.4f", value=14.900)
    if st.button("Calcular Taxa Mensal"):
        if taxa_anual >= 0:
            taxa_mensal_equivalente = anual_para_mensal(taxa_anual)
            st.success(f"A taxa mensal equivalente é: **{taxa_mensal_equivalente:.4f}%**")
        else:
            st.error("A taxa anual não pode ser negativa.")

elif tipo_conversao == "MENSAL para ANUAL":
    st.header("Mensal para Anual")
    taxa_mensal = st.number_input("Digite a taxa MENSAL (%):", min_value=0.0, format="%.4f")
    if st.button("Calcular Taxa Anual"):
        if taxa_mensal >= 0:
            taxa_anual_equivalente = mensal_para_anual(taxa_mensal)
            st.success(f"A taxa anual equivalente é: **{taxa_anual_equivalente:.4f}%**")
        else:
            st.error("A taxa mensal não pode ser negativa.")

elif tipo_conversao == "ANUAL para DIÁRIA":
    st.header("Anual para Diária")
    taxa_anual_diaria = st.number_input("Digite a taxa ANUAL (%):", min_value=0.0, format="%.4f", key="anual_diaria_input", value=14.900)
    dias_no_ano = st.radio(
        "Número de dias no ano:",
        (365, 360),
        index=0, # 365 é o padrão
        key="dias_ano_radio"
    )
    if st.button("Calcular Taxa Diária", key="calc_diaria_anual_btn"):
        if taxa_anual_diaria >= 0:
            taxa_diaria_equivalente = anual_para_diaria(taxa_anual_diaria, dias_no_ano)
            st.success(f"A taxa diária equivalente é: **{taxa_diaria_equivalente:.4f}%**")
        else:
            st.error("A taxa anual não pode ser negativa.")

elif tipo_conversao == "MENSAL para DIÁRIA":
    st.header("Mensal para Diária")
    taxa_mensal_diaria = st.number_input("Digite a taxa MENSAL (%):", min_value=0.0, format="%.4f", key="mensal_diaria_input")
    dias_no_mes = st.radio(
        "Número de dias no mês:",
        (30, 31, 28, 29),
        index=0, # 30 é o padrão
        key="dias_mes_radio"
    )
    if st.button("Calcular Taxa Diária", key="calc_diaria_mensal_btn"):
        if taxa_mensal_diaria >= 0:
            taxa_diaria_equivalente = mensal_para_diaria(taxa_mensal_diaria, dias_no_mes)
            st.success(f"A taxa diária equivalente é: **{taxa_diaria_equivalente:.4f}%**")
        else:
            st.error("A taxa mensal não pode ser negativa.")

st.markdown("---")
st.info("Desenvolvido com Python e Streamlit.")