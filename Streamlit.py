import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.offline as pyo # Paga gerar arquivo html fora do Jupyter


### PASSO1: Criação das Fuções a serem usadas no DashBoard Streamlit
df = pd.read_excel('out/Final_df.xlsx')
df = df.loc[df['dt_emissao'].dt.year != 2010].reset_index()

## Gráfico 1: Total de Vendas por período
def total_vendas_period(period):
    # Imput da pase de Dados
    slice_df = df.copy()
    slice_df = slice_df.groupby(by=['num_nfe', 'dt_emissao']).sum()

    slice_df = slice_df.reset_index(0).sort_index()
    m = slice_df.resample(period).sum()
    #### Início Plotly ###
    ## Parte 1: Montagem dos "Traces"
    trace_subtotal = go.Bar(
        x=m.index,
        y=m['sub_total'],
        name = 'Sub Total',
        marker=dict(color='#319ee0'), # set the marker color to gold
        #xperiod="M1",
        xperiodalignment="start"
    )

    trace_qtd = go.Scatter(
         x=m.index,
         y=m['qtd'] * 10,
         name='Quant. x10',
         #marker=dict(color='#2de88e'),
         marker_color='red',
         #mode='lines',
         mode='lines+markers',
        #xperiod="M1",
        xperiodalignment="start"
    )

    ## Parte 2: Montagem do Layout
    data = [trace_subtotal, trace_qtd]
    layout = go.Layout(
        title=f'Sub Total de Vendas Periodo: {period}',
        barmode='stack',
        width=1400, 
        height=400,
        plot_bgcolor='rgba(255,255,255,1)',
    )
    fig = go.Figure(data=data, layout=layout)
    return fig

## Gráfico 2: Análise CPF CNPJ
def vendas_cpf_cnpj(barmode='group', period='M'):
    slice_cpf_cnpj = df.copy()
    slice_cpf_cnpj.set_index('dt_emissao', inplace=True)
    df_cnpj = slice_cpf_cnpj.loc[slice_cpf_cnpj['tipo_comprador'] == 'CNPJ'].resample(period).sum()
    df_cpf = slice_cpf_cnpj.loc[slice_cpf_cnpj['tipo_comprador'] == 'CPF'].resample(period).sum()
    
    trace_cnpj = go.Bar(
            x = list(df_cnpj.index),
            y = df_cnpj['sub_total'],
            opacity=0.7,
            #mode='lines',
            marker=dict(color='#319ee0'),
            name='CNPJ'
        )
    trace_cpf = go.Bar(
            x = list(df_cpf.index),
            y = df_cpf['sub_total'],
            #mode='lines',
            marker=dict(color='#ef25f6'),
            name='CPF'
        )
    data = [trace_cpf, trace_cnpj]
    layout= go.Layout(
        title='CPF Vs. CNPJ',
        barmode=barmode,
        width=1400, 
        height=400,
        #paper_bgcolor='rgba(255,255,255,0.5)',
        plot_bgcolor='rgba(255,255,255,1)',
        )
    
    fig = go.Figure(data=data, layout=layout)
    return fig
    
    ## Busca por nome de Produto
dff = df.copy()
def busca_por_keyword(period, keyword1='Penalty', keyword2=None, keyword3=None):
    keyword1 = keyword1.title()
    a = dff.loc[( dff['nome_prod'].str.contains(keyword1) )]

    if keyword2: #Se possui 2a Keyword, gera Df com 2a Key e concatena com a 1a Df
        keyword2 = keyword2.title()
        b = dff.loc[( dff['nome_prod'].str.contains(keyword2) )]
        a = pd.concat([a, b])

    if keyword3:   #Se possui 3a Keyword, gera Df com 3a Key e concatena com a 1a e 2a Df 
        keyword3 = keyword3.title()
        c = dff.loc[( dff['nome_prod'].str.contains(keyword3) )]
        a = pd.concat([a, c])

  
    a.set_index('dt_emissao', inplace=True)
    a.drop_duplicates(inplace=True)
    a = a[['qtd', 'sub_total']]
    a.sort_index(inplace=True)

    df = a.resample(period).sum()

    ## início Plotly Keyword
    trace_subtotal = go.Bar(
        x = list(df.index),
        y = df['sub_total'],
        opacity=0.7,
        #mode='lines',
        marker=dict(color='#319ee0'),
        name='Subtotal'
    )

    trace_qtd = go.Scatter(
        x=df.index,
        y=df['qtd'] * 10,
        name='Quant. x10',
        #marker=dict(color='#2de88e'),
        marker_color='red',
        #mode='lines',
        mode='lines+markers',
        xperiodalignment="start",
        #xperiod="M1",
)
    ## Parte 2: Montagem do Layout
    data = [trace_subtotal, trace_qtd]
    layout = go.Layout(
    title=f'Sub Total de Vendas Mensais: Periodo {period}, Keywords: {keyword1} {keyword2} {keyword3}',
    barmode='stack',
    width=1400, 
    height=400,
    plot_bgcolor='rgba(255,255,255,1)',
    #rangemode = "tozero",
    
)
    fig = go.Figure(data=data, layout=layout)
    return(fig)


### PASSO2: Geração DashBoard Streamlit

st.set_page_config(layout="wide")

## SIDEBAR
st.sidebar.header('Total de Vendas')
period = st.sidebar.radio( 'Período', ('YS', 'M', 'W', 'D')  )

st.sidebar.markdown('___')


st.sidebar.header('CPF/CNPJ')
barmodes = st.sidebar.select_slider('Estilo de Barras:', ('group', 'stack'))

st.sidebar.markdown('___')
st.sidebar.header('Produtos')
st.sidebar.text('Ex. Adidas, Penalty')
keyword1 = st.sidebar.text_input('keyword1', )
keyword2 = st.sidebar.text_input('keyword2',)
keyword3 = st.sidebar.text_input('keyword3')


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