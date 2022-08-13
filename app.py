mport numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash
from jupyter_dash import JupyterDash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

gss = pd.read_csv("https://github.com/jkropko/DS-6001/raw/master/localdata/gss2018.csv",
                 encoding='cp1252', na_values=['IAP','IAP,DK,NA,uncodeable', 'NOT SURE',
                                               'DK', 'IAP, DK, NA, uncodeable', '.a', "CAN'T CHOOSE"])

mycols = ['id', 'wtss', 'sex', 'educ', 'region', 'age', 'coninc',
          'prestg10', 'mapres10', 'papres10', 'sei10', 'satjob',
          'fechld', 'fefam', 'fepol', 'fepresch', 'meovrwrk'] 
gss_clean = gss[mycols]
gss_clean = gss_clean.rename({'wtss':'weight', 
                              'educ':'education', 
                              'coninc':'income', 
                              'prestg10':'job_prestige',
                              'mapres10':'mother_job_prestige', 
                              'papres10':'father_job_prestige', 
                              'sei10':'socioeconomic_index', 
                              'fechld':'relationship', 
                              'fefam':'male_breadwinner', 
                              'fehire':'hire_women', 
                              'fejobaff':'preference_hire_women', 
                              'fepol':'men_bettersuited', 
                              'fepresch':'child_suffer',
                              'meovrwrk':'men_overwork'},axis=1)
gss_clean.age = gss_clean.age.replace({'89 or older':'89'})
gss_clean.age = gss_clean.age.astype('float')

gender_wage_gap = 'The Pew Research Center has found over the past 15 years, women have earned 84% of what men earned. The gap has become smaller over the years because women have worked to gain a higher education and work experience. Gender discrimination is always going to be a factor when it comes to the pay gap. Motherhood is another factor as mothers are more likely to take time off work for thier kids vs. fathers, which many mothers have said that it has affected their job or career. It will be hard to say that the gender wage gap will ever disappear but there are a number of steps that could be taken to help improve it and therefore improve the lives of women. Source: https://www.pewresearch.org/fact-tank/2021/05/25/gender-pay-gap-facts/'

gss_text = 'The GSS (General Social Survey) is a survery of American adults that has been collecting data since 1972. The purpose of the GSS is to keep track of the trends in the opinions of American society by asking questions about a wide range of relevant topics. Data is collected by interviewing Americans that are 18 years and older in order to easyily provide data to people wanting to study sociological and attiudinal trends in data. Source: https://www.gss.norc.org/About-The-GSS'


scatter = px.scatter(gss_clean, x='job_prestige', y='income', color='sex',
           trendline='ols',
           labels={'job_prestige':'Occupational Prestige', 'income':'Annual Income'},
           hover_data=['education','socioeconomic_index'])


box = px.box(gss_clean, x='sex', y='income', color='sex',
            labels={'income':'Annual Income','sex':''})
box.update_layout(showlegend=False)


box2 = px.box(gss_clean, x='sex', y='job_prestige', color='sex',
             labels={'job_prestige':'Occupational Prestige','sex':''})
box2.update_layout(showlegend=False)

new_df = gss_clean[['income','sex','job_prestige']]


new_df['job_level'] = pd.cut(new_df.job_prestige, bins=[0,29,39,49,59,69,100], 
                             labels=('low', 'medium low', 'medium', 'medium high', 'high', 'very high'))
new_df = new_df.dropna()


facet = px.box(new_df, x='sex', y='income', color='sex',
              facet_col='job_level', facet_col_wrap=2,
              category_orders={'job_level':['low', 'medium low', 'medium', 'medium high', 'high', 'very high']},
              color_discrete_map = {'male':'blue', 'female':'red'},
              labels={'income':'Annual Income','sex':'Sex'},
              height=800)
facet.update_layout(showlegend=True)
facet.for_each_annotation(lambda a: a.update(text=a.text.replace("job_level=", "")))


colors = {'background': '#F5F5F5',
         'text':'#006270'}

table.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
scatter.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
box.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
box2.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])
facet.update_layout(
    plot_bgcolor=colors['background'],
    paper_bgcolor=colors['background'],
    font_color=colors['text'])

questions = ['satjob','relationship', 'male_breadwinner', 'men_bettersuited', 'child_suffer','men_overwork']
groupings = ['sex','region','education']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(style={'backgroundColor': colors['background']}, children=
    [
        html.H1("Exploring the 2019 General Social Survey", 
                style={'textAlign': 'center','color': colors['text']}),
        dcc.Markdown(children = gss_text), 
        dcc.Markdown(children = gender_wage_gap),

        html.Div([html.H3("Comparing Men and Women",
                style={'textAlign': 'center','color': colors['text']}),
                dcc.Graph(figure=table)]),

        html.H3("Compare GSS Questions",
                style={'textAlign': 'center','color': colors['text']}),
        html.Div([dcc.Dropdown(options=questions,
                value='male_breadwinner',
                id='question')
                ],style={'width': '48%', 'display': 'inline-block'}),
        html.Div([dcc.Dropdown(options=groupings,
                value='sex',
                id='group')
                ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'}),
        dcc.Graph(id='displaybar'),
        
        html.H3("Occupation Prestige vs Annual Income",
               style={'textAlign': 'center','color': colors['text']}),
        dcc.Graph(figure=scatter),
        
        html.Div([html.H3("Comparing Annual Income",
                style={'textAlign': 'center','color': colors['text']}),
                dcc.Graph(figure=box)],
                style={'width':'48%', 'height':'50%','float':'left'}),
        
        html.Div([html.H3("Comparing Occupational Prestige",
                style={'textAlign': 'center','color': colors['text']}),
                dcc.Graph(figure=box2)],
                style={'width':'48%','height':'50%', 'float':'right'}),
        
        html.H3("Annual Income by Occupational Prestige Level",
               style={'textAlign': 'center','color': colors['text']}),
        dcc.Graph(figure=facet),
    ]
)

@app.callback(Output('displaybar', 'figure'),
             Input('question', 'value'),
             Input('group', 'value'))

def barchart(question, group):
    gss_clean[question] = gss_clean[question].astype('category')
    table = gss_clean.groupby([group, question]).size().reset_index().rename({0:'count'},axis=1)
    bar = px.bar(table, x=question, y='count', color=group, 
    labels={question:'Level of Agreement', 'count':'Count'},
        hover_name = group,
        barmode = 'group')
    bar.update_layout(
        plot_bgcolor=colors['background'],
        paper_bgcolor=colors['background'],
        font_color=colors['text'])
    return bar
        
if __name__ == '__main__':
    app.run_server(debug=True)
