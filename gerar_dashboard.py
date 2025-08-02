{\rtf1\ansi\ansicpg1252\cocoartf2822
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\paperw11900\paperh16840\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # gerar_dashboard.py\
\
import pandas as pd\
import plotly.express as px\
import panel as pn\
\
# Garante que a extens\'e3o do Plotly seja carregada para o Panel\
pn.extension('plotly')\
\
# --- 1. Carregar e Preparar os Dados ---\
# Carrega os dados do seu arquivo CSV.\
# Use um tratamento de erro para caso o arquivo n\'e3o seja encontrado.\
try:\
    df = pd.read_csv('dados.csv', parse_dates=['Data da Venda'])\
except FileNotFoundError:\
    print("Arquivo 'dados.csv' n\'e3o encontrado! Crie um com algumas colunas para testar.")\
    # Cria um DataFrame de exemplo se o arquivo n\'e3o existir\
    df = pd.DataFrame(\{\
        'Data da Venda': pd.to_datetime(['2024-01-15', '2024-01-20', '2024-02-10']),\
        'Vendedor': ['Ana', 'Bruno', 'Ana'],\
        'Regi\'e3o': ['Sul', 'Sudeste', 'Sul'],\
        'Valor': [500, 1200, 850]\
    \})\
\
# --- 2. Criar os Componentes do Dashboard (Gr\'e1ficos e KPIs) ---\
\
# KPI: Faturamento Total\
faturamento_total = df['Valor'].sum()\
kpi_faturamento = pn.indicators.Number(\
    name='Faturamento Total',\
    value=faturamento_total,\
    format='R$ \{:,.2f\}', # Formato de moeda\
    font_size='32pt',\
    align='center'\
)\
\
# Gr\'e1fico 1: Vendas por Regi\'e3o (Gr\'e1fico de Barras)\
vendas_por_regiao = px.bar(\
    df.groupby('Regi\'e3o')['Valor'].sum().reset_index(),\
    x='Regi\'e3o',\
    y='Valor',\
    title='Vendas por Regi\'e3o',\
    labels=\{'Valor': 'Total de Vendas (R$)', 'Regi\'e3o': 'Regi\'e3o do Brasil'\}\
)\
\
# Gr\'e1fico 2: Evolu\'e7\'e3o das Vendas no Tempo (Gr\'e1fico de Linha)\
vendas_no_tempo = px.line(\
    df.sort_values('Data da Venda'),\
    x='Data da Venda',\
    y='Valor',\
    title='Evolu\'e7\'e3o das Vendas no Tempo',\
    labels=\{'Valor': 'Valor da Venda (R$)', 'Data da Venda': 'Data'\}\
)\
\
\
# --- 3. Montar o Layout do Dashboard ---\
# Organize os componentes em colunas e linhas para criar o layout final.\
dashboard = pn.Column(\
    pn.Row(\
        "# \uc0\u55357 \u56522  Dashboard de Vendas da Empresa",\
        align='center'\
    ),\
    pn.Row(\
        kpi_faturamento,\
        align='center'\
    ),\
    pn.Row(\
        vendas_por_regiao,\
        vendas_no_tempo\
    ),\
    # Permite que o layout se ajuste ao tamanho da tela\
    sizing_mode='stretch_width' \
)\
\
# --- 4. Salvar o Dashboard como um arquivo HTML est\'e1tico ---\
# Esta \'e9 a parte mais importante!\
# 'embed=True' garante que todos os dados, JS e CSS sejam inclu\'eddos no arquivo.\
# O Netlify ir\'e1 procurar por um 'index.html' por padr\'e3o.\
dashboard.save(\
    'index.html',\
    embed=True, # Essencial para criar um arquivo aut\'f4nomo\
    title='Dashboard de Vendas'\
)\
\
print("Dashboard gerado com sucesso como 'index.html'")}