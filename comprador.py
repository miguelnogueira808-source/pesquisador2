import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
import os

if not os.path.exists("buscas_salvas"):
    os.makedirs("buscas_salvas")

st.title("Robô de Revenda ML")

nome_busca = st.text_input("Nome desta busca:")
produtos_input = st.text_area("Cole os itens (um por linha):")

if st.button("Buscar no ML"):
    lista_produtos = [p.strip() for p in produtos_input.split('\n') if p.strip()]
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    }
    
    resultados_finais = []
    
    for produto in lista_produtos:
        st.subheader(f"Buscando: {produto}")
        time.sleep(3)
        
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscando itens
            itens = soup.select('li.ui-search-layout__item')
            st.write(f"Itens encontrados: {len(itens)}")
            
            if itens:
                for item in itens[:3]:
                    titulo = item.select_one('h2.ui-search-item__title')
                    preco = item.select_one('span.andes-money-amount__fraction')
                    
                    if titulo and preco:
                        resultado = f"✅ {titulo.text.strip()} -> R$ {preco.text.strip()}"
                        st.success(resultado)
                        resultados_finais.append(resultado)
            else:
                st.warning("Nenhum item encontrado nesta página.")
                
        except Exception as e:
            st.error(f"Erro: {e}")

    if nome_busca and resultados_finais:
        with open(f"buscas_salvas/{nome_busca}.json", "w") as f:
            json.dump(resultados_finais, f)
        st.success("Busca salva!")
