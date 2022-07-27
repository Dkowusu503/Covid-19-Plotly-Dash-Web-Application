import dash
from dash import dcc
from dash import html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np

def drawFigure4():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div(
                dcc.Graph(
                    id='fig3',figure=fig3),

                ),
            ],style={"margin-bottom": "99.5px"}),
        ),
    ])

def drawFigure3():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div(
                dcc.Graph(
                    id='fig2',figure=fig2),

                ),
            ],style={"margin-bottom": "0.5px"}),
        ),
    ])

def drawFigure2():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div(
                dcc.Graph(
                    id='fig',figure=fig1),

                ),
            ],style={"margin-bottom": "20px"}),
        ),
    ])

def drawFigure1():
    return  html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H5("Filter by Date:", style={"textAlign": "left", "margin-bottom": "8px"}),
                    html.Div(["Select a date Range: ",
                              dcc.DatePickerRange(
                                  id="date-picker-covid",
                                  start_date=sf["date"].iloc[0],
                                  end_date=sf["date"].iloc[-1],
                                  min_date_allowed=sf["Date"].iloc[0],
                                  max_date_allowed=sf["Date"].iloc[-1],
                                  start_date_placeholder_text="DD-MMM-YYYY",
                                  display_format='DD-MMM-YYYY',
                                  first_day_of_week=1,
                                  end_date_placeholder_text='DD-MMM-YYYY'),
                              ]),
                ]),
                html.Div([
                    html.H5("Filter by Continent:",
                            style={"textAlign": "left", "margin-top": "25px", "margin-bottom": "8px"}),
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown1",
                            options=sf_all,
                            value=[''],
                            multi=True,
                            placeholder='Filter by continent...'),
                    ]),
                ]),
                html.Div([
                    html.H5("Filter by Country:",
                            style={"textAlign": "left", "margin-top": "25px", "margin-bottom": "8px"}),
                    html.Div([
                        dcc.Dropdown(
                            id="dropdown2",
                            options=sf_all2,
                            value=[''],
                            multi=True,
                            placeholder='Filter by country...'),
                    ]),
                ]),
        ],style={"margin-bottom": "80px"}),
        ),
    ])

# Text field
def drawText1():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H5("Total Confirmed Cases"),
                    html.H4(f'{sf["new_cases"].sum():,.0f}', id='c-cases'),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])
def drawText2():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H5("Total Deaths"),
                    html.H4(f'{sf["new_deaths"].sum():,.0f}', id='c-deaths'),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])
def drawText3():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H5("Total Vaccinations"),
                    html.H4(f'{sf["new_vaccinations"].sum():,.0f}', id='vacc'),
                ], style={'textAlign': 'center'})
            ])
        ),
    ])
def drawText4():
    return html.Div([
        dbc.Card(
            dbc.CardBody([
                html.Div([
                    html.H5("Fatality Rate"),
                    html.H4(f'{(sf["new_deaths"].sum()/sf["new_cases"].sum())*100:,.2f}'+'%', id='p-cases'),
                ], style={'textAlign': 'center'})
            ]),
        ),
    ])
########################################## Data####################################################
sf = pd.read_csv("Covid data 2022.csv")
#Paretto Chart
d_paa=sf.groupby("countries").sum()
d_paa["countries"] = d_paa.index
d_pa=d_paa.sort_values(by="new_cases",ascending=False)
z=0
results = []
x=d_pa["new_cases"].sum()
for j in range(10):
    a=d_pa["countries"][j]
    y=(d_pa["new_cases"][j]/x)*100
    z=z+y
    p=[a,y,z]
    results.append(p)
