import math
import numpy as np
import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

app = dash.Dash(__name__)
df = pd.read_csv('filled_data.csv')
income_bins = [0, 10000, 20000, 30000, 50000, 70000, 100000]
income_labels = ['0-10k', '10k-20k', '20k-30k', '30k-50k', '50k-70k', '70k+']
df['Grouped_Annual_Income'] = pd.cut(df['Annual_Income'], bins=income_bins, labels=income_labels)

age_bins = [0, 20, 35, 50, 75]
age_labels = ['0-20', '20-35', '35-50', '50-75']
df['Grouped_Age'] = pd.cut(df['Age'], bins=age_bins, labels=age_labels)

# Sample data for each dropdown
occupation_options = []
occupations = df['Occupation'].dropna().unique().tolist()
occupations.sort()
for occupation in occupations:
    if not pd.isna(occupation):
        occupation_options.append({'label': occupation, 'value': occupation})

age_options = []

age_groups = df['Grouped_Age'].dropna().unique().tolist()
age_groups.sort()
for age_group in age_groups:
    if not pd.isna(age_group):
        age_options.append({'label': age_group, 'value': age_group})

income_options = []
income_groups = df['Grouped_Annual_Income'].dropna().unique().tolist()
income_groups.sort()

for income_group in income_groups:
    if not pd.isna(income_group):
        income_options.append({'label': income_group, 'value': income_group})

loan_options = []
loan_types = ['Payday Loan', 'Auto Loan', 'Home Equity Loan', 'Mortgage Loan', 'Student Loan', 'Personal Loan',
              'Debt Consolidation Loan', 'Credit-Builder Loan']
loan_types.sort()
for loan_type in loan_types:
    loan_options.append({'label': loan_type, 'value': loan_type})

# Options for the category filter dropdown
category_options = [
    {'label': 'Occupation', 'value': 'Occupation'},
    {'label': 'Loan Type', 'value': 'Loan_Type'}
]

fields = ['Credit_Utilization_Ratio', 'Outstanding_Debt',
          'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment']

left_first_barplot = go.Figure()
left_second_barplot = go.Figure()
right_first_barplot = go.Figure()
right_second_barplot = go.Figure()

scatterplot_columns = ['Grouped_Annual_Income', 'Grouped_Age', 'Occupation']
scatterplot_columns += loan_types
scatterplot_columns += fields

