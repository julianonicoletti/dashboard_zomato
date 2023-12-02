import os
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import inflection
import datetime
from PIL import Image
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import folium_static
import time

st.set_page_config(page_title='Visão Geral', layout='wide')

script_dir = os.path.dirname(os.path.realpath(__file__))
file_path = os.path.join(script_dir, "../dataset/zomato.csv")
df = pd.read_csv(file_path)

def gerar_mapa(df):
    cols = ['Restaurant Name', 'Average Cost for two', 'Longitude',
        'Latitude', 'Cuisines', 'Aggregate rating', 'Rating color']

    df_aux = df.loc[:, cols]
    map = folium.Map()
    marker_cluster = MarkerCluster().add_to(map)
    for index, location_info in df_aux.iterrows():
            icon = folium.Icon(color=color_name(location_info['Rating color']), icon='cutlery', prefix='fa') 
            html = f'''
            <b>{location_info['Restaurant Name']}</b><br>
            Price: $ {location_info['Average Cost for two']} para dois<br>
            Type: {location_info['Cuisines']}<br>
            Rating: {location_info['Aggregate rating']}
            '''
            iframe = folium.IFrame(html, width=200, height=120)
            popup = folium.Popup(iframe, max_width=150)
            
            folium.Marker([location_info[ 'Latitude'],
                    location_info['Longitude']],
                    icon=icon,
                    popup=popup).add_to(marker_cluster)
            
    folium.LayerControl().add_to(map)
    return map


def country_name(country_id):
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
st.sidebar.markdown('### Desenvolvido por: Juliano B Nicoletti')
st.sidebar.markdown("""---""")

#LAYOUT STREAMLIT
with st.container():
    st.markdown('# Visão Geral')
    st.markdown('---')
    

with st.container():
    st.header('Dados Gerais')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1: 
        paises_unicos = len(df.loc[:, 'Country Name'].unique())
        col1.metric('Países', paises_unicos)    
    with col2:
        cidades_cadastradas = len (df.loc[:, 'City'].unique())
        col2.metric('Cidades', cidades_cadastradas)
    with col3:
        restaurantes_cadastrados = len (df.loc[:, 'Restaurant ID'].unique())
        col3.metric('Restaurantes', restaurantes_cadastrados)
    with col4:
        total_culinaria = len(df.loc[:, 'Cuisines'].unique())
        col4.metric('Culinárias diferentes', total_culinaria)
    with col5:
        total_avaliações = df.loc[:, 'Votes'].sum()
        col5.metric('Total Avaliações', total_avaliações)
    st.markdown('---')

with st.container():
    st.header('Restaurantes pelo Mundo')
    map1 = gerar_mapa(df)
    folium_static(map1, width=1024, height=600)
    
    