temporary_df = pd.DataFrame(results, columns=['countries','Perc_Cases', 'Cum_Perc'])
de_ten=d_pa.head(10)
fig3 = go.Figure()
trace1 = go.Bar(
    x=de_ten["countries"],
    y=de_ten["new_cases"],
    marker_color='rgb(55, 83, 109)',
    name="Covid Cases"
)
trace2 = go.Scatter(
    x=temporary_df["countries"],
    y=temporary_df["Cum_Perc"],
    name='%cumulative'
         ' cases',
    yaxis='y2'

)
fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(trace1)
fig3.add_trace(trace2)
fig3.update_layout(template='plotly_white',title={'text': "Top 10 Countries with Most Covid Cases - Paretto Analysis",'y':0.99,'x':0.5,'xanchor': 'center','yanchor': 'top'}, width=550, height=350, margin=dict(l=2, r=2, t=20, b=2))

covid_fields = {
    'date' : 'date',
    'continent' : 'continent',
    'countries' : 'countries',
    'total_cases' : 'Total_cases',
    'new_cases' : 'New_cases',
    'total_deaths' : 'Total_deaths',
    'new_deaths' : 'New_deaths'
    }
#Create Continent Dropdown options
sf_1=sf[covid_fields['continent']].unique()
sf_2 = [
    {'label' : k, 'value' : k} for k in sorted(sf_1)
    ]
sf_3 = [{'label' : '(Select All)', 'value' : 'All'}]
sf_all = sf_2 + sf_3
#Create initial Countries dropdown options
sf_11=sf[covid_fields['countries']].unique()
sf_12 = [
    {'label' : k, 'value' : k} for k in sorted(sf_11)
    ]
sf_13 = [{'label' : '(Select All)', 'value' : 'All'}]
sf_all2 = sf_12 + sf_13
sf_1_12 = {}
for i in sf_1:
    l2 = sf[sf[covid_fields['continent']] == i][covid_fields['countries']].unique()
    sf_1_12[i] = l2

#########################################################################################
sf = sf.astype({"date": np.datetime64})
#dff=df.groupby(df.date.dt.month).sum()
dff=sf.groupby(['date', 'countries'])[['continent','total_cases','new_cases','total_deaths','new_deaths']].sum().reset_index()
d_spcc=dff.tail(7000)
d_spc = d_spcc.groupby(['date'])[['total_cases', 'new_cases', 'total_deaths', 'new_deaths']].sum().reset_index()
d_median=d_spc["new_cases"].median()
d_mmedian = []
for i in d_spc["new_cases"]:
    d_mmedian.append(abs(i - d_median))
    d_MAD = np.median(d_mmedian)
UCL = d_median + 3 * d_MAD
LCL = d_median - 3 * d_MAD
if (LCL < 0):
    LCL = 0
else:
    LCL == LCL
d_spc["Median"]=d_median
d_spc["UCL"]=UCL
d_spc["LCL"]=LCL
fig1=go.Figure()
fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["UCL"],
                         mode='lines',
                         name='UCL='))
fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["new_cases"],
                         mode='lines+markers',
                         name='daily covid cases'))
fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["Median"],
                         mode='lines',
                         name='Median=2,004,084 daily cases'))
fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["LCL"],
                         mode='lines', name='LCL=0 daily cases'))
fig1.update_layout(template='plotly_white',title={'text': "Control Chart For Last 30 days Daily Confirmed Cases",'y':0.99,'x':0.5,'xanchor': 'center','yanchor': 'top'},width=800, height=350, margin=dict(l=20, r=20, t=20, b=20))
#fig2=go.Figure()
#fig2.add_trace(go.Scatter(x=dff["date"], y=dff['new_cases'],
                         #mode='lines',showlegend=True,
                         #)),
fig2= px.line(dff, x='date',y='new_cases',color='countries',template='plotly_white')
fig2.update_layout(template='plotly_white',title={'text': "Line Chart Of Daily Confirmed Cases Over Time",'y':0.99,'x':0.5,'xanchor': 'center','yanchor': 'top'},margin=dict(l=20, r=20, t=20, b=20))
for axis in fig2.layout:
    if type(fig2.layout[axis]) == go.layout.YAxis:
        fig2.layout[axis].title.text = ''
    if type(fig2.layout[axis]) == go.layout.XAxis:
        fig2.layout[axis].title.text = ''


