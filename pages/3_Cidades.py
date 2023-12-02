import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import inflection
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static


st.set_page_config(page_title='Visão Cidades', layout='wide')

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, "../dataset/zomato.csv")
df = pd.read_csv(file_path)

PAISES =[  
    "India",
    "Australia",
    "Brazil",
    "Canada",
    "Indonesia",
    "New Zeland",
    "Philippines",
    "Qatar",
    "Singapure",
    "South Africa",
    "Sri Lanka",
    "Turkey",
    "United Arab Emirates",
    "England",
    "United States of America"]
    

COUNTRIES = { #dando nomes aos códigos de países
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America",
    }
def country_name(country_id):
    
    return COUNTRIES[country_id]

def color_name(color_code):
    COLORS = {
    "3F7E00": "darkgreen",
    "5BA829": "green",
    "9ACD32": "lightgreen",
    "CDD614": "orange",
    "FFBA00": "red",
    "CBCBC8": "darkred",
    "FF7800": "darkred",
    }
    return COLORS[color_code]

def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df

def cidades_mais(df):
    cols = ['City', 'Restaurant ID', 'Country Name']
    cidades_mais_restaurantes = (df.loc[:, cols].groupby(['City', 'Country Name'])
                                .count().sort_values('Restaurant ID', ascending=False)
                                .head(quant_cidades)
                                .reset_index())
    fig = px.bar(cidades_mais_restaurantes, x='City', y='Restaurant ID',
                color='Country Name',
                labels={'City':'Cidade', 'Restaurant ID': 'Total de Restaurantes', 'Country Name':'País'},
                text_auto=True)
    fig.update_traces(textposition='outside', textangle=0)
    return fig

def rest_media(df, valor, operador=['maior', 'menor']):
    cols = ['City', 'Aggregate rating', 'Country Name']
    if operador == 'maior':
        df_filtrado = df[df.loc[:, 'Aggregate rating'] > valor]
    elif operador =='menor':
        df_filtrado = df[df.loc[:, 'Aggregate rating'] < valor]
    restaurante_acima4 = (df_filtrado.loc[:, cols].groupby(['City', 'Country Name'])
                        .count()
                        .sort_values('Aggregate rating', ascending=False)
                        .head(quant_cidades)).reset_index()
    fig = px.bar(restaurante_acima4, x='City', y='Aggregate rating',
                color='Country Name',
                labels={'City':'Cidade', 'Aggregate rating': 'Total de Restaurantes', 'Country Name':'País'},
                text_auto=True)
    fig.update_traces(textposition='outside', textangle=0)
    return fig

def cidades_maiorvariedade(df):
    cols = ['City', 'Cuisines', 'Country Name']
    cidades_cuisines = (df.loc[:, cols].groupby(['City', 'Country Name'])
                        .nunique().sort_values('Cuisines', ascending=False)
                        .head(quant_cidades).reset_index())
    fig = px.bar(cidades_cuisines, x='City', y='Cuisines',
                color='Country Name',
                labels={'City':'Cidade', 'Cuisines': 'Total de Restaurantes', 'Country Name':'País'}, text_auto=True)
    fig.update_traces(textposition='outside', textangle=0)
    return fig
    

df['Country Name'] = df['Country Code'].map(country_name)
df["Cuisines"] = df.loc[:, "Cuisines"].astype(str).apply(lambda x: x.split(",")[0])

# =================================================================================
# STREAMLIT
# SIDEBAR
script_dir = os.path.dirname(os.path.realpath(__file__))
caminho_imagem = os.path.join(script_dir, "../pages/zomato-logo.jpg")
image = Image.open(caminho_imagem)
st.sidebar.image(image, width=350)
st.sidebar.title('ZOMATO RESTAURANTS')
st.sidebar.markdown('# For the love of Food')
st.sidebar.markdown("""---""")
st.sidebar.markdown('## Filtros')
#Filtro País
country_filter = st.sidebar.multiselect(
    "Escolha o País que deseja visualizar as informações:",
    PAISES,
    default=PAISES
)
linhas_selecionadas = df['Country Name'].isin(country_filter)
df = df.loc[linhas_selecionadas, :]
quant_cidades = st.sidebar.slider('Quantas cidades quer visualizar?', 1, 20, 10)

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Desenvolvido por: Juliano B Nicoletti')

#LAYOUT STREAMLIT

st.title('Visão Cidades')
st.markdown('---')

with st.container():
    st.subheader('Cidades com mais Restaurantes')
    fig = cidades_mais(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Cidades Restaurantes com média acima de 4')
        fig = rest_media(df, 4, 'maior')
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.subheader('Cidades com Restaurantes com média abaixo de 2,5')
        fig = rest_media(df, 2.5, 'menor')
        st.plotly_chart(fig, use_container_width=True)
        
st.markdown('---')
with st.container():
    st.subheader('Cidades com maior variedade de tipos culinários')
    fig = cidades_maiorvariedade(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')
    