app.layout = html.Div([
    html.Div([
        html.H1("Credit Score Demographic Exploratory for Marketing", style={'textAlign': 'center',
                                                                             'fontFamily': 'Trebuchet MS'}),

    ], style={'display': 'flex', 'flexDirection': 'column',
              'alignItems': 'center', 'justifyContent': 'center'}),
    html.Div([
        # Left block
        html.Div([
            # Demographic name at the top
            html.H3(id='left-demographic-name', style={'color': '#0474BA', 'textAlign': 'center'}),

            # Dropdowns for x and y
            html.Div([
                # Select x
                html.Div([
                    html.Label('Select x', style={'color': 'cornflowerblue'}),
                    dcc.Dropdown(
                        id='left-side-select-x-dropdown',
                        options=[{'label': field, 'value': field} for field in fields],
                        value=fields[0],
                        style={'width': '180px'}
                    )
                ], style={'marginRight': '20px'}),
                # Select y
                html.Div([
                    html.Label('Select y', style={'color': 'darkblue'}),
                    dcc.Dropdown(
                        id='left-side-select-y-dropdown',
                        options=[{'label': field, 'value': field} for field in fields],
                        value=fields[1],
                        style={'width': '180px'}
                    )
                ]),
            ], style={'display': 'flex', 'flexDirection': 'row',
                      'alignItems': 'center', 'justifyContent': 'center'}),

            # Scatterplot
            dcc.Graph(id='left-side-scatterplot',
                      responsive=True,
                      style={'width': '500px', 'height': '500px'}),

            # Two bar plots
            html.Div([
                dcc.Graph(id='left-side-first-barplot',
                          responsive=True,
                          style={'width': '250px', 'height': '250px'}),
                dcc.Graph(id='left-side-second-barplot',
                          responsive=True,
                          style={'width': '250px', 'height': '250px'})
            ], style={'display': 'flex', 'flexDirection': 'row',
                      'alignItems': 'center', 'justifyContent': 'center'}),

            # Scatterpolar graph for left side
            dcc.Graph(id='scatterpolar-left'),

        ], style={'width': '25%', 'display': 'inline-'}, id='left-block'),

        # Middle block
        html.Div([
            html.Div([
                # Category Dropdown
                html.Label('Select Category',
                           style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=category_options,
                    value='Occupation',
                    style={'width': '200px'}
                ),
            ], style={'display': 'flex', 'flexDirection': 'column',
                      'alignItems': 'center', 'justifyContent': 'center'}),
            html.Div([
                # First demographic
                html.Div([
                    # Dynamic Dropdowns for the first and second occupations
                    html.Label('Select Left-side Demographic', style={'color': '#0474BA'}),
                    dcc.Dropdown(
                        id='first-demographic-dropdown',
                        options=occupation_options,
                        multi=False,
                        style={'width': '180px'}
                    ),
                    dcc.Checklist(
                        id='left-side-checklist',
                        options=[
                            {'label': 'In-depth Left Side', 'value': 'left'},
                        ])
                ], style={'marginRight': '10px'}),
                # Second demographic
                html.Div([
                    html.Label('Select Right-side Demographic', style={'color': '#F79500'}),
                    dcc.Dropdown(
                        id='second-demographic-dropdown',
                        options=occupation_options,
                        multi=False,
                        style={'width': '200px'}
                        # value=occupation_options[1]['value']
                    ),
                    dcc.Checklist(
                        id='right-side-checklist',
                        options=[
                            {'label': 'In-depth Right Side', 'value': 'right'}
                        ])
                ]),

            ], style={'display': 'flex', 'flexDirection': 'row',
                      'alignItems': 'center', 'justifyContent': 'center'}),

            # Scatterpolar graph for displaying selected values
            dcc.Graph(id='scatterpolar-middle',
                      responsive=True,
                      style={'width': '600px', 'height': '600px'}),

            # Pcp graph for displaying selected values
            dcc.Graph(id='pcp',
                      responsive=True,
                      style={'width': '800px', 'height': '500px'}),

        ], style={'width': '50%', 'display': 'flex', 'flexDirection': 'column',
                  'alignItems': 'center', 'justifyContent': 'center'},
            id='middle-block'),

        # Right block
        html.Div([
            # Demographic name at the top
            html.H3(id='right-demographic-name', style={'color': '#F79500'}),
            # Dropdowns for x and y
            html.Div([
                # Select x
                html.Div([
                    html.Label('Select x', style={'color': 'orange'}),
                    dcc.Dropdown(
                        id='right-side-select-x-dropdown',
                        options=[{'label': field, 'value': field} for field in fields],
                        value=fields[0],
                        style={'width': '180px'}
                    )
                ], style={'marginRight': '20px'}),
                # Select y
                html.Div([
                    html.Label('Select y', style={'color': 'chocolate'}),
                    dcc.Dropdown(
                        id='right-side-select-y-dropdown',
                        options=[{'label': field, 'value': field} for field in fields],
                        value=fields[1],
                        style={'width': '180px'}
                    )
                ]),
            ], style={'display': 'flex', 'flexDirection': 'row',
                      'alignItems': 'center', 'justifyContent': 'center'}),

            # Scatterplot
            dcc.Graph(id='right-side-scatterplot',
                      responsive=True,
                      style={'width': '500px', 'height': '500px'}),

            # Two bar plots
            html.Div([
                dcc.Graph(id='right-side-first-barplot',
                          responsive=True,
                          style={'width': '250px', 'height': '250px'}),
                dcc.Graph(id='right-side-second-barplot',
                          responsive=True,
                          style={'width': '250px', 'height': '250px'})
            ], style={'display': 'flex', 'flexDirection': 'row',
                      'alignItems': 'center', 'justifyContent': 'center'}),

            # Scatterpolar graph for right side
            dcc.Graph(id='scatterpolar-right'),

        ], style={'width': '25%', 'display': 'inline-block'},
            id='right-block'),

    ], style={'display': 'flex',
              'flexDirection': 'row', 'alignItems': 'flex-start',
              'justifyContent': 'center'})
], style={'fontFamily': 'Trebuchet MS'})


