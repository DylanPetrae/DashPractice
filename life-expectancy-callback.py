import pandas as pd     
import plotly           
import plotly.express as px

import dash            
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
from dash.exceptions import PreventUpdate

#prints the first 15 lines of data to the console
#print(px.data.gapminder()[:15])

app = dash.Dash(__name__)

#---------------------------------------------------------------#
#                        LAYOUT                                 #
#---------------------------------------------------------------#
app.layout = html.Div([

    html.Div([
        dcc.Graph(id='the_graph')
    ]),

    html.Div([
        dcc.Input(id='input_state', type='number', inputMode='numeric', value=2007,
                  max=2007, min=1952, step=5, required=True),
        html.Button(id='submit_button', n_clicks=0, children='Submit'),
        html.Div(id='output_state'),
    ],style={'text-align': 'center'}),

])

#---------------------------------------------------------------
@app.callback(
    [Output('output_state', 'children'),
    Output(component_id='the_graph', component_property='figure')],
    [Input(component_id='submit_button', component_property='n_clicks')],
    # Difference between State and Input
    # State allows you to pass along extra values without firing the callbacks
    [State(component_id='input_state', component_property='value')]
)

# We need two arguments because we have an Input and a State
def update_output(num_clicks, val_selected):
    
    # If year field is empty
    if val_selected is None:
        # Prevents the map from updating when user attempts to press Submit with an empty field
        raise PreventUpdate

    # If the year field is NOT empty
    else:

        # Filter the data
        # Grab only the data with the year that is in the input field
        df = px.data.gapminder().query("year=={}".format(val_selected))
        
        fig = px.choropleth(
            df, 
            locations="iso_alpha",
            color="lifeExp",
            hover_name="country",
            projection='natural earth',
            title='Global Life Expectancy by Year',
            color_continuous_scale=px.colors.sequential.Plasma
            )

        # Set Title font size to 28 and center it horizontally above the map
        # Increase margins of map to make a little bit larger
        fig.update_layout(title=dict(font=dict(size=28),x=0.5,xanchor='center'),
                          margin=dict(l=60, r=60, t=50, b=50))

        return ('The input value was "{}" and the button has been \
                clicked {} times'.format(val_selected, num_clicks), fig)

if __name__ == '__main__':
    app.run_server(debug=True)