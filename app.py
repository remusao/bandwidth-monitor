from flask import Flask, render_template

import json
import sqlite3
import datetime

import plotly
import plotly.graph_objs as go


app = Flask(__name__)
app.debug = True

def scale(s):
    """Scale bandwidths in Bytes to MB."""
    if s > 100:
        return s // 1000000
    return s

@app.route('/')
def index():
    with sqlite3.connect('speedtest.db') as connection:
        rows = connection.execute('SELECT * FROM RESULTS').fetchall()

        x_axis_fast = [
            datetime.datetime.fromtimestamp(r[1]) for r in rows
            if r[0] == 'fast.com'
        ]
        x_axis_speed = [
            datetime.datetime.fromtimestamp(r[1]) for r in rows
            if r[0] != 'fast.com'
        ]

        graph = dict(
            data=[
                go.Scatter(
                    x = x_axis_fast,
                    y = [
                        scale(r[3]) for r in rows
                        if r[0] == 'fast.com'
                    ],
                    mode = 'lines+markers',
                    name = 'Download: fast.com'
                ),
                go.Scatter(
                    x = x_axis_speed,
                    y = [
                        scale(r[3]) for r in rows
                        if r[0] != 'fast.com'
                    ],
                    mode = 'lines+markers',
                    name = 'Download: speedtest-cli'
                ),
                go.Scatter(
                    x = x_axis_speed,
                    y = [
                        scale(r[4]) for r in rows
                        if r[0] != 'fast.com'
                    ],
                    mode = 'lines+markers',
                    name = 'Upload'
                ),
                go.Scatter(
                    x = x_axis_speed,
                    y = [
                        r[2] for r in rows
                        if r[0] != 'fast.com'
                    ],
                    mode = 'lines+markers',
                    name = 'Ping'
                )
            ],
            layout=dict(
                title='Bandwidth',
                yaxis=dict(
                    title="Bandwidth"
                ),
                xaxis=dict(
                    title="Time"
                )
            )
        )

        return render_template(
            'layouts/index.html',
            graph=json.dumps(
                graph,
                cls=plotly.utils.PlotlyJSONEncoder
            ),
        )


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
