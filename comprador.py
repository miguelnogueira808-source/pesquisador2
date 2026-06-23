import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
import os

# Configuração de pasta
if not os.path.exists("buscas_salvas"):
    os.makedirs("buscas_salvas")

st.title("Robô de Revenda ML - Versão Robusta")

# Sidebar
st.sidebar.subheader("Histórico")
lista_arquivos = [f.replace(".json", "") for f in os.listdir("buscas_salvas") if f.endswith(".json")]
busca_escolhida = st.sidebar.selectbox("Ver busca salva:", [""] + lista_arquivos)

if busca_escolhida:
    with open(f"buscas_salvas/{busca_escolhida}.json", "r") as f:
        dados = json.load(f)
        for d in dados:
            st.write(d)
    st.divider()

# Input
nome_busca = st.text_input("Nome desta busca:")
produtos_input = st.text_area("Cole os itens (um por linha):")

if st.button("Buscar tudo no ML"):
    lista_produtos = [p.strip() for p in produtos_input.split('\n') if p.strip()]
    # User-Agent atualizado para parecer um navegador de verdade
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
    }
    
    resultados_finais = []
    
    for produto in lista_produtos:
        st.subheader(f"Buscando: {produto}")
        time.sleep(2.5) # Aumentei um pouco o tempo para ser mais seguro
        
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        response = requests.get(url, headers=headers)
        
        # DEBUG: Se der erro, o robô te avisa na tela
        if response.status_code != 200:
            st.error(f"Erro ao acessar o ML (Código {response.status_code})")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Tenta achar os itens de formas diferentes
        itens = soup.find_all('div', class_='ui-search-result__wrapper')
        if not itens:
            itens = soup.find_all('li', class_='ui-search-layout__item')
            
        if itens:
            item = itens[0]
            # Procura o título em vários lugares possíveis
            titulo_tag = item.find('h2', class_='ui-search-item__title') or item.find('a', class_='ui-search-item__group__element')
            titulo = titulo_tag.text if titulo_tag else "Título não encontrado"
            
            # Procura o preço
            preco_tag = item.find('span', class_='andes-money-amount__fraction')
            preco = preco_tag.text if preco_tag else "Preço não disponível"
            
            resultado = f"✅ {titulo} -> R$ {preco}"
            st.success(resultado)
            resultados_finais.append(resultado)
        else:
            st.warning(f"❌ Nenhum resultado encontrado para: {produto}")

    # SALVAR
    if nome_busca and resultados_finais:
        with open(f"buscas_salvas/{nome_busca}.json", "w") as f:
            json.dump(resultados_finais, f)
        st.success(f"Busca '{nome_busca}' salva!")
