# Libraries

from haversine import haversine
import plotly.express as px
import plotly.graph_objects as go

# Necessary Libraries
import pandas as pd
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title = 'Visão Entregadores', page_icon = '🚚', layout = 'wide')

#--------------------------------------
#Funções
#--------------------------------------
def top_delivers(df1, top_asc):

    df2 = (df1.loc[:, ['Delivery_person_ID', 'City', 'Time_taken(min)']]
              .groupby(['City', 'Delivery_person_ID'])
              .mean()
              .reset_index()
              .sort_values('Time_taken(min)', ascending = top_asc))

    df_aux01 = df2.loc[df2['City'] == 'Metropolitian', :].head(10)
    df_aux02 = df2.loc[df2['City'] == 'Urban', :].head(10)
    df_aux03 = df2.loc[df2['City'] == 'Semi-Urban', :].head(10)

    df3 = pd.concat( [df_aux01, df_aux02, df_aux03] ).reset_index( drop = True)
    return df3

def clean_code( df1 ):
    """ Esta função tem a responsabilidade de limpar o dataframe 
    
        Tipos de limpeza:
        1. Remoção dos dados NaN;
        2. Mudança do tipo da coluna de dados;
        3. Remoção dos espaços das variáveis de texto;
        4. Formatação da coluna de datas;
        5. Limpeza da coluna de tempo (remoção do texto da variável número).
        
        Input: Dataframe
        Output: Dataframe
    """
    #Retirando a sujeira
    linhas_selecionadas = df1['Delivery_person_Age'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['Road_traffic_density'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['City'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()

    linhas_selecionadas = df1['Festival'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()
    #Convertendo a coluna Age para número
    df1['Delivery_person_Age'] = df1['Delivery_person_Age'].astype(int)

    #Convertendo a coluna Ratings de str para float
    df1['Delivery_person_Ratings'] = df1['Delivery_person_Ratings'].astype(float)

    #Convertendo a coluna  Order_Date de string para Data
    df1['Order_Date'] = pd.to_datetime(df1['Order_Date'], format = '%d-%m-%Y')

    #Convertendo multiples_delivery de str para int
    linhas_selecionadas = df1['multiple_deliveries'] != 'NaN '
    df1 = df1.loc[linhas_selecionadas, : ].copy()
    df1['multiple_deliveries'] = df1['multiple_deliveries'].astype(int)

    #Removendo os espaços dentro de strings
    df1 = df1.reset_index(drop=True)
    # for i in range(len(df1)):
    #   df1.loc[i, 'ID'] = df1.loc[i, 'ID'].strip()
    df1.loc[:, 'ID'] = df1.loc[:, 'ID'].str.strip()
    df1.loc[:, 'Road_traffic_density'] = df1.loc[:, 'Road_traffic_density'].str.strip()
    df1.loc[:, 'Type_of_order'] = df1.loc[:, 'Type_of_order'].str.strip()
    df1.loc[:, 'Type_of_vehicle'] = df1.loc[:, 'Type_of_vehicle'].str.strip()
    df1.loc[:, 'City'] = df1.loc[:, 'City'].str.strip()
    df1['Festival'] = df1['Festival'].str.strip()

    # Comando para remover o texto de números
    # df1['Time_taken(min)'] = df1['Time_taken(min)'].apply(lambda x: re.findall( r'\d+', x))
    df1['Time_taken(min)'] = df1['Time_taken(min)'].apply( lambda x: x.split( '(min) ')[1] )
    df1['Time_taken(min)'] = df1['Time_taken(min)'].astype(int)
    return df1

# Import dataset
df_raw = pd.read_csv('dataset/train.csv')

#Criando uma copia
df1 = df_raw.copy()

#Cleaning dataset
df1 = clean_code( df1 )

#==================================================
# Barra Lateral
#==================================================
st.header('Marketplace - Visão Entregadores')
# image_path = 'logo.png'
image = Image.open( 'logo.png' )
st.sidebar.image( image, width=120)

st.sidebar.markdown( '### Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown("""---""")

st.sidebar.markdown('## Selecione uma data limite')
date_slider = st.sidebar.slider(
    'Até qual valor?',
    value = pd.datetime( 2022, 4, 13),
    min_value=pd.datetime(2022, 2, 11),
    max_value=pd.datetime(2022, 4, 6),
    format ='DD-MM-YYYY')

st.sidebar.markdown("""---""")

traffic_options = st.sidebar.multiselect(
    'Quais as condições do trânsito',
    ['Low','Medium','High','Jam'],
    default=['Low','Medium','High','Jam'])
st.sidebar.markdown("""---""")
st.sidebar.markdown('### Powered by Comunidade DS')

#Filtros de data
linhas_selecionadas = df1['Order_Date'] < date_slider
df1 = df1.loc[linhas_selecionadas, :]

#Filtro de trânsito
linhas_selecionadas = df1['Road_traffic_density'].isin(traffic_options)
df1 = df1.loc[linhas_selecionadas, :]

#==================================================
# Layout no Streamlit
#==================================================

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', '_', '_'])

with tab1:
    with st.container():
        st.title('Overall Metrics')
        col1, col2, col3, col4 = st.columns( 4, gap = 'large' )
        with col1:
            maior_idade = df1["Delivery_person_Age"].max()
            col1.metric( 'Maior idade', maior_idade)
        with col2:
            menor_idade = df1["Delivery_person_Age"].min()
            col2.metric( 'Menor idade', menor_idade)
        with col3:
            melhor_condicao_veiculo = df1["Vehicle_condition"].max()
            col3.metric('Melhor condição', melhor_condicao_veiculo)
        with col4:
            pior_condicao_veiculo = df1["Vehicle_condition"].min()
            col4.metric('Pior condição', pior_condicao_veiculo)
    with st.container():
        st.markdown ("""---""")
        st.title('Avalições')
        
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown('##### Avaliação média por entregador')
            df_avg_ratings_per_delivery = (df1.loc[:,['Delivery_person_Ratings', 'Delivery_person_ID']]
                                              .groupby(['Delivery_person_ID'])
                                              .mean()
                                              .sort_values('Delivery_person_Ratings', ascending = False)
                                              .reset_index())
            st.dataframe(df_avg_ratings_per_delivery)
        with col2:
            st.markdown('##### Avaliação média por trânsito')
            df_std_avg_by_traffic = (df1.loc[:, ['Delivery_person_Ratings', 'Road_traffic_density']]
                                        .groupby(['Road_traffic_density'])
                                        .agg({'Delivery_person_Ratings' : ['mean', 'std']}))
            # mudança de nome das colunas
            df_std_avg_by_traffic.columns = ['mean_ratings', 'std_ratings']
            # reset do index
            df_std_avg_by_traffic = df_std_avg_by_traffic.reset_index()
            st.dataframe(df_std_avg_by_traffic)
            
            
            st.markdown('##### Avaliação média por clima')
            df_std_avg_by_weather_conditions = (df1.loc[:, ['Delivery_person_Ratings', 'Weatherconditions']]
                                                   .groupby(['Weatherconditions'])
                                                   .agg({'Delivery_person_Ratings' : ['mean', 'std']}))
            df_std_avg_by_weather_conditions.columns = ['mean_ratings', 'std_ratings']
            df_std_avg_by_weather_conditions = df_std_avg_by_weather_conditions.reset_index()
            st.dataframe(df_std_avg_by_weather_conditions)
    with st.container():
        st.markdown ("""---""")
        st.title('Velocidade de entrega')
        col1, col2 = st.columns( 2 )
        with col1:
            st.markdown('##### Top entregadores mais rápidos')
            df3 = top_delivers( df1, top_asc = True )
            st.dataframe(df3)
        with col2:
            st.markdown('##### Top entregadores mais lentos')
            df3 = top_delivers( df1, top_asc = False )
            st.dataframe(df3)