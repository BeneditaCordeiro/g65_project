from flask import render_template, session
import sqlite3, json
import plotly.graph_objects as go
import pandas as pd

DB_PATH = 'data/projeto_grupo5.db'

def get_df(query):
    con = sqlite3.connect(DB_PATH)
    df = pd.read_sql(query, con)
    con.close()
    return df

def make_chart_json(fig):
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(family='Inter, Arial', color='#555', size=12),
        margin=dict(l=50, r=20, t=45, b=40),
    )
    return json.loads(fig.to_json())

def apps_dashboard():
    ulogin = session.get("user")
    if ulogin is None:
        return render_template("index.html", ulogin=None)

    NAVY   = '#1a2e4a'
    MID    = '#4a6fa5'
    LIGHT  = '#8aafd4'
    CREAM  = '#e8dfc8'

    # Chart 1: Transacoes por ano
    df_t = get_df('SELECT payment_date, amount FROM "Transaction"')
    df_t['year'] = pd.to_datetime(df_t['payment_date'], errors='coerce').dt.year
    by_year = df_t.groupby('year').agg(count=('amount','count')).reset_index()
    by_year = by_year[by_year['year'].notna()]

    fig1 = go.Figure(go.Bar(
        x=by_year['year'], y=by_year['count'],
        marker_color=MID, marker_line_width=0,
    ))
    fig1.update_layout(title='Transações por Ano',
                       xaxis_title='Ano', yaxis_title='Número de Transações',
                       xaxis=dict(dtick=1))
    chart1 = make_chart_json(fig1)

    # Chart 2: Top 10 agencias por valor total
    df_ag  = get_df('SELECT id, name FROM Agency')
    df_tx  = get_df('SELECT agency_id, amount FROM "Transaction"')
    merged = df_tx.merge(df_ag, left_on='agency_id', right_on='id')
    top10  = merged.groupby('name')['amount'].sum().reset_index().sort_values('amount', ascending=True).tail(10)

    fig2 = go.Figure(go.Bar(
        x=top10['amount'], y=top10['name'],
        orientation='h',
        marker_color=NAVY, marker_line_width=0,
    ))
    fig2.update_layout(title='Top 10 Agencias por Valor Total', xaxis_title='Total (EUR)')
    chart2 = make_chart_json(fig2)

    # Chart 3: Distribuicao de cargos
    df_o    = get_df('SELECT role FROM Officer')
    by_role = df_o['role'].value_counts().reset_index()
    by_role.columns = ['role', 'count']

    fig3 = go.Figure(go.Bar(
        x=by_role['role'], y=by_role['count'],
        marker_color=LIGHT, marker_line_width=0,
    ))
    fig3.update_layout(title='Distribuicao de Cargos', xaxis_title='Cargo', yaxis_title='Numero')
    chart3 = make_chart_json(fig3)

    from classes.agency import Agency
    from classes.project import Project
    from classes.transaction import Transaction
    from classes.officer import Officer as OfficerCls

    kpis = {
        'agencias':        len(Agency.lst),
        'projetos':        len(Project.lst),
        'transacoes':      len(Transaction.lst),
        'officers':        len(OfficerCls.lst),
        'total_pago':      f"{df_t['amount'].sum():,.0f} EUR",
        'media_transacao': f"{df_t['amount'].mean():,.0f} EUR",
    }

    return render_template("dashboard.html",
                           ulogin=ulogin,
                           chart1=chart1, chart2=chart2, chart3=chart3,
                           kpis=kpis)