@app.callback(
    [Output('left-block', 'style'),
     Output('middle-block', 'style'),
     Output('right-block', 'style')],
    [Input('left-side-checklist', 'value'),
     Input('right-side-checklist', 'value')]
)
def show_sides(left_side, right_side):
    left_display = {'width': '25%', 'display': 'none'}
    right_display = {'width': '25%', 'display': 'none'}
    selected_sides = left_side if left_side is not None else []
    selected_sides += right_side if right_side is not None else []
    if selected_sides is not None:
        if len(selected_sides) <= 1:
            middle_size = 70
            side_size = 30
        else:
            middle_size = 50
            side_size = 23
        if 'left' in selected_sides:
            left_display = {'width': f'{side_size}%', 'display': 'flex', 'flexDirection': 'column'}
        if 'right' in selected_sides:
            right_display = {'width': f'{side_size}%', 'display': 'flex', 'flexDirection': 'column'}
        middle_display = {'width': f'{middle_size}%', 'display': 'flex', 'flexDirection': 'column',
                          'alignItems': 'center', 'justifyContent': 'center'}
        return left_display, middle_display, right_display


# Callback to dynamically update the options of the first occupation dropdown
@app.callback(
    [Output('first-demographic-dropdown', 'options'),
     Output('first-demographic-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_first_occupation_dropdown_options(selected_category):
    if selected_category == 'Occupation':
        options = occupation_options
    elif selected_category == 'Grouped_Age':
        options = age_options
    elif selected_category == 'Grouped_Annual_Income':
        options = income_options
    elif selected_category == 'Loan_Type':
        options = loan_options
    else:
        options = []
    # Pre-select the first option for the first occupation dropdown
    values = options[0]['value']
    return options, values


# Callback to dynamically update the options of the second occupation dropdown
@app.callback(
    [Output('second-demographic-dropdown', 'options'),
     Output('second-demographic-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_second_occupation_dropdown_options(selected_category):
    if selected_category == 'Occupation':
        options = occupation_options
    elif selected_category == 'Grouped_Age':
        options = age_options
    elif selected_category == 'Grouped_Annual_Income':
        options = income_options
    elif selected_category == 'Loan_Type':
        options = loan_options
    else:
        options = []
    # Pre-select the second option for the second occupation dropdown
    values = options[1]['value'] if len(options) > 1 else ''
    return options, values


def get_options_and_defaults_second_category(selected_category, options):
    if options is None:
        return [], ''
    constrained_options = options.copy()
    if selected_category == 'Occupation':
        constrained_options.remove(category_options[0])
    elif selected_category == 'Grouped_Age':
        constrained_options.remove(category_options[1])
    elif selected_category == 'Grouped_Annual_Income':
        constrained_options.remove(category_options[2])
    else:
        constrained_options.remove(category_options[3])
    return constrained_options, constrained_options[0]['value']


# Helper function to get options and default values based on selected category
def get_options_and_defaults(selected_category):
    options = get_options_based_on_category(selected_category)
    values = options[0]['value'] if options else ''

    return options, values


# Helper function to get options based on selected category
def get_options_based_on_category(selected_category):
    if selected_category == 'Occupation':
        return occupation_options
    elif selected_category == 'Grouped_Age':
        return age_options
    elif selected_category == 'Grouped_Annual_Income':
        return income_options
    elif selected_category == 'Loan_Type':
        return loan_options
    else:
        return []


# Callback to update the first barplot for the left side
def create_first_barplot(filtered_df):
    # Define the color mapping
    color_mapping = {'0-10k': '#b0d767', '10k-20k': '#da8ec0', '30k-50k': '#f9da56',
                     '50k-70k': '#e0c59a', '70k+': '#b3b3b3'}
    # Create histogram
    barplot = px.histogram(filtered_df, x='Grouped_Annual_Income', color='Grouped_Annual_Income',
                           category_orders={
                               'Grouped_Annual_Income': income_labels},
                           labels={'Grouped_Annual_Income': 'Income Group', 'count': 'Frequency'})

    # Update layout
    barplot.update_layout(title='Income Groups Frequency',
                          xaxis_title='Income Group',
                          dragmode="select",
                          yaxis_title='Frequency',
                          showlegend=False)
    return barplot


def create_second_barplot(filtered_df):
    # Calculate frequency of each age group
    age_group_freq = filtered_df['Grouped_Age'].value_counts().reset_index()
    age_group_freq.columns = ['Grouped_Age', 'Frequency']

    # Create scatter plot
    barplot = px.scatter(age_group_freq, x='Grouped_Age', y='Frequency',
                         size_max=15,
                         symbol='Grouped_Age',
                         labels={'Grouped_Age': 'Age Group', 'Frequency': 'Frequency'},
                         category_orders={'Grouped_Age': ['0-20', '20-35', '35-50', '50-75']})

    # Set the color of all markers to black
    barplot.update_traces(marker=dict(color='black'))

    # Update layout
    barplot.update_layout(title='Age Groups Frequency',
                          xaxis_title='Age Group',
                          dragmode="select",
                          yaxis_title='Frequency',
                          showlegend=False)
    return barplot


def create_barplot_filtered_df(category, demographic, selected_data):
    if selected_data is None:
        # Filter database based on chosen demographic
        if category == 'Loan_Type':
            filtered_df = df[df[demographic] == 1]
        else:
            filtered_df = df[df[category] == demographic]
    else:
        counter = dict()
        incomes = []
        ages = []
        for point in selected_data['points']:
            incomes.append(point['customdata'][0])
            ages.append(point['customdata'][1])
        counter['Grouped_Annual_Income'] = incomes
        counter['Grouped_Age'] = ages
        filtered_df = pd.DataFrame(counter)
    return filtered_df


# Callback to update the scatterplot for the left side
@app.callback(
    Output('left-side-scatterplot', 'figure'),
    [Input('left-side-select-x-dropdown', 'value'),
     Input('left-side-select-y-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('first-demographic-dropdown', 'value'),
     Input('left-side-first-barplot', 'selectedData'),
     Input('left-side-second-barplot', 'selectedData')]
)
def update_scatterplot_left(x_value, y_value, category, left_demographic, first_barplot_data, second_barplot_data):
    # Filter database based on chosen demographic
    if category == 'Loan_Type':
        filtered_df = df[df[left_demographic] == 1]
    else:
        filtered_df = df[df[category] == left_demographic]

    fig = px.scatter(filtered_df, x=x_value, y=y_value,
                     color='Grouped_Annual_Income', symbol='Grouped_Age',
                     custom_data=scatterplot_columns)
    fig.update_traces(marker_size=4, marker_opacity=0.5)

    # Update layout
    fig.update_layout(title='Scatter Plot',
                      xaxis_title=x_value,
                      yaxis_title=y_value,
                      dragmode="select",
                      legend_title='Income - Age',
                      legend_title_font=dict(size=12))

    if (first_barplot_data and first_barplot_data['points']) or (second_barplot_data and second_barplot_data['points']):
        groups = []
        incomes, ages = get_barplot_groups(first_barplot_data, second_barplot_data)

        for income in incomes:
            for age in ages:
                groups.append(f"{income}, {age}")
        fig.for_each_trace(
            lambda trace: trace.update(opacity=1) if trace.name in groups else trace.update(opacity=0))
    else:
        fig.update_traces(opacity=1)

    return fig

def get_barplot_groups(first_barplot_data, second_barplot_data):
    incomes = []
    ages = []
    if second_barplot_data is not None:
        for bar in second_barplot_data['points']:
            ages.append(bar['x'])
    else:
        ages = age_labels.copy()
    if first_barplot_data is not None:
        for bar in first_barplot_data['points']:
            incomes.append(bar['x'])
    else:
        incomes = income_labels.copy()
    return incomes, ages

@app.callback(
    [Output('left-side-first-barplot', 'figure'),
     Output('left-side-second-barplot', 'figure')],
    [Input('category-dropdown', 'value'),
     Input('first-demographic-dropdown', 'value'),
     Input('left-side-scatterplot', 'selectedData')]
)
def update_left_side_first_second_barplot(category, left_demographic, selected_data):
    filtered_df = create_barplot_filtered_df(category, left_demographic, selected_data)

    left_first_barplot = create_first_barplot(filtered_df)
    left_second_barplot = create_second_barplot(filtered_df)

    return left_first_barplot, left_second_barplot


# Callback to update the radarplot for the right side
@app.callback(
    Output('scatterpolar-left', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('left-side-select-x-dropdown', 'value'),
     Input('left-side-select-y-dropdown', 'value'),
     Input('left-side-first-barplot', 'selectedData'),
     Input('left-side-second-barplot', 'selectedData')]
)
def update_radarplot_left(category, x_value, y_value, first_barplot_data, second_barplot_data):
    # Get unique labels for the main category selected in the middle
    if category == 'Loan_Type':
        main_category_labels = loan_types
    else:
        main_category_labels = df[category].unique()

    fig = go.Figure()
    incomes, ages = get_barplot_groups(first_barplot_data, second_barplot_data)

    incomes_mask = df['Grouped_Annual_Income'].isin(incomes)
    ages_mask = df['Grouped_Age'].isin(ages)

    # Create traces for the selected field
    for xy, line_color in zip([x_value, y_value], ['cornflowerblue', 'darkblue']):
        values = []
        for label in main_category_labels:
            if category == 'Loan_Type':
                label_data = df[(df[label] == 1) & incomes_mask & ages_mask]
            else:
                label_data = df[(df[category] == label) & incomes_mask & ages_mask]

            mean_value = label_data[xy].mean()
            if not math.isnan(mean_value):
                values.append(math.log(round(mean_value)))
            else:
                values.append(None)

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=main_category_labels,
            name=xy,
            line=dict(color=line_color),
            hovertemplate='%{r}',
            hoverinfo="text"
        ))

    return fig



# Callback to update the scatterplot for the left side
@app.callback(
    Output('right-side-scatterplot', 'figure'),
    [Input('right-side-select-x-dropdown', 'value'),
     Input('right-side-select-y-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('second-demographic-dropdown', 'value'),
     Input('right-side-first-barplot', 'selectedData'),
     Input('right-side-second-barplot', 'selectedData'),]
)
def update_scatterplot_right(x_value, y_value, category, right_demographic, first_barplot_data, second_barplot_data):
    if category == 'Loan_Type':
        filtered_df = df[df[right_demographic] == 1]
    else:
        filtered_df = df[df[category] == right_demographic]

    fig = px.scatter(filtered_df, x=x_value, y=y_value,
                     color='Grouped_Annual_Income', symbol='Grouped_Age',
                     custom_data=scatterplot_columns)
    fig.update_traces(marker_size=4, marker_opacity=0.5)

    # Update layout
    fig.update_layout(title='Scatter Plot',
                      xaxis_title=x_value,
                      yaxis_title=y_value,
                      dragmode="select",
                      legend_title='Income - Age',
                      legend_title_font=dict(size=12))

    if (first_barplot_data and first_barplot_data['points']) or (second_barplot_data and second_barplot_data['points']):
        groups = []
        incomes, ages = get_barplot_groups(first_barplot_data, second_barplot_data)

        for income in incomes:
            for age in ages:
                groups.append(f"{income}, {age}")
        fig.for_each_trace(
            lambda trace: trace.update(opacity=1) if trace.name in groups else trace.update(opacity=0))
    else:
        fig.update_traces(opacity=1)

    return fig


# Callback to update the first barplot for the right side
@app.callback(
    [Output('right-side-first-barplot', 'figure'),
     Output('right-side-second-barplot', 'figure')],
    [Input('category-dropdown', 'value'),
     Input('second-demographic-dropdown', 'value'),
     Input('right-side-scatterplot', 'selectedData')]
)
def update_right_side_first_second_barplot(category, right_demographic, selected_data):
    filtered_df = create_barplot_filtered_df(category, right_demographic, selected_data)

    right_first_barplot = create_first_barplot(filtered_df)
    right_second_barplot = create_second_barplot(filtered_df)

    return right_first_barplot, right_second_barplot


# Callback to update the radarplot for the right side
@app.callback(
    Output('scatterpolar-right', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('right-side-select-x-dropdown', 'value'),
     Input('right-side-select-y-dropdown', 'value'),
     Input('right-side-first-barplot', 'selectedData'),
     Input('right-side-second-barplot', 'selectedData')]
)
def update_radarplot_right(category, x_value, y_value, first_barplot_data, second_barplot_data):
    # Get unique labels for the main category selected in the middle
    if category == 'Loan_Type':
        main_category_labels = loan_types
    else:
        main_category_labels = df[category].unique()

    fig = go.Figure()
    incomes, ages = get_barplot_groups(first_barplot_data, second_barplot_data)

    incomes_mask = df['Grouped_Annual_Income'].isin(incomes)
    ages_mask = df['Grouped_Age'].isin(ages)

    # Create traces for the selected field
    for xy, line_color in zip([x_value, y_value], ['orange', 'chocolate']):
        values = []
        for label in main_category_labels:
            if category == 'Loan_Type':
                label_data = df[(df[label] == 1) & incomes_mask & ages_mask]
            else:
                label_data = df[(df[category] == label) & incomes_mask & ages_mask]

            mean_value = label_data[xy].mean()
            if not math.isnan(mean_value):
                values.append(math.log(round(mean_value)))
            else:
                values.append(None)

        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=main_category_labels,
            name=xy,
            line=dict(color=line_color),
            hovertemplate='%{r}',
            hoverinfo="text",
        ))

    return fig


# Callbacks for updating the occupation names in the left and right side blocks
@app.callback(
    [Output('left-demographic-name', 'children'),
     Output('right-demographic-name', 'children')],
    [Input('first-demographic-dropdown', 'value'),
     Input('second-demographic-dropdown', 'value')]
)
def update_occupation_names(first_occupation, second_occupation):
    return f'{first_occupation}s', f'{second_occupation}s'


# Callback to update the output div based on the selected occupations
@app.callback(
    [Output('scatterpolar-middle', 'figure'),
     Output('pcp', 'figure')],
    [Input('first-demographic-dropdown', 'value'),
     Input('second-demographic-dropdown', 'value'),
     Input('category-dropdown', 'value'),
     Input('left-side-scatterplot', 'selectedData'),
     Input('right-side-scatterplot', 'selectedData'),
     Input('left-side-first-barplot', 'selectedData'),
     Input('left-side-second-barplot', 'selectedData'),
     Input('right-side-first-barplot', 'selectedData'),
     Input('right-side-second-barplot', 'selectedData')]
)
def update_output(left_demographic, right_demographic, selected_category, left_scatter_data, right_scatter_data,
                  left_first_barplot_data, left_second_barplot_data, right_first_barplot_data, right_second_barplot_data):
    if any(item is None for item in
           [left_demographic, right_demographic, selected_category]):
        return go.Figure(), go.Figure()
    # Convert single selected values to lists
    selected_values = [left_demographic] if isinstance(left_demographic, str) else left_demographic
    selected_values += [right_demographic] if isinstance(right_demographic, str) else right_demographic

    scatterpolar_middle = go.Figure()

    left_incomes, left_ages = get_barplot_groups(left_first_barplot_data, left_second_barplot_data)
    right_incomes, right_ages = get_barplot_groups(right_first_barplot_data, right_second_barplot_data)

    if (left_scatter_data and left_scatter_data['points']) or (right_scatter_data and right_scatter_data['points']):

        filtered_df = pd.DataFrame(columns=scatterplot_columns)
        if left_scatter_data and left_scatter_data['points']:
            for point in left_scatter_data['points']:
                filtered_df = pd.concat([filtered_df, pd.DataFrame([point['customdata']],
                                                                   columns=scatterplot_columns)]
                                        , ignore_index=True)
            if not (right_scatter_data and right_scatter_data['points']):
                if selected_category == 'Loan_Type':
                    filtered_df = pd.concat([filtered_df, df[df[right_demographic] == 1]],
                                            join="inner")
                else:
                    filtered_df = pd.concat([filtered_df,
                                             df[df[selected_category] == right_demographic]],
                                            join="inner")
            else:
                for point in right_scatter_data['points']:
                    filtered_df = pd.concat([filtered_df, pd.DataFrame([point['customdata']],
                                                                       columns=scatterplot_columns)]
                                            , ignore_index=True)
        elif right_scatter_data and right_scatter_data['points']:
            for point in right_scatter_data['points']:
                filtered_df = pd.concat([filtered_df, pd.DataFrame([point['customdata']],
                                                                   columns=scatterplot_columns)]
                                        , ignore_index=True)
            if selected_category == 'Loan_Type':
                filtered_df = pd.concat([filtered_df, df[df[left_demographic] == 1]],
                                        join="inner")
            else:
                filtered_df = pd.concat([filtered_df,
                                         df[df[selected_category] == left_demographic]],
                                        join="inner")
    else:
        filtered_df = df.copy()


    left_income_mask = filtered_df['Grouped_Annual_Income'].isin(left_incomes)
    left_age_mask = filtered_df['Grouped_Age'].isin(left_ages)
    right_income_mask = filtered_df['Grouped_Annual_Income'].isin(right_incomes)
    right_age_mask = filtered_df['Grouped_Age'].isin(right_ages)
    # Making fig1 scatterpolar
    dimensions = []
    for i, value in enumerate(selected_values):
        mean_table = []
        if i == 0:
            incomes_mask = left_income_mask
            ages_mask = left_age_mask
        else:
            incomes_mask = right_income_mask
            ages_mask = right_age_mask
        if selected_category == 'Loan_Type':
            masked_df = filtered_df[(filtered_df[value] == 1) & incomes_mask & ages_mask]
        else:
            masked_df = filtered_df[(filtered_df[selected_category] == value) & incomes_mask & ages_mask]

        for field in fields:
            calculated_mean = masked_df[field].mean()
            if not math.isnan(calculated_mean):
                mean_table.append(math.log(round(calculated_mean)))
            else:
                mean_table.append(0)

        # Define color for the trace
        trace_color = '#0474ba' if i == 0 else '#f79500'
        # Remove underscores from each string in fields
        fields_without_underscore = [x.replace('_', ' ') for x in fields]

        # Create meanlist with modified strings
        meanlist = ["Mean " + x for x in fields_without_underscore]

        scatterpolar_middle.add_trace(go.Scatterpolar(
            r=mean_table,
            theta=meanlist,
            name=value,
            line=dict(color=trace_color)  # Set the line color
        ))
        scatterpolar_middle.update_traces(fill='toself')

    masked_df = pd.DataFrame()
    custom_color_scale = ['rgba(4,116,186,0.2)', 'rgba(247,149,0,0.2)']

    for field in fields:
        if selected_category == 'Loan_Type':
            masked_df = filtered_df[(filtered_df[left_demographic] == 1) | (filtered_df[right_demographic] == 1)]
            masked_field = masked_df[field]
        else:
            masked_df = filtered_df[filtered_df[selected_category].isin(selected_values)]
            masked_field = masked_df[field]
        dimensions.append(
            dict(range=[masked_field.min(), masked_field.max()], label=field.replace("_", " "),
                 values=masked_field))
    if selected_category == 'Loan_Type':
        category_codes = masked_df[left_demographic].astype('category').cat.codes
        pcp_plot = go.Figure(data=
        go.Parcoords(
            line=dict(color=category_codes, colorscale=custom_color_scale),
            dimensions=dimensions,
        ))
    else:
        category_codes = pd.Categorical(masked_df[selected_category],
                                        categories=masked_df[selected_category].unique()).codes
        pcp_plot = go.Figure(
            go.Parcoords(
                line=dict(color=category_codes, colorscale=custom_color_scale),
                dimensions=dimensions,
            ))
    return scatterpolar_middle, pcp_plot


if __name__ == '__main__':
    app.run_server(debug=True)