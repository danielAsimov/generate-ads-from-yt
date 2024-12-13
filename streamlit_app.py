from youtube_transcript_api import YouTubeTranscriptApi as yta
import re
import streamlit as st
from urllib.parse import urlparse, parse_qs
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_openai import ChatOpenAI

# Função para extrair o ID do vídeo do YouTube
def extrair_id_youtube(url):
    try:
        # Parsear a URL
        video_id = "dd"
        parsed_url = urlparse(url)
        
        # Caso seja um link padrão (e.g., https://www.youtube.com/watch?v=ID)
        if parsed_url.hostname in ("www.youtube.com", "youtube.com"):
            query_params = parse_qs(parsed_url.query)
            return query_params.get("v", [None])[0]
        
        # Caso seja um link encurtado (e.g., https://youtu.be/ID)
        elif parsed_url.hostname in ("youtu.be",):
            return parsed_url.path.lstrip("/")
        
        return None
    except Exception as e:
        return None

# Interface do Streamlit
st.title("Extrator de ID do YouTube")

# Campo de entrada para o link do YouTube
url_input = st.text_input("Cole o link do YouTube aqui:")

# Mostrar o ID do vídeo após o usuário inserir um link válido
if url_input:
    video_id = extrair_id_youtube(url_input)
    if video_id:
        st.success(f"O ID do vídeo é: {video_id}")
        data = yta.get_transcript(video_id, languages=['pt'])

        transcript = ''
        for value in data:
            for key,val in value.items():
                if key == 'text':
                    transcript += val
        l = transcript.splitlines()
        final_transcript = " ".join(l)

        llm = ChatOpenAI(model='gpt-4o-mini')

        _ = load_dotenv(find_dotenv())

        responseEmail = llm.invoke('Crie um pequeno texto de 100 a 140 palavras. Será um e-mail com o objetivo de apresentar um resumo de um projeto, com alguns detalhes técnicos, para gerar curiosidade no leitor. Faça esse texto baseado no texto a seguir:' + final_transcript)
        responseWhats = llm.invoke('Crie um texto que será disparado por whatsapp e terá o objetivo de gerar curiosidade, deve conter alguns detalhes técnicos, e deverá ter de 60 a 80 palavras e paragrafos curtos. Faça esse texto baseado no texto a seguir:' + final_transcript)

        st.title("Aqui estão suas peças:")
        st.header("E-mail:")
        st.text(responseEmail.content)
        st.header("WhatsApp:")
        st.text(responseWhats.content)

    else:
        st.error("URL inválida. Por favor, insira um link válido do YouTube.")








