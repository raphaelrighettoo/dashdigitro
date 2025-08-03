# gerar_dashboard.py
import pandas as pd
import plotly.express as px
import panel as pn

# Garante que a extensão do Plotly seja carregada
pn.extension('plotly')

# Carrega os dados do seu arquivo CSV
try:
    # Tenta carregar com ponto e vírgula, informando que o dia vem primeiro
    df = pd.read_csv('dados.csv', sep=';', parse_dates=['Data da Venda'], dayfirst=True)
except Exception:
    # Se falhar, tenta com vírgula, também informando que o dia vem primeiro
    df = pd.read_csv('dados.csv', sep=',', parse_dates=['Data da Venda'], dayfirst=True)


# --- Criar os Componentes do Dashboard ---

# KPI: Faturamento Total
faturamento_total = df['Valor'].sum()
kpi_faturamento = pn.indicators.Number(
    name='Faturamento Total',
    value=faturamento_total,
    format='R$ {:,.2f}',
    font_size='32pt',
    align='center'
)

# Gráfico 1: Vendas por Região
vendas_por_regiao = px.bar(
    df.groupby('Região')['Valor'].sum().reset_index(),
    x='Região',
    y='Valor',
    title='Vendas por Região',
    labels={'Valor': 'Total de Vendas (R$)', 'Região': 'Região'}
)

# Gráfico 2: Evolução das Vendas
vendas_no_tempo = px.line(
    df.sort_values('Data da Venda'),
    x='Data da Venda',
    y='Valor',
    title='Evolução das Vendas',
    labels={'Valor': 'Valor da Venda (R$)', 'Data da Venda': 'Data'}
)

# Montar o Layout do Dashboard
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

# Salvar o Dashboard como um arquivo HTML estático
dashboard.save(
    'index.html',
    embed=True,
    title='Dashboard de Vendas'
)

print("Dashboard 'index.html' gerado com sucesso.")