# gerar_dashboard.py
import pandas as pd
import plotly.express as px
import panel as pn

# --- CONFIGURAÇÃO DAS COLUNAS ---
# ATENÇÃO: Verifique se os nomes abaixo correspondem EXATAMENTE
# aos nomes das colunas no seu arquivo CSV.
# Se algum for diferente, altere apenas o texto à direita.

COLUNA_DATA = 'data da venda'
COLUNA_VALOR_VENDA = 'Valor total da venda'
COLUNA_REGIONAL = 'regional'
COLUNA_CONSULTOR = 'consultor'
COLUNA_UNIDADE_NEGOCIO = 'unid negocio'
COLUNA_TIPO_CONTRATO = 'modalidade'

# -----------------------------------

# Garante que a extensão do Plotly seja carregada
pn.extension('plotly')

# Carrega os dados do seu arquivo CSV
try:
    # Tenta carregar com ponto e vírgula, que é comum em CSVs brasileiros
    df = pd.read_csv('dados.csv', sep=';')
except Exception:
    # Se falhar, tenta com vírgula, o padrão universal
    df = pd.read_csv('dados.csv', sep=',')

# --- LIMPEZA E PREPARAÇÃO DOS DADOS ---

# 1. Converte a coluna de data para o formato de data, esperando o dia primeiro (formato BR)
df[COLUNA_DATA] = pd.to_datetime(df[COLUNA_DATA], dayfirst=True, errors='coerce')

# 2. Limpa e converte a coluna de valor para um formato numérico
#    - Garante que a coluna seja tratada como texto para a limpeza
#    - Remove 'R$' e espaços em branco
#    - Remove o ponto de milhar
#    - Troca a vírgula do decimal por um ponto
#    - Converte o resultado para um número, tratando erros
df[COLUNA_VALOR_VENDA] = df[COLUNA_VALOR_VENDA].astype(str)
df[COLUNA_VALOR_VENDA] = df[COLUNA_VALOR_VENDA].str.replace('R$', '', regex=False).str.strip()
df[COLUNA_VALOR_VENDA] = df[COLUNA_VALOR_VENDA].str.replace('.', '', regex=False)
df[COLUNA_VALOR_VENDA] = df[COLUNA_VALOR_VENDA].str.replace(',', '.', regex=False)
df[COLUNA_VALOR_VENDA] = pd.to_numeric(df[COLUNA_VALOR_VENDA], errors='coerce')

# Remove linhas onde a conversão de data ou valor falhou
df.dropna(subset=[COLUNA_DATA, COLUNA_VALOR_VENDA], inplace=True)


# --- CÁLCULO DOS KPIs ---

faturamento_total = df[COLUNA_VALOR_VENDA].sum()
total_contratos = len(df)
ticket_medio = faturamento_total / total_contratos if total_contratos > 0 else 0

# --- CRIAÇÃO DOS GRÁFICOS ---

# Gráfico 1: Vendas por Regional
vendas_regional = px.bar(
    df.groupby(COLUNA_REGIONAL)[COLUNA_VALOR_VENDA].sum().sort_values(ascending=False).reset_index(),
    x=COLUNA_REGIONAL, y=COLUNA_VALOR_VENDA,
    title='Faturamento por Regional', text_auto='.2s'
).update_layout(yaxis_title='Faturamento (R$)', xaxis_title='Regional')

# Gráfico 2: Top 10 Consultores
top_10_consultores = df.groupby(COLUNA_CONSULTOR)[COLUNA_VALOR_VENDA].sum().nlargest(10).sort_values().reset_index()
vendas_consultor = px.bar(
    top_10_consultores,
    x=COLUNA_VALOR_VENDA, y=COLUNA_CONSULTOR,
    title='Top 10 Consultores por Faturamento', text_auto='.2s', orientation='h'
).update_layout(xaxis_title='Faturamento (R$)', yaxis_title='Consultor')

# Gráfico 3: Vendas por Unidade de Negócio
vendas_unidade_negocio = px.pie(
    df, names=COLUNA_UNIDADE_NEGOCIO, values=COLUNA_VALOR_VENDA,
    title='Faturamento por Unidade de Negócio', hole=0.4
)

# Gráfico 4: Evolução do Faturamento Mensal
df_mensal = df.set_index(COLUNA_DATA).groupby(pd.Grouper(freq='M'))[COLUNA_VALOR_VENDA].sum().reset_index()
evolucao_vendas = px.line(
    df_mensal, x=COLUNA_DATA, y=COLUNA_VALOR_VENDA,
    title='Evolução Mensal do Faturamento', markers=True
).update_layout(xaxis_title='Mês', yaxis_title='Faturamento (R$)')


# --- MONTAGEM DO LAYOUT DO DASHBOARD ---

# Cria os componentes de KPI
kpi_faturamento = pn.indicators.Number(name='Faturamento Total', value=faturamento_total, format='R$ {:,.2f}')
kpi_ticket_medio = pn.indicators.Number(name='Ticket Médio', value=ticket_medio, format='R$ {:,.2f}')
kpi_total_contratos = pn.indicators.Number(name='Total de Contratos', value=total_contratos, format='{value:,.0f}')

dashboard = pn.Column(
    pn.Row(
        pn.pane.Markdown("# Dashboard de Vendas Estratégico", styles={'font-size': '24pt', 'margin-left': '20px'}),
        align='center'
    ),
    pn.Row(
        kpi_faturamento, kpi_ticket_medio, kpi_total_contratos,
        align='center', styles={'gap': '2em'}
    ),
    pn.layout.Divider(),
    pn.Row(
        pn.Column(vendas_regional, evolucao_vendas),
        pn.Column(vendas_consultor, vendas_unidade_negocio)
    ),
    sizing_mode='stretch_width'
)

# --- SALVAR O DASHBOARD ---
dashboard.save(
    'index.html',
    embed=True,
    title='Dashboard de Vendas'
)

print("Dashboard 'index.html' gerado com sucesso.")
