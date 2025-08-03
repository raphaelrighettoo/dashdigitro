# gerar_dashboard.py
import pandas as pd
import plotly.express as px
import panel as pn

# --- CONFIGURAÇÃO DAS COLUNAS ---
# ATENÇÃO: Altere os nomes à direita para que correspondam EXATAMENTE
# aos nomes das colunas no seu arquivo CSV.
COLUNA_DATA = 'Data da Venda'
COLUNA_VALOR = 'Valor'
COLUNA_REGIAO = 'Região'
# -----------------------------------

# Garante que a extensão do Plotly seja carregada
pn.extension('plotly')

# Carrega os dados do seu arquivo CSV
try:
    # Tenta carregar com ponto e vírgula
    df = pd.read_csv('dados.csv', sep=';')
except Exception:
    # Se falhar, tenta com vírgula
    df = pd.read_csv('dados.csv', sep=',')

# --- LIMPEZA E PREPARAÇÃO DOS DADOS ---

# 1. Converte a coluna de data para o formato de data, esperando o dia primeiro
df[COLUNA_DATA] = pd.to_datetime(df[COLUNA_DATA], dayfirst=True)

# 2. Limpa e converte a coluna de valor para um formato numérico
#    - Remove 'R$' e espaços em branco
#    - Troca o ponto de milhar por nada
#    - Troca a vírgula do decimal por um ponto
#    - Converte o resultado para um número (float)
df[COLUNA_VALOR] = df[COLUNA_VALOR].astype(str).str.replace('R$', '', regex=False).str.strip()
df[COLUNA_VALOR] = df[COLUNA_VALOR].str.replace('.', '', regex=False)
df[COLUNA_VALOR] = df[COLUNA_VALOR].str.replace(',', '.', regex=False)
df[COLUNA_VALOR] = pd.to_numeric(df[COLUNA_VALOR])

# --- Criar os Componentes do Dashboard ---

# KPI: Faturamento Total
faturamento_total = df[COLUNA_VALOR].sum()
kpi_faturamento = pn.indicators.Number(
    name='Faturamento Total',
    value=faturamento_total,
    format='R$ {:,.2f}',
    font_size='32pt',
    align='center'
)

# Gráfico 1: Vendas por Região
vendas_por_regiao = px.bar(
    df.groupby(COLUNA_REGIAO)[COLUNA_VALOR].sum().reset_index(),
    x=COLUNA_REGIAO,
    y=COLUNA_VALOR,
    title='Vendas por Região',
    labels={
        COLUNA_VALOR: 'Total de Vendas (R$)',
        COLUNA_REGIAO: 'Região'
    }
)

# Gráfico 2: Evolução das Vendas
vendas_no_tempo = px.line(
    df.sort_values(COLUNA_DATA),
    x=COLUNA_DATA,
    y=COLUNA_VALOR,
    title='Evolução das Vendas',
    labels={
        COLUNA_VALOR: 'Valor da Venda (R$)',
        COLUNA_DATA: 'Data'
    }
)

# --- Montar o Layout do Dashboard ---
dashboard = pn.Column(
    pn.Row(
        "# 📊 Dashboard de Vendas",
        align='center'
    ),
    pn.Row(
        kpi_faturamento,
        align='center'
    ),
    pn.Row(
        vendas_por_regiao,
        vendas_no_tempo
    ),
    sizing_mode='stretch_width'
)

# --- Salvar o Dashboard como um arquivo HTML estático ---
dashboard.save(
    'index.html',
    embed=True,
    title='Dashboard de Vendas'
)

print("Dashboard 'index.html' gerado com sucesso.")