# Build App
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.COSMO])
server = app.server
app.layout = html.Div([
    dbc.Card(
        dbc.CardBody([
            dbc.Row([
                dbc.Col(
                    html.Div([html.Img(src=app.get_asset_url("Covid 19 logo.png"), id='covid-pic')]),
                    width=3),
                dbc.Col(
                    html.Div([
                        html.H1("Coronavirus Dashboard", style={"textAlign": "center","margin-bottom": "8px"}),
                        html.H3("Covid-19 Updates", style={"textAlign": "center","margin-bottom": "8px"}),
                    ]),
                    width=5),
                dbc.Col(
                    html.Div([html.H5("Last Update: "+ sf["Date"].iloc[-1] ,style={"textAlign": "right","margin-top": "25px"})]),
                    width=4),

            ],style={"margin-top": "20px","margin-bottom": "30px","margin-right": "30px","margin-left": "30px" },
            align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawText1()
                ], width=3),
                dbc.Col([
                    drawText2()
                ], width=3),
                dbc.Col([
                    drawText3()
                ], width=3),
                dbc.Col([
                    drawText4()
                ], width=3),
            ],style={"margin-right": "30px","margin-left": "30px" }, align='center'),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure1()
                ], width=4),
                dbc.Col([
                    drawFigure2()
                ], width=8),
            ],style={"margin-right": "30px","margin-left": "30px" }, align="start"),
            html.Br(),
            dbc.Row([
                dbc.Col([
                    drawFigure3()
                ], width=7),
                dbc.Col([
                    drawFigure4()
                ], width=5),
            ],style={"margin-right": "30px","margin-left": "30px" }, align='start'),
        ]), color = '#eeeeee'
    )
])

################## Dynamic Callback For Countries
@app.callback(
    Output('dropdown2', 'options'),
    Input('dropdown1', 'value'))
def set_countries_options(selected_continent):
    isselect_all = 'Start'  # Initialize isselect_all
    for i in selected_continent:
        if i == 'All':
            isselect_all = 'Y'
            break
        elif i != '':
            isselect_all = 'N'
        else:
            pass
        # Create options for individual selections
    if isselect_all == 'N':
        options_0 = []
        for i in selected_continent:
            options_0.append(sf_1_12[i])
        options_1 = []  # Extract string of string
        for i1 in options_0:
            for i2 in i1:
                options_1.append(i2)
        options_list = []  # Get unique values from the string
        for i in options_1:
            if i not in options_list:
                options_list.append(i)
            else:
                pass
        options_final_1 = [
            {'label': k, 'value': k} for k in sorted(options_list)]
        options_final_0 = [{'label': '(Select All)', 'value': 'All'}]
        options_final = options_final_0 + options_final_1

        # Create options for select all or none
    else:
        options_final_1 = [
            {'label': k, 'value': k} for k in sorted(sf_11)]
        options_final_0 = [{'label': '(Select All)', 'value': 'All'}]
        options_final = options_final_0 + options_final_1

    return options_final


@app.callback(
    Output('c-cases', 'children'),
    Output('c-deaths','children'),
    Output('vacc','children'),
    Output('p-cases','children'),
    [Input('date-picker-covid', 'start_date'),
     Input('date-picker-covid', 'end_date'),
     Input('dropdown1', 'value'),
     Input('dropdown2', 'value')])
