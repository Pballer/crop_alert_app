import base64
import datetime
import io

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
from PIL import Image
from tensorflow import keras
from coffee_prediction import make_prediction

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css',
                        'https://dash.plot.ly/assets/override.css?m=1571412266.0',
                        ]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server # the Flask app

model = keras.models.load_model('coffee.h5')

app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        #children=html.Div([
            #'Drag and Drop or ',
        #    html.A('Take a Picture!')
        #]),
        style={
            #'width': '100%',
            'height': '120px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            #'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'background-image': 'url(https://png2.cleanpng.com/sh/86c39b36cbc59bde176d8f6d2f986a53/L0KzQYm3UsA2N6F2iZH0aYP2gLBuTfNidZZ3eZ9yY3BxPcX5gf50eJJ3fdD9LXPkfbb5gb1qa5DzReJ3Zz24cYiCUPQzaZY1S9Q6Mj60QYi7V8IyQGI6SakDOEK5RoeCUcg2NqFzf3==/kisspng-camera-icon-transparent-camera-icon-png-5a790d2ae03b12.1174721815178826669185.png)',
            'background-repeat': 'no-repeat',
            'background-position': 'center',
            'background-size': 'contain',
            #'background-attachment': 'fixed',

        },
        # Allow multiple files to be uploaded
        multiple=True
    ),

    html.Div(id='output-data-upload', className='content-container container'),
], className='background') #style={'background-image': 'url(https://i.imgur.com/oOfouhD.jpg)',
   #       'background-repeat': 'no-repeat',
   #       'background-position': 'center'} ) #className='background')


def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'image' in content_type:
            image = Image.open(io.BytesIO(decoded))
            image = image.resize((224, 224))
            prediction = make_prediction(image, model)

    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H2(prediction),
        html.Img(src=contents,
                 style={
                    #'flex-shrink': 0,
                     'max-width': '100%',
                     'max-height': '100%',
                     #'display': 'flex',
                     #'overflow': 'hidden',
                    'height' : 'auto',
                    'width' : 'auto',
                    #'float' : 'right',
                    #'position' : 'center',
                    #'padding-top' : 0,
                    #'padding-right' : 0
                }),
        html.H5(filename),
        html.H6(datetime.datetime.fromtimestamp(date).strftime('%Y-%m-%d %H:%M:%S')),
        #html.Hr(),
    ], className='example-container')


@app.callback(Output('output-data-upload', 'children'),
              [Input('upload-data', 'contents')],
              [State('upload-data', 'filename'),
               State('upload-data', 'last_modified')])
def update_output(list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children


if __name__ == '__main__':
    app.run_server(debug=True)
