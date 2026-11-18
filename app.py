import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="CaixaTrava Pro", page_icon="💼", layout="wide")

st.title("💼 CaixaTrava Pro — Gestão de Gastos, Pedidos & Investimentos")
st.markdown("---")

if 'pedidos' not in st.session_state:
    st.session_state.pedidos = pd.DataFrame([
        {"Cliente": "Michel", "Categoria": "Personalizados", "Produto": "michel", "Valor": 101.65, "Status": "Pago", "Filamento": 19.46, "Eletricidade": 1.10, "Impressora": 12.81, "Trabalho": 30.00, "Lucro": 20.00},
        {"Cliente": "Harry Fã", "Categoria": "Harry Potter", "Produto": "HP1 (Livros)", "Valor": 51.00, "Status": "Pendente", "Filamento": 20.44, "Eletricidade": 0.83, "Impressora": 2.78, "Trabalho": 2.50, "Lucro": 10.00}
    ])

if 'gastos' not in st.session_state:
    st.session_state.gastos = pd.DataFrame([
        {"Data": "18/11/2026", "Descricao": "Filamento Voolt3D PLA", "Tipo": "Empresa", "Forma": "Crédito", "Essencial": "Essencial", "Valor": 75.00},
        {"Data": "17/11/2026", "Descricao": "Conta de Luz", "Tipo": "Empresa", "Forma": "Pix", "Essencial": "Essencial", "Valor": 45.00}
    ])

if 'metas' not in st.session_state:
    st.session_state.metas = [
        {"Nome": "Reserva de Emergência", "Alvo": 1000.00, "Guardado": 350.00},
        {"Nome": "Segunda Impressora 3D", "Alvo": 2500.00, "Guardado": 625.00}
    ]

aba1, aba2, aba3, aba4, aba5 = st.tabs(["📦 Pedidos & Todas as Abas", "💳 Gastos (Trava)", "🎯 Metas", "📈 Investimentos", "📊 Gráficos & Análise"])

with aba1:
    st.subheader("📦 Gestão de Pedidos (Catálogo Completo de Abas e Nomes)")
    st.markdown("Selecione a aba correspondente da sua planilha para puxar os produtos e preços corretos.")
    
    # Catálogo completo espelhado de todas as abas da sua planilha
    catalogo_abas = {
        "Harry Potter": {
            "HP1 (Livros)": 51.00, "HP2": 33.45, "HP3": 75.12, "HP4 (Chapéu Seletor)": 48.32, 
            "HP5": 19.83, "HP6": 27.88, "HP7": 29.39, "HP8 (Suporte Livros)": 37.23, 
            "HP9": 66.72, "HP10": 68.42, "HP16 (Pomo de Ouro)": 33.40, "HP18": 20.28, "HP21": 16.90, "HP22": 73.02
        },
        "Natal": {
            "md1 (Árvore/Decoração)": 68.38, "Rejiane (Enfeite)": 72.96, "Silvanna": 50.61, 
            "Jussara": 70.74, "Mirielle": 59.26, "Viviane": 73.99, "Glaucia": 78.01, "Glaucia 4.1": 104.91
        },
        "Patricia": {
            "md1 (Patricia)": 57.17, "md2": 46.72, "md4": 30.21, "md5": 35.94
        },
        "Personalizados": {
            "projeto mih": 20.17, "SDPS": 42.44, "michel": 101.65, "tempestade ge de": 46.03
        },
        "Nomes": {
            "MIGUEL": 18.74, "MILENA": 18.80, "pedro": 18.40
        },
        "Em Site": {
            "Chaveiro Pokebola": 6.96, "Funko Pop Miles Morales": 11.71, "Estrela Sensorial": 15.55, 
            "Funko Pop Homem Aranha": 11.93, "Suporte de Livros Levitam": 15.42
        }
    }
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: cli = st.text_input("Nome do Cliente / Projeto")
    with col2: cat_escolhida = st.selectbox("Aba da Planilha", list(catalogo_abas.keys()))
    with col3: prod_escolhido = st.selectbox("Produto / Nome", list(catalogo_abas[cat_escolhida].keys()))
    
    val_sugerido = catalogo_abas[cat_escolhida][prod_escolhido]
    with col4: val = st.number_input("Valor de Venda (R$)", value=val_sugerido, min_value=0.0, step=0.01)
    with col5: status = st.selectbox("Status do Pedido", ["Pendente", "Pago"])
    
    if st.button("Adicionar Pedido"):
        if cli and val > 0:
            novo_p = pd.DataFrame([{
                "Cliente": cli, 
                "Categoria": cat_escolhida, 
                "Produto": prod_escolhido, 
                "Valor": val, 
                "Status": status, 
                "Filamento": val * 0.30, 
                "Eletricidade": val * 0.05, 
                "Impressora": val * 0.15, 
                "Trabalho": val * 0.20, 
                "Lucro": val * 0.30
            }])
            st.session_state.pedidos = pd.concat([st.session_state.pedidos, novo_p], ignore_index=True)
            st.success("Pedido adicionado com sucesso!")
            st.rerun()
            
    st.dataframe(st.session_state.pedidos, use_container_width=True)

