import streamlit as st
from PIL import Image

st.set_page_config(
    page_title = "Home",
    page_icon = '📊'
)

# image_path = 'C:/Users/Breno/Documents/Repos/analises_de_dados_python/projeto_ftc/'
image = Image.open ('logo.png')
st.sidebar.image(image, width = 120)

st.sidebar.markdown( '### Cury Company' )
st.sidebar.markdown( '## Fastest Delivery in Town' )
st.sidebar.markdown("""---""")

st.write("# Curry Company Growth Dashboard")

st.markdown(
    """
    Growth Dashboard foi contruído para acompanhar as métricas de crescimento dos Entregadores e Restaurantes.
    ### Como utilizar esse Growth Dashboard?
    - Visão Empresa:
        - Visão Gerencial: Métricas gerais de comportamento.
        - Visão Tática: Indicadores semanais de crescimento.
        - Visão Geográfica: Insight de geolocalização.
    - Visão Entregador:
        - Acompanhamento dos indicadores semanais de crescimento.
    - Visão Restaurante:
        - Indicadores semanais de crescimento dos restaurantes.
    ### Ask for Help
    - favor entrar em contato brenolobracci@gmail.com
    """
)