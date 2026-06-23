# ... dentro do loop for produto in lista_produtos:
        
        # Simulando um navegador real do Chrome
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Referer": "https://www.mercadolivre.com.br/"
        }
        
        url = f"https://lista.mercadolivre.com.br/{produto.replace(' ', '-')}"
        
        try:
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Buscando os cards de produtos de forma genérica
            # O ML usa classes que começam com 'ui-search-result'
            itens = soup.select('li.ui-search-layout__item')
            
            st.write(f"Itens encontrados na lista: {len(itens)}")
            
            if itens:
                for item in itens[:3]: # Pega os 3 primeiros
                    titulo = item.select_one('h2.ui-search-item__title')
                    preco = item.select_one('span.andes-money-amount__fraction')
                    
                    if titulo and preco:
                        resultado = f"✅ {titulo.text.strip()} -> R$ {preco.text.strip()}"
                        st.success(resultado)
                        resultados_finais.append(resultado)
            else:
                # Se não achar nada, mostra o que o ML retornou para a gente analisar
                st.warning("⚠️ Não localizei os itens. O ML pode estar bloqueando ou mudou o layout.")
                # st.write(response.text[:500]) # Se quiser ver o HTML bruto (cuidado: é grande!)

        except Exception as e:
            st.error(f"Erro: {e}")