with aba2:
    st.subheader("💳 Registrar Gasto com Trava de Saldo")
    p_pagos = st.session_state.pedidos[st.session_state.pedidos['Status'] == 'Pago']['Valor'].sum()
    g_nao_credito = st.session_state.gastos[st.session_state.gastos['Forma'] != 'Crédito']['Valor'].sum()
    saldo_livre = p_pagos - g_nao_credito
    
    st.metric("Saldo Livre Disponível (PIX / Débito)", f"R$ {saldo_livre:.2f}")
    
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: desc = st.text_input("Descrição do Gasto")
    with col2: g_val = st.number_input("Valor (R$)", min_value=0.0, step=0.01, key="g_val")
    with col3: forma = st.selectbox("Forma de Pagamento", ["Pix", "Débito", "Crédito"])
    with col4: tipo = st.selectbox("Tipo de Gasto", ["Empresa", "Pessoal"])
    with col5: essencial = st.selectbox("Essencialidade", ["Essencial", "Desnecessário"])
    
    if st.button("Registrar e Validar Gasto"):
        if desc and g_val > 0:
            if forma != 'Crédito' and g_val > saldo_livre:
                st.error("❌ BLOQUEIO DE SEGURANÇA: Gasto negado! O valor excede seu saldo disponível em Pix/Débito.")
            else:
                novo_g = pd.DataFrame([{"Data": "Hoje", "Descricao": desc, "Tipo": tipo, "Forma": forma, "Essencial": essencial, "Valor": g_val}])
                st.session_state.gastos = pd.concat([st.session_state.gastos, novo_g], ignore_index=True)
                st.success("Gasto registrado com sucesso!")
                st.rerun()
                
    st.dataframe(st.session_state.gastos, use_container_width=True)

with aba3:
    st.subheader("🎯 Controle de Metas Financeiras")
    c1, c2, c3 = st.columns(3)
    with c1: m_nome = st.text_input("Nome da Meta")
    with c2: m_alvo = st.number_input("Valor Alvo (R$)", min_value=0.0, step=0.01)
    with c3: m_ini = st.number_input("Valor Inicial Guardado (R$)", min_value=0.0, step=0.01)
    
    if st.button("Criar Nova Meta"):
        if m_nome and m_alvo > 0:
            st.session_state.metas.append({"Nome": m_nome, "Alvo": m_alvo, "Guardado": m_ini})
            st.success("Meta criada!")
            st.rerun()
            
    st.markdown("---")
    for idx, m in enumerate(st.session_state.metas):
        pct = min(100.0, (m["Guardado"] / m["Alvo"]) * 100)
        alta_falta = max(0.0, m["Alvo"] - m["Guardado"])
        st.write(f"**🎯 {m['Nome']}** — Guardado: R$ {m['Guardado']:.2f} / R$ {m['Alvo']:.2f} ({pct:.1f}%)")
        st.progress(int(pct))
        st.caption(f"Faltam R$ {alta_falta:.2f} para concluir.")
        
        col_m1, col_m2 = st.columns([2, 1])
        with col_m1:
            val_add = st.number_input(f"Guardar em {m['Nome']}", min_value=0.0, step=10.0, key=f"add_{idx}")
        with col_m2:
            if st.button("Adicionar Valor", key=f"btn_{idx}"):
                st.session_state.metas[idx]["Guardado"] += val_add
                st.rerun()
        st.markdown("---")

with aba4:
    st.subheader("📈 Carteira de Investimentos Automática")
    st.info("O sistema separa automaticamente 20% de todos os ganhos (pedidos pagos) divididos entre Dólar, CDB e Renda Variável.")
    
    total_pagos = st.session_state.pedidos[st.session_state.pedidos['Status'] == 'Pago']['Valor'].sum()
    total_investido_auto = total_pagos * 0.20
    
    inv_dolar = total_investido_auto * 0.30
    inv_cdb = total_investido_auto * 0.50
    inv_rv = total_investido_auto * 0.20
    
    col_i1, col_i2, col_i3 = st.columns(3)
    col_i1.metric("🇺🇸 Dólar (30%)", f"R$ {inv_dolar:.2f}")
    col_i2.metric("🏦 CDB (50%)", f"R$ {inv_cdb:.2f}")
    col_i3.metric("📊 Renda Variável (20%)", f"R$ {inv_rv:.2f}")

with aba5:
    st.subheader("📊 Análise Gráfica de Essencialidade")
    if not st.session_state.gastos.empty:
        fig, ax = plt.subplots(figsize=(6, 4))
        ess_counts = st.session_state.gastos.groupby('Essencial')['Valor'].sum()
        ax.pie(ess_counts, labels=ess_counts.index, autopct='%1.1f%%', colors=['#10b981', '#ef4444'])
        ax.set_title("Essencial vs Desnecessário")
        st.pyplot(fig)
    else:
        st.write("Sem gastos registrados ainda.")
