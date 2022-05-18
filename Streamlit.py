import pandas as pd
import streamlit as st
## Gerada as funções no arquivo "df_to_streamlit.py"
from df_to_streamlit import total_vendas_period, vendas_cpf_cnpj, busca_por_keyword


st.set_page_config(layout="wide")

#df = pd.read_pickle('out/Final_df.pkl')

## SIDEBAR
st.sidebar.header('Total de Vendas')
period = st.sidebar.radio( 'Período', ('YS', 'M', 'W', 'D')  )

st.sidebar.markdown('___')


st.sidebar.header('CPF/CNPJ')
barmodes = st.sidebar.select_slider('Estilo de Barras:', ('group', 'stack'))

st.sidebar.markdown('___')
st.sidebar.header('Produtos')
keyword1 = st.sidebar.text_input('keyword1', placeholder='Ex. Penalty')
keyword2 = st.sidebar.text_input('keyword2', placeholder='Ex. Nike')
keyword3 = st.sidebar.text_input('keyword3', placeholder='Ex. Adidas')


## Main page
### Total de Vendas no perído
total_vendas_graph = total_vendas_period(period)
st.plotly_chart(total_vendas_graph)


### Graph Cpf Cnpj
vendas_cpf_cnpj = vendas_cpf_cnpj(barmodes, period)
st.plotly_chart(vendas_cpf_cnpj)

### Graph Keywords
graph_keyword = busca_por_keyword(period, keyword1, keyword2, keyword3)
st.plotly_chart(graph_keyword)