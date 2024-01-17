import math
import numpy as np
import dash
import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
df = pd.read_csv('filled_data.csv')
income_bins = [0, 10000, 20000, 30000, 50000, 70000]
income_labels = ['0-10000', '10000-20000', '30000-50000', '50000-70000', '70000+']
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
              'Loan Not Specified', 'Debt Consolidation Loan', 'Credit-Builder Loan']
loan_types.sort()
for loan_type in loan_types:
    loan_options.append({'label': loan_type, 'value': loan_type})

# Options for the category filter dropdown
category_options = [
    {'label': 'Occupation', 'value': 'Occupation'},
    {'label': 'Age Group', 'value': 'Grouped_Age'},
    {'label': 'Income Group', 'value': 'Grouped_Annual_Income'},
    {'label': 'Loan Type', 'value': 'Loan_Type'}
]

fields = ['Credit_Utilization_Ratio', 'Total_EMI_per_month', 'Outstanding_Debt',
          'Interest_Rate', 'Num_of_Loan', 'Delay_from_due_date', 'Num_of_Delayed_Payment']

scatterpolar_middle = go.Figure()
pcp_plot = go.Figure()

app.layout = html.Div([
    html.Div([
        html.H1("Credit Score Demographic Exploratory for Marketing", style={'textAlign': 'center',
                                                                             'fontFamily': 'Trebuchet MS'}),
        dcc.Checklist(
            id= 'sides-checklist',
            options=[
                {'label': 'In-depth Left Side', 'value': 'left'},
                {'label': 'In-depth Right Side', 'value': 'right'}
            ],
            style={'textAlign': 'center'})

    ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center', 'justifyContent': 'center'}),
    html.Div([
    # Left block
        html.Div([

            # Occupation name at the top
            html.H3(id='left-occupation-name', style={'color': '#0474BA'}),

            # Four dropdowns for the left side
            html.Label('Select Left-side Category', style={'color': '#0474BA'}),
            dcc.Dropdown(
                id='left-side-category-dropdown',
                # options=category_options,
                # value=category_options[1]['value'],
            ),

            html.Label('Select Left-side Demographic', style={'color': '#0474BA'}),
            dcc.Dropdown(
                id='left-side-label-dropdown',
                multi=False,
                # value=df[category_options[1]['value']].unique().tolist()[0]
            ),

            html.Label('Select Left-side Second Category', style={'color': '#0474BA'}),
            dcc.Dropdown(
                id='left-side-second-category-dropdown',
                # options=category_options,
                # value=category_options[2]['value']
            ),

            html.Label('Select Left-side Second Label', style={'color': '#0474BA'}),
            dcc.Dropdown(
                id='left-side-second-label-dropdown',
                multi=False,
                # value=df[category_options[2]['value']].unique().tolist()[0]
            ),

            html.Label('Select Left-side Categories to Compare', style={'color': '#0474BA'}),
            dcc.Dropdown(
                id='left-side-field-dropdown',
                options=[{'label': field, 'value': field} for field in fields],
                value=fields[0]
            ),

            # Bar chart for left side
            dcc.Graph(id='bar-chart-left'),

            # Scatterpolar graph for left side
            dcc.Graph(id='scatterpolar-left'),

        ], style={'width': '25%', 'display': 'inline-block'},
        id='left-block'),

        # Middle block
        html.Div([
            # Category Dropdown
            html.Label('Select Category'),
            dcc.Dropdown(
                id='category-dropdown',
                options=category_options,
                value='Occupation'
            ),

            # Dynamic Dropdowns for the first and second occupations
            html.Label('Select Left-side Demographic', style={'color': '#0474BA'}),
            dcc.Dropdown(
                id='first-occupation-dropdown',
                options=occupation_options,
                multi=False,
                # value=occupation_options[0]['value']
            ),

            html.Label('vs \n'),

            html.Label('Select Right-side Demographic', style={'color': '#F79500'}),
            dcc.Dropdown(
                id='second-occupation-dropdown',
                options=occupation_options,
                multi=False,
                # value=occupation_options[1]['value']
            ),

            # Scatterpolar graph for displaying selected values
            dcc.Graph(id='scatterpolar-middle',
                      responsive=True),

            # Pcp graph for displaying selected values
            dcc.Graph(id='pcp',
                      responsive=True),
        ], style={'width': '50%', 'display': 'inline-block'},
        id='middle-block'),

        # Right block
        html.Div([
            # Occupation name at the top
            html.H3(id='right-occupation-name', style={'color': '#F79500'}),

            # Four dropdowns for the right side
            html.Label('Select Right-side Category', style={'color': '#F79500'}),
            dcc.Dropdown(
                id='right-side-category-dropdown',
                # options=category_options,
                # value=category_options[1]['value']
            ),

            html.Label('Select Right-side Demographic', style={'color': '#F79500'}),
            dcc.Dropdown(
                id='right-side-label-dropdown',
                options=occupation_options,
                multi=False,
                # value=occupation_options[0]['value']
            ),

            html.Label('Select Right-side Second Category', style={'color': '#F79500'}),
            dcc.Dropdown(
                id='right-side-second-category-dropdown',
                # options=category_options,
                # value=category_options[2]['value']
            ),

            html.Label('Select Right-side Second Label', style={'color': '#F79500'}),
            dcc.Dropdown(
                id='right-side-second-label-dropdown',
                options=occupation_options,
                multi=False,
                # value=occupation_options[0]['value']
            ),

            html.Label('Select Right-side Categories to Compare', style={'color': '#F79500'}),
            dcc.Dropdown(
                id='right-side-field-dropdown',
                options=[{'label': field, 'value': field} for field in fields],
                value=fields[0]
            ),

            # Bar chart for right side
            dcc.Graph(id='bar-chart-right'),

            # Scatterpolar graph for right side
            dcc.Graph(id='scatterpolar-right'),

        ], style={'width': '25%', 'display': 'inline-block'},
        id='right-block'),

    ])
], style={'fontFamily': 'Trebuchet MS'})

@app.callback(
    [Output('left-block', 'style'),
     Output('middle-block', 'style'),
     Output('right-block', 'style')],
    [Input('sides-checklist', 'value')]
)
def show_sides(selected_sides):
    left_display = {'width': '25%', 'display': 'none'}
    middle_display = {'width': '50%', 'display': 'inline-block', 'alignItems': 'center', 'justifyContent': 'center'}
    right_display = {'width': '25%', 'display': 'none'}
    if selected_sides is not None:
        print(selected_sides)
        if len(selected_sides) == 1:
            middle_size = 70
            side_size = 30
        else:
            middle_size = 50
            side_size = 25
        if 'left' in selected_sides:
            left_display = {'width': f'{side_size}%', 'display': 'inline-block'}
        if 'right' in selected_sides:
            right_display = {'width': f'{side_size}%', 'display': 'inline-block'}
        middle_display = {'width': f'{middle_size}%', 'display': 'inline-block'}
    return left_display, middle_display, right_display


# Callback to dynamically update the options of the first occupation dropdown
@app.callback(
    [Output('first-occupation-dropdown', 'options'),
     Output('first-occupation-dropdown', 'value')],
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
    [Output('second-occupation-dropdown', 'options'),
     Output('second-occupation-dropdown', 'value')],
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


@app.callback(
    [Output('left-side-category-dropdown', 'options'),
     Output('left-side-category-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_left_side_category_dropdown_options(selected_category):
    return get_options_and_defaults_side_first_category(selected_category)


@app.callback(
    [Output('left-side-second-category-dropdown', 'options'),
     Output('left-side-second-category-dropdown', 'value')],
    [Input('left-side-category-dropdown', 'value'),
     Input('left-side-category-dropdown', 'options')]
)
def update_left_side_category_second_dropdown_options(selected_category, options):
    return get_options_and_defaults_second_category(selected_category, options)


# Callback to dynamically update the options of the left side label dropdown
@app.callback(
    [Output('left-side-label-dropdown', 'options'),
     Output('left-side-label-dropdown', 'value')],
    [Input('left-side-category-dropdown', 'value')]
)
def update_left_side_label_dropdown_options(selected_category):
    return get_options_and_defaults(selected_category)


@app.callback(
    [Output('left-side-second-label-dropdown', 'options'),
     Output('left-side-second-label-dropdown', 'value')],
    [Input('left-side-second-category-dropdown', 'value')]
)
def update_left_side_second_label_dropdown_options(selected_category):
    return get_options_and_defaults(selected_category)

@app.callback(
    [Output('right-side-category-dropdown', 'options'),
     Output('right-side-category-dropdown', 'value')],
    [Input('category-dropdown', 'value')]
)
def update_right_side_category_dropdown_options(selected_category):
    return get_options_and_defaults_side_first_category(selected_category)


@app.callback(
    [Output('right-side-second-category-dropdown', 'options'),
     Output('right-side-second-category-dropdown', 'value')],
    [Input('right-side-category-dropdown', 'value'),
     Input('right-side-category-dropdown', 'options')]
)
def update_right_side_category_second_dropdown_options(selected_category, options):
    return get_options_and_defaults_second_category(selected_category, options)


# Callback to dynamically update the options of the right side label dropdown
@app.callback(
    [Output('right-side-label-dropdown', 'options'),
     Output('right-side-label-dropdown', 'value')],
    [Input('right-side-category-dropdown', 'value')]
)
def update_right_side_label_dropdown_options(selected_category):
    return get_options_and_defaults(selected_category)


@app.callback(
    [Output('right-side-second-label-dropdown', 'options'),
     Output('right-side-second-label-dropdown', 'value')],
    [Input('right-side-second-category-dropdown', 'value')]
)
def update_right_side_second_label_dropdown_options(selected_category):
    return get_options_and_defaults(selected_category)


def get_options_and_defaults_side_first_category(selected_category):
    constrained_options = category_options.copy()
    if selected_category == 'Occupation':
        constrained_options.pop(0)
    elif selected_category == 'Grouped_Age':
        constrained_options.pop(1)
    elif selected_category == 'Grouped_Annual_Income':
        constrained_options.pop(2)
    else:
        constrained_options.pop(3)
    return constrained_options, constrained_options[0]['value']


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


all_categories = ['Occupation', 'Grouped_Age', 'Grouped_Annual_Income', 'Loan_Type']


# Callback to update the bar chart for the left side
@app.callback(
    Output('bar-chart-left', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('left-side-category-dropdown', 'value'),
     Input('left-side-label-dropdown', 'value'),
     Input('left-side-second-category-dropdown', 'value'),
     Input('left-side-second-label-dropdown', 'value'),
     Input('left-side-field-dropdown', 'value'),
     Input('first-occupation-dropdown', 'value')]
)
def update_bar_chart_left(main_category, selected_category, selected_label, second_category, second_label,
                          selected_field, left_occupation):
    if any(item is None for item in
           [main_category, selected_category, selected_label, second_category, second_label,
            selected_field]):
        return go.Figure()

    unchosen_category = [category for category in all_categories if
                         category not in [selected_category, second_category, main_category]][0]
    # Get unique labels for the unchosen category
    if unchosen_category == 'Loan_Type':
        main_category_labels = loan_types
    else:
        main_category_labels = df[unchosen_category].unique()

    # Filter the database based on left-side category labels and second category labels
    if selected_category == 'Loan_Type':
        filtered_data = df[df[selected_label] == 1]
    else:
        filtered_data = df[df[selected_category] == selected_label]

    if second_category == 'Loan_Type':
        filtered_data = filtered_data[filtered_data[second_label] == 1]
    else:
        filtered_data = filtered_data[filtered_data[second_category] == second_label]

    if main_category == 'Loan_Type':
        filtered_data = filtered_data[filtered_data[left_occupation] == 1]
    else:
        filtered_data = filtered_data[filtered_data[main_category] == left_occupation]

    # Create traces for the selected field
    values = []
    for label in main_category_labels:
        if unchosen_category == 'Loan_Type':
            label_data = filtered_data[filtered_data[label] == 1]
        else:
            label_data = filtered_data[filtered_data[unchosen_category] == label]
        mean_value = label_data[selected_field].mean()
        if not math.isnan(mean_value):
            values.append(math.log(round(mean_value)))
        else:
            values.append(None)

    # Pad 'r' values with None to match the length of 'theta' values
    while len(values) < len(main_category_labels):
        values.append(None)

    trace = go.Bar(
        y=main_category_labels,
        x=values,
        name=selected_field,
        marker=dict(color='#0474BA'),
        orientation='h'
    )

    layout = go.Layout(
        title=dict(
            text=f'{left_occupation}s\' {selected_field} by {unchosen_category}',
            font=dict(color='#0474BA')
        ),
        xaxis={'title': f'Mean {selected_field}'}
    )
    return go.Figure(data=[trace], layout=layout)


# Similar callback for updating the bar chart for the right side
@app.callback(
    Output('bar-chart-right', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('right-side-category-dropdown', 'value'),
     Input('right-side-label-dropdown', 'value'),
     Input('right-side-second-category-dropdown', 'value'),
     Input('right-side-second-label-dropdown', 'value'),
     Input('right-side-field-dropdown', 'value'),
     Input('second-occupation-dropdown', 'value')]
)
def update_bar_chart_right(main_category, selected_category, selected_label, second_category, second_label,
                           selected_field, right_occupation):

    if any(item is None for item in
           [main_category, selected_category, selected_label, second_category, second_label,
            selected_field]):
        return go.Figure()
    unchosen_category = [category for category in all_categories if
                         category not in [selected_category, second_category, main_category]][0]
    # Get unique labels for the unchosen category selected
    if unchosen_category == 'Loan_Type':
        main_category_labels = loan_types
    else:
        main_category_labels = df[unchosen_category].unique()

    # Filter the database based on left-side category labels and second category labels
    if selected_category == 'Loan_Type':
        filtered_data = df[df[selected_label] == 1]
    else:
        filtered_data = df[df[selected_category] == selected_label]

    if second_category == 'Loan_Type':
        filtered_data = filtered_data[filtered_data[second_label] == 1]
    else:
        filtered_data = filtered_data[filtered_data[second_category] == second_label]

    if main_category == 'Loan_Type':
        filtered_data = filtered_data[filtered_data[right_occupation] == 1]
    else:
        filtered_data = filtered_data[filtered_data[main_category] == right_occupation]

    # Create traces for the selected field
    values = []
    for label in main_category_labels:
        if unchosen_category == 'Loan_Type':
            label_data = filtered_data[filtered_data[label] == 1]
        else:
            label_data = filtered_data[filtered_data[unchosen_category] == label]
        mean_value = label_data[selected_field].mean()
        if not math.isnan(mean_value):
            values.append(math.log(round(mean_value)))
        else:
            values.append(None)

    # Pad 'r' values with None to match the length of 'theta' values
    while len(values) < len(main_category_labels):
        values.append(None)

    trace = go.Bar(
        y=main_category_labels,
        x=values,
        name=selected_field,
        marker=dict(color='#F79500'),
        orientation = 'h'
    )

    layout = go.Layout(
        title=dict(
            text=f'{right_occupation}s\' {selected_field} by {unchosen_category}',
            font=dict(color='#F79500')
        ),
        xaxis={'title': f'Mean {selected_field}'},

    )
    return go.Figure(data=[trace], layout=layout)


# Callbacks for updating the occupation names in the left and right side blocks
@app.callback(
    [Output('left-occupation-name', 'children'),
     Output('right-occupation-name', 'children')],
    [Input('first-occupation-dropdown', 'value'),
     Input('second-occupation-dropdown', 'value')]
)
def update_occupation_names(first_occupation, second_occupation):
    return f'{first_occupation}s', f'{second_occupation}s'


# Callback to update the scatterpolar graph for the left side
@app.callback(
    Output('scatterpolar-left', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('left-side-category-dropdown', 'value'),
     Input('left-side-label-dropdown', 'value'),
     Input('left-side-second-category-dropdown', 'value'),
     Input('left-side-second-label-dropdown', 'value'),
     Input('left-side-field-dropdown', 'value'),
     Input('first-occupation-dropdown', 'value')]
)
def update_scatterpolar_left(main_category, selected_category, selected_label, second_category, second_label,
                             selected_field, first_occupation):
    if any(item is None for item in
           [main_category, selected_category, selected_label, second_category, second_label,
            selected_field]):
        return go.Figure()

    # Get unique labels for the main category selected in the middle
    if main_category == 'Loan_Type':
        main_category_labels = loan_types
    else:
        main_category_labels = df[main_category].unique()


    # Filter the database based on left-side category labels and second category labels
    if selected_category == 'Loan_Type':
        filtered_data = df[df[selected_label] == 1]
    else:
        filtered_data = df[df[selected_category] == selected_label]

    if second_category == 'Loan_Type':
        filtered_data = filtered_data[filtered_data[second_label] == 1]
    else:
        filtered_data = filtered_data[filtered_data[second_category] == second_label]

    # Create traces for the selected field
    values = []
    for label in main_category_labels:
        if main_category == 'Loan_Type':
            label_data = filtered_data[filtered_data[label] == 1]
        else:
            label_data = filtered_data[filtered_data[main_category] == label]
        mean_value = label_data[selected_field].mean()
        if not math.isnan(mean_value):
            values.append(math.log(round(mean_value)))
        else:
            values.append(None)

    colors = ['#0474BA' if label == first_occupation else 'black' for label in main_category_labels]

    # Pad 'r' values with None to match the length of 'theta' values
    while len(values) < len(main_category_labels):
        values.append(None)

    trace = go.Scatterpolar(
        r=values,
        theta=main_category_labels,
        name=selected_field,
        line=dict(color='black'),
        marker=dict(
            color=colors
        ),
    )

    layout = go.Layout(
        title=dict(
            text=f'{main_category}s by {selected_field}',
            font=dict(color='black')
        ),
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True)



    return go.Figure(data=[trace], layout=layout)


# Callback to update the scatterpolar graph for the right side
@app.callback(
    Output('scatterpolar-right', 'figure'),
    [Input('category-dropdown', 'value'),
     Input('right-side-category-dropdown', 'value'),
     Input('right-side-label-dropdown', 'value'),
     Input('right-side-second-category-dropdown', 'value'),
     Input('right-side-second-label-dropdown', 'value'),
     Input('right-side-field-dropdown', 'value'),
     Input('second-occupation-dropdown', 'value')]
)
def update_scatterpolar_right(main_category, selected_category, selected_label, second_category, second_label,
                              selected_field, second_occupation):
    if any(item is None for item in
           [main_category, selected_category, selected_label, second_category, second_label,
            selected_field]):
        return go.Figure()
    # Get unique labels for the main category selected in the middle
    if main_category == 'Loan_Type':
        main_category_labels = loan_types
    else:
        main_category_labels = df[main_category].unique()

    # Filter the database based on left-side category labels and second category labels
    if selected_category == 'Loan_Type':
        filtered_data = df[df[selected_label] == 1]
    else:
        filtered_data = df[df[selected_category] == selected_label]

    if second_category == 'Loan_Type':
        filtered_data = filtered_data[filtered_data[second_label] == 1]
    else:
        filtered_data = filtered_data[filtered_data[second_category] == second_label]

    # Create traces for the selected field
    values = []
    for label in main_category_labels:
        if main_category == 'Loan_Type':
            label_data = filtered_data[filtered_data[label] == 1]
        else:
            label_data = filtered_data[filtered_data[main_category] == label]
        mean_value = label_data[selected_field].mean()
        if not math.isnan(mean_value):
            values.append(math.log(round(mean_value)))
        else:
            values.append(None)

    colors = ['#F79500' if label == second_occupation else 'black' for label in main_category_labels]

    # Pad 'r' values with None to match the length of 'theta' values
    while len(values) < len(main_category_labels):
        values.append(None)

    trace = go.Scatterpolar(
        r=values,
        theta=main_category_labels,
        name=selected_field,
        line=dict(color='black'),
        marker=dict(
            color=colors
        ),
    )

    layout = go.Layout(
        title=dict(
            text=f'{main_category}s by {selected_field}',
            font=dict(color='black')
        ),
        polar=dict(radialaxis=dict(visible=True)),
        showlegend=True)
    return go.Figure(data=[trace], layout=layout)


# Callback to update the output div based on the selected occupations
@app.callback(
    [Output('scatterpolar-middle', 'figure'),
     Output('pcp', 'figure')],
    [Input('first-occupation-dropdown', 'value'),
     Input('second-occupation-dropdown', 'value'),
     Input('category-dropdown', 'value')]
)
def update_output(first_occupation, second_occupation, selected_category):
    if any(item is None for item in
           [first_occupation, second_occupation, selected_category]):
        return go.Figure(), go.Figure()
    # Convert single selected values to lists
    selected_values = [first_occupation] if isinstance(first_occupation, str) else first_occupation
    selected_values += [second_occupation] if isinstance(second_occupation, str) else second_occupation

    # Making fig1 scatterpolar
    dimensions = []
    for i, value in enumerate(selected_values):
        mean_table = []
        for field in fields:
            if selected_category == 'Loan_Type':
                masked_df = df[df[value] == 1]
            else:
                masked_df = df[df[selected_category] == value]
            calculated_mean = masked_df[field].mean()
            if not math.isnan(calculated_mean):
                mean_table.append(math.log(round(calculated_mean)))
            else:
                mean_table.append(0)

        # Define color for the trace
        trace_color = '#0474BA' if i == 0 else '#F79500'

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

    # Making fig2 pcp with go.parcoods
    def freedman_diaconis_bin_width(data):
        # Convert data to numeric type
        data_numeric = pd.to_numeric(data, errors='coerce').dropna()

        # Check if there are values in the numeric data
        if len(data_numeric) == 0:
            return 0  # Return 0 or another appropriate default value

        # Calculate percentiles on numeric data
        q75, q25 = np.percentile(data_numeric, [75, 25])
        iqr = q75 - q25
        n = len(data_numeric)

        # Check for non-zero length before calculating bin_width
        bin_width = 2 * iqr / (n ** (1 / 3)) if n > 0 else 0

        return bin_width

    def cluster_values_with_freedman_diaconis(df):
        clusters = {}

        # Determine the common length for clusters
        common_length = np.inf

        for column in df.columns:
            data = df[column].dropna()  # Drop missing values
            data_numeric = pd.to_numeric(data, errors='coerce').dropna()  # Convert to numeric
            bin_width = freedman_diaconis_bin_width(data_numeric)

            # Check if bin_width is 0 or NaN, set a default value (e.g., 1)
            bin_width = max(bin_width, 1)

            # Check for an empty data_numeric array
            if len(data_numeric) == 0:
                # Set default values for minimum and maximum
                min_value, max_value = 0, 1
            else:
                min_value, max_value = np.nanmin(data_numeric), np.nanmax(data_numeric)

            # Use linspace with a maximum number of points
            max_points = 1000  # Set a reasonable maximum number of points
            bins = np.linspace(min_value, max_value, num=min(max_points, int((max_value - min_value) / bin_width) + 1))

            # Store clusters with common length
            clusters[column] = np.digitize(data_numeric, bins)
            common_length = min(common_length, len(clusters[column]))

        # Ensure all clusters have the same length
        for column in df.columns:
            clusters[column] = clusters[column][:common_length]

        return clusters

    clustered_data = cluster_values_with_freedman_diaconis(df)

    # Create a DataFrame with the original data and cluster assignments
    clustered_df = pd.DataFrame(clustered_data)

    # Add the original values to the clustered DataFrame
    for column in df.columns:
        clustered_df[column] = df[column]

    for column in clustered_df.columns:
        df[column] = clustered_df[column]

    for field in fields:
        if selected_category == 'Loan_Type':
            masked_field = df[(df[first_occupation] == 1) | (df[second_occupation] == 1)][field]
        else:
            masked_field = df[df[selected_category].isin(selected_values)][field]
        dimensions.append(
            dict(range=[masked_field.min(), masked_field.max()], label=field.replace("_", " "),
                 values=masked_field))

    if selected_category == 'Loan_Type':
        pcp_plot = go.Figure(data=
        go.Parcoords(
            line=dict(color=df[first_occupation].astype('category').cat.codes,
                      showscale=True),
            dimensions=dimensions,
        ))
    else:
        pcp_plot = go.Figure(
        go.Parcoords(
            line=dict(color=df[selected_category].astype('category').cat.codes,
                      showscale=True),
            dimensions=dimensions,

        ))

    scatterpolar_middle.update_layout(
        autosize=True
    )
    pcp_plot.update_layout(
        autosize=True
    )

    return scatterpolar_middle, pcp_plot


if __name__ == '__main__':
    app.run_server(debug=True)
