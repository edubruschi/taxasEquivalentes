import streamlit as st

# --- Funções de Cálculo ---

def calcular_aliquota_ir(prazo_dias):
    """Calcula a alíquota de IR com base no prazo em dias."""
    if prazo_dias <= 180:
        return 0.225  # 22,5%
    elif 181 <= prazo_dias <= 360:
        return 0.20   # 20%
    elif 361 <= prazo_dias <= 720:
        return 0.175  # 17,5%
    else:
        return 0.15   # 15%

def comparar_investimentos(percentual_cdi_tributado, percentual_cdi_isento, cdi_anual, prazo_dias):
    """
    Compara um investimento tributado (em % do CDI) com um isento (em % do CDI), considerando o IR.

    Args:
        percentual_cdi_tributado (float): Porcentagem do CDI da taxa tributada (ex: 1.0 para 100% do CDI).
        percentual_cdi_isento (float): Porcentagem do CDI da taxa isenta (ex: 0.08 para 80% do CDI).
        cdi_anual (float): Valor anual do CDI (ex: 0.1490 para 14.90% a.a.).
        prazo_dias (int): Prazo do investimento em dias.

    Returns:
        tuple: (taxa_tributada_liquida, taxa_isenta_liquida, taxa_tributada_bruta, taxa_isenta_bruta,
                rent_liquida_tributado_vs_cdi, rent_liquida_isento_vs_cdi,
                mensagem_resultado, recomendacao)
    """
    if prazo_dias <= 0:
        return None, None, None, None, None, None, "O prazo precisa ser um número positivo de dias.", "Verifique o prazo inserido."

    # Calcula a taxa anual bruta do investimento tributado
    taxa_tributada_anual_bruta = percentual_cdi_tributado * cdi_anual

    # A taxa anual bruta do investimento isento é a sua própria taxa líquida, pois não tem IR
    taxa_isenta_anual_bruta = percentual_cdi_isento * cdi_anual

    aliquota_ir = calcular_aliquota_ir(prazo_dias)
    taxa_tributada_liquida = taxa_tributada_anual_bruta * (1 - aliquota_ir)
    taxa_isenta_liquida = taxa_isenta_anual_bruta # A taxa do isento já é líquida

    # CDI proporcional ao período (considerando capitalização simples para facilitar a comparação direta)
    # Para capitalização composta seria (1 + cdi_anual)**(prazo_dias/365) - 1
    cdi_proporcional = cdi_anual * (prazo_dias / 365)

    # Rentabilidade líquida dos investimentos em relação ao CDI no período
    # Isso mostra quanto % do CDI nominal o investimento rendeu *líquido*
    rent_liquida_tributado_vs_cdi = (taxa_tributada_liquida * (prazo_dias / 365)) / cdi_proporcional if cdi_proporcional else 0
    rent_liquida_isento_vs_cdi = (taxa_isenta_liquida * (prazo_dias / 365)) / cdi_proporcional if cdi_proporcional else 0

    mensagem_resultado = (
        f"**Taxa Líquida do Investimento Tributado (após IR):** {taxa_tributada_liquida:.2%} a.a.\n"
        f"**Taxa Líquida do Investimento Isento:** {taxa_isenta_liquida:.2%} a.a."
    )

    recomendacao = ""
    if taxa_tributada_liquida > taxa_isenta_liquida:
        recomendacao = f"**Recomendação:** O **investimento tributado** está mais vantajoso, mesmo com o IR."
    elif taxa_isenta_liquida > taxa_tributada_liquida:
        recomendacao = f"**Recomendação:** O **investimento isento** está mais vantajoso."
    else:
        recomendacao = f"**Recomendação:** Os dois investimentos estão com rentabilidade líquida **equivalente**."

    return taxa_tributada_liquida, taxa_isenta_liquida, taxa_tributada_anual_bruta, taxa_isenta_anual_bruta, \
           rent_liquida_tributado_vs_cdi, rent_liquida_isento_vs_cdi, \
           mensagem_resultado, recomendacao

# --- Interface Streamlit ---

