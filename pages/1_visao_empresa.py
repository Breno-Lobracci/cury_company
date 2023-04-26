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

st.set_page_config(page_title = 'Visão Empresa', page_icon = '📈', layout = 'wide')

#--------------------------------------
#Funções
#--------------------------------------
def country_maps(df1):
    
    """ Esta função tem a responsabilidade de mapear os restaurantes"""
    data_plot = df1.loc[:, ['City', 'Road_traffic_density', 'Delivery_location_latitude', 'Delivery_location_longitude']].groupby( ['City', 'Road_traffic_density']).median().reset_index()
    # Desenhar o mapa
    map_ = folium.Map( zoom_start=11 )
    for index, location_info in data_plot.iterrows():
         folium.Marker( [location_info['Delivery_location_latitude'],
         location_info['Delivery_location_longitude']],
         popup=location_info[['City', 'Road_traffic_density']] ).add_to( map_ )

    folium_static(map_, width = 1024, height = 600)

def order_share_by_week( df1 ):
    """ Esta função tem a responsabilidade de calcular a quantidade entregas na semana dividido pela quantidade de entregadores únicos por semana
        Logo em seguida um gráfico de linha sera plotado
    """
    # Quantidade de pedidos por entregador por Semana
    # Quantas entregas na semana / Quantos entregadores únicos por semana
    df_aux1 = (df1.loc[:, ['ID', 'week_of_year']]
                  .groupby( 'week_of_year' )
                  .count()
                  .reset_index())
    df_aux2 = (df1.loc[:, ['Delivery_person_ID', 'week_of_year']]
                  .groupby( 'week_of_year')
                  .nunique()
                  .reset_index())
    
    df_aux = pd.merge( df_aux1, df_aux2, how='inner' )
    df_aux['order_by_delivery'] = df_aux['ID'] / df_aux['Delivery_person_ID']
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='order_by_delivery' )
    return fig

def order_by_week(df1):
    """ Esta função tem a responsabilidade de calcular a quantidade de pedidos por semana
        Sua resposta será em forma de um gráfico em linha
    """
    
    # Quantidade de pedidos por Semana
    df1['week_of_year'] = df1['Order_Date'].dt.strftime( "%U" )
    df_aux = df1.loc[:, ['ID', 'week_of_year']].groupby( 'week_of_year' ).count().reset_index()
    # gráfico
    fig = px.line( df_aux, x='week_of_year', y='ID' )
    return fig

def traffic_order_city( df1 ):
    """ Esta função tem a responsabilidade de calcular os pedidos junto ao tráfego 
        Sua resposta será em forma de um gráfico
    """
    
    df_aux = (df1.loc[:, ['ID', 'City', 'Road_traffic_density']]
                 .groupby(['City', 'Road_traffic_density'])
                 .count()
                 .reset_index())
    fig = px.scatter (df_aux, x = 'City', y = 'Road_traffic_density', size = 'ID', color = 'City')
    return fig


def traffic_order_share(df1):
    """ Esta função tem a responsabilidade de verificar a densisdade do trafego em relação ao pedidos
        Sua respota será em forma de um gráfico de pizza
    """            
    df_aux = (df1.loc[:, ['ID', 'Road_traffic_density']]
                 .groupby( 'Road_traffic_density' )
                 .count()
                 .reset_index())
    df_aux['perc_ID'] = 100 * ( df_aux['ID'] / df_aux['ID'].sum() )
    # gráfico
    fig = px.pie( df_aux, values='perc_ID', names='Road_traffic_density' )
                 
    return fig            

def order_metric( df1 ):
    """ Esta função tem a responsabilidade contar a quantidade de pedidos
        Ações:
        1. Utiliza a função count;
        2. cria coluna para o dia que o pedido foi feito 'order_date'
        3. cria coluna para quantidade de entregas 'qtde_entregas'
        4. Seleciona linhas
        5. Plota um gráfico de barras como resposta
    
    """
    
    #Seleção de linhas       
    df_aux = df1.loc[:, ['ID', 'Order_Date']].groupby( 'Order_Date' ).count().reset_index()
    df_aux.columns = ['order_date', 'qtde_entregas']
    # Desenhar gráfico        
    fig = px.bar( df_aux, x='order_date', y='qtde_entregas' )        
    return fig                        
        
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


#-------------------------------------- Ínicio da Estrutura Lógica do Código --------------------------------------
#--------------------------------------
# Import dataset
#--------------------------------------
df_raw = pd.read_csv('dataset/train.csv')

#--------------------------------------
#Criando uma copia
#--------------------------------------
df1 = df_raw.copy()

#--------------------------------------
#Limpando os dados
#--------------------------------------
df1 = clean_code( df1)


#==================================================
# Barra Lateral
#==================================================
st.header('Marketplace - Visão Cliente')
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

tab1, tab2, tab3 = st.tabs (['Visão Gerencial', 'Visão Tática', 'Visão Geográfica'])

with tab1:
    with st.container():
        #Order Metric
        fig = order_metric( df1 )
        st.markdown ('# Orders by Day')
        st.plotly_chart(fig , use_container_width = True)
        
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            fig = traffic_order_share( df1 )
            st.header("Traffic Order Share")
            st.plotly_chart( fig, use_container_width = True )
            
        with col2:
            st.header("Traffic Order City")
            fig = traffic_order_city( df1)
            st.plotly_chart( fig, use_container_width = True )
with tab2:
    with st.container():
        st.markdown( "# Order by Week")
        fig = order_by_week(df1)
        st.plotly_chart(fig, use_container_width = True )
        
    with st.container():
        st.markdown("# Order Share by Week")
        fig = order_share_by_week( df1 )
        st.plotly_chart(fig, use_container_width = True )
with tab3:
    st.markdown("# Country Maps")
    country_maps(df1)