def update_chart0(start_date, end_date, dropdown11, dropdown22):
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    end = pd.to_datetime(end_date, format='%Y-%m-%d')
    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 (Continent) selection (dropdown value is a list!)
    for i in dropdown11:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l1 == 'N':
        df_1 = sf.loc[sf['continent'].isin(dropdown11), :].copy()
    else:
        df_1 = sf.copy()
    # L2 (Country) selection
    for i in dropdown22:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l2 == 'N':
        df_2 = df_1.loc[df_1['countries'].isin(dropdown22), :].copy()
    else:
        df_2 = df_1.copy()
    # Filter based on the date filters
    df_3 = df_2.loc[(df_2['date'] >= start) & (df_2['date'] <= end), :].copy()
    card1 = html.H4(f'{df_3["new_cases"].sum():,.0f}', id='c-cases')
    card2 = html.H4(f'{df_3["new_deaths"].sum():,.0f}', id='c-deaths')
    card3 = html.H4(f'{df_3["new_vaccinations"].sum():,.0f}', id='vacc')
    card4 = html.H4(f'{(df_3["new_deaths"].sum()/sf["new_cases"].sum())*100:,.2f}'+'%', id='p-cases')
    return card1, card2, card3, card4


@app.callback(
    Output('fig', 'figure'),
    [Input('date-picker-covid', 'start_date'),
    Input('date-picker-covid', 'end_date'),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value')])
def update_chart(start_date, end_date, dropdown11, dropdown22):
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    end = pd.to_datetime(end_date, format='%Y-%m-%d')
    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 (Continent) selection (dropdown value is a list!)
    for i in dropdown11:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l1 == 'N':
        df_1 = sf.loc[sf['continent'].isin(dropdown11), :].copy()
    else:
        df_1 = sf.copy()
    # L2 (Country) selection
    for i in dropdown22:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l2 == 'N':
        df_2 = df_1.loc[df_1['countries'].isin(dropdown22), :].copy()
    else:
        df_2 = df_1.copy()
    # Filter based on the date filters
    df_3 = df_2.loc[(df_2['date'] >= start) & (df_2['date'] <= end), :].copy()
    dff = df_3.groupby(['date', 'countries'])[['continent', 'total_cases', 'new_cases', 'total_deaths', 'new_deaths']].sum().reset_index()
    #d_spcc = dff.tail(7000)
    d_spcc = dff.groupby(['date'])[['total_cases', 'new_cases', 'total_deaths', 'new_deaths']].sum().reset_index()
    d_spc = d_spcc.tail(30).copy()
    d_median = d_spc["new_cases"].median()
    #calculate median absolute deviation
    d_mmedian = []
    for i in d_spc["new_cases"]:
        d_mmedian.append(abs(i - d_median))
        d_MAD = np.median(d_mmedian)
    UCL = d_median + 3 * d_MAD
    LCL = d_median - 3 * d_MAD
    if (LCL < 0):
        LCL = 0
    else:
        LCL == LCL
    d_spc["Median"] = d_median
    d_spc["UCL"] = UCL
    d_spc["LCL"] = LCL
    fig1 = go.Figure()
    fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["UCL"],
                              mode='lines',
                              name='Upper Control Limit'))
    fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["new_cases"],
                              mode='lines+markers',
                              name='Daily covid cases'))
    fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["Median"],
                              mode='lines',
                              name='Median Covid Case'))
    fig1.add_trace(go.Scatter(x=d_spc["date"], y=d_spc["LCL"],
                              mode='lines', name='Lower Control Limit'))
    fig1.update_layout(template='plotly_white',title={'text': "Control Chart For Last 30 days Daily Confirmed Cases",'y':0.99,'x':0.5,'xanchor': 'center','yanchor': 'top'}, width=800, height=350, margin=dict(l=20, r=20, t=20, b=20))
    return fig1

@app.callback(
    Output('fig2', 'figure'),
    [Input('date-picker-covid', 'start_date'),
    Input('date-picker-covid', 'end_date'),
    Input('dropdown1', 'value'),
    Input('dropdown2', 'value')])
