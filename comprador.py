import streamlit as st
import requests
from bs4 import BeautifulSoup
import time
import json
import os

if not os.path.exists("buscas_salvas"):
    os.makedirs("buscas_salvas")

st.title("Robô de Revenda ML - Modo Disfarçado")

nome_busca = st.text_input("Nome desta busca:")
produtos_input = st.text_area("Cole os itens (um por linha):")

if st.button("Buscar no ML"):
    lista_produtos = [p.strip() for p in produtos_input.split('\n') if p.strip()]
    
    # Headers super completos para parecer um humano real
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Referer": "https://www.google.com/",
        "Connection": "keep-alive"
    }
    
    resultados_finais = []
    
    for produto in lista_produtos:
        st.subheader(f"Buscando: {produto}")
        time.sleep(3) # Tempo um pouco maior para segurança
        
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        
        try:
            response = requests.get(url, headers=headers)
            st.write(f"Status da conexão: {response.status_code}") # Pra saber se o ML bloqueou
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscando os produtos de forma bem ampla
            itens = soup.find_all(['li', 'div'], class_=['ui-search-layout__item', 'ui-search-result__wrapper'])
            
            st.write(f"Itens encontrados na página: {len(itens)}")
            
            if itens:
                item = itens[0]
                titulo = item.find(['h2', 'a'], class_=['ui-search-item__title', 'ui-search-result__content-wrapper'])
                titulo_texto = titulo.get_text(strip=True) if titulo else "Título não encontrado"
                
                preco = item.find('span', class_='andes-money-amount__fraction')
                preco_texto = preco.text if preco else "Preço não disponível"
                
                resultado = f"✅ {titulo_texto} -> R$ {preco_texto}"
                st.success(resultado)
                resultados_finais.append(resultado)
            else:
                st.warning(f"⚠️ Não achei o formato dos itens. O ML pode ter mudado o layout.")
                
        except Exception as e:
            st.error(f"Erro no robô: {e}")

    if nome_busca and resultados_finais:
        with open(f"buscas_salvas/{nome_busca}.json", "w") as f:
            json.dump(resultados_finais, f)
        st.success("Busca salva!")
