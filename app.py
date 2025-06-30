import streamlit as st
import json
from bs4 import BeautifulSoup

# Carregar o JSON
with open('questoes_processadas.json', 'r') as f:
    questoes = json.load(f)

# Função para limpar o HTML e também extrair imagens
def processar_enunciado(html):
    soup = BeautifulSoup(html, "html.parser")
    texto = soup.get_text(separator="\n")
    imagens = [img['src'] for img in soup.find_all('img') if img.get('src')]
    return texto, imagens

# Sidebar: escolher a questão
ids_questoes = [q['id_original_json'] for q in questoes]
id_selecionado = st.sidebar.selectbox("📋 Escolha a questão:", ids_questoes)

# Obter a questão atual
questao_atual = next(q for q in questoes if q['id_original_json'] == id_selecionado)

# Exibir título
st.title(f"Questão {questao_atual['id_original_json']}: {questao_atual['titulo_original']}")

# Exibir link
st.markdown(f"[🔗 Ver discussão original]({questao_atual['url_original']})")

# Processar enunciado
texto_enunciado, imagens = processar_enunciado(questao_atual['enunciado_html'])

# Exibir enunciado como texto limpo
st.markdown("---")
st.write(texto_enunciado)

# Exibir imagens (se houver)
for url_imagem in imagens:
    st.image(url_imagem, use_container_width=True)

st.markdown("---")

# Opções de resposta
alternativas = [f"{op['letra']}. {op['texto']}" for op in questao_atual['opcoes']]
resposta_usuario = st.radio(
    "Escolha sua resposta:",
    options=alternativas,
    key=f"questao_{questao_atual['id_original_json']}"
)

# Botão para confirmar
if st.button("✅ Confirmar resposta"):

    letra_escolhida = resposta_usuario.split('.')[0].strip()
    resposta_correta = questao_atual['resposta_sugerida_letra']

    if letra_escolhida == resposta_correta:
        st.success(f"✅ Você acertou! Resposta correta: {resposta_correta}")
    else:
        st.error(f"❌ Você errou. Resposta correta: {resposta_correta}")