def update_chart1(start_date, end_date, dropdown11, dropdown22):
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    end = pd.to_datetime(end_date, format='%Y-%m-%d')
    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 (Continent) selection (dropdown value is a list!)
    for i in dropdown11:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l1 == 'N':
        df_1 = sf.loc[sf['continent'].isin(dropdown11), :].copy()
    else:
        df_1 = sf.copy()
    # L2 (Country) selection
    for i in dropdown22:
        if i == 'All':
            isselect_all_l2 = 'Y'
            break
        elif i != '':
            isselect_all_l2 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l2 == 'N':
        df_2 = df_1.loc[df_1['countries'].isin(dropdown22), :].copy()
    else:
        df_2 = df_1.copy()
    # Filter based on the date filters
    df_3 = df_2.loc[(df_2['date'] >= start) & (df_2['date'] <= end), :].copy()
    fig2 = px.line(df_3, x='date', y='new_cases', color='countries', template='plotly_white')
    fig2.update_layout(template='plotly_white',title={'text': "Line Chart Of Daily Confirmed Cases Over Time",'y':0.99,'x':0.5,'xanchor': 'center','yanchor': 'top'}, margin=dict(l=20, r=20, t=20, b=20))
    for axis in fig2.layout:
        if type(fig2.layout[axis]) == go.layout.YAxis:
            fig2.layout[axis].title.text = ''
        if type(fig2.layout[axis]) == go.layout.XAxis:
            fig2.layout[axis].title.text = ''
    return fig2

@app.callback(
    Output('fig3', 'figure'),
    [Input('date-picker-covid', 'start_date'),
    Input('date-picker-covid', 'end_date'),
    Input('dropdown1', 'value')])
def update_chart2(start_date, end_date, dropdown11):
    start = pd.to_datetime(start_date, format='%Y-%m-%d')
    end = pd.to_datetime(end_date, format='%Y-%m-%d')
    # Filter based on the dropdowns
    isselect_all_l1 = 'Start'  # Initialize isselect_all
    isselect_all_l2 = 'Start'  # Initialize isselect_all
    # L1 (Continent) selection (dropdown value is a list!)
    for i in dropdown11:
        if i == 'All':
            isselect_all_l1 = 'Y'
            break
        elif i != '':
            isselect_all_l1 = 'N'
        else:
            pass
    # Filter dataframe according to selection
    if isselect_all_l1 == 'N':
        df_1 = sf.loc[sf['continent'].isin(dropdown11), :].copy()
    else:
        df_1 = sf.copy()
    # Filter based on the date filters
    df_4 = df_1.loc[(df_1['date'] >= start) & (df_1['date'] <= end), :].copy()
    # Paretto Chart
    d_paa = df_4.groupby("countries").sum()
    d_paa["countries"] = d_paa.index
    d_pa = d_paa.sort_values(by="new_cases", ascending=False)
    z = 0
    results = []
    x = d_pa["new_cases"].sum()
    for j in range(10):
        a = d_pa["countries"][j]
        y = (d_pa["new_cases"][j] / x) * 100
        z = z + y
        p = [a, y, z]
        results.append(p)
    temporary_df = pd.DataFrame(results, columns=['countries', 'Perc_Cases', 'Cum_Perc'])
    de_ten = d_pa.head(10)
    fig3 = go.Figure()
    trace1 = go.Bar(
        x=de_ten["countries"],
        y=de_ten["new_cases"],
        marker_color='rgb(55, 83, 109)',
        name="Covid Cases"
    )
    trace2 = go.Scatter(
        x=temporary_df["countries"],
        y=temporary_df["Cum_Perc"],
        name='%cumulative'
             ' cases',
        yaxis='y2'

    )
    fig3 = make_subplots(specs=[[{"secondary_y": True}]])
    fig3.add_trace(trace1)
    fig3.add_trace(trace2)
    fig3.update_layout(template='plotly_white',title={'text': "Top 10 Countries with Most Covid Cases - Paretto Analysis",'y':0.99,'x':0.5,'xanchor': 'center','yanchor': 'top'}, width=550, height=350, margin=dict(l=2, r=2, t=20, b=2))
    return fig3

if __name__ == '__main__':
    app.run_server(debug=True)
