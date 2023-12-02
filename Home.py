import streamlit as st
from PIL import Image

st.set_page_config(
    page_title='Home',
    layout='wide'
)

image= Image.open('pages/zomato-logo.jpg')

st.sidebar.image(image, width=250)

st.sidebar.title('Zomato Restaurants')
st.sidebar.markdown('## For the Love of Fodd')
st.sidebar.markdown("""---""")

st.markdown(
    '''
    # Zomato Restaurants - Dashbord
    Este Dashboard foi construído para dar uma visão melhor dos dados da empresa Zomato Restaurants.
    Nele reunimos tabelas e gráficos que mostram a abrangência dessa plataforma de Restaurantes e 
    também dados relevantes para traçar novas métricas de alcance. Nele dividimos os dados
    em Visão Geral, Países, Cidades e Culinárias e utilizamos filtros para ajudar na navegação.
    
    ## Sobre a Zomato
    A Zomato é um serviço de busca de restaurantes para quem quer sair para jantar,
    buscar comida ou pedir em casa na Índia, Brasil, Portugal, Turquia, Indonésia,
    Nova Zelândia, Itália, Filipinas, África do Sul, Sri Lanka, Catar, Emirados Árabes Unidos,
    Reino Unido, Estados Unidos, Austrália e Canadá.

    ## Origem dos Dados
    Os dados foram retirados da plataforma Kaggle e são públicos. O link para donwload é:
    https://www.kaggle.com/datasets/akashram/zomato-restaurants-autoupdated-dataset?resource=download&select=zomato.csv

    ## Como utilizar o Dashboard?
    - Visão Geral:
        - Informações gerais sobre a plataforma e sua abrangência.
        - Mapa com localização dos restaurantes e cores para diferenciar sua avaliação média.
    - Visão Países:
        - Informações úteis agrupadas por países presentes na plataforma como nota e preço médio por país.
    - Visão Cidades:
        - Gráficos que mostram a participação de cada cidade, com informações como avaliação média por cidade e tipos de comida.
    - Visão Culinária:
        - Divisão feita por tipo de comida como os melhores, os tipos de comida mais bem avaliados.

    ## Contato:
    - Discord: juliano.nicoletti
    - LinkedIn: https://www.linkedin.com/in/juliano-nicoletti/
    - Github: https://github.com/julianonicoletti
    '''
)
