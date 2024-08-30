import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

df = pd.read_csv('train.csv')

df['AgeGroup'] = pd.cut(df['Age'], bins=[0, 12, 18, 60, 80], labels=['Child', 'Teenager', 'Adult', 'Senior'])

df['FamilySize'] = df['SibSp'] + df['Parch'] + 1  

app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1("Titanic Interactive Survival Dashboard", style={'text-align': 'center', 'color': '#4CAF50'}),

    html.Div([
        html.Label("Select Passenger Class:", style={'font-size': '18px', 'font-weight': 'bold'}),
        dcc.Dropdown(id="class_dropdown",
                     options=[
                         {"label": "First Class", "value": 1},
                         {"label": "Second Class", "value": 2},
                         {"label": "Third Class", "value": 3}],
                     multi=False,
                     value=1,
                     style={'width': "60%", 'margin-bottom': '20px'}
                     ),
    ], style={'padding': '20px'}),

    html.Div([
        dcc.Graph(id='survival_graph', figure={}),
        dcc.Graph(id='age_gender_graph', figure={})
    ], style={'display': 'flex', 'flex-wrap': 'wrap'}),

    html.Div([
        dcc.Graph(id='fare_violin', figure={})
    ]),

    html.Div([
        dcc.Graph(id='family_size_graph', figure={})
    ]),

    html.Div([
        html.Label("Filter by Gender:", style={'font-size': '18px', 'font-weight': 'bold'}),
        dcc.RadioItems(id='gender_filter',
                       options=[
                           {'label': 'All', 'value': 'All'},
                           {'label': 'Male', 'value': 'male'},
                           {'label': 'Female', 'value': 'female'}
                       ],
                       value='All',
                       style={'margin-top': '20px', 'margin-bottom': '20px'},
                       labelStyle={'display': 'inline-block', 'margin-right': '20px'}
                       )
    ], style={'padding': '20px'})
])

@app.callback(
    [Output('survival_graph', 'figure'),
     Output('age_gender_graph', 'figure'),
     Output('fare_violin', 'figure'),
     Output('family_size_graph', 'figure')],
    [Input('class_dropdown', 'value'),
     Input('gender_filter', 'value')]
)
def update_graphs(selected_class, gender_filter):
    
    if gender_filter != 'All':
        filtered_df = df[(df['Pclass'] == selected_class) & (df['Sex'] == gender_filter)]
    else:
        filtered_df = df[df['Pclass'] == selected_class]

    # Survival by gender
    survival_fig = px.histogram(filtered_df, x='Survived', color='Sex', barmode='group',
                                labels={'Survived': 'Survived', 'Sex': 'Gender'},
                                title=f'Survival by Gender in Class {selected_class}',
                                color_discrete_map={'female': 'pink', 'male': 'blue'})

    # Age group distribution by gender
    age_gender_fig = px.histogram(filtered_df, x='AgeGroup', color='Sex', barmode='group',
                                  labels={'AgeGroup': 'Age Group', 'Sex': 'Gender'},
                                  title=f'Age Group Distribution by Gender in Class {selected_class}',
                                  color_discrete_map={'female': 'pink', 'male': 'blue'})

    # Fare distribution using Violin Plot
    if gender_filter == 'female':
        fare_violin = px.violin(filtered_df, y='Fare', color='Sex', box=True, points='all',
                                title=f'Fare Distribution in Class {selected_class}',
                                labels={'Fare': 'Fare'},
                                color_discrete_map={'female': 'pink'})
    else:
        fare_violin = px.violin(filtered_df, y='Fare', box=True, points='all',
                                title=f'Fare Distribution in Class {selected_class}',
                                labels={'Fare': 'Fare'},
                                color_discrete_map={'All': 'purple'})

    fare_violin.update_traces(meanline_visible=True)

    # Family size survival rate
    family_size_fig = px.histogram(filtered_df, x='FamilySize', color='Survived', barmode='group',
                                   labels={'FamilySize': 'Family Size', 'Survived': 'Survived'},
                                   title=f'Survival by Family Size in Class {selected_class}')

    return survival_fig, age_gender_fig, fare_violin, family_size_fig

if __name__ == '__main__':
    app.run_server(debug=True)
