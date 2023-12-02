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


st.set_page_config(page_title='Visão Culinárias', layout='wide')

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, "../dataset/zomato.csv")
df = pd.read_csv(file_path)

def melhor_cuisine(cuisine):
    filtro = df[df.loc[:,'Cuisines'] == cuisine]
    melhor_cuisine = (filtro.loc[:, ['Restaurant Name', 'Aggregate rating', 'Restaurant ID']]
                    .groupby('Restaurant Name').max()
                    .sort_values(['Aggregate rating', 'Restaurant ID'], ascending=[False, True])
                    .reset_index().head(1))
    return melhor_cuisine

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

def top10_melhor(df1):
    cols=['Restaurant Name', 'Country Name', 'City', 'Cuisines', 'Average Cost for two', 'Aggregate rating', 'Votes']
    outliers = ['India', 'Indonesia', 'Philippines']
    df_filtrado = df.loc[df['Country Name'].isin(outliers)==False]

    melhores_restaurantes = (df_filtrado.loc[:,cols].groupby(cols)
                            .max().sort_values(['Aggregate rating', 'Votes'], ascending=False)
                            .head(10).reset_index())
    return melhores_restaurantes


def avaliacao_cuisine(df, filtro):
    cols = ['Aggregate rating', 'Cuisines']
    df_filtrado = df.loc[(df['Aggregate rating']!=0) & (df['Cuisines']!='nan')]
    pior_cuisine = (df_filtrado.loc[:, cols].groupby('Cuisines')
                    .mean().round(2).sort_values('Aggregate rating', ascending=filtro)
                    .head(12)).reset_index()
    fig = px.bar(pior_cuisine, x='Cuisines', y='Aggregate rating',
                labels={'Cuisines': 'Tipo de Culinária', 'Aggregate rating':'Média da Avaliação'},
                text_auto=True)
    fig.update_traces(textposition='outside', textangle=0)
    return fig

def top10_forabrasil (df):
    st.subheader('Top 10 restaurantes de comida brasileira fora do Brasil')
    df_filtrado = df.loc[(df['Cuisines']=='Brazilian') & (df['Country Name']!='Brazil')]

    cols = ['Restaurant Name','City', 'Country Name', 'Average Cost for two', 'Aggregate rating', 'Votes']
    brasileiros_forabrazil = (df_filtrado.loc[:, cols].groupby(cols)
                            .max().sort_values(['Aggregate rating', 'Votes'], ascending=[False, False])
                            .head(10).reset_index())
    return brasileiros_forabrazil
    

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
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Desenvolvido por: Juliano B Nicoletti')

#LAYOUT STREAMLIT

st.title('Visão Culinária')
st.markdown('---')

with st.container():
    st.subheader('Melhores restaurantes das Principais Culinárias')
    col1, col2, col3 = st.columns(3)
    with col1:
        top = melhor_cuisine('North Indian')
        name = top.loc[0, 'Restaurant Name']
        aggregate = top.loc[0, 'Aggregate rating']
        st.metric(label=(f'Comida Indiana:\n {name}'), value=(f'{aggregate}/5.0'))
    with col2:
        top = melhor_cuisine('American')
        name = top.loc[0, 'Restaurant Name']
        aggregate = top.loc[0, 'Aggregate rating']
        st.metric(label=(f'Comida Americana:\n {name}'), value=(f'{aggregate}/5.0'))
    with col3:
        top = melhor_cuisine('Cafe')
        name = top.loc[0, 'Restaurant Name']
        aggregate = top.loc[0, 'Aggregate rating']
        st.metric(label=(f'Café:\n {name}'), value=(f'{aggregate}/5.0'))
with st.container():
    col4, col5, col6 = st.columns(3)
    with col4:
        top = melhor_cuisine('Pizza')
        name = top.loc[0, 'Restaurant Name']
        aggregate = top.loc[0, 'Aggregate rating']
        st.metric(label=(f'Pizza:\n {name}'), value=(f'{aggregate}/5.0'))
    with col5:
        top = melhor_cuisine('Italian')
        name = top.loc[0, 'Restaurant Name']
        aggregate = top.loc[0, 'Aggregate rating']
        st.metric(label=(f'Comida Italiana:\n {name}'), value=(f'{aggregate}/5.0'))
    with col6:
        top = melhor_cuisine('Brazilian')
        name = top.loc[0, 'Restaurant Name']
        aggregate = top.loc[0, 'Aggregate rating']
        st.metric(label=(f'Comida Brasileira:\n {name}'), value=(f'{aggregate}/5.0'))
st.markdown('---')

with st.container():
    st.subheader('Top 10 melhores Restaurantes do Mundo')
    melhores_restaurantes = top10_melhor(df)
    st.dataframe(melhores_restaurantes, use_container_width=True, hide_index=True)
    st.markdown("ℹ️ *O critério de desempate foi a quantidade de Votos*")
st.markdown('---')

with st.container():
    col1, col2 = st.columns(2)
    with col1:  
        st.subheader('Tipos de Culinária mais bem avaliada')
        cuisine_bem = avaliacao_cuisine(df, False)
        st.plotly_chart(cuisine_bem, use_container_width=True)
    with col2:
        st.subheader('Tipos de culinária mais mal avaliada')
        cuisine_mal = avaliacao_cuisine(df, True)
        st.plotly_chart(cuisine_mal, use_container_width=True)
st.markdown('---')
        
with st.container():
    df_forabrasil = top10_forabrasil(df)
    st.dataframe(df_forabrasil, use_container_width=True, hide_index=True)