st.set_page_config(
    page_title="Comparador de Investimentos",
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("💰 Comparador de Investimentos Pós-Fixados")
st.write("Compare a rentabilidade líquida de investimentos tributados (ex: CDBs) com investimentos isentos (ex: LCIs/LCAs), ambos em percentual do CDI, considerando a incidência do Imposto de Renda.")

st.markdown("---")

st.header("Dados de Entrada")

cdi_anual_input = st.number_input(
    "Valor Atual do CDI (em % a.a.)",
    min_value=0.01,
    max_value=50.00,
    value=14.90, # Valor padrão do CDI
    step=0.1,
    format="%.2f",
    help="Informe o valor anual do CDI que será a base para os cálculos."
)
cdi_anual = cdi_anual_input / 100 # Converte para decimal

percentual_cdi_tributado_input = st.number_input(
    "Percentual do CDI do Investimento Tributado (ex: 100 para 100% do CDI)",
    min_value=1.0,
    max_value=300.0,
    value=100.0,
    step=1.0,
    format="%.1f",
    help="Ex: CDB que paga 100% do CDI."
)
percentual_cdi_tributado = percentual_cdi_tributado_input / 100 # Converte para decimal

percentual_cdi_isento_input = st.number_input(
    "Percentual do CDI do Investimento Isento (ex: 90 para 90% do CDI)",
    min_value=1.0,
    max_value=300.0,
    value=90.0,
    step=1.0,
    format="%.1f",
    help="Ex: LCI/LCA que paga 90% do CDI."
)
percentual_cdi_isento = percentual_cdi_isento_input / 100 # Converte para decimal

st.markdown("---")

st.header("Prazo do Investimento")

prazo_em_meses = st.slider(
    "Prazo do Investimento (em meses)",
    min_value=1,
    max_value=60, # Até 5 anos para ter uma boa visualização
    value=12,
    step=1
)
prazo_dias = prazo_em_meses * 30.4375 # Média de dias por mês para cálculo do IR

st.markdown("---")

if st.button("Comparar Investimentos"):
    taxa_tributada_liquida, taxa_isenta_liquida, taxa_tributada_bruta, taxa_isenta_bruta, \
    rent_liquida_tributado_vs_cdi, rent_liquida_isento_vs_cdi, \
    mensagem, recomendacao = comparar_investimentos(
        percentual_cdi_tributado, percentual_cdi_isento, cdi_anual, prazo_dias
    )

    if taxa_tributada_liquida is not None:
        st.subheader("Resultados da Comparação:")
        st.markdown(f"- **CDI Anual Base:** **{cdi_anual_input:.2f}% a.a.**")
        st.markdown(f"- **Prazo Considerado:** **{prazo_em_meses} meses** (aprox. {int(prazo_dias)} dias)")
        st.markdown(f"- **Alíquota de IR para este prazo:** **{calcular_aliquota_ir(prazo_dias):.1%}** (do rendimento bruto)")

        st.subheader("Rentabilidade Bruta (sem considerar IR):")
        st.markdown(f"- Investimento Tributado (CDB, etc.): **{percentual_cdi_tributado_input:.1f}% do CDI** ({taxa_tributada_bruta:.2%} a.a.)")
        st.markdown(f"- Investimento Isento (LCI/LCA, etc.): **{percentual_cdi_isento_input:.1f}% do CDI** ({taxa_isenta_bruta:.2%} a.a.)")

        st.subheader("Rentabilidade Líquida (após IR):")
        st.success(mensagem)
        st.info(recomendacao)

        st.subheader("Rentabilidade Líquida em Relação ao CDI no Período:")
        if cdi_anual > 0: # Evita divisão por zero
            st.markdown(f"- Investimento Tributado: **{rent_liquida_tributado_vs_cdi:.2%} do CDI**")
            st.markdown(f"- Investimento Isento: **{rent_liquida_isento_vs_cdi:.2%} do CDI**")
        else:
            st.warning("Não é possível calcular a rentabilidade em relação ao CDI se o CDI for zero.")

    else:
        st.error(mensagem)

st.markdown("---")
st.caption("Desenvolvido para assessores de investimento. Este cálculo é uma simulação e não substitui uma análise completa.")