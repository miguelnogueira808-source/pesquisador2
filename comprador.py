import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
import os

# Cria a pasta para salvar as buscas
if not os.path.exists("buscas_salvas"):
    os.makedirs("buscas_salvas")

st.title("Robô de Revenda - Busca em Massa ML")

# Sidebar para carregar buscas antigas
st.sidebar.subheader("Histórico de Buscas")
lista_arquivos = [f.replace(".json", "") for f in os.listdir("buscas_salvas") if f.endswith(".json")]
busca_escolhida = st.sidebar.selectbox("Ver busca salva:", [""] + lista_arquivos)

if busca_escolhida:
    with open(f"buscas_salvas/{busca_escolhida}.json", "r") as f:
        dados = json.load(f)
        st.write(f"Resultados de **{busca_escolhida}**:")
        for d in dados:
            st.write(d)
    st.divider()

# Input da nova busca
nome_busca = st.text_input("Nome desta nova busca:")
produtos_input = st.text_area("Cole os itens (um por linha):")

if st.button("Buscar tudo no ML"):
    lista_produtos = [p.strip() for p in produtos_input.split('\n') if p.strip()]
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
    
    resultados_finais = []
    
    for produto in lista_produtos:
        st.subheader(f"Buscando por: {produto}")
        time.sleep(2)  # O respiro para o ML não bloquear
        
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        itens = soup.find_all('li', class_='ui-search-layout__item')
        
        if itens:
            titulo = itens[0].find('h2', class_='ui-search-item__title').text
            try:
                preco = itens[0].find('span', class_='andes-money-amount__fraction').text
                resultado = f"✅ {titulo} -> R$ {preco}"
                st.success(resultado)
            except:
                resultado = f"⚠️ {titulo} -> Preço não encontrado"
                st.warning(resultado)
        else:
            resultado = f"❌ {produto} -> Nenhum resultado"
            st.error(resultado)
            
        resultados_finais.append(resultado)

    # SALVAR:
    if nome_busca and resultados_finais:
        with open(f"buscas_salvas/{nome_busca}.json", "w") as f:
            json.dump(resultados_finais, f)
        st.success(f"Busca '{nome_busca}' salva!")