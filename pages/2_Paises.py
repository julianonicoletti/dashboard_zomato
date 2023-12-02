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


st.set_page_config(page_title='Visão Países', layout='wide')

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

def rest_porpais(df):
    cols = ['Restaurant ID', 'Country Name']
    restaurantes_porpais = (df.loc[:, cols].groupby('Country Name').count().sort_values('Restaurant ID', ascending=False).reset_index())
    restaurantes_porpais2 = restaurantes_porpais[restaurantes_porpais['Country Name'] != 'India'].head(quant_paises)
    fig = px.bar(restaurantes_porpais2, x='Country Name', y='Restaurant ID',
                labels={'Restaurant ID': 'Quantidade de Restaurantes', 'Country Name': 'País'},
                text_auto=True,)
    return fig

def cidade_porpais(df):
    cols = ['City', 'Country Name']
    cidades_porpais = (df.loc[:, cols].groupby('Country Name').nunique().sort_values('City', ascending=False).reset_index())

    cidades_porpais2 = cidades_porpais[cidades_porpais['Country Name'] != 'India'].head(quant_paises)
    fig = px.bar(cidades_porpais2, x='Country Name', y='City',
                labels={'Country Name': 'País', 'City':'Quantidade de Cidades'}, text_auto=True)
    return fig

def media_porpais(df):
    cols = ['Country Name', 'Votes']
    media_votospais = df.loc[:, cols].groupby('Country Name').mean().sort_values('Votes', ascending=False).head(quant_paises).reset_index()
    fig = px.bar(media_votospais, x='Country Name', y='Votes',
                labels={'Country Name':'País', 'Votes':'Quantidade de Avaliações'}, text_auto=True)
    return fig

def maiores_notas(df):
    cols = ['Country Name', 'Aggregate rating']
    media_maiornota_pais = (df.loc[:, cols].groupby('Country Name')
                            .mean().round(2).sort_values('Aggregate rating', ascending=False).head(quant_paises).reset_index())
    fig = px.bar(media_maiornota_pais, x='Country Name', y='Aggregate rating',
                labels={'Country Name':'País', 'Aggregate rating':'Média das avaliações'}, text_auto=True)
    return fig

def mediana_preco(df):
    cols = ['Country Name', 'Average Cost for two']
    outliers = ['India', 'Indonesia', 'Philippines', 'Sri Lanka']
    df_semoutliers = df[~df['Country Name'].isin(outliers)]
    mediana_preco = (df_semoutliers.loc[:, cols].groupby('Country Name').median()
    .sort_values('Average Cost for two', ascending=False)
    .head(quant_paises).reset_index())
    fig = px.bar(mediana_preco, x='Country Name', y='Average Cost for two',
                labels={'Country Name': 'País', 'Average Cost for two': 'Custo Médio para 2 pessoas'},
                text_auto=True)
    return fig

def melhor_brasil(df):
    cols = ['Restaurant Name','City', 'Average Cost for two', 'Cuisines', 'Aggregate rating', 'Votes']
    df_filtrado = df.loc[(df['Country Name']=='Brazil')]
    melhores_brasil = (df_filtrado.loc[:, cols].groupby(cols)
                    .max().sort_values(['Aggregate rating','Votes'], ascending=False)
                    .head(10).reset_index())
    return melhores_brasil
    
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
st.sidebar.markdown('')

quant_paises = st.sidebar.slider('Quantos países quer visualizar?', 1, 15, 8)

st.sidebar.markdown("""---""")
st.sidebar.markdown('### Desenvolvido por: Juliano B Nicoletti')

# LAYOUT STREAMLIT
st.title('Visão Países')
st.markdown('---')

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.subheader('Quantidade de Restaurantes por País')
        fig = rest_porpais(df)
        st.plotly_chart(fig, use_container_width=True, theme='streamlit')
    with col2:
        st.subheader('Quantidade de Cidades por País')
        fig = cidade_porpais(df)        
        st.plotly_chart(fig, use_container_width=True)
st.markdown('---')

with st.container():
    st.subheader('Média de Avaliações por pais')
    fig = media_porpais(df)    
    st.plotly_chart(fig, use_container_width=True)
st.markdown('---')

with st.container():
    st.subheader('Maiores médias de nota por País')
    fig = maiores_notas(df)    
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')

with st.container():
    st.subheader('Mediana do Preço por País (prato para 2 pessoas)')
    fig = mediana_preco(df)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('---')

with st.container():
    st.subheader('Melhores Restaurantes do Brasil')
    melhores_brasil = melhor_brasil(df)
    st.dataframe(melhores_brasil, use_container_width=True, hide_index=True)
    st.markdown('---')


    
    
